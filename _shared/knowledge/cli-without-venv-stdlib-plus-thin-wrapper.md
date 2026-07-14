# CLI tools without activation friction: system interpreter + stdlib + thin shell wrapper

- Status: active
- Context: new CLI tool on Linux/macOS, requirement "directly invocable, no venv/sourcing"
- Rule: First check whether the system interpreter (e.g. `python3`) plus standard library suffices;
  invocability via a thin shell wrapper in `bin/` (resolves its own path, calls `python3 -m <package>`),
  installation = PATH entry or symlink. Introduce dependencies only when a must-have outcome forces them.
- Why: standup CLI (2026-07-11): stdlib-only + wrapper met the hard user condition without a
  package manager, venv, or install step; setup→MVP in 3 cycles without a single dependency conflict.
- Application: autonomous-setup at the stack decision (ADR); PO when cutting the invocability packages.
