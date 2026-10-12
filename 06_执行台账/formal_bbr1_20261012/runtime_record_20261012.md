# BBRv1 Module Runtime Record

- Runtime kernel: `6.13.7-bbr3`
- Module: `/home/ubuntu/bbr3-build/source-bbr3/net/ipv4/tcp_bbr1.ko`
- Module vermagic: `6.13.7-bbr3 SMP preempt mod_unload modversions`
- Registered algorithm after `insmod`: `bbr1`
- Source: `/home/ubuntu/bbr-3.tar.gz`, `tcp_bbr1.c`, archive SHA256 `03008d20a9908d9087ed34fcf3d89cda267e4d88864b282bad61aa1025c025c4`
- Compatibility patch: `bbr1_module_compat_20261012.patch`; it replaces the unavailable exported `tcp_tso_autosize()` call with the local pacing-based sizing calculation used for this module build.
- Formal scope: E1/E2, 60 runs, same matrix and collection procedure as BBR2/BBRv3.
- Pilot: `pilot_bbr1_20261012` completed with h1/h2 using `bbr1`, all flow exits 0 and cleanup `ok`; a direct socket test also returned `actual=bbr1`.
- Formal batch started: `2026-10-12T02:47:59+08:00`.
- Detached launcher PID: `242692`.
- Batch ended: `2026-10-12T05:52:28+08:00`.
- Status: completed; 60/60 runs completed, 0 invalid, all topology cleanups reported `ok`.
- Analysis: `run_metrics.csv`, `condition_summary.csv`, `bbr1_acceptance_20261012.md`.
- Overleaf modified: no.
