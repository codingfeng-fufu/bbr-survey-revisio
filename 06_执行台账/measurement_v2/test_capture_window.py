import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('collector', Path(__file__).with_name('capture_window.py'))
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


class Clock:
    def __init__(self): self.now=0
    def read(self): return self.now
    def sleep(self, seconds): self.now+=seconds


class Process:
    returncode=None
    def poll(self): return self.returncode
    def terminate(self): self.returncode=-15
    def wait(self, timeout): return self.returncode


class Host:
    def __init__(self, clock, fail=False): self.clock=clock;self.fail=fail;self.processes=[]
    def cmd(self, command): self.clock.now+=0.1;return 'queue counters\n'
    def popen(self, command, **kwargs):
        if self.fail: raise RuntimeError('probe startup failed')
        process=Process();self.processes.append(process);return process


class CollectorTests(unittest.TestCase):
    def test_probes_overlap_window_and_snapshots_have_bounds(self):
        clock=Clock();a=Host(clock);b=Host(clock)
        with tempfile.TemporaryDirectory() as output:
            result=collector.capture_window(output, {'h1':a,'h2':b}, {'bottleneck':(a,'s1-eth3')}, 0, 30, 180, clock.read,clock.sleep)
            probes=result['probe_processes']
            self.assertEqual(len(probes),2)
            self.assertLess(max(p['start_s'] for p in probes),min(p['stop_s'] for p in probes))
            self.assertGreaterEqual(result['queue_samples'][0]['sample_start_s'],30)
            self.assertGreaterEqual(result['queue_samples'][1]['sample_start_s'],180)
            self.assertTrue(all(p.returncode is not None for h in [a,b] for p in h.processes))
            self.assertTrue(Path(output,'measurement_timing.json').exists())

    def test_failure_cleans_already_started_probe(self):
        clock=Clock();a=Host(clock);b=Host(clock,fail=True)
        with tempfile.TemporaryDirectory() as output:
            with self.assertRaises(RuntimeError):
                collector.capture_window(output,{'h1':a,'h2':b},{},0,30,180,clock.read,clock.sleep)
            self.assertEqual(a.processes[0].returncode,-15)
            self.assertTrue(Path(output,'measurement_timing.json').exists())

    def test_invalid_window_does_not_spawn(self):
        clock=Clock();a=Host(clock)
        with tempfile.TemporaryDirectory() as output:
            with self.assertRaises(ValueError):
                collector.capture_window(output,{'h1':a},{},0,180,30,clock.read,clock.sleep)
            self.assertEqual(a.processes,[])

if __name__=='__main__': unittest.main()
