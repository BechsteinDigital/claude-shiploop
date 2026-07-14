# claude-shiploop

**English** · [Deutsch](README.de.md)

[![CI](https://github.com/BechsteinDigital/claude-shiploop/actions/workflows/ci.yml/badge.svg)](https://github.com/BechsteinDigital/claude-shiploop/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-support%20this%20project-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/bechsteindigital)

**Autonomous delivery skills for Claude Code — pitch an idea, get an MVP.**
A project- and language-agnostic skill suite: from an idea pitch through
autonomous setup to a parallel, self-controlled delivery loop — with contracts, gates, and
evidence rules instead of hope.

**Proven end-to-end:** full run from pitch → interview → setup → 3 loop cycles
(2 DEV agents in parallel) → MVP gate on a real project (`standup` CLI, 36/36 tests passing).

## How it works

```
Pitch ──▶ project-onboarding ──▶ autonomous-setup ──▶ autonomous-loop ──▶ MVP report
          (the only inter-        (research, stack,     (CEO→PO→DEV∥DEV→REVIEWER,
           active step)            scaffold, backlog)     idea funnel, gates)
```

You pitch an idea and answer the onboarding interview once. Everything after that runs
autonomously: the suite researches, picks a stack, scaffolds the project, cuts work packages,
and orchestrates role agents in parallel until the MVP gate — escalating to you only on
criteria you explicitly agreed to.

## Quickstart

**As a plugin (recommended):** inside Claude Code, run

```
/plugin marketplace add BechsteinDigital/claude-shiploop
/plugin install claude-shiploop@bechstein-digital
```

**Or via install script:**

```bash
git clone https://github.com/BechsteinDigital/claude-shiploop.git
cd claude-shiploop
./install.sh /path/to/your/project    # or: ./install.sh --global
```

Then start a Claude Code session **inside the target project** and pitch your idea —
`project-onboarding` picks it up from there.

## The skills

| Skill | Purpose |
|---|---|
| `project-onboarding` | Pitch interview to Definition of Ready; produces an approved brief incl. core contract and autonomy contract |
| `autonomous-setup` | Bootstrapping without questions: research, ADRs, scaffold, backlog |
| `autonomous-loop` | Orchestrates roles as (parallel) subagents until the MVP gate |
| `role-ceo` | Portfolio decisions, gates, WIP, anti-thrash |
| `role-po` | Work-package cutting, acceptance criteria, claim zones, **idea triage (value filter)** |
| `role-dev` | Implements exactly one package, silent, evidence output |
| `role-reviewer` | Delta review: acceptance, claim audit, zone check |
| `role-auditor` | State audit via parallel read-only fan-out |

## Why this and not a loose skill collection?

Most skill collections are toolboxes — you still drive. This suite is an operating model:

- **Autonomy with a contract:** escalation to the user only via explicitly agreed criteria;
  everything else gets decided and logged.
- **Focus as mechanics, not appeals:** value filter, cooling-off, idea-chain rule, extension
  budget — prohibitions alone don't keep an autonomous loop on course.
- **Claims need evidence:** documentation may never claim more than code + tests prove.
- **Parallelism via claim zones:** disjoint file zones per package; worktree isolation when in doubt.

## Project artifacts (created in the target project)

```
project/
  BRIEF.md        product brief + core contract + autonomy contract (the constitution)
  PROFILE.md      stack, verified commands, quality rules (single source for commands)
  STATE.md        single state store (WIP, milestone, budget, cycle)
  DECISIONS.md    ADR-light log of autonomous decisions
  IDEAS.md        idea funnel with triage rules
  LEARNINGS.md    retro distillate of this project (gate requirement)
  backlog/        WORK cards (incl. claim zone + complexity)
  log/            research, audit, and cycle logs
```

## Design principles

1. **One source per truth:** commands only in `PROFILE.md`, state only in `STATE.md` — no
   snapshot duplicates that drift.
2. **Focus as mechanics, not as appeal:** value filter, cooling-off, idea-chain rule, extension
   budget — prohibitions alone don't keep an autonomous loop on course.
3. **Autonomy with a contract:** escalation to the user only via explicitly agreed criteria;
   everything else is decided and logged.
4. **Parallelism via claim zones:** disjoint file zones per package; worktree isolation when
   uncertain.
5. **Claims need evidence:** documentation may never claim more than code + tests prove.
6. **Model hierarchy:** expensive tokens where judgment happens (orchestrator, PO cutting, gate
   reviews); cheap tokens where execution happens (DEV/review by card complexity, auditor
   fan-out). Card quality is what makes small models safe — which is why the PO is never
   downgraded.
7. **Experience as distillate:** retro at the milestone gate → max. 3–5 learnings into
   `project/LEARNINGS.md`, generalizable ones into the global KB `_shared/knowledge/` (master
   location only, not installed into projects). Setup and reviews read them — every project
   starts with the experience of all previous ones.

## Installation details

```bash
./install.sh /path/to/project    # copies skills + _shared/ to <project>/.claude/skills/
./install.sh --global            # installs to ~/.claude/skills/ for all projects
```

The skills reference the scripts in `_shared/scripts/` relative to the installation location —
both variants work.

The global knowledge base stays in this repo (single source, never installed into projects).
`install.sh` records its absolute path in the installation (`_shared/knowledge.path`), so skills
find it from any project — no fixed clone location required. If you move the repo, re-run
`./install.sh`, or override via `export SKILLS_KNOWLEDGE_DIR=<repo>/_shared/knowledge`.

When installed as a plugin, there is no `knowledge.path` (the plugin cache is ephemeral):
learnings then stay project-local, unless you clone this repo and set `SKILLS_KNOWLEDGE_DIR`.

**Operational note:** always start the Claude Code session **in the target project** — subagents
cannot write outside the session root. For the autonomous loop, DEV subagents need a permission
mode without interactive prompts (`acceptEdits`/`bypassPermissions`), otherwise every write
blocks while nobody is watching.

## License

[MIT](LICENSE)
