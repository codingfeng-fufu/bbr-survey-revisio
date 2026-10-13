# Tagged Linux v5.4 BBRv1 reference source audit

URL and hash in literature_sources_20261012/linux_v5_4_bbr1_source_20261013.json. This reference file is not an attestation of the archived module build.

CYCLE_LEN=8 denotes phases, not exactly eight packet-timed rounds. bbr_is_next_cycle_phase checks elapsed min-RTT time for unit gain; the gain>1 phase also checks loss or inflight target, while gain<1 can finish when inflight drains to BDP. Thus BBRv1 does consult losses in this probing transition even though it does not use a Reno-style loss-triggered multiplicative reduction as its primary controller model.

bbr_update_min_rtt checks filter expiration, idle_restart and current mode for ProbeRTT entry. Once inflight is reduced, it requires 200 ms and a completed packet-timed round before exit. A ten-second filter is not guaranteed ten-second entry periodicity; 200 ms is not guaranteed total ProbeRTT duration.

Candidate ProbeBW prose/table corrected to eight-phase sequence with conditional phase duration. Full compiled CAS and source-to-experiment identity remain outstanding.
