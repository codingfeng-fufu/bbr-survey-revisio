"""Collect timed, concurrent RTT probes and queue snapshots for a new run.

Invoke immediately before starting traffic with a monotonic origin, then call
capture_window after starting clients. This is a new collector, not a repair
of archived samples. The caller must save final counters after all clients exit.
"""
import json
import math
import subprocess
import time
from pathlib import Path


def snapshot(output, label, points, origin, clock=time.monotonic):
    records = []
    for name, (host, interface) in points.items():
        if not interface or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.:' for c in interface):
            raise ValueError('Invalid network interface')
        started = clock()
        text = host.cmd('tc -s qdisc show dev ' + interface)
        ended = clock()
        Path(output, f'qdisc_{label}_{name}.txt').write_text(text or '')
        records.append({'point': name, 'sample_start_s': started-origin,
                        'sample_end_s': ended-origin, 'file': f'qdisc_{label}_{name}.txt'})
    return records


def capture_window(output, hosts, points, origin, warmup, duration,
                   clock=time.monotonic, sleep=time.sleep, wall_clock=time.time):
    if not math.isfinite(warmup) or not math.isfinite(duration) or not 0 <= warmup < duration:
        raise ValueError('Require finite 0 <= warmup < duration')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    sleep(max(0, origin+warmup-clock()))
    samples = snapshot(output, 'window_start', points, origin, clock)
    calibration_before = {"monotonic_s": clock(), "wall_s": wall_clock()}
    probes = []
    probe_records = []
    try:
        for name, host in hosts.items():
            remaining = origin+duration-clock()
            if remaining <= 0:
                raise RuntimeError('Measurement window expired before probe start')
            handle = (output / f'ping_window_{name}.txt').open('w')
            try:
                process = host.popen(['ping', '-n', '-D', '-i', '1', '10.0.0.3'],
                                     stdout=handle, stderr=subprocess.STDOUT, text=True)
            except BaseException:
                handle.close()
                raise
            probes.append((name, process, handle, clock()-origin))
        sleep(max(0, origin+duration-clock()))
        samples += snapshot(output, 'window_end', points, origin, clock)
    finally:
        for name, process, handle, started in probes:
            try:
                if process.poll() is None:
                    process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
                probe_records.append({'host': name, 'start_s': started,
                                      'stop_s': clock()-origin, 'returncode': process.returncode})
            finally:
                handle.close()
        calibration_after = {"monotonic_s": clock(), "wall_s": wall_clock()}
        record = {'clock_calibration_before': calibration_before,
                  'clock_calibration_after': calibration_after,
                  'origin_monotonic_s': origin, 'requested_start_s': warmup,
                  'requested_end_s': duration, 'queue_samples': samples,
                  'probe_processes': probe_records,
                  'note': 'Sequential snapshot commands have recorded bounds; probes overlap but do not start atomically. Final transfer counters must be captured separately after client exit.'}
        (output/'measurement_timing.json').write_text(json.dumps(record, indent=2)+'\n')
    return record


def stop_processes(processes):
    """Attempt every owned process; return diagnostics instead of hiding failures."""
    records=[]
    for name, process in processes:
        record={'process':name}
        try:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
            record['returncode']=process.returncode
        except Exception as exc:
            record['error']=repr(exc)
        records.append(record)
    return records
