#!/usr/bin/env python3
"""Audit archived full-run metrics against complete post-warmup intervals.
Writes separate sensitivity artifacts; never modifies archived results or predictions.
"""
import csv
import json
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parent
BATCHES = ["formal_baseline_20261010", "formal_bbr1_20261012", "formal_bbr2_20261010", "formal_bbr3_20261011", "formal_e3_20261011", "formal_random_loss_20261012"]

def flow(path, start, end):
    data = json.loads(path.read_text())
    intervals = [x["sum"] for x in data.get("intervals", []) if "sum" in x and not x["sum"].get("omitted", False) and float(x["sum"]["start"]) >= start and float(x["sum"]["end"]) <= end]
    if not intervals:
        raise ValueError(f"No complete in-window receiver intervals: {path}")
    seconds = sum(float(x["seconds"]) for x in intervals)
    return {"full": float(data["end"]["sum_received"]["bits_per_second"]) / 1e6,
            "window": sum(int(x["bytes"]) for x in intervals) * 8 / seconds / 1e6,
            "start": intervals[0]["start"], "end": intervals[-1]["end"], "seconds": seconds, "intervals": len(intervals)}

def jain(a,b):
    return (a+b)**2/(2*(a*a+b*b))

def main():
    rows=[]
    for batch in BATCHES:
        for run in sorted((ROOT/batch/"runs").iterdir()):
            if not run.is_dir(): continue
            cfg=json.loads((run/"config.json").read_text())
            start=float(cfg["analysis_start_s"]); end=float(cfg["analysis_end_s"])
            a=flow(run/"iperf_server_1.json",start,end); b=flow(run/"iperf_server_2.json",start,end)
            rows.append({"batch":batch,"run_id":cfg["run_id"],"condition_id":cfg["condition_id"],"requested_start_s":start,"requested_end_s":end,
                "flow1_actual_start_s":a["start"],"flow1_actual_end_s":a["end"],"flow1_interval_seconds":a["seconds"],"flow2_actual_start_s":b["start"],"flow2_actual_end_s":b["end"],"flow2_interval_seconds":b["seconds"],
                "full_total_mbps":a["full"]+b["full"],"postwarmup_total_mbps":a["window"]+b["window"],"full_jain":jain(a["full"],b["full"]),"postwarmup_jain":jain(a["window"],b["window"]),"full_flow2_share":b["full"]/(a["full"]+b["full"]),"postwarmup_flow2_share":b["window"]/(a["window"]+b["window"])})
    out=ROOT/"measurement_window_audit_20261012";out.mkdir(exist_ok=True)
    with (out/"run_sensitivity.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
    groups={}
    for row in rows:
        groups.setdefault((row["batch"],row["condition_id"]),[]).append(row)
    condition_rows=[]
    for (batch,condition), values in sorted(groups.items()):
        row={"batch":batch,"condition_id":condition,"n_runs":len(values)}
        for key in ["full_total_mbps","postwarmup_total_mbps","full_jain","postwarmup_jain","full_flow2_share","postwarmup_flow2_share"]:
            row[key+"_mean"]=mean(v[key] for v in values)
            row[key+"_median"]=median(v[key] for v in values)
        row["total_mbps_mean_change"]=row["postwarmup_total_mbps_mean"]-row["full_total_mbps_mean"]
        row["jain_mean_change"]=row["postwarmup_jain_mean"]-row["full_jain_mean"]
        row["flow2_share_mean_change"]=row["postwarmup_flow2_share_mean"]-row["full_flow2_share_mean"]
        condition_rows.append(row)
    with (out/"condition_sensitivity.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(condition_rows[0]),lineterminator="\n");writer.writeheader();writer.writerows(condition_rows)
    summaries=[]
    for batch in BATCHES:
        vals=[x for x in rows if x["batch"]==batch]
        summaries.append({"batch":batch,"runs":len(vals),"max_absolute_total_mbps_change":max(abs(x["postwarmup_total_mbps"]-x["full_total_mbps"]) for x in vals),"max_absolute_jain_change":max(abs(x["postwarmup_jain"]-x["full_jain"]) for x in vals),"max_absolute_flow2_share_change":max(abs(x["postwarmup_flow2_share"]-x["full_flow2_share"]) for x in vals)})
    (out/"summary.json").write_text(json.dumps({"method":"Sensitivity only: whole receiver intervals completely contained in each configured window; boundary intervals excluded, no interpolated bytes. Primary frozen judgements and archived metrics unchanged.","batches":summaries},indent=2)+"\n")
    print(json.dumps(summaries,indent=2))

if __name__ == "__main__": main()
