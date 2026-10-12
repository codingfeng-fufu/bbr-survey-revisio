#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
RUNNER="$ROOT/run_formal_bbr1.py"
LOG="$ROOT/batch_controller_20261012.log"

run_one() {
  local a1="$1" a2="$2" rtt="$3" queue="$4" rep="$5"
  local qtag=${queue/./p}
  local dir="$ROOT/runs/BBR1_${a1}_${a2}_C100_R20-${rtt}_Q${qtag}_rep$(printf '%02d' "$rep")"
  if [[ -d "$dir" ]]; then
    printf '%s SKIP existing %s\n' "$(date -Is)" "$dir"
    return 0
  fi
  printf '%s START a1=%s a2=%s rtt2=%s q=%s rep=%s\n' "$(date -Is)" "$a1" "$a2" "$rtt" "$queue" "$rep"
  sudo -n python3 "$RUNNER" --algorithm1 "$a1" --algorithm2 "$a2" --rtt2 "$rtt" --queue "$queue" --repeat "$rep"
  local rc=$?
  printf '%s END rc=%s a1=%s a2=%s rtt2=%s q=%s rep=%s\n' "$(date -Is)" "$rc" "$a1" "$a2" "$rtt" "$queue" "$rep"
  if [[ $rc -ne 0 ]]; then
    printf '%s BATCH_ABORT reason=run_failed rc=%s\n' "$(date -Is)" "$rc"
    exit "$rc"
  fi
}

exec >>"$LOG" 2>&1
printf '%s BATCH_START pid=%s\n' "$(date -Is)" "$$"

for rtt in 20 40 80; do
  for queue in 0.5 2 10; do
    for rep in 1 2 3 4 5; do
    run_one BBR1 BBR1 "$rtt" "$queue" "$rep"
    done
  done
done

for queue in 0.5 2 10; do
  for rep in 1 2 3 4 5; do
    run_one BBR1 CUBIC 20 "$queue" "$rep"
  done
done

printf '%s BATCH_END\n' "$(date -Is)"
