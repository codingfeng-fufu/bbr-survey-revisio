# Random-Loss Extension Runtime Record

- Scope: BBRv3/CUBIC × 0/0.1% artificial loss × 5 repeats = 20 runs.
- Runtime kernel: `6.13.7-bbr3`; BBR source identity: `BBR_VERSION=3`; runtime name: `bbr`.
- Fixed path: 100 Mbps, 20 ms RTT, 2×BDP queue, ECN off.
- Artificial loss point: `s2-eth1`, the h3 access link, separate from bottleneck `s1-eth3`.
- Required evidence per run: artificial-loss qdisc before/after, bottleneck qdisc before/after, `tc` configuration, `ss`, iperf3 JSON, and exit status.
- Random seed: not exposed by the Mininet/iproute2 interface used here; record as unavailable rather than fabricate one.
- Pilot: `pilot_random_loss_20261012` completed a 0.1% BBRv3 run and a 0% CUBIC run; both exited cleanly. The 0.1% pilot recorded artificial-link drops and zero bottleneck drops.
- Formal batch started: `2026-10-12T01:00:38+08:00`.
- Detached launcher PID: `202994`.
- Batch ended: `2026-10-12T02:02:01+08:00`.
- Status: completed; 20/20 runs completed, 0 invalid, all topology cleanups reported `ok`.
- Analysis: `run_metrics.csv`, `condition_summary.csv`, `random_loss_acceptance_20261012.md`.
- Observed artificial-link drops were separated from zero bottleneck drops in all 0.1% runs; retransmissions are reported by algorithm and loss level.
- Overleaf modified: no.
