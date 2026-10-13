# Response to Reviewers

Manuscript: COMNET-D-26-03761. We thank the editor and reviewers for reading the manuscript carefully. Several comments identified errors in our reasoning and gaps in the evidence we reported. We have corrected those errors, added the experimental and analytical material described below, and stated where the available records do not allow us to meet the original request in full. Page numbers refer to the revised manuscript.

## Reviewer 1

### R1-M1: RTT, inflight, and bandwidth allocation

Reviewer comment (summary): The in-flight/BDP identity alone does not determine bandwidth allocation; a longer propagation RTT need not imply a larger bandwidth share.

Response: We agree. Our original discussion treated a rate–delay identity as if it determined bandwidth allocation. That inference was incorrect. We have removed it and separated the BDP operating point from measured flow shares. The revised discussion treats fairness as dependent on probing, queue conditions, implementation, and flow count. We also corrected Figure 7’s caption to identify the plotted RTT, which includes propagation and queueing components, rather than label it as queueing delay alone. The E1 figure summarizes five repetitions in each of 36 conditions. Across the 24 unequal-RTT conditions, mean long-RTT shares and Jain indices are reported numerically in Section 7.2. E2 provides all twelve BBR/CUBIC comparisons; total goodput is 95.58–95.59 Mbps while BBR shares range from 0.143 to 0.327. These measurements describe the observed allocation; they do not establish its cause from the BDP identity. We also redrew the fairness schematics to remove the RTT-proportional bandwidth-share law and distinguish model targets from measured allocation.

Manuscript locations: Section 5 (p. 15); Section 7 (p. 21); Figure 9 (p. 23); Table 10 (p. 24); Section 3.5 (p. 12); Figure 5 (p. 16); Figure 6 (p. 17).

### R1-M2: Operation without ECN

Reviewer comment (summary): The manuscript implies that BBRv2/v3 revert toward BBRv1 without ECN, overlooking their loss-driven mechanisms.

Response: Our original description was misleading. Without ECN, BBRv2 and BBRv3 lose the ECN feedback channel but retain their loss-driven bounds and state logic. We have corrected the text and version table accordingly. The revised text distinguishes unavailable ECN feedback from remaining loss-driven updates and state logic. It also separates source identity, kernel environment, and runtime registration name. The experiment's no-ECN setting is reported as a configuration choice, not an algorithm identity. The experimental supplement includes the implementation manifests used to identify the tested controllers. We redrew the BBRv1 architecture to remove later-version ECN logic and unconditional ProbeRTT timing.

Manuscript locations: Section 2.2 (p. 6); Table 4 (p. 9); Figure 9 (p. 23); Table 10 (p. 24); Section 2.1 (p. 5); Figure 3 (p. 7); Figure 4 (p. 8).

### R1-M3: Sources and ranges of applicability boundaries

Reviewer comment (summary): Explain the numerical applicability boundaries and reconcile the medium-buffer ranges in the text and table.

Response: We did not provide a defensible basis for presenting the numerical boundaries as general selection thresholds. We have recast them as working bins for organizing evidence. Buffer depth now consistently uses shallow below 1.5 BDP, medium from 1.5 to 10 BDP, and deep above 10 BDP. Section 3.2 relates these bins to the measurements discussed by Cao and Jaeger, while explaining that their effects depend on version, queue policy, RTT and flow count. The 1-MB and 10-MB BDP boundaries are also organizing choices; we have not derived or validated them as performance transition points. We have corrected the former 1–10 BDP range in the table.

The experiments report absolute queue sizes as well as their reference-BDP ratios. In four 50-Mbps E3 cases, the physical ratios are 4 and 16 despite frozen labels of 1 and 4. We retain the original records and report the corrected ratios. Those cases do not validate the intended buffer bins.

Manuscript locations: Section 3.2 (p. 10); Section 3.4 (p. 10); Table 11 (p. 24).

### R1-M4: Definition of suitability

Reviewer comment (summary): Define suitability by performance metrics, specify the reference RTT for BDP, and account for version, queue management, flow count and scenario capacity/RTT.

Response: We agree that “suitable” was too ambiguous. The revision removes the unexplained aggregate suitability ratings and evaluates throughput, delay, fairness and retransmissions separately. Section 3.5 gives explicit, service-dependent requirements and returns meets, does not meet or undetermined for each required metric. For example, Jain >=0.95 requires two-flow shares between approximately 0.385 and 0.615; high total goodput alone cannot satisfy that fairness requirement.

We distinguish the reference propagation RTT used for BDP from each flow’s RTT. In E1/E2 the reference is the first flow’s configured 20-ms RTT, giving 250,000 bytes at 100 Mbps, even when the second flow’s RTT is 40 or 80 ms. Implementation, queue policy, competing algorithms and flow count are explicit inputs. Our two-flow FIFO/no-ECN experiments cannot establish the same conclusions for AQM or larger flow populations.

We have removed the fixed high-BDP label for LEO links. Section 4.6 requires capacity and reference RTT for the relevant direction and observation period; a reported goodput or a network name cannot substitute for these inputs. The reviewed records do not provide a complete capacity/RTT pair for every scenario. Where those inputs are absent, we now leave the classification undetermined rather than retain an unsupported label. This addresses the classification error without supplying values we cannot substantiate.

Manuscript locations: Section 3.4 (p. 10); Section 4.6 (p. 14); Section 7 (p. 21); Section 3.5 (p. 12).

### R1-M5: Added value relative to existing surveys

Reviewer comment (summary): Explain the new insights relative to existing surveys, especially reference [20].

Response: The original contribution statement placed too much weight on the number of scenarios covered. We have rewritten it to explain what readers gain from comparing the studies under a common set of conditions. Relative to reference [20] and other surveys, the paper adds a common condition vector (capacity, RTT, queue, loss source, implementation, queue policy and flow count), metric-separated assessment, a reference-level traceability register and the controlled E1/E2/E3 comparison. We have removed the claim that prior surveys did not discuss these scenarios. Our contribution is the way their evidence is connected to explicit assessment inputs and to the added experiments. The related-work discussion now presents the comparison as coverage and explains the added conditional assessment and experiments, without claiming that these topics were absent from all prior work.

Manuscript locations: Section 1.2 (p. 2); Section 1.4 (p. 3); Table 1 (p. 2).

### R1-M6: Evidence for AI-related conclusions

Reviewer comment (summary): Support or narrow the AI-related generalizations, and distinguish limitations of studies from capabilities of simulation software.

Response: The evidence we reviewed did not justify those general statements. We have removed the claims that virtually all AI schemes optimize one objective, that none addresses fairness and service requirements together, and that simulation tools cannot represent dynamic paths. The revised discussion distinguishes training objectives from reported metrics and study-specific model coverage from tool capabilities. TCP-Drinc provides a concrete example with its action space, simulation setting, Jain estimate and overlapping baseline intervals; we do not infer superiority over BBR, which is absent from its baselines. We also replace categorical sub-RTT deployment claims with requirements for measured inference time, stability and transfer evaluation.

Manuscript locations: Section 6.2 (p. 20); Section 6.3 (p. 21).

### R1-m1: Scientific wording

Reviewer comment (summary): Replace rhetorical formulations with precise, qualified scientific language.

Response: We removed the rhetorical formulations identified in the comment and replaced them with statements tied to the reported conditions. We also removed claims of inevitable long-RTT dominance, universal applicability and exhausted optimization options. The BDP identity no longer serves as a proof of bandwidth allocation, and the AI discussion avoids rhetorical claims about production deployment. A final read-through also removed claims that earlier work could not answer deployment questions and replaced fixed adaptation times in the scenario table with condition-dependent descriptions.

Manuscript locations: Section 5 (p. 15); Section 8 (p. 26).

### R1-m2: Repetition across the manuscript

Reviewer comment (summary): Reduce repetition across the abstract, framework, scenario matrix, fairness discussion and conclusion.

Response: We rewrote the abstract to state the review scope, organizing dimensions, added experiments and bounded conclusion once. We also shortened the search-method narrative, removed duplicated implementation details from the results subsection, and replaced numerical universal predictions in the external comparison with conditional expectations. Detailed numerical settings remain in the experimental section. The abstract and conclusion now lead with the E2 finding: aggregate goodput of 95.58–95.59 Mbps accompanies BBR shares of 0.143–0.327. Methodological scope is stated in the methods and experimental design rather than repeated after every result. The highlights summarize the contribution without repeating scenario-level conclusions. The revised Abstract and Highlights appear on the manuscript opening pages.

Manuscript locations: Section 8 (p. 26); Section 1.4 (p. 3); Section 3.4 (p. 10).

### R1-m3: Figure 2 delay definition

Reviewer comment (summary): The delay increasing with queue occupancy in Figure 2 should not be labelled propagation delay.

Response: We redrew Figure 2 as a conceptual single-bottleneck diagram. The increasing curve now denotes total RTT, while propagation RTT remains constant. The caption explicitly attributes the increase beyond the reference BDP to queueing delay. We also removed algorithm-specific labels that could imply a measured comparison.

Manuscript locations: Figure 2 (p. 6).

## Reviewer 2

### R2-1: Reproducibility of the review process

Reviewer comment (summary): Provide reproducible search/screening counts and reasons, remove the circular citation-based inclusion criterion, and explain how the claimed 165-item corpus was derived.

Response: This comment identified a substantial problem in our methods reporting. The original citation count did not establish a reproducible systematic-review corpus, and we should not have presented it as one. The revision now supplies a reference-level identity and evidence-role register for all 165 original citations, rather than treating them as 165 screened primary studies. The register distinguishes 34 direct BBR evaluations/analyses, 5 mechanism/version materials, 2 related surveys, 15 learning/control comparators and 109 supporting transport/network references. These are retrospective citation roles assigned from metadata and manuscript use, not full-text inclusion decisions. Exact DOI matching locates 41 citations in the supplemental exports; seven additional citations have exact normalized-title candidate matches, and 117 are not located by those rules in the capped exports. The register records the original acquisition route as a legacy citation baseline where historical retrieval is unknown, and preserves matching rules and source-record IDs instead of assigning invented database origins.

The documented supplemental search exported 1,018 OpenAlex and 1,600 Crossref records before normalization. DOI/title/author matching reduced these to 1,916 report groups; 171 were excluded at title/abstract level, 1,745 were forwarded to eligibility review, and 15 full-text assessments are complete (8 retained and 7 excluded), leaving 1,730 pending. The completed full-text exclusions are recorded by scope or report type in the screening supplement; unavailable reports remain separate from exclusions. We report these as stage counts, not as a completed corpus. Citation in the manuscript is not an eligibility criterion. Automated triage is prioritization only, and the capped exports are not an exhaustive search. We cannot retrospectively prove the originally implied historical 165-study screening process. Accordingly, we withdraw that claim and present a critical narrative synthesis with a documented supplemental search and an explicit, reproducible register of its legacy references. This removes the circular inclusion criterion and gives readers records they can inspect. It does not recover the missing historical inclusion chain, so we cannot claim to have fulfilled the request for a complete reconstruction of the original 165-study screening process.

Manuscript locations: Section 1.3 (p. 2); Figure 1 (p. 4); Table 2 (p. 4).

### R2-2: Formal criteria and independent validation

Reviewer comment (summary): Clarify decision criteria and metric-specific suitability, interactions among the dimensions, and the limits of the claimed independent validation.

Response: We have added an explicit analytical assessment procedure and a quantitative transfer evaluation. The condition vector includes capacity, reference and per-flow RTTs, absolute queue size, loss process, implementation, AQM/queue policy, flow count and measurement window. Workload requirements specify separate utilization, Jain fairness, delay and retransmission limits. The procedure returns meets, does not meet or undetermined for each required metric; a missing or incompatible window cannot produce a pass. For two flows, we derive J=1/[1+(2s-1)^2], so a Jain requirement of 0.95 corresponds to shares between approximately 0.385 and 0.615. These are service-dependent acceptance conditions, not universal buffer or BDP thresholds.

We also added a numerical transfer comparison. We calibrate a log-queue interpolation predictor using only 15 equal-RTT BBRv3 E1 runs and evaluate it on disjoint E3 conditions. The analysis is retrospective: the archived outcomes were available when the test was designed, and we do not describe it as preregistered or untouched independent validation. At 200 Mbps, where the four physical queue inputs match the frozen labels, normalized-goodput MAE is 0.00264 and Jain MAE is 0.01010, compared with 0.00264 and 0.01134 for a constant calibration baseline. At 50 Mbps, using corrected physical ratios 4 and 16, queue-conditioned Jain MAE is 0.02027, worse than the constant baseline's 0.01444. All errors and failure cases are reported; the queue descriptor alone therefore does not establish predictive added value. With illustrative retrospective utilization/fairness requirements, all 80 E3 runs meet utilization >=0.90, but only 40/40 BBRv3 and 27/40 CUBIC runs also meet Jain >=0.95. Raising the illustrative utilization requirement to 0.95 changes the joint counts to 0/40 for BBRv3 and 27/40 for CUBIC, exposing the requirement-dependent tradeoff. The supplement provides run-level decisions and threshold sensitivity. Delay assessment remains undetermined because the relevant windows do not align. The earlier Scholz comparison remains an external consistency check, and the archived prediction sheet is retained without assigning numerical acceptance margins after seeing the results.

Manuscript locations: Section 3.6 (p. 12); Section 7 (p. 21); Figure 9 (p. 23); Table 10 (p. 24); Table 11 (p. 24); Section 3.5 (p. 12); Section 7.5 (p. 24); Table 12 (p. 26); Table 13 (p. 26).

### R2-3: Version parameters and ECN statements

Reviewer comment (summary): Correct ProbeRTT minimum-window constraints, state-dependent cwnd gains and the misleading ECN-free reversion statement.

Response: We have corrected the ProbeRTT target for the described BBRv2/v3 implementations to max(4 MSS, BDP/2). The cwnd_gain row now distinguishes the BBRv1 baseline value from state-dependent BBRv2/v3 gains instead of presenting 2.0 as a fixed value in every state and version.

We have also removed the ECN-free reversion statement. BBRv2/v3 retain loss-feedback updates to bandwidth and in-flight bounds, including bw_lo, inflight_lo and inflight_hi as applicable to the inspected implementation, and their associated state logic. ECN absence removes an additional feedback channel; it does not remove this loss-based control. The table identifies source-specific defaults and distinguishes them from the experimental builds. Section 2.2 also separates minimum-RTT filter horizons from ProbeRTT freshness and entry conditions.

Manuscript locations: Table 4 (p. 9); Section 2.2 (p. 6).

### R2-4: Figure provenance and AI disclosure

Reviewer comment (summary): Disclose whether and how AI generated Figures 3–6, name the tool and purposes, and explain technical verification.

Response: The original disclosure was incomplete. GPT Image 2.0 generated Figures 3–6 in the original manuscript, and the authors manually checked their technical content. We now state this in the declaration and in the corresponding figure captions.

For the revision, Figures 2–6 were redrawn with Python/matplotlib. AI assistance was used in preparing plotting code and editing text; the retained scripts generate the replacement figures. We distinguish that work from the original image-generation history. The technical checks concern the points raised in the reviews: Figure 2 separates propagation RTT from queueing delay; Figure 3 excludes later-version ECN logic from the BBRv1 diagram; Figure 4 avoids an unsupported version-performance ranking; and Figures 5–6 no longer infer allocation from the in-flight identity. These diagrams are explanatory schematics, not measured results. The measurements are presented separately in Figure 9 and the experimental tables.

Manuscript locations: Declaration of generative AI (p. 27); Figure 3 (p. 7); Figure 4 (p. 8); Figure 5 (p. 16); Figure 6 (p. 17); Figure 2 (p. 6).

## Reviewer 3

### R3-1: Abstract readability

Reviewer comment (summary): Rewrite the abstract for readability, removing citations and unnecessary numerical detail.

Response: We rewrote the abstract with a clearer progression from scope to framework, experiments and conclusion. It reports the 340-run experiment scope without repeating detailed external throughput ratios or embedding citations. Revised location: Abstract.

### R3-2: BDP-Veno and OVeno

Reviewer comment (summary): Discuss other BDP-aware TCP designs, including BDP-Veno and OVeno.

Response: We have added BDP-Veno and OVeno to Section 1.2 and the bibliography, with their titles, publication metadata and DOIs. They broaden the related-work discussion beyond BBR variants. The revision distinguishes these BDP-aware designs from BBR rather than assuming they use the same estimator, probing policy or loss response.

Our available source records establish their bibliographic identities and the scope described in their abstracts, but do not supply a matched experiment against our BBR implementations. We therefore keep this discussion qualitative and do not report a cross-paper performance ranking. This is a limited addition to related work, not a comparative evaluation of the two protocols.

Manuscript locations: Section 1.2 (p. 2).

### R3-3: Analytical contribution

Reviewer comment (summary): Clarify the analytical contribution beyond numerical evaluation.

Response: We have added an analytical assessment in response to this concern. The paper remains a survey with an analytical study and controlled measurements; we have not developed a new congestion-control algorithm. First, the revised analysis demonstrates non-identifiability: for fixed capacity, RTTs and queue limit, every algebraic allocation x1=(1-s)G, x2=sG satisfies the aggregate-rate and propagation-pipe identities, so those identities alone cannot determine s. This is a statement about what the equations identify, not a claim that every allocation is a controller equilibrium. Second, we transform Jain's established two-flow index into an explicit share-feasibility interval and separate utilization from allocation requirements. Third, we define a requirement-dependent assessment procedure with explicit inputs, observation windows, per-metric outputs and an undetermined result when evidence is missing. Repeated-run assessment reports the fraction jointly satisfying utilization and fairness requirements, alongside the metric means.

The controlled measurements then evaluate this procedure and quantify transfer from E1 calibration to disjoint E3 conditions against a constant baseline. The analysis reports both small errors and conditions where queue conditioning performs worse, and makes its retrospective design explicit. We have rewritten the contribution statement to identify this analysis and its experimental evaluation explicitly. We attribute BDP and Jain identities to established theory and do not present them as new formulas, a new TCP controller or a proof of universal suitability thresholds.

Manuscript locations: Section 1.4 (p. 3); Section 2.1 (p. 5); Section 3.4 (p. 10); Section 7 (p. 21); Section 3.5 (p. 12); Section 7.5 (p. 24); Table 12 (p. 26); Table 13 (p. 26).

### R3-4: Implementation details and reproducibility

Reviewer comment (summary): Provide sufficient implementation, tool, platform and configuration details for reproduction.

Response: Section 7.1 now specifies the two-sender/shared-bottleneck/one-receiver topology, Mininet 2.3.0, iperf3 3.9, iproute2 5.15.0, kernel environments, runtime algorithm names, FIFO/tbf/netem queue settings, MTU, ECN configuration, run duration and repetition count. It defines total goodput, Jain fairness and per-run shares, and gives the reference BDP, queue targets and packet-limit rounding. The experimental supplement supplies raw logs, manifests and analysis scripts for all 340 runs. Receiver goodput and derived Jain/share metrics use a stated full-run window, with a separate post-warmup sensitivity analysis. Early RTT probes and queue snapshots are not represented as complete end-of-run measurements. Different kernel environments and the BBRv1 compatibility patch are reported as limitations on causal attribution.

Manuscript locations: Section 7 (p. 21); Figure 9 (p. 23); Table 10 (p. 24); Table 11 (p. 24).

### R3-5: Positive assessment of the remaining presentation

Reviewer comment (summary): The remaining presentation of the BBR study is well done.

Response: Thank you for this assessment. We have kept the overall explanatory structure and revised the sections affected by the other comments.


## Compiled revision index

Page numbers refer to the printed manuscript pages, excluding the separate Highlights sheet. Reviewer comments above are faithful summaries; the original review text is supplied separately.

R1-M1: Section 5 (p. 15); Section 7 (p. 21); Figure 9 (p. 23); Table 10 (p. 24); Section 3.5 (p. 12); Figure 5 (p. 16); Figure 6 (p. 17).

R1-M2: Section 2.2 (p. 6); Table 4 (p. 9); Figure 9 (p. 23); Table 10 (p. 24); Section 2.1 (p. 5); Figure 3 (p. 7); Figure 4 (p. 8).

R1-M3: Section 3.2 (p. 10); Section 3.4 (p. 10); Table 11 (p. 24).

R1-M4: Section 3.4 (p. 10); Section 4.6 (p. 14); Section 7 (p. 21); Section 3.5 (p. 12).

R1-M5: Section 1.2 (p. 2); Section 1.4 (p. 3); Table 1 (p. 2).

R1-M6: Section 6.2 (p. 20); Section 6.3 (p. 21).

R1-m1: Section 5 (p. 15); Section 8 (p. 26).

R1-m2: Section 8 (p. 26); Section 1.4 (p. 3); Section 3.4 (p. 10).

R1-m3: Figure 2 (p. 6).

R2-1: Section 1.3 (p. 2); Figure 1 (p. 4); Table 2 (p. 4).

R2-2: Section 3.6 (p. 12); Section 7 (p. 21); Figure 9 (p. 23); Table 10 (p. 24); Table 11 (p. 24); Section 3.5 (p. 12); Section 7.5 (p. 24); Table 12 (p. 26); Table 13 (p. 26).

R2-3: Table 4 (p. 9); Section 2.2 (p. 6).

R2-4: Figure 3 (p. 7); Figure 4 (p. 8); Figure 5 (p. 16); Figure 6 (p. 17); Figure 2 (p. 6).

R3-1: Abstract/Highlights (unnumbered) or acknowledgement of positive comment.

R3-2: Section 1.2 (p. 2).

R3-3: Section 1.4 (p. 3); Section 2.1 (p. 5); Section 3.4 (p. 10); Section 7 (p. 21); Section 3.5 (p. 12); Section 7.5 (p. 24); Table 12 (p. 26); Table 13 (p. 26).

R3-4: Section 7 (p. 21); Figure 9 (p. 23); Table 10 (p. 24); Table 11 (p. 24).

R3-5: Abstract/Highlights (unnumbered) or acknowledgement of positive comment.

