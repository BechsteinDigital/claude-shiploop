#!/usr/bin/env bash
# Installiert die Skill-Suite in ein Projekt (.claude/skills/) oder global (~/.claude/skills/).
set -euo pipefail

usage() { echo "Usage: install.sh <projekt-pfad> [--global]"; exit 1; }
[[ $# -ge 1 ]] || usage

src_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target_root="$1"
[[ -d "$target_root" ]] || { echo "Zielpfad existiert nicht: $target_root" >&2; exit 1; }

if [[ "${2:-}" == "--global" ]]; then
  dest="$HOME/.claude/skills"
else
  dest="$target_root/.claude/skills"
fi

mkdir -p "$dest"

skills=(project-onboarding autonomous-setup autonomous-loop role-ceo role-po role-dev role-reviewer role-auditor)
for s in "${skills[@]}"; do
  rm -rf "${dest:?}/$s"
  cp -r "$src_dir/$s" "$dest/"
done
# _shared kopieren — OHNE knowledge/: die globale Wissensbasis hat genau einen Ort (Master),
# damit Learnings aus Projekt A in Projekt B ankommen und nichts driftet.
rm -rf "${dest:?}/_shared"
mkdir -p "$dest/_shared"
cp -r "$src_dir/_shared/templates" "$dest/_shared/"
cp -r "$src_dir/_shared/scripts" "$dest/_shared/"
chmod +x "$dest/_shared/scripts/"*.sh

echo "Installiert nach: $dest"
echo "Skills: ${skills[*]}"
echo "Start: Idee pitchen -> project-onboarding wird getriggert."
