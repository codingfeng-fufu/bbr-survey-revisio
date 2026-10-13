# Response to reviewers — audited working draft

Manuscript: COMNET-D-26-03761. This is an English working draft, not a submission-ready response. Changes described below exist in the repository candidate; their incorporation into the Overleaf main manuscript and final page locations remains unverified. Open items must be completed before the response is submitted.

## Reviewer 1

### R1-M1: RTT, inflight, and bandwidth allocation

Thank you for identifying the inference gap. We revised the candidate discussion to distinguish the BDP operating point from observed bandwidth shares. The revised discussion treats fairness as dependent on probing, queue conditions, implementation, and flow count. Archived two-flow measurements provide condition-specific rates and Jain indices. They do not prove an internal mechanism from the BDP identity alone. Candidate locations: `sec:fairness`, `sec:controlled_experiments`. Final page numbers: pending main-manuscript integration.

### R1-M2: Operation without ECN

We agree that disabling ECN does not make BBRv2 or BBRv3 equivalent to BBRv1. The candidate text distinguishes unavailable ECN feedback from remaining loss-driven updates and state logic. It also separates source identity, kernel environment, and runtime registration name. The experiment's no-ECN setting is reported as a configuration choice, not an algorithm identity. Evidence: mechanism audit, implementation manifests, and candidate version discussion. Final table and page references remain to be checked.

### R1-M3: Sources and ranges of applicability boundaries

We revised the candidate boundaries as working bins and require capacity, reference RTT, absolute buffer, implementation, queue policy, and flow count to accompany them. Subsequent audit identified inconsistent frozen buffer labels in four E3 cases. Those cases are not accepted as validation of the intended input bins. Full-text source verification and reconciled validation remain open; we cannot yet claim that this concern has been fully resolved.

### R1-M4: Definition of suitability

The candidate framework reports goodput, delay, fairness, and retransmissions separately, with an undetermined outcome where evidence is insufficient. It avoids a single undefined suitability score. The controlled-experiment section reports the observation windows and distinguishes receiver summaries from early RTT probes and in-run queue snapshots. Final checks of all scenario tables remain necessary. The candidate broadband section and summary table no longer assert a fixed 48% BBRv3 advantage. The acquired Gomez author manuscript does not substantiate the quoted 95/63.8-Mbps pair; its separate 100-Gbps low-RTT experiment reports different, configuration-specific results. Figure 13 has been visually checked, with MTU and parallel streams retained. Other experiments and full-study eligibility remain pending.

### R1-M5: Added value relative to existing surveys

The candidate contribution is a conditional evidence organization and an explicitly audited controlled comparison, rather than a new congestion-control algorithm. A complete comparison against existing surveys requires the remaining M07 full-text work. We retain this item as unresolved rather than claim comprehensive novelty from an incomplete comparison table.

### R1-M6: Evidence for AI-related conclusions

The AI section still requires study-specific evidence on evaluation conditions, inference costs, interpretability, and transfer to deployment. Broad claims must be narrowed or removed where those fields are unavailable. This issue is not closed by general statements about the promise of learning-based control. We have begun a source-level evidence table. In the inspected WiFi study (DOI 10.3390/fi16090330), the action selects a CCA and the authors explicitly use offline DRL; this is different from tuning the BBR state machine or demonstrating an online controller. Its reward combines throughput, latency and loss, without an explicit Jain term in the inspected definition. Training convergence does not establish deployment overhead or fairness generalization. Full-study appraisal remains pending. Separately, TCP-Drinc full-study eligibility and DOI metadata have been reviewed. The candidate AI section now reports its ns-3 action space, scoped Jain estimate and overlapping baseline intervals, without presenting the result as superiority over BBR or an online BBRv3 deployment. Its bibliography candidate requires merging into the actual main refs.bib.

### R1-m1: Scientific wording

We revised the candidate conclusion to remove the claim that the multiplicative BDP structure alone establishes RTT unfairness. It now states the observed configuration dependence and the validation limitations. A final manuscript-wide language pass remains pending integration.

### R1-m2: Repetition in the abstract

The candidate abstract distinguishes literature synthesis from the supplemental search whose full-text screening is ongoing. The abstract and highlights now include the archived experiments and their audit limitations, consistent with the candidate conclusion. Final full-manuscript readability and page checks remain pending.

### R1-m3: Figure 2 delay definition

The propagation and queuing components must be separately labelled. The original figure assets and their source history are not present in the candidate directory, so final visual acceptance remains open. We will not infer that the figure has been corrected from text changes alone.

## Reviewer 2

### R2-1: Reproducibility of the review process

The candidate methods and search flowchart now describe the retained OpenAlex/Crossref search rather than an unreconstructed seven-database search. They distinguish 2,618 exported records and their screening-stage counts from the manuscript's 165-key citation baseline. Retrieval retained at most 200 records per query, and 12 of 16 archived responses report more hits than were saved. The exports are therefore a capped sample, not an exhaustive enumeration; broad Crossref hit totals are not relevant-study counts. The historical human-screening file was generated by keyword rules; its counts are automated triage labels, not proof of independent manual screening. All 218 groups originally labelled excluded only by these rules have now been independently reassessed using available indexed titles and abstracts, because an unbounded gene substring can match relevant network terminology. The reassessment restored 174 groups to full-text review and excluded 44 at title/abstract level with documented reasons. This does not complete full-text screening. Existing citation is no longer an inclusion criterion. A subsequent normalization audit found that the 400-record candidate queue contains 328 report groups, with 72 duplicate record pairs across sources; this is not a final included-study count. The full exported record set yields 1,916 normalized report groups, with an original automated split of 1,698 forwarded groups and 218 proposed exclusions, plus 25 historical source-record screening conflicts. Subsequent independent reassessment has restored relevant reports to eligibility review; current counts are tracked in the regenerated ledger. Those conflicts have been reviewed at title/abstract level and retained for full-text assessment; this does not establish final inclusion. The smaller candidate queue does not cover the entire remaining review workload. Full-text eligibility and final inclusion remain incomplete; the present record does not substantiate a completed 165-study systematic review. Evidence: frozen M02 protocol, raw exports, screening logs, and current full-text queue. Candidate locations: `sec:method`, `fig:prisma`.

### R2-2: Formal criteria and independent validation

F07-v1 predictions and archived measurements are preserved. A subsequent audit identified input-label errors, a difference between the planned post-warmup window and full-run primary analysis, and queue snapshots collected before transfer completion. Historical automatic support decisions are not accepted as formal validation. A separate audited observation table records undetermined outcomes and reasons. New collection scripts are prepared, but target-kernel pilot runs, reconciled inputs, and final acceptance are outstanding. We therefore do not claim complete independent validation.

### R2-3: Version parameters and ECN statements

The candidate version discussion has been revised to separate mechanism evidence from observed performance. The source/kernel audit and implementation manifests provide the basis for checking Table 3. The final table must still be reconciled with the integrated manuscript; a performance difference alone is not treated as proof of a particular internal state transition.

An immutable Google BBRv3 source snapshot has additionally been archived. It distinguishes the minimum-RTT filter from ProbeRTT freshness checks and makes Startup loss/ECN exits conditional. The candidate now distinguishes loss-marking events from lost packets and ECN capability from sender eligibility. This snapshot does not attest to the archived experiment builds; A separately pinned BBRv2alpha source confirms eight loss-marking events, distinct RTT windows and a default-disabled ECN knob; the BBRv3 snapshot uses a fixed-point Down gain of 232/256. Matching these revisions and runtime parameters to the archived experiment builds remains outstanding.

### R2-4: Figure provenance and AI disclosure

This item requires factual confirmation from the figure creators. The candidate repository does not establish which tools produced Figures 2–6 or which steps used generative AI. Tool names, model names, usage, and manual checks must be confirmed before the disclosure is finalized. We have not treated an unconfirmed disclosure draft as completed evidence.

## Reviewer 3

### R3-1: Abstract readability

The candidate abstract no longer presents the supplemental search as a completed systematic review. Unverified external throughput multipliers have been removed. The revised abstract reports the 340-run scope, conditional findings, and outstanding validation limitations. Final abstract acceptance remains pending author review and full-manuscript integration.

### R3-2: BDP-Veno and OVeno

We verified both papers' bibliographic metadata directly against Crossref. BDP-Veno is published in Journal of Network and Computer Applications 231 (2024), article 103983, DOI 10.1016/j.jnca.2024.103983. OVeno is published in Simulation Modelling Practice and Theory 142 (2025), article 103121, DOI 10.1016/j.simpat.2025.103121. Both are by Subhra Priyadarshini Biswal and Sanjeev Patel. The publisher API responses obtained in this environment contain metadata only. Full-text mechanism and experimental-condition checks remain outstanding; no quantitative comparison with BBR is signed off from these responses.

### R3-3: Analytical contribution

The candidate provides explicit framework inputs, separate outputs, and an audited experimental comparison. It makes no claim to propose a new transport algorithm. Because validation deficiencies remain, the present contribution is bounded to evidence organization and descriptive measurements. Stronger validation claims require completing the outstanding experiments and source checks.

The theoretical discussion now identifies the Mathis expression as a Reno-like steady-state approximation, rather than a universal CUBIC throughput bound. We removed the claimed derivation of 1 MB and 10 MB performance thresholds and the fixed WAN throughput ratios pending verification against the original measurement conditions. The BDP bins organize the discussion; they do not prove controller superiority or a fairness transition. Candidate locations: `sec:framework_dim` and `sec:wan`.

### R3-4: Implementation details and reproducibility

The repository retains configurations, raw logs, implementation identities, commands, and analysis scripts for 340 runs. Saved-data analysis was reproduced on the current node; some standard deviations differ only in floating-point trailing digits. A separate window sensitivity analysis covers every archived run. These checks reproduce saved-data computations, not independent network runs. The new collector records overlapping post-warmup RTT probes and timed queue snapshots, but real target-kernel validation is outstanding. Candidate location: `sec:controlled_experiments`.

### R3-5: Positive assessment of the remaining presentation

Thank you for this assessment. We will preserve the useful explanatory structure while completing the source, figure, and consistency checks required for the revision.

## Submission gate

Before use, reconcile this draft with the completed work, replace pending locations with actual sections/pages, obtain figure/author factual confirmations, and review the full compiled manuscript. Unresolved issues cannot be changed to completed merely by deleting these qualifications.
