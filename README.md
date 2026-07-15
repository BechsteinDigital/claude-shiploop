# claude-shiploop

**English** · [Deutsch](README.de.md)

[![CI](https://github.com/BechsteinDigital/claude-shiploop/actions/workflows/ci.yml/badge.svg)](https://github.com/BechsteinDigital/claude-shiploop/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-support%20this%20project-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/bechsteindigital)

**Autonomous delivery skills for Claude Code — pitch an idea, get an MVP.**
A project- and language-agnostic skill suite: from an idea pitch through
autonomous setup to a parallel, self-controlled delivery loop — with contracts, gates, and
evidence rules instead of hope.

<p align="center">
  <img src="docs/demo.svg" alt="Replay of a real shiploop run: pitch → onboarding → setup → 3 loop cycles with parallel DEV agents → MVP gate, 36/36 tests" width="800">
</p>

**Proven end-to-end, artifacts included:** the demo above replays a real run — pitch →
interview → setup → 3 loop cycles (2 DEV agents in parallel) → MVP gate (`standup` CLI,
36/36 tests). The unedited project artifacts live in [`examples/standup`](examples/README.md),
and CI re-runs its full test suite on every push.

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

## Running it

The whole chain is **hands-off after the pitch**: onboarding hands to setup, setup starts the
loop — you never type the next step. Your only inputs are the pitch, the interview answers, and
one brief approval.

### 0 · Start the session (once, in the target project)

```bash
cd /path/to/your/project
claude --permission-mode bypassPermissions   # or start normally and press Shift+Tab
```

The loop runs unattended: DEV agents write files **and** run tests/build with nobody at the
keyboard. In `default` mode every write and every command blocks on a prompt — so give it a
non-interactive mode (`bypassPermissions`, or a pre-approved allowlist in
`.claude/settings.json`). Shift+Tab cycles the mode live.

The model is wired into each skill (frontmatter) — you don't need to set one. For very long
runs you may prefer a 1M-context session: `/model opus[1m]`.

### 1 · Pitch (the only interactive step)

Just describe the idea — `project-onboarding` loads on its own — or invoke it explicitly:

```
/project-onboarding
```

It mirrors the idea back, runs the interview (≤ 4 questions per round: Core → Scope → Frame →
Autonomy), checks the Definition of Ready, and writes `project/BRIEF.md`. **You approve the
brief explicitly** — that approval is the gate to autonomy.

### 2 · Setup + loop (automatic)

On approval, `autonomous-setup` starts immediately (research → ADRs → scaffold → backlog), then
launches `autonomous-loop` directly. From here the roles run as (parallel) subagents:
CEO → PO → DEV ∥ DEV → REVIEWER, idea funnel, gates. No questions — decisions are logged as ADRs.
You see only: milestone/gate reports, escalation memos, and the final MVP report.

### 3 · When it comes back to you

- **Escalation** — only on the criteria you agreed to in the autonomy contract (core-contract
  change, money/accounts/deployment, legal/security gray area, a blocker after 2 attempts). You
  get a compact decision memo; answer in your next message and it continues.
- **MVP gate reached** — retro + final report, then it stops (no gold-plating).
- **Context pressure / runaway cap** — it writes a handoff and stops cleanly.

### 4 · Resume a run

After a handoff, an interruption, or a new session on an already-set-up project:

```
/autonomous-loop
```

It reads `project/STATE.md` and picks up where it left off.

### Running a single role (optional)

The roles also work standalone — handy for a one-off audit or re-running one card:

```
/role-auditor payments               # state audit (optional: scope to one subsystem)
/role-dev WORK-042                    # implement exactly one approved card
/role-reviewer WORK-042 main HEAD     # delta review of one package
```

In the loop these are orchestrated for you; the arguments above are only for direct use.

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
6. **Model hierarchy:** expensive tokens where judgment happens, cheap where execution happens —
   wired into each skill's frontmatter. Opus for onboarding, setup, loop, CEO, PO, and auditor;
   DEV and reviewer carry `inherit` so the loop picks per card: Sonnet for S/M work, Opus for
   large/sensitive cards and gate reviews, Haiku for light reviews. Card quality is what makes
   small models safe — which is why the PO is never downgraded.
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
