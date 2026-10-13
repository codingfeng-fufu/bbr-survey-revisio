# Measurement v2: prepared, not network-validated

New runners: `formal_e3_20261011/run_e3_measurement_v2.py` and `formal_random_loss_20261012/run_random_loss_measurement_v2.py`. The historical runners and archived results remain intact. New default outputs use `runs_measurement_v2/`.

The collector starts two overlapping ping processes after warmup and records monotonic start/stop bounds. It captures queue counters at window boundaries, and the runners capture final transfer counters after all client/server processes exit. Probe output includes wall-clock timestamps (`ping -D`). Actual command bounds, rather than an assumed exact start, must be used during analysis.

E3 v1 cases with inconsistent physical BDP labels are rejected. Do not silently change frozen bytes or labels. Reconciled cases need a separately versioned input/protocol, preserving v1 and its audit. These runners do not supply revised prediction tolerances.

The old analysis scripts are not v2-compatible acceptance tools: they expect `ping_loaded_*` and historical queue filenames and compute full-run throughput. V2 analysis must use interval-level receiver bytes, timestamped RTT samples, window-start/end counters, and per-run coverage checks. No current manuscript number is replaced by an unrun v2 result.

Local validation: syntax checks and three simulated-clock tests cover overlapping probes, bounded snapshot timing, invalid windows and cleanup after probe startup failure. They do not validate Mininet, kernel identity, packet loss, or a real 180-second network run. A target-kernel pilot must pass before formal reruns.

## Preliminary v2 extractor

`python 06_执行台账/measurement_v2/analyze_run.py RUN_DIRECTORY --output RESULT.json` extracts complete in-window receiver intervals, individual ping RTT median/nearest-rank p95, and separately paired qdisc counters. It rejects historical v1 data, incomplete exits, missing samples, changed counter hierarchy, and counter resets. Nested qdisc counters remain separate to avoid double counting.

The extractor does not sign off a prediction. Strict common-window filtering of ping wall-clock reply timestamps still requires recorded wall-to-monotonic clock calibration, which the current collector has not yet added. Per-flow launch alignment and interval gaps also require coverage validation before formal acceptance. Syntax and rejection of a real archived v1 directory were checked; no real v2 run exists yet.

## Clock calibration update

The collector now records wall/monotonic offsets before and after sampling. The extractor retains only timestamped exact RTT replies in the declared half-open window and rejects missing calibration or offset drift above 50 ms. This 50-ms check is a collection-integrity guard, not a new F07 prediction tolerance. Probe launch bounds and actual overlap still require review, and receiver intervals remain relative to each transfer's own origin. The old statement that calibration is absent applies to the prior development snapshot.

Validation: existing three process/timing tests pass; a boundary example verifies exclusion at the window end, retention at the start, median and nearest-rank p95. No target-kernel network test has been run.

## Extractor validation and coverage

Three additional synthetic end-to-end checks passed: exact receiver interval selection/RTT filtering/hierarchical counter preservation, clock-step rejection, and counter-reset rejection. Receiver output now explicitly reports fraction of the requested window covered and maximum internal gap; overlapping or unordered intervals are rejected. A sparse input may yield descriptive measurements but remains pending acceptance and exposes its missing coverage. These synthetic fixtures are not network experiment results.

## Target identity preflight

Both new runners now reject a kernel different from their archived manifest's `6.13.7-bbr3`, require the BBRv3 source marker for BBR3-labelled runs, and query runtime availability before creating a per-run output. Preflight evidence is saved. Three simulated checks pass for kernel mismatch, missing registration and matching-target limitations. Matching a kernel name is not build/source attestation; deployed hashes still require verification. Existing runners/results are unchanged.

## Owned traffic-process cleanup

New runners track client/server processes and attempt bounded termination before topology shutdown, including after collector failure. Individual cleanup errors are retained and invalidate the run; one failed termination does not prevent attempts on later processes. Syntax checks and a simulated failure-continuation check pass. Kernel/network integration and actual resource cleanup still need the target-node pilot.

## Partial launch failure

Client and server creation now appends each successfully launched process immediately. If a later `popen` fails, existing handles remain available to the owned-process cleanup path. This avoids list-comprehension assignment losing partial launches. Both runner syntax checks pass; real Mininet startup failure injection remains part of target-node pilot validation.

## Retransmission window extraction

V2 extraction includes sender interval retransmission counts and actual covered seconds. Missing interval counters produce undetermined, without substituting the end-of-run total or inventing a loss-rate denominator. Synthetic checks verify exclusion of outside-window counts and refusal to use a full-run total when interval fields are missing. Actual v2 logs and common-time alignment remain pending target-node validation.

## Complete exit-map requirement

Analysis now requires zero exits for flow1, flow2, server1 and server2, plus successful topology cleanup; a partial exit dictionary cannot validate a run. Recorded owned-process cleanup errors also reject analysis. Four analyzer tests pass, including a partial-exit-map fixture. This does not establish target-kernel experiment validity.

## Numeric validity

Receiver intervals must contain finite values, positive durations/end-start and nonnegative bytes; configured windows must be finite and ordered. Aggregate goodput must be positive before Jain is computed. Six analyzer tests now pass, including negative-byte and zero-goodput rejection. No values from these synthetic fixtures are research results.
