#!/usr/bin/env python3
"""Run the frozen random-loss extension: BBRv3/CUBIC x 0/0.1%."""

import argparse
import json
import math
import subprocess
import time
from pathlib import Path

from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.topo import Topo


ROOT = Path(__file__).resolve().parent
DEFAULT_RUNS = ROOT / "runs"
CAPACITY = 100
RTT_MS = 20
QUEUE_BYTES = 500000
QUEUE_PACKETS = math.ceil(QUEUE_BYTES / 1500)


class LossTopo(Topo):
    def __init__(self, algorithm_loss_pct, **opts):
        self.algorithm_loss_pct = algorithm_loss_pct
        super().__init__(**opts)

    def build(self):
        h1 = self.addHost("h1", ip="10.0.0.1/24")
        h2 = self.addHost("h2", ip="10.0.0.2/24")
        h3 = self.addHost("h3", ip="10.0.0.3/24")
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        # Artificial loss is on the h3 access link, separate from the bottleneck.
        self.addLink(h3, s2, cls=TCLink, delay="10ms", loss=self.algorithm_loss_pct)
        self.addLink(
            s1, s2, cls=TCLink, bw=CAPACITY,
            max_queue_size=QUEUE_PACKETS, use_tbf=True, enable_ecn=False,
        )


def write(path, text):
    path.write_text(text or "", encoding="utf-8")


def run_one(algorithm, loss_pct, repeat, runs_root, duration, warmup):
    loss_tag = "0p1" if loss_pct else "0"
    condition = f"LOSS_{algorithm}_C100_R20_Q2_L{loss_tag}"
    run_id = f"{condition}_rep{repeat:02d}"
    out = runs_root / run_id
    out.mkdir(parents=False, exist_ok=False)
    registered = "bbr" if algorithm == "BBR3" else "cubic"
    cfg = {
        "run_id": run_id, "condition_id": condition, "experiment": "LOSS_EXTENSION",
        "algorithm_flow1": algorithm, "algorithm_flow2": algorithm,
        "registered_algorithm_flow1": registered, "registered_algorithm_flow2": registered,
        "capacity_mbps": CAPACITY, "rtt1_ms": RTT_MS, "rtt2_ms": RTT_MS,
        "queue_bdp_multiplier": 2, "queue_target_bytes": QUEUE_BYTES,
        "queue_packets": QUEUE_PACKETS, "ecn": "off",
        "artificial_loss_pct": loss_pct, "artificial_loss_point": "s2-eth1 (h3 access link)",
        "bottleneck_point": "s1-eth3", "random_loss_seed": None,
        "duration_s": duration, "warmup_s": warmup, "analysis_start_s": warmup,
        "analysis_end_s": duration, "repeat": repeat,
        "manifest_id": "random-loss-bbr3-cubic-20261012", "status": "running",
    }
    write(out / "config.json", json.dumps(cfg, indent=2) + "\n")
    net = None
    status = {"run_id": run_id, "start": time.time(), "flow_exit": {}, "cleanup": None}
    try:
        net = Mininet(
            topo=LossTopo(loss_pct), switch=OVSBridge, controller=None,
            link=TCLink, autoSetMacs=True, autoStaticArp=True, cleanup=True,
        )
        net.start()
        h1, h2, h3 = net.get("h1", "h2", "h3")
        if net.pingAll() != 0:
            raise RuntimeError("topology pingAll failed")
        for host in (h1, h2):
            host.cmd(f"sysctl -q -w net.ipv4.tcp_congestion_control={registered}")
            host.cmd("sysctl -q -w net.ipv4.tcp_ecn=0")
            if host.cmd("sysctl -n net.ipv4.tcp_congestion_control").strip() != registered:
                raise RuntimeError(f"{host.name}: failed to apply {registered}")
        h3.cmd("sysctl -q -w net.ipv4.tcp_congestion_control=cubic")
        h3.cmd("sysctl -q -w net.ipv4.tcp_ecn=0")
        write(out / "host_sysctl.txt", "\n".join(
            f"[{h.name}]\n{h.cmd('sysctl net.ipv4.tcp_congestion_control net.ipv4.tcp_ecn')}"
            for h in (h1, h2, h3)
        ))
        s1, s2 = net.get("s1", "s2")
        write(out / "qdisc_before_bottleneck.txt", s1.cmd("tc -s qdisc show dev s1-eth3"))
        write(out / "qdisc_before_artificial_loss.txt", s2.cmd("tc -s qdisc show dev s2-eth1"))
        write(out / "tc_loss_configuration.txt", s2.cmd("tc qdisc show dev s2-eth1"))
        write(out / "ping_baseline_h1.txt", h1.cmd("ping -c 10 -i 0.05 10.0.0.3"))
        write(out / "ping_baseline_h2.txt", h2.cmd("ping -c 10 -i 0.05 10.0.0.3"))
        servers = [h3.popen(
            ["iperf3", "-s", "-1", "-p", str(port), "--json"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        ) for port in (5201, 5202)]
        time.sleep(1)
        clients = [(name, host.popen(
            ["iperf3", "-c", "10.0.0.3", "-p", str(port), "-t", str(duration), "-i", "1", "-J"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )) for host, port, name in ((h1, 5201, "flow1"), (h2, 5202, "flow2"))]
        ping_count = max(2, min(30, duration // 2))
        write(out / "ping_loaded_h1.txt", h1.cmd(f"ping -c {ping_count} -i 1 10.0.0.3"))
        write(out / "ping_loaded_h2.txt", h2.cmd(f"ping -c {ping_count} -i 1 10.0.0.3"))
        write(out / "qdisc_after_bottleneck.txt", s1.cmd("tc -s qdisc show dev s1-eth3"))
        write(out / "qdisc_after_artificial_loss.txt", s2.cmd("tc -s qdisc show dev s2-eth1"))
        write(out / "ss_h1.txt", h1.cmd("ss -tin"))
        write(out / "ss_h2.txt", h2.cmd("ss -tin"))
        for name, proc in clients:
            stdout, _ = proc.communicate(timeout=duration + 30)
            status["flow_exit"][name] = proc.returncode
            write(out / f"iperf_client_{name}.json", stdout)
        for idx, proc in enumerate(servers, 1):
            stdout, _ = proc.communicate(timeout=30)
            status["flow_exit"][f"server{idx}"] = proc.returncode
            write(out / f"iperf_server_{idx}.json", stdout)
        cfg["status"] = "completed" if all(v == 0 for v in status["flow_exit"].values()) else "invalid_exit"
    except Exception as exc:
        cfg["status"] = "failed"
        status["exception"] = repr(exc)
        write(out / "exception.txt", repr(exc) + "\n")
    finally:
        if net is not None:
            try:
                net.stop()
                status["cleanup"] = "ok"
            except Exception as exc:
                status["cleanup"] = repr(exc)
        subprocess.run(["mn", "-c"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
        status["end"] = time.time()
        write(out / "exit_status.json", json.dumps(status, indent=2) + "\n")
        write(out / "config.json", json.dumps(cfg, indent=2) + "\n")
    return cfg["status"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--algorithm", choices=["BBR3", "CUBIC"], required=True)
    ap.add_argument("--loss-pct", type=float, choices=[0.0, 0.1], required=True)
    ap.add_argument("--repeat", type=int, required=True)
    ap.add_argument("--duration", type=int, default=180)
    ap.add_argument("--warmup", type=int, default=30)
    ap.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS)
    args = ap.parse_args()
    args.runs_root.mkdir(parents=True, exist_ok=True)
    setLogLevel("info")
    status = run_one(args.algorithm, args.loss_pct, args.repeat, args.runs_root, args.duration, args.warmup)
    print(status, flush=True)
    raise SystemExit(0 if status == "completed" else 1)


if __name__ == "__main__":
    main()
