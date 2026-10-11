#!/usr/bin/env python3
"""Run frozen F07-v1 E3 cases under BBRv3 and CUBIC."""

import argparse
import csv
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
REPO = ROOT.parent.parent
PREDICTIONS = REPO / "07_Overleaf修订候选" / "F07_predictions_TO_FILL.csv"
DEFAULT_RUNS = ROOT / "runs"


def load_cases():
    with PREDICTIONS.open(encoding="utf-8", newline="") as f:
        return {row["case_id"]: row for row in csv.DictReader(f)}


class E3Topo(Topo):
    def __init__(self, capacity_mbps, rtt_ms, queue_packets, **opts):
        self.capacity_mbps = capacity_mbps
        self.rtt_ms = rtt_ms
        self.queue_packets = queue_packets
        super().__init__(**opts)

    def build(self):
        h1 = self.addHost("h1", ip="10.0.0.1/24")
        h2 = self.addHost("h2", ip="10.0.0.2/24")
        h3 = self.addHost("h3", ip="10.0.0.3/24")
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2, delay=f"{self.rtt_ms / 2:.3f}ms")
        self.addLink(
            s1, s2, cls=TCLink, bw=self.capacity_mbps,
            max_queue_size=self.queue_packets, use_tbf=True, enable_ecn=False,
        )


def write(path, text):
    path.write_text(text or "", encoding="utf-8")


def run_one(case_id, algorithm, repeat, runs_root, duration, warmup):
    case = load_cases().get(case_id)
    if case is None:
        raise ValueError(f"unknown F07 case: {case_id}")
    if case["source_type"] != "experiment" or case["framework_version"] != "F07-v1":
        raise ValueError(f"case is not a frozen F07-v1 experiment: {case_id}")
    capacity = int(case["capacity_mbps"])
    rtt_ms = int(case["reference_rtt_ms"])
    buffer_bytes = int(case["buffer_bytes"])
    ratio = case["buffer_bdp_ratio"]
    qtag = ratio.replace(".", "p")
    condition = f"{case_id}_{algorithm}_C{capacity}_R{rtt_ms}_Q{qtag}"
    run_id = f"{condition}_rep{repeat:02d}"
    out = runs_root / run_id
    out.mkdir(parents=False, exist_ok=False)
    queue_packets = max(1, math.ceil(buffer_bytes / 1500))
    registered = "bbr" if algorithm == "BBR3" else "cubic"
    cfg = {
        "run_id": run_id, "condition_id": condition, "experiment": "E3",
        "prediction_case_id": case_id, "framework_version": case["framework_version"],
        "algorithm_flow1": algorithm, "algorithm_flow2": algorithm,
        "registered_algorithm_flow1": registered, "registered_algorithm_flow2": registered,
        "capacity_mbps": capacity, "rtt1_ms": rtt_ms, "rtt2_ms": rtt_ms,
        "queue_bdp_multiplier_frozen": float(ratio), "queue_target_bytes_frozen": buffer_bytes,
        "queue_packets": queue_packets, "loss_source": case["loss_source"],
        "ecn": case["ecn"], "queue_management": case["queue_management"],
        "flow_count": int(case["flow_count"]), "duration_s": duration, "warmup_s": warmup,
        "analysis_start_s": warmup, "analysis_end_s": duration, "repeat": repeat,
        "manifest_id": "e3-bbr3-cubic-f07v1-20261011",
        "prediction_snapshot": {
            "throughput": case["throughput_prediction"], "delay": case["delay_prediction"],
            "fairness": case["fairness_prediction"],
            "retransmission": case["retransmission_prediction"],
            "tolerance_basis": case["tolerance_basis"],
        },
        "status": "running",
    }
    write(out / "config.json", json.dumps(cfg, indent=2) + "\n")
    net = None
    status = {"run_id": run_id, "start": time.time(), "flow_exit": {}, "cleanup": None}
    try:
        net = Mininet(
            topo=E3Topo(capacity, rtt_ms, queue_packets), switch=OVSBridge,
            controller=None, link=TCLink, autoSetMacs=True,
            autoStaticArp=True, cleanup=True,
        )
        net.start()
        h1, h2, h3 = net.get("h1", "h2", "h3")
        if net.pingAll() != 0:
            raise RuntimeError("topology pingAll failed")
        for host in (h1, h2):
            host.cmd(f"sysctl -q -w net.ipv4.tcp_congestion_control={registered}")
            host.cmd("sysctl -q -w net.ipv4.tcp_ecn=0")
            actual = host.cmd("sysctl -n net.ipv4.tcp_congestion_control").strip()
            if actual != registered:
                raise RuntimeError(f"{host.name}: requested {registered!r}, got {actual!r}")
        h3.cmd("sysctl -q -w net.ipv4.tcp_congestion_control=cubic")
        h3.cmd("sysctl -q -w net.ipv4.tcp_ecn=0")
        write(out / "host_sysctl.txt", "\n".join(
            f"[{h.name}]\n{h.cmd('sysctl net.ipv4.tcp_congestion_control net.ipv4.tcp_ecn')}"
            for h in (h1, h2, h3)
        ))
        write(out / "ping_baseline_h1.txt", h1.cmd("ping -c 10 -i 0.05 10.0.0.3"))
        write(out / "ping_baseline_h2.txt", h2.cmd("ping -c 10 -i 0.05 10.0.0.3"))
        s1 = net["s1"]
        intf = "s1-eth3"
        write(out / "qdisc_before.txt", s1.cmd(f"tc -s qdisc show dev {intf}"))
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
        write(out / "qdisc_after.txt", s1.cmd(f"tc -s qdisc show dev {intf}"))
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
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--algorithm", choices=["BBR3", "CUBIC"], required=True)
    ap.add_argument("--repeat", type=int, required=True)
    ap.add_argument("--duration", type=int, default=180)
    ap.add_argument("--warmup", type=int, default=30)
    ap.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS)
    args = ap.parse_args()
    args.runs_root.mkdir(parents=True, exist_ok=True)
    setLogLevel("info")
    status = run_one(args.case_id, args.algorithm, args.repeat, args.runs_root, args.duration, args.warmup)
    print(status, flush=True)
    raise SystemExit(0 if status == "completed" else 1)


if __name__ == "__main__":
    main()
