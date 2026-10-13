import importlib.util
import subprocess
import tempfile
import json
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('preflight',Path(__file__).with_name('preflight.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Tests(unittest.TestCase):
    def test_wrong_kernel_rejected_before_algorithm_query(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'manifest.json';p.write_text(json.dumps({'runtime_kernel':'6.13.7-bbr3','source_bbr_version':3}))
            def query(*args,**kwargs): self.fail('Should not query after kernel mismatch')
            with self.assertRaisesRegex(RuntimeError,'kernel mismatch'):m.verify_target(p,'BBR3',lambda:'5.4.0',query)

    def test_missing_runtime_algorithm_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'manifest.json';p.write_text(json.dumps({'runtime_kernel':'6.13.7-bbr3','source_bbr_version':3}))
            with self.assertRaisesRegex(RuntimeError,'algorithm absent'):
                m.verify_target(p,'BBR3',lambda:'6.13.7-bbr3',lambda *a,**k:subprocess.CompletedProcess(a,0,stdout='reno cubic'))

    def test_matching_target_keeps_identity_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'manifest.json';p.write_text(json.dumps({'runtime_kernel':'6.13.7-bbr3','source_bbr_version':3}))
            result=m.verify_target(p,'BBR3',lambda:'6.13.7-bbr3',lambda *a,**k:subprocess.CompletedProcess(a,0,stdout='reno bbr cubic'))
            self.assertIn('hashes',result['identity_limit'])

if __name__=='__main__':unittest.main()
