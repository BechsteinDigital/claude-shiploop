#!/usr/bin/env bash
# Mechanical merge check: hard-checks zone violations and the test run before the orchestrator merges.
# Exit 0 = PASS, 1 = FAIL (merge blocked), 2 = usage error.
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: merge-check.sh <base-ref> --zone <path>... [--allow <path>...] [--deny <path>...] [--test-cmd "<command>"]
  <base-ref>   comparison base (e.g. main or the last merge commit)
  --zone       claim zone of the package: file or directory prefix (repeatable)
  --allow      additionally permitted paths, e.g. the package's own WORK card (repeatable)
  --deny       blocked paths, override zone AND allow (repeatable) — for files
               a package must never change (e.g. project/STATE.md)
  --test-cmd   full test command from project/PROFILE.md; exit != 0 blocks the merge
Checked are committed changes since <base-ref>, uncommitted changes, and new
(untracked) files. Every file outside zone+allow or on deny is a violation.
USAGE
}

[[ $# -ge 1 ]] || { usage; exit 2; }
base_ref="$1"; shift

declare -a zones=() allows=() denies=()
test_cmd=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --zone)     shift; zones+=("${1:?--zone requires a path}") ;;
    --allow)    shift; allows+=("${1:?--allow requires a path}") ;;
    --deny)     shift; denies+=("${1:?--deny requires a path}") ;;
    --test-cmd) shift; test_cmd="${1:?--test-cmd requires a command}" ;;
    -h|--help)  usage; exit 0 ;;
    *) echo "Unknown parameter: $1" >&2; usage; exit 2 ;;
  esac
  shift
done
[[ ${#zones[@]} -ge 1 ]] || { echo "FAIL: no --zone given" >&2; exit 2; }
git rev-parse --verify "$base_ref" >/dev/null 2>&1 || { echo "FAIL: base-ref not found: $base_ref" >&2; exit 2; }

matches() { # <file> <pattern...> — exact match or directory prefix
  local f="$1"; shift
  local p
  for p in "$@"; do
    p="${p%/}"
    [[ "$f" == "$p" || "$f" == "$p"/* ]] && return 0
  done
  return 1
}

mapfile -t changed < <(
  { git diff --name-only "${base_ref}...HEAD"
    git diff --name-only
    git ls-files --others --exclude-standard
  } | sed '/^$/d' | sort -u
)

fail=0
declare -a violations=()
for f in "${changed[@]}"; do
  if [[ ${#denies[@]} -gt 0 ]] && matches "$f" "${denies[@]}"; then
    violations+=("$f (DENY)"); fail=1
    continue
  fi
  in_zone=0
  matches "$f" "${zones[@]}" && in_zone=1
  if [[ $in_zone -eq 0 && ${#allows[@]} -gt 0 ]]; then
    matches "$f" "${allows[@]}" && in_zone=1
  fi
  [[ $in_zone -eq 0 ]] && { violations+=("$f"); fail=1; }
done

allow_str=""
[[ ${#allows[@]} -gt 0 ]] && allow_str=" · allow: ${allows[*]}"
deny_str=""
[[ ${#denies[@]} -gt 0 ]] && deny_str=" · deny: ${denies[*]}"
echo "Merge check against ${base_ref} — zone: ${zones[*]}${allow_str}${deny_str}"
if [[ ${#violations[@]} -gt 0 ]]; then
  echo "ZONE VIOLATION — ${#violations[@]} file(s) outside zone+allow or on deny:"
  printf '  - %s\n' "${violations[@]}"
else
  echo "Zone check: OK (${#changed[@]} changed/new files, all within zone+allow, none on deny)"
fi

if [[ -n "$test_cmd" ]]; then
  echo "Test run: $test_cmd"
  if bash -c "$test_cmd"; then
    echo "Test run: OK"
  else
    echo "Test run: FAILED"
    fail=1
  fi
fi

if [[ $fail -eq 0 ]]; then echo "PASS"; else echo "FAIL — merge blocked"; fi
exit "$fail"
