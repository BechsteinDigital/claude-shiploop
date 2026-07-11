#!/usr/bin/env bash
# Mechanischer Merge-Check: prüft Zonen-Verletzungen und Testlauf hart, bevor der Orchestrator merged.
# Exit 0 = PASS, 1 = FAIL (Merge blockiert), 2 = Bedienfehler.
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: merge-check.sh <base-ref> --zone <pfad>... [--allow <pfad>...] [--deny <pfad>...] [--test-cmd "<kommando>"]
  <base-ref>   Vergleichsbasis (z. B. main oder letzter Merge-Commit)
  --zone       Claim-Zone des Pakets: Datei oder Verzeichnis-Präfix (mehrfach angebbar)
  --allow      zusätzlich erlaubte Pfade, z. B. die eigene WORK-Karte (mehrfach)
  --deny       gesperrte Pfade, überstimmen Zone UND Allow (mehrfach) — für Dateien,
               die ein Paket nie ändern darf (z. B. project/STATE.md)
  --test-cmd   volles Test-Kommando aus project/PROFILE.md; Exit != 0 blockiert den Merge
Geprüft werden committete Änderungen seit <base-ref>, uncommittete Änderungen und neue
(untracked) Dateien. Jede Datei außerhalb von Zone+Allow oder auf Deny ist eine Verletzung.
USAGE
}

[[ $# -ge 1 ]] || { usage; exit 2; }
base_ref="$1"; shift

declare -a zones=() allows=() denies=()
test_cmd=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --zone)     shift; zones+=("${1:?--zone braucht einen Pfad}") ;;
    --allow)    shift; allows+=("${1:?--allow braucht einen Pfad}") ;;
    --deny)     shift; denies+=("${1:?--deny braucht einen Pfad}") ;;
    --test-cmd) shift; test_cmd="${1:?--test-cmd braucht ein Kommando}" ;;
    -h|--help)  usage; exit 0 ;;
    *) echo "Unbekannter Parameter: $1" >&2; usage; exit 2 ;;
  esac
  shift
done
[[ ${#zones[@]} -ge 1 ]] || { echo "FAIL: keine --zone angegeben" >&2; exit 2; }
git rev-parse --verify "$base_ref" >/dev/null 2>&1 || { echo "FAIL: base-ref nicht gefunden: $base_ref" >&2; exit 2; }

matches() { # <datei> <pattern...> — exakter Treffer oder Verzeichnis-Präfix
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
[[ ${#allows[@]} -gt 0 ]] && allow_str=" · Allow: ${allows[*]}"
deny_str=""
[[ ${#denies[@]} -gt 0 ]] && deny_str=" · Deny: ${denies[*]}"
echo "Merge-Check gegen ${base_ref} — Zone: ${zones[*]}${allow_str}${deny_str}"
if [[ ${#violations[@]} -gt 0 ]]; then
  echo "ZONEN-VERLETZUNG — ${#violations[@]} Datei(en) außerhalb Zone+Allow oder auf Deny:"
  printf '  - %s\n' "${violations[@]}"
else
  echo "Zonen-Check: OK (${#changed[@]} geänderte/neue Dateien, alle in Zone+Allow, keine auf Deny)"
fi

if [[ -n "$test_cmd" ]]; then
  echo "Testlauf: $test_cmd"
  if bash -c "$test_cmd"; then
    echo "Testlauf: OK"
  else
    echo "Testlauf: FEHLGESCHLAGEN"
    fail=1
  fi
fi

if [[ $fail -eq 0 ]]; then echo "PASS"; else echo "FAIL — Merge blockiert"; fi
exit "$fail"
