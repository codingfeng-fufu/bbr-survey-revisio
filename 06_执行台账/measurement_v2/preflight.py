"""Reject a new run unless its kernel matches the archived target identity.
Matching a kernel string is necessary but not source attestation; retain manifest.
"""
import json
import platform
import subprocess


def verify_target(manifest_path, algorithm, kernel_reader=platform.release,
                  command_runner=subprocess.run):
    manifest=json.loads(manifest_path.read_text())
    expected=manifest.get('runtime_kernel')
    actual=kernel_reader()
    if not expected or actual!=expected:
        raise RuntimeError(f'Target kernel mismatch: expected {expected!r}, observed {actual!r}')
    if algorithm=='BBR3' and manifest.get('source_bbr_version')!=3:
        raise RuntimeError('Manifest does not establish BBRv3 source marker')
    result=command_runner(['sysctl','-n','net.ipv4.tcp_available_congestion_control'],capture_output=True,text=True,check=True)
    required='bbr' if algorithm=='BBR3' else 'cubic'
    if required not in result.stdout.split():
        raise RuntimeError(f'Required runtime algorithm absent: {required}')
    return {'expected_kernel':expected,'observed_kernel':actual,
            'available_algorithms':result.stdout.split(),'requested_algorithm':algorithm,
            'identity_limit':'Kernel string and archived manifest checked; verify deployed source/build hashes independently before acceptance.'}
