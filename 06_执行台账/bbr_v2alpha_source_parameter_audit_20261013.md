# BBRv2alpha source parameter audit

Immutable commit URL and SHA256: literature_sources_20261012/google_bbr_v2alpha_source_20261013.json.

min_rtt_win_sec=10 and probe_rtt_win_ms=5000 are distinct. full_loss_cnt=8 counts loss-marking events, with Recovery/loss-round/inflight conditions, not eight packets. bbr_ecn_enable=false by default; sender eligibility uses the enabled knob and min-RTT condition (default ecn_max_rtt_us=5000). ProbeBW Down gain=3/4. Module parameters can change defaults.

The separately inspected BBRv3 snapshot uses integer Down gain BBR_UNIT*91/100, or 232/256 with BBR_UNIT=256, rather than exactly 0.9. Manuscript prose/table corrected. Neither snapshot proves archived experiment source identity or historical defaults across all revisions.
