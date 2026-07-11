#!/usr/bin/env bash
# Kompakter Diff-Scan: Scope -> Größe -> Risiko-Kandidaten -> Hunk-Header.
# Sprachunabhängig. Risiko-Regex per 5. Argument oder Default überschreibbar.
set -euo pipefail

base_ref="${1:-main}"
head_ref="${2:-HEAD}"
max_files="${3:-8}"
max_hunks_per_file="${4:-20}"
risk_regex="${5:-(auth|secur|crypt|secret|password|token|payment|lock|mutex|thread|async|concurren|migration|schema|config|deploy|public|export)}"

range="${base_ref}...${head_ref}"

for ref in "$base_ref" "$head_ref"; do
  git rev-parse --verify "$ref" >/dev/null 2>&1 || { echo "Ref nicht gefunden: $ref" >&2; exit 1; }
done

echo "Range: $range"
echo
echo "1) Scope (name-only, top $max_files)"
git diff --name-only "$range" | sed '/^$/d' | head -n "$max_files"
echo
echo "2) Größe (numstat, top $max_files)"
git diff --numstat "$range" | head -n "$max_files"
echo
echo "3) Risiko-Kandidaten"
high_risk="$(git diff --name-only "$range" | grep -iE "$risk_regex" || true)"
if [[ -z "$high_risk" ]]; then
  echo "(keine Treffer für Risiko-Regex)"
else
  printf "%s\n" "$high_risk" | head -n "$max_files"
fi
echo
echo "4) Hunk-Header (Risiko zuerst, sonst alle)"

declare -a files_to_scan=()
src="${high_risk:-$(git diff --name-only "$range" | sed '/^$/d')}"
while IFS= read -r f; do
  [[ -n "$f" ]] && files_to_scan+=("$f")
done < <(printf "%s\n" "$src" | head -n "$max_files")

for file in "${files_to_scan[@]}"; do
  echo
  echo "### $file"
  git diff -U0 "$range" -- "$file" | grep '^@@' | head -n "$max_hunks_per_file" || true
done
