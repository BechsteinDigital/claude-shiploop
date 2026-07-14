#!/usr/bin/env bash
# Installs the skill suite into a project (.claude/skills/) or globally (~/.claude/skills/).
set -euo pipefail

usage() { echo "Usage: install.sh <project-path> | install.sh --global"; exit 1; }
[[ $# -ge 1 ]] || usage

src_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$1" == "--global" || "${2:-}" == "--global" ]]; then
  dest="$HOME/.claude/skills"
else
  target_root="$1"
  [[ -d "$target_root" ]] || { echo "Target path does not exist: $target_root" >&2; exit 1; }
  dest="$target_root/.claude/skills"
fi

mkdir -p "$dest"

skills=(project-onboarding autonomous-setup autonomous-loop role-ceo role-po role-dev role-reviewer role-auditor)
for s in "${skills[@]}"; do
  rm -rf "${dest:?}/$s"
  cp -r "$src_dir/$s" "$dest/"
done
# Copy _shared — WITHOUT knowledge/: the global knowledge base has exactly one location (master),
# so learnings from project A reach project B and nothing drifts.
rm -rf "${dest:?}/_shared"
mkdir -p "$dest/_shared"
cp -r "$src_dir/_shared/templates" "$dest/_shared/"
cp -r "$src_dir/_shared/scripts" "$dest/_shared/"
chmod +x "$dest/_shared/scripts/"*.sh
# Record where the master repo's knowledge base lives, so skills can find it from any
# installation without a hardcoded path ($SKILLS_KNOWLEDGE_DIR overrides at runtime).
printf '%s\n' "$src_dir/_shared/knowledge" > "$dest/_shared/knowledge.path"

echo "Installed to: $dest"
echo "Skills: ${skills[*]}"
echo "Start: pitch an idea -> project-onboarding takes over."
