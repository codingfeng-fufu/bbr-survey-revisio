#!/usr/bin/env python3
"""Extract one v2 run; output measurements, never automatic F07 acceptance."""
import argparse
import json
import math
import re
from pathlib import Path
from statistics import median


def receiver(path, start, end):
    data=json.loads(path.read_text())
    intervals=[r['sum'] for r in data.get('intervals',[]) if 'sum' in r and not r['sum'].get('omitted',False) and float(r['sum']['start'])>=start and float(r['sum']['end'])<=end]
    if not intervals: raise ValueError(f'No complete receiver intervals in window: {path}')
    for row in intervals:
        values=[float(row[k]) for k in ('start','end','seconds','bytes')]
        if not all(math.isfinite(v) for v in values) or float(row['seconds'])<=0 or float(row['end'])<=float(row['start']) or float(row['bytes'])<0:
            raise ValueError('Invalid receiver interval values')
    seconds=sum(float(r['seconds']) for r in intervals)
    if seconds<=0: raise ValueError('Nonpositive receiver coverage')
    gaps=[float(b['start'])-float(a['end']) for a,b in zip(intervals,intervals[1:])]
    if any(g < -0.001 for g in gaps): raise ValueError('Overlapping or unordered receiver intervals')
    return {'window_fraction_covered':seconds/(end-start),
            'max_internal_gap_s':max([0.0]+gaps),
            'goodput_mbps':sum(int(r['bytes']) for r in intervals)*8/seconds/1e6,'covered_seconds':seconds,'first_interval_start_s':intervals[0]['start'],'last_interval_end_s':intervals[-1]['end'],'interval_count':len(intervals)}


def sender_retransmissions(path, start, end):
    data=json.loads(path.read_text())
    intervals=[row['sum'] for row in data.get('intervals',[]) if 'sum' in row
               and not row['sum'].get('omitted',False)
               and float(row['sum']['start'])>=start
               and float(row['sum']['end'])<=end]
    if not intervals or any('retransmits' not in row for row in intervals):
        return {'status':'undetermined','reason':'Missing per-interval sender retransmission counters; full-run summary is not substituted.'}
    seconds=sum(float(row['seconds']) for row in intervals)
    if seconds<=0:raise ValueError('Nonpositive sender interval coverage')
    if any(int(row['retransmits'])<0 for row in intervals):raise ValueError('Negative retransmission counter')
    return {'status':'measured','count':sum(int(row['retransmits']) for row in intervals),
            'covered_seconds':seconds,'window_fraction_covered':seconds/(end-start),
            'first_interval_start_s':intervals[0]['start'],'last_interval_end_s':intervals[-1]['end'],
            'note':'Sender retransmissions, not inferred packet-loss rate; no denominator invented.'}


def rtt(path, wall_start, wall_end):
    values=[]
    discarded=0
    for line in path.read_text().splitlines():
        match=re.search(r'^\[([0-9.]+)\].*\btime=([0-9.]+)\s*ms',line)
        if match:
            if wall_start <= float(match.group(1)) < wall_end:
                values.append(float(match.group(2)))
            else:
                discarded+=1
    if not values: raise ValueError(f'No timestamped individual RTT samples in window: {path}')
    ordered=sorted(values)
    import math
    return {'n':len(values),'discarded_outside_window':discarded,'median_ms':median(values),'p95_ms':ordered[math.ceil(.95*len(values))-1],'p95_estimator':'nearest rank','wall_window_start_s':wall_start,'wall_window_end_s':wall_end}


def counters(path):
    text=path.read_text()
    values=[int(x) for x in re.findall(r'Sent \d+ bytes \d+ pkt \(dropped (\d+),',text)]
    if not values: raise ValueError(f'Missing qdisc drop counters: {path}')
    return values


def analyze(path):
    cfg=json.loads((path/'config.json').read_text())
    if cfg.get('measurement_version')!='v2-windowed-collector': raise ValueError('Only v2 collector data are accepted')
    status=json.loads((path/'exit_status.json').read_text())
    exits=status.get('flow_exit',{})
    required={'flow1','flow2','server1','server2'}
    if cfg.get('status')!='completed' or not required.issubset(exits) or any(exits[name]!=0 for name in required) or status.get('cleanup')!='ok':
        raise ValueError('Run completion/cleanup not verified; require both clients and both servers')
    if any('error' in record for record in status.get('owned_process_cleanup',[])):
        raise ValueError('Owned process cleanup failed')
    timing=json.loads((path/'measurement_timing.json').read_text())
    final=json.loads((path/'transfer_end_timing.json').read_text())
    start=float(cfg['analysis_start_s']);end=float(cfg['analysis_end_s'])
    if not math.isfinite(start) or not math.isfinite(end) or not 0<=start<end:
        raise ValueError('Invalid configured measurement window')
    before=timing['clock_calibration_before'];after=timing['clock_calibration_after']
    offset=float(before['wall_s'])-float(before['monotonic_s'])
    drift=abs((float(after['wall_s'])-float(after['monotonic_s']))-offset)
    if drift > 0.05: raise ValueError('Wall/monotonic offset changed by more than 50 ms; timestamp filtering unsafe')
    wall_start=float(timing['origin_monotonic_s'])+start+offset
    wall_end=float(timing['origin_monotonic_s'])+end+offset

    flows=[receiver(path/f'iperf_server_{i}.json',start,end) for i in [1,2]]
    rates=[r['goodput_mbps'] for r in flows]
    if not all(math.isfinite(rate) and rate>=0 for rate in rates) or sum(rates)<=0:
        raise ValueError('Nonpositive or invalid aggregate goodput; Jain undefined')
    queues=[]
    points={r['point'] for r in timing['queue_samples']}
    for point in sorted(points):
        a=counters(path/f'qdisc_window_start_{point}.txt');b=counters(path/f'qdisc_window_end_{point}.txt');c=counters(path/f'qdisc_transfer_end_{point}.txt')
        if len(a)!=len(b) or len(b)!=len(c): raise ValueError('Qdisc hierarchy changed; counter pairing unsafe')
        if any(y<x for x,y in zip(a,b)) or any(y<x for x,y in zip(b,c)): raise ValueError('Counters decreased; possible reset')
        queues.append({'point':point,'window_drop_deltas_by_qdisc': [y-x for x,y in zip(a,b)],'transfer_end_counters_by_qdisc':c,'note':'Nested qdisc counters may double count; do not sum across hierarchy.'})
    return {'run_id':cfg['run_id'],'receiver_flows':flows,'total_goodput_mbps':sum(rates),'jain':sum(rates)**2/(2*sum(x*x for x in rates)),'rtt_probe_samples':{h:rtt(path/f'ping_window_{h}.txt',wall_start,wall_end) for h in ['h1','h2']},'sender_window_retransmissions':{f'flow{i}':sender_retransmissions(path/f'iperf_client_flow{i}.json',start,end) for i in [1,2]},'queue_measurements':queues,'timing':timing,'final_snapshot_timing':final,'acceptance':'pending: verify implementation identity, actual coverage, timestamps and frozen input/prediction criteria'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('run',type=Path);parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=analyze(args.run)
    text=json.dumps(result,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    else: print(text,end='')

if __name__=='__main__':main()
