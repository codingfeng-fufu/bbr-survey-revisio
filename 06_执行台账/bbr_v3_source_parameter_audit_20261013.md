# BBRv3 source snapshot parameter audit

Source and immutable commit URL/hash: literature_sources_20261012/google_bbr_v3_source_20261013.json.

Inspected tcp_bbr.c constants distinguish min_rtt_win_sec=10 from probe_rtt_win_ms=5000; probe_rtt_mode_ms=200 and probe_rtt_cwnd_gain=1/2 are separate parameters. full_loss_cnt=6 exists, but the exit condition also checks loss-round state and loss-rate criteria. ECN response is eligibility-dependent; constants alone do not establish activation.

Manuscript correction: ProbeRTT freshness windows are no longer described as guaranteed periodic entry intervals. BBRv2 parameters remain implementation-specific pending source checking. This source snapshot is not an attestation of the archived experiment kernel/module build, and does not prove historical deployment defaults.


Additional source inspection: bbr_check_ecn_too_high_in_startup gates on ecn_eligible and tests ce_ratio >= ecn_thresh for full_ecn_cnt consecutive rounds. Constants are 50% and 2 rounds, subject to integer fixed-point representation. bbr_update_ecn_alpha requires bbr_can_use_ecn (TCP_ECN_OK and TCP_ECN_LOW), nonzero ecn_factor, and min_rtt_us <= 5000 (unless RTT restriction disabled). This is not proof of compatibility or activation in arbitrary ECN networks.

The Startup loss exit checks loss_round_start, TCP_CA_Recovery, loss_events_in_round >= 6 and bbr_is_inflight_too_high; the counter increments on rate samples with losses. Six events must not be described as six packets. Manuscript prose and BBRv3 table cell corrected. BBRv2 source remains to be verified independently.
