# Tools that write to user paths need an env override from the skeleton on — and all existing tests must use it

- Status: active
- Context: any tool that creates files in the home/user directory (configs, logs, data stores)
- Rule: The path is overridable via an env variable from the first line of code (e.g. `STANDUP_FILE`),
  and **every** test — including skeleton/smoke tests from setup — runs exclusively against tmp overrides.
  During setup additionally check: which existing tests break when skeleton behavior becomes real? Assign
  those files to a claim zone (no-man's-land rule).
- Why: standup CLI (2026-07-11): two smoke tests from the walking skeleton ran without an override —
  a full suite run actually wrote `~/.standup.log` and the suite was red after implementation.
  Cost a full fix cycle (WORK-005, ~106k tokens); caught by review, not by the DEV.
- Application: autonomous-setup (skeleton design + zone assignment of existing tests); role-reviewer
  (isolation check as a standard checkpoint on test diffs).
