# Global Knowledge Base (experience)

Cross-project, distilled learning of the skill suite. **The canonical location is exactly this
directory.** `install.sh` records its absolute path in the installation
(`<skills-dir>/_shared/knowledge.path`), so skills find it from any project regardless of where
this repo is cloned; the env variable `SKILLS_KNOWLEDGE_DIR` overrides that (useful if the repo
moved — or re-run `install.sh`). `install.sh` deliberately does NOT copy this directory into
projects, so there is only one truth. Skills read/write directly here; if the path can't be
resolved on a machine, they degrade to project-local `project/LEARNINGS.md`.

## What belongs here
- Generalizable rules from retros (milestone/MVP gate of `autonomous-loop`)
- Recurring review-finding patterns, blocker causes, revised decisions
- Proven setup/stack patterns with evidence

## What does NOT belong here
- Project state (lives in `project/STATE.md` — never mirror it)
- Rules already codified in a skill (then they belong in the skill)
- Running logs, session transcripts, raw data — knowledge bases rot through noise

## Format
One file per learning, kebab-case, per `LEARNING.template.md`. Max. 3–5 new entries per retro.
Don't delete refuted entries; mark them at the top with `Status: refuted by <file/evidence>`.

## Scaling path
If the base grows beyond a few hundred entries, put a semantic index in front (recommendation:
Graphiti/Zep as MCP — temporal knowledge graph). The markdown files remain the source;
the graph is only an index — analogous to graphify over code.
