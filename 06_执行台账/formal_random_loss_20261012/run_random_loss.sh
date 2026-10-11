#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
RUNNER="$ROOT/run_random_loss.py"
LOG="$ROOT/batch_controller_20261012.log"

run_one() {
  local algorithm="$1" loss="$2" rep="$3"
  local tag=0
  [[ "$loss" == "0.1" ]] && tag=0p1
  local dir="$ROOT/runs/LOSS_${algorithm}_C100_R20_Q2_L${tag}_rep$(printf '%02d' "$rep")"
  if [[ -d "$dir" ]]; then
    printf '%s SKIP existing %s\n' "$(date -Is)" "$dir"
    return 0
  fi
  printf '%s START algorithm=%s loss=%s rep=%s\n' "$(date -Is)" "$algorithm" "$loss" "$rep"
  sudo -n python3 "$RUNNER" --algorithm "$algorithm" --loss-pct "$loss" --repeat "$rep"
  local rc=$?
  printf '%s END rc=%s algorithm=%s loss=%s rep=%s\n' "$(date -Is)" "$rc" "$algorithm" "$loss" "$rep"
  if [[ $rc -ne 0 ]]; then
    printf '%s BATCH_ABORT reason=run_failed rc=%s\n' "$(date -Is)" "$rc"
    exit "$rc"
  fi
}

exec >>"$LOG" 2>&1
printf '%s LOSS_BATCH_START pid=%s\n' "$(date -Is)" "$$"
for algorithm in BBR3 CUBIC; do
  for loss in 0 0.1; do
    for rep in 1 2 3 4 5; do
      run_one "$algorithm" "$loss" "$rep"
    done
  done
done
printf '%s LOSS_BATCH_END\n' "$(date -Is)"
