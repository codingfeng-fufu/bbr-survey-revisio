#!/usr/bin/env python3
"""Run the independently built BBRv3 kernel batch; preserve every attempt."""

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
RUNS = ROOT / "runs"
CAPACITY = 100
BASE_RTT = 20
DURATION = 180
WARMUP = 30


class BaselineTopo(Topo):
    def __init__(self, extra_rtt2_ms=0, queue_packets=84, **opts):
        self.extra_rtt2_ms = extra_rtt2_ms
        self.queue_packets = queue_packets
        super().__init__(**opts)

    def build(self):
        h1 = self.addHost("h1", ip="10.0.0.1/24")
        h2 = self.addHost("h2", ip="10.0.0.2/24")
        h3 = self.addHost("h3", ip="10.0.0.3/24")
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        self.addLink(h1, s1)
        self.addLink(h2, s1, delay=f"{self.extra_rtt2_ms / 2:.3f}ms" if self.extra_rtt2_ms else None)
        self.addLink(h3, s2, delay="10ms")
        self.addLink(
            s1, s2, cls=TCLink, bw=CAPACITY, delay=None,
            max_queue_size=self.queue_packets, use_tbf=True, enable_ecn=False,
        )


def qpackets(queue_multiplier):
    return max(1, math.ceil(250000 * queue_multiplier / 1500))


def write(path, text):
    path.write_text(text or "", encoding="utf-8")


def run_one(algorithm1, algorithm2, rtt2, queue_multiplier, repeat):
    condition = f"BBR3_{algorithm1}_{algorithm2}_C100_R20-{rtt2}_Q{str(queue_multiplier).replace('.', 'p')}"
    run_id = f"{condition}_rep{repeat:02d}"
    out = RUNS / run_id
    out.mkdir(parents=False, exist_ok=False)
    cfg = {
        "run_id": run_id, "condition_id": condition, "experiment": "E1" if algorithm1 == algorithm2 else "E2",
        "algorithm_flow1": algorithm1, "algorithm_flow2": algorithm2,
        "registered_algorithm_flow1": "bbr" if algorithm1 == "BBR3" else "cubic",
        "registered_algorithm_flow2": "bbr" if algorithm2 == "BBR3" else "cubic",
        "capacity_mbps": CAPACITY, "rtt1_ms": 20, "rtt2_ms": rtt2,
        "queue_bdp_multiplier": queue_multiplier, "queue_target_bytes": int(250000 * queue_multiplier),
        "queue_packets": qpackets(queue_multiplier), "ecn": "off", "random_loss": 0,
        "duration_s": DURATION, "warmup_s": WARMUP, "analysis_start_s": WARMUP,
        "analysis_end_s": DURATION, "repeat": repeat, "manifest_id": "bbr3-kernel-formal-20261011",
        "status": "running"
    }
    write(out / "config.json", json.dumps(cfg, indent=2) + "\n")
    net = None
    status = {"run_id": run_id, "start": time.time(), "flow_exit": {}, "cleanup": None}
    try:
        net = Mininet(topo=BaselineTopo(extra_rtt2_ms=rtt2 - 20, queue_packets=cfg["queue_packets"]),
                      switch=OVSBridge, controller=None, link=TCLink, autoSetMacs=True,
                      autoStaticArp=True, cleanup=True)
        net.start()
        h1, h2, h3 = net.get("h1", "h2", "h3")
        if net.pingAll() != 0:
            raise RuntimeError("topology pingAll failed")
        for host, algo in ((h1, cfg["registered_algorithm_flow1"]), (h2, cfg["registered_algorithm_flow2"]), (h3, "cubic")):
            host.cmd(f"sysctl -q -w net.ipv4.tcp_congestion_control={algo}")
            host.cmd("sysctl -q -w net.ipv4.tcp_ecn=0")
            if host.cmd("sysctl -n net.ipv4.tcp_congestion_control").strip() != algo:
                raise RuntimeError(f"{host.name}: requested congestion control {algo!r} was not applied")
        write(out / "host_sysctl.txt", "\n".join(f"[{h.name}]\n{h.cmd('sysctl net.ipv4.tcp_congestion_control net.ipv4.tcp_ecn')}" for h in (h1, h2, h3)))
        write(out / "ping_baseline_h1.txt", h1.cmd("ping -c 10 -i 0.05 10.0.0.3"))
        write(out / "ping_baseline_h2.txt", h2.cmd("ping -c 10 -i 0.05 10.0.0.3"))
        intf = "s1-eth3"
        write(out / "qdisc_before.txt", s1.cmd(f"tc -s qdisc show dev {intf}") if (s1 := net["s1"]) else "")
        servers = []
        for port in (5201, 5202):
            servers.append(h3.popen(["iperf3", "-s", "-1", "-p", str(port), "--json"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True))
        time.sleep(1)
        clients = []
        for host, algo, port, name in ((h1, cfg["registered_algorithm_flow1"], 5201, "flow1"), (h2, cfg["registered_algorithm_flow2"], 5202, "flow2")):
            clients.append((name, host.popen(["iperf3", "-c", "10.0.0.3", "-p", str(port), "-t", str(DURATION), "-i", "1", "-J"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)))
        write(out / "ping_loaded_h1.txt", h1.cmd(f"ping -c 30 -i 1 10.0.0.3"))
        write(out / "ping_loaded_h2.txt", h2.cmd(f"ping -c 30 -i 1 10.0.0.3"))
        write(out / "qdisc_after.txt", s1.cmd(f"tc -s qdisc show dev {intf}"))
        write(out / "ss_h1.txt", h1.cmd("ss -tin"))
        write(out / "ss_h2.txt", h2.cmd("ss -tin"))
        for name, proc in clients:
            stdout, _ = proc.communicate(timeout=DURATION + 30)
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
    ap.add_argument("--rtt2", type=int, default=20)
    ap.add_argument("--queue", type=float, default=0.5)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--algorithm1", choices=["BBR3", "CUBIC"], default="BBR3")
    ap.add_argument("--algorithm2", choices=["BBR3", "CUBIC"], default="BBR3")
    args = ap.parse_args()
    setLogLevel("info")
    status = run_one(args.algorithm1, args.algorithm2, args.rtt2, args.queue, args.repeat)
    print(status, flush=True)
    raise SystemExit(0 if status == "completed" else 1)


if __name__ == "__main__":
    main()
