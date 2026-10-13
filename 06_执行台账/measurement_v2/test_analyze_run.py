import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('analyzer',Path(__file__).with_name('analyze_run.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def write(root,name,data):
    (root/name).write_text(json.dumps(data))


def fixture(root):
    write(root,'config.json',{'measurement_version':'v2-windowed-collector','status':'completed','analysis_start_s':30,'analysis_end_s':180,'run_id':'synthetic'})
    write(root,'exit_status.json',{'flow_exit':{'flow1':0,'flow2':0,'server1':0,'server2':0},'cleanup':'ok'})
    write(root,'measurement_timing.json',{'origin_monotonic_s':100,'clock_calibration_before':{'monotonic_s':130,'wall_s':1030},'clock_calibration_after':{'monotonic_s':280,'wall_s':1180},'queue_samples':[{'point':'bottleneck'}]})
    write(root,'transfer_end_timing.json',[{'point':'bottleneck','sample_start_s':181,'sample_end_s':181.1}])
    for i in [1,2]:
        write(root,f'iperf_server_{i}.json',{'intervals':[{'sum':{'start':29,'end':30,'seconds':1,'bytes':999999,'omitted':False}},{'sum':{'start':30,'end':31,'seconds':1,'bytes':125000,'omitted':False}},{'sum':{'start':179,'end':180,'seconds':1,'bytes':125000,'omitted':False}},{'sum':{'start':180,'end':181,'seconds':1,'bytes':999999,'omitted':False}}]})
        write(root,f'iperf_client_flow{i}.json',{'intervals':[{'sum':{'start':30,'end':31,'seconds':1,'retransmits':3}},{'sum':{'start':180,'end':181,'seconds':1,'retransmits':100}}]})
        (root/f'ping_window_h{i}.txt').write_text('[1029.0] 64 bytes time=100 ms\n[1030.0] 64 bytes time=2 ms\n[1179.0] 64 bytes time=4 ms\n[1180.0] 64 bytes time=200 ms\n')
    for label,counts in [('window_start',[10,10]),('window_end',[14,14]),('transfer_end',[15,15])]:
        (root/f'qdisc_{label}_bottleneck.txt').write_text(''.join(f'Sent 100 bytes 10 pkt (dropped {n}, overlimits 0 requeues 0)\n' for n in counts))


class AnalysisTests(unittest.TestCase):
    def test_window_and_counter_hierarchy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);fixture(root);r=m.analyze(root)
            self.assertEqual(r['total_goodput_mbps'],2)
            self.assertEqual(r['jain'],1)
            self.assertEqual(r['sender_window_retransmissions']['flow1']['count'],3)
            self.assertEqual(r['receiver_flows'][0]['covered_seconds'],2)
            self.assertAlmostEqual(r['receiver_flows'][0]['window_fraction_covered'],2/150)
            self.assertEqual(r['receiver_flows'][0]['max_internal_gap_s'],148)
            self.assertEqual(r['rtt_probe_samples']['h1']['median_ms'],3)
            self.assertEqual(r['queue_measurements'][0]['window_drop_deltas_by_qdisc'],[4,4])
            self.assertTrue(r['acceptance'].startswith('pending'))

    def test_zero_goodput_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);fixture(root)
            for i in [1,2]:
                write(root,f'iperf_server_{i}.json',{'intervals':[{'sum':{'start':30,'end':31,'seconds':1,'bytes':0}}]})
            with self.assertRaisesRegex(ValueError,'Jain undefined'):m.analyze(root)

    def test_invalid_receiver_values_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);fixture(root)
            write(root,'iperf_server_1.json',{'intervals':[{'sum':{'start':30,'end':31,'seconds':1,'bytes':-1}}]})
            with self.assertRaisesRegex(ValueError,'Invalid receiver'):m.analyze(root)

    def test_partial_exit_map_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);fixture(root)
            write(root,'exit_status.json',{'flow_exit':{'flow1':0},'cleanup':'ok'})
            with self.assertRaisesRegex(ValueError,'both clients'):m.analyze(root)

    def test_clock_step_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);fixture(root);t=json.loads((root/'measurement_timing.json').read_text());t['clock_calibration_after']['wall_s']+=1;write(root,'measurement_timing.json',t)
            with self.assertRaisesRegex(ValueError,'offset changed'):m.analyze(root)

    def test_counter_reset_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);fixture(root);(root/'qdisc_window_end_bottleneck.txt').write_text('Sent 100 bytes 10 pkt (dropped 1, overlimits 0)\nSent 100 bytes 10 pkt (dropped 1, overlimits 0)\n')
            with self.assertRaisesRegex(ValueError,'decreased'):m.analyze(root)

if __name__=='__main__':unittest.main()
