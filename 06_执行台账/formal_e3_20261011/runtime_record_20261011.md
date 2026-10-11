# E3 Runtime Record

- Framework: `F07-v1`
- Prediction source: `07_Overleaf修订候选/F07_predictions_TO_FILL.csv`
- Runtime kernel: `6.13.7-bbr3`
- BBR identity: source `BBR_VERSION=3`, runtime algorithm name `bbr`
- Scope: 8 frozen cases × BBRv3/CUBIC × 5 repeats = 80 runs.
- E3 runner: `06_执行台账/formal_e3_20261011/run_e3.py`
- Batch command: `sudo -n bash 06_执行台账/formal_e3_20261011/run_e3.sh`
- Controller log: `06_执行台账/formal_e3_20261011/batch_controller_20261011.log`
- Absolute buffer values and ratios are copied from frozen F07-v1 predictions; no prediction was changed.
- Pilot: `pilot_e3_20261011` completed two 10-second runs (BBRv3 and CUBIC), both exit status `completed` with topology cleanup `ok`.
- Formal batch started: `2026-10-11T20:04:40+08:00`.
- Detached launcher PID: `112151` (PPID 1 at launch).
- Batch ended: `2026-10-12T00:10:34+08:00`.
- Status: completed; 80/80 runs completed, 0 invalid, all topology cleanups reported `ok`.
- Analysis: `run_metrics.csv`, `condition_summary.csv`, `prediction_observation.csv`, `e3_acceptance_20261012.md`.
- Prediction judgement: pending manual F07-v1 review; no rule or prediction was changed after observing results.
- Coverage limitation: this E3 batch covers congestion loss only; independent random-loss validation remains unrun.
- Overleaf modified: no.
