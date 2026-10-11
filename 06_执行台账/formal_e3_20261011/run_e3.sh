#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
RUNNER="$ROOT/run_e3.py"
LOG="$ROOT/batch_controller_20261011.log"

run_one() {
  local case_id="$1" algorithm="$2" capacity="$3" rtt="$4" ratio="$5" rep="$6"
  local qtag=${ratio/./p}
  local dir="$ROOT/runs/${case_id}_${algorithm}_C${capacity}_R${rtt}_Q${qtag}_rep$(printf '%02d' "$rep")"
  if [[ -d "$dir" ]]; then
    printf '%s SKIP existing %s\n' "$(date -Is)" "$dir"
    return 0
  fi
  printf '%s START case=%s algorithm=%s capacity=%s rtt=%s q=%s rep=%s\n' "$(date -Is)" "$case_id" "$algorithm" "$capacity" "$rtt" "$ratio" "$rep"
  sudo -n python3 "$RUNNER" --case-id "$case_id" --algorithm "$algorithm" --repeat "$rep"
  local rc=$?
  printf '%s END rc=%s case=%s algorithm=%s capacity=%s rtt=%s q=%s rep=%s\n' "$(date -Is)" "$rc" "$case_id" "$algorithm" "$capacity" "$rtt" "$ratio" "$rep"
  if [[ $rc -ne 0 ]]; then
    printf '%s BATCH_ABORT reason=run_failed rc=%s\n' "$(date -Is)" "$rc"
    exit "$rc"
  fi
}

exec >>"$LOG" 2>&1
printf '%s E3_BATCH_START pid=%s\n' "$(date -Is)" "$$"

# Values and absolute buffers are copied from frozen F07-v1 predictions.
for spec in \
  "E3_001 50 10 1 250000" \
  "E3_002 50 10 4 1000000" \
  "E3_003 50 60 1 1500000" \
  "E3_004 50 60 4 6000000" \
  "E3_005 200 10 1 250000" \
  "E3_006 200 10 4 1000000" \
  "E3_007 200 60 1 1500000" \
  "E3_008 200 60 4 6000000"; do
  read -r case_id capacity rtt ratio buffer <<<"$spec"
  for algorithm in BBR3 CUBIC; do
    for rep in 1 2 3 4 5; do
      run_one "$case_id" "$algorithm" "$capacity" "$rtt" "$ratio" "$rep"
    done
  done
done

printf '%s E3_BATCH_END\n' "$(date -Is)"
