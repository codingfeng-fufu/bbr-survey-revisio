#!/usr/bin/env python3
"""Short environment pilot; not a paper experiment."""

import json
import os
import re
import shlex
import subprocess
import time
from pathlib import Path

from mininet.log import error, info, setLogLevel
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.topo import Topo
from mininet.link import TCLink


OUT = Path(__file__).resolve().parent / "raw_logs"
RUN_ID = time.strftime("pilot_%Y%m%dT%H%M%S%z")
RUN_DIR = OUT / RUN_ID
RUN_DIR.mkdir(parents=True, exist_ok=False)

CAPACITY_MBPS = 100
RTT_MS = 20
ONE_WAY_DELAY = "10ms"
BDP_BYTES = CAPACITY_MBPS * 1_000_000 * (RTT_MS / 1000.0) / 8
QUEUE_PACKETS = max(1, round(0.5 * BDP_BYTES / 1500))
IPERF_SECONDS = 10


class TwoFlowBottleneck(Topo):
    """h1/h2 -> s1 -> s2 -> h3; only s1-s2 is rate-limited."""

    def build(self):
        h1 = self.addHost("h1", ip="10.0.0.1/24")
        h2 = self.addHost("h2", ip="10.0.0.2/24")
        h3 = self.addHost("h3", ip="10.0.0.3/24")
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(
            s1,
            s2,
            cls=TCLink,
            bw=CAPACITY_MBPS,
            delay=ONE_WAY_DELAY,
            max_queue_size=QUEUE_PACKETS,
            use_tbf=True,
            enable_ecn=False,
        )
        self.addLink(h3, s2)


def write_text(name, text):
    (RUN_DIR / name).write_text(text, encoding="utf-8")


def run_root(command, name):
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    write_text(name, result.stdout)
    return result.returncode, result.stdout


def parse_ping(text):
    match = re.search(r"rtt .* = ([0-9.]+)/([0-9.]+)/([0-9.]+)/([0-9.]+) ms", text)
    if not match:
        return {"matched": False}
    return {
        "matched": True,
        "min_ms": float(match.group(1)),
        "avg_ms": float(match.group(2)),
        "max_ms": float(match.group(3)),
        "mdev_ms": float(match.group(4)),
    }


def main():
    setLogLevel("info")
    metadata = {
        "run_id": RUN_ID,
        "purpose": "short environment pilot; not a paper experiment",
        "topology": "h1,h2 -> s1 -> s2 -> h3",
        "unique_bottleneck": "s1-s2",
        "capacity_mbps": CAPACITY_MBPS,
        "rtt_target_ms": RTT_MS,
        "one_way_delay": ONE_WAY_DELAY,
        "queue": "tbf + netem, netem limit; ECN disabled",
        "bdp_bytes": BDP_BYTES,
        "buffer_target_ratio": 0.5,
        "queue_limit_packets": QUEUE_PACKETS,
        "iperf_seconds": IPERF_SECONDS,
        "flow_count": 2,
        "version": "BBR selected in each Mininet host namespace; kernel implementation recorded outside this script",
    }
    write_text("run_config.json", json.dumps(metadata, indent=2) + "\n")

    net = None
    states = {"cleanup_rc": None, "start_rc": None, "flow_exit": {}}
    try:
        net = Mininet(
            topo=TwoFlowBottleneck(),
            switch=OVSBridge,
            controller=None,
            link=TCLink,
            autoSetMacs=True,
            autoStaticArp=True,
            cleanup=True,
        )
        net.start()
        states["start_rc"] = 0

        h1, h2, h3 = net.get("h1", "h2", "h3")
        s1, s2 = net.get("s1", "s2")
        pingall_loss = net.pingAll()
        write_text("pingall.txt", f"packet_loss_percent={pingall_loss}\n")
        bottleneck_s1 = str(s1.intf("s1-eth3"))
        bottleneck_s2 = str(s2.intf("s2-eth1"))
        metadata["bottleneck_interfaces"] = [bottleneck_s1, bottleneck_s2]
        write_text("run_config.json", json.dumps(metadata, indent=2) + "\n")

        for host in (h1, h2, h3):
            host.cmd("sysctl -q -w net.ipv4.tcp_congestion_control=bbr")
            host.cmd("sysctl -q -w net.ipv4.tcp_ecn=0")
        write_text(
            "host_sysctl.txt",
            "\n".join(
                f"[{host.name}]\n{host.cmd('sysctl net.ipv4.tcp_congestion_control net.ipv4.tcp_ecn')}"
                for host in (h1, h2, h3)
            ),
        )

        run_root(["tc", "-s", "qdisc", "show", "dev", bottleneck_s1], "qdisc_before_s1.txt")
        run_root(["tc", "-s", "qdisc", "show", "dev", bottleneck_s2], "qdisc_before_s2.txt")

        baseline_h1 = h1.cmd("ping -c 10 -i 0.05 10.0.0.3")
        baseline_h2 = h2.cmd("ping -c 10 -i 0.05 10.0.0.3")
        write_text("ping_baseline_h1.txt", baseline_h1)
        write_text("ping_baseline_h2.txt", baseline_h2)

        server1 = h3.popen(
            ["iperf3", "-s", "-1", "-p", "5201", "--json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        server2 = h3.popen(
            ["iperf3", "-s", "-1", "-p", "5202", "--json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        time.sleep(1)

        client1 = h1.popen(
            ["iperf3", "-c", "10.0.0.3", "-p", "5201", "-t", str(IPERF_SECONDS), "-i", "1", "-J"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        client2 = h2.popen(
            ["iperf3", "-c", "10.0.0.3", "-p", "5202", "-t", str(IPERF_SECONDS), "-i", "1", "-J"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        loaded_h1 = h1.cmd("ping -c 10 -i 0.2 10.0.0.3")
        loaded_h2 = h2.cmd("ping -c 10 -i 0.2 10.0.0.3")
        write_text("ping_loaded_h1.txt", loaded_h1)
        write_text("ping_loaded_h2.txt", loaded_h2)
        run_root(["tc", "-s", "qdisc", "show", "dev", bottleneck_s1], "qdisc_loaded_s1.txt")
        run_root(["tc", "-s", "qdisc", "show", "dev", bottleneck_s2], "qdisc_loaded_s2.txt")
        write_text("ss_h1.txt", h1.cmd("ss -tin"))
        write_text("ss_h2.txt", h2.cmd("ss -tin"))

        for name, proc in (("h1", client1), ("h2", client2), ("server_5201", server1), ("server_5202", server2)):
            try:
                stdout, _ = proc.communicate(timeout=20)
                states["flow_exit"][name] = proc.returncode
                write_text(
                    {
                        "h1": "iperf_client_h1.json",
                        "h2": "iperf_client_h2.json",
                        "server_5201": "iperf_server_5201.json",
                        "server_5202": "iperf_server_5202.json",
                    }[name],
                    stdout or "",
                )
            except Exception as exc:
                states["flow_exit"][name] = f"wait_error:{exc}"
                try:
                    proc.kill()
                    stdout, _ = proc.communicate(timeout=5)
                    write_text(
                        {
                            "h1": "iperf_client_h1.json",
                            "h2": "iperf_client_h2.json",
                            "server_5201": "iperf_server_5201.json",
                            "server_5202": "iperf_server_5202.json",
                        }[name],
                        stdout or "",
                    )
                except Exception as kill_exc:
                    states["flow_exit"][name] += f";kill_error:{kill_exc}"

        write_text(
            "rtt_summary.json",
            json.dumps(
                {
                    "baseline_h1": parse_ping(baseline_h1),
                    "baseline_h2": parse_ping(baseline_h2),
                    "loaded_h1": parse_ping(loaded_h1),
                    "loaded_h2": parse_ping(loaded_h2),
                },
                indent=2,
            )
            + "\n",
        )
    except Exception as exc:
        states["exception"] = repr(exc)
        error("pilot exception: %s\n" % exc)
    finally:
        if net is not None:
            try:
                net.stop()
                states["cleanup_rc"] = 0
            except Exception as exc:
                states["cleanup_rc"] = repr(exc)
        cleanup_rc, cleanup_out = run_root(["mn", "-c"], "mininet_cleanup.txt")
        states["mn_cleanup_rc"] = cleanup_rc
        write_text("exit_status.json", json.dumps(states, indent=2) + "\n")

    print(str(RUN_DIR))
    return 0 if states.get("exception") is None and states.get("cleanup_rc") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
