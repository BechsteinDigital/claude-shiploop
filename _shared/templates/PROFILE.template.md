# Project Profile (technical)

Maintained by `autonomous-setup`. Role skills read commands and rules ONLY here — never guess,
never carry over from other projects. A command is only listed here after it ran successfully once.

## Stack
- Language(s): …
- Framework(s) / runtime: …
- Package manager: …
- Rationale: see `project/DECISIONS.md` ADR-…

## Commands (verified on <date>)
- Setup: `…`
- Build: `…`
- Test (targeted): `…`
- Test (full): `…`
- Lint / format: `…`
- Start / run: `…`

## Architecture overview
- Cut / layers: …
- Module and directory boundaries: …
- Subsystems (for auditor fan-out): …

## Quality rules
Defaults — add or override project-specific rules here:
- Keep files small (< ~500 lines preferred).
- Never swallow errors silently; log critical paths.
- No secrets in code or commits.
- Tests prove behavior — green tests alone are no DONE proof.
- Docs never claim more than code + tests prove.
- Document public interfaces.

## Risk patterns (for diff scan)
Adapt per project. Default regex:
`(auth|secur|crypt|secret|password|token|payment|lock|mutex|thread|async|concurren|migration|schema|config|deploy|public|export)`
