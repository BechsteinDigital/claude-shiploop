# Example: `standup` — a real end-to-end run

[`standup/`](standup/) is an **unedited snapshot of a real shiploop run** (2026-07-11): from a
one-sentence pitch to a working, tested CLI tool — pitch interview, autonomous setup, three loop
cycles (two DEV agents in parallel), MVP gate. Nothing in `standup/project/` was written by a
human; every artifact below was produced by the role agents.

The artifacts are in German because the run was driven in German — the suite is
language-agnostic. This walkthrough tells the story in English; the file references let you
verify every claim.

> The claim "36/36 tests green" is not just history: CI runs this snapshot's full suite on
> every push (`example-tests` job).

## The pitch

> "A CLI tool that captures my workday in one line and gives me back my last workday before
> standup — because I keep walking into the daily unprepared."

## What happened, cycle by cycle

### Onboarding (interactive — the only step with user questions)

`project-onboarding` mirrored the pitch, ran 4 interview rounds, and produced
[`project/BRIEF.md`](standup/project/BRIEF.md): 4 verifiable must-have outcomes, 5 explicit
non-goals, an extension budget of 1, and the autonomy contract. Note the spontaneous feature
idea from the interview ("AI weekly summary") — it was **not** built; it went into the idea
funnel as I-001, marked as a v1 non-goal.

### Autonomous setup (no user questions from here on)

`autonomous-setup` ran three parallel research agents
([`project/log/`](standup/project/log/)), then decided and logged
[5 ADRs](standup/project/DECISIONS.md) — including "Python 3, stdlib only, no venv" (ADR-001)
and "data file overridable via env var for test isolation" (ADR-003). It scaffolded a walking
skeleton and cut [6 WORK cards](standup/project/backlog/) with disjoint claim zones.

### Cycle 1 — foundation

One DEV agent implemented WORK-001 (storage append/read). Review: APPROVED, 14/14 tests.

### Cycle 2 — two DEVs in parallel

WORK-002 (capture) and WORK-003 (show last workday) ran as parallel DEV subagents in disjoint
claim zones. The reviewer caught a real defect the DEVs couldn't see: two smoke tests from the
setup skeleton ran against the real `~/.standup.log` instead of a tmp override. Because those
files were outside both claim zones (no-man's-land rule), the PO cut a dedicated fix card —
WORK-005 — which ran before the merges. Suite after cycle 2: 31/31.

### Cycle 3 — MVP gate

WORK-004 delivered the end-to-end proof. Review: APPROVED, suite 36/36. All four must-have
outcomes proven by review verdicts → the loop performed the retro and **stopped at the MVP
gate** — no gold-plating, no "one more feature".

## What the focus mechanics prevented

[`project/IDEAS.md`](standup/project/IDEAS.md) shows four ideas that were captured and
**not built**: two from the user/research (triaged POST-MVP — one would even trigger the
money/external-API escalation rule), two discovered by DEVs mid-implementation (second-order,
cooling-off). [`project/STATE.md`](standup/project/STATE.md) shows the extension budget at 0/1
consumed, and one open P1 follow-up (WORK-006) waiting for a new assignment.

## What the retro distilled

Two generalizable learnings went into the global knowledge base of this repo — every future
project starts with them:

- [`cli-without-venv-stdlib-plus-thin-wrapper.md`](../_shared/knowledge/cli-without-venv-stdlib-plus-thin-wrapper.md)
- [`test-isolation-env-override-for-user-paths.md`](../_shared/knowledge/test-isolation-env-override-for-user-paths.md)
  (the WORK-005 incident above — caught by review, cost one fix cycle, now prevented at setup time)

## Run it yourself

```bash
cd examples/standup
PYTHONPATH=src python3 -m unittest discover -s tests   # 36 tests, stdlib only
bin/standup "wrote the shiploop walkthrough"
bin/standup
```
