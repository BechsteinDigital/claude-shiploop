# Setup-Report (2026-07-11, autonomous-setup)

## Entschieden (ADR-001…005 in `project/DECISIONS.md`)
- Python 3 stdlib-only, System-Interpreter — kein venv, keine Dependencies (ADR-001)
- Aufrufbarkeit über `bin/standup`-Wrapper; PATH-Eintrag/Symlink nur in README dokumentiert, nichts installiert (ADR-002)
- Datenablage `~/.standup.log`, `YYYY-MM-DD<TAB>Text`, append-only, Test-Override `STANDUP_FILE` (ADR-003)
- src-Layout mit disjunkten Modulen storage/capture/show + stdlib-unittest (ADR-004)
- UX: `standup <text>` erfasst, `standup` ohne Args zeigt letzten Arbeitstag (ADR-005)

## Research
Kompakt aus Modellwissen (triviale Domäne, kein WebSearch): Alternativen-, Tech- und Risiko-Notizen
in `project/log/2026-07-11-research-*.md`. Kernvertrag bestätigt; Ideen-Fund I-002 in IDEAS.md.

## Angelegt
- Walking Skeleton: `bin/standup`, `src/standup/{__init__,__main__,cli,storage,capture,show}.py`, `tests/test_smoke.py`, `README.md`, `.gitignore`
- Steuerung: `project/PROFILE.md`, `project/STATE.md`, `project/DECISIONS.md`, `project/IDEAS.md` (Template-Form, Inhalte erhalten), `project/backlog/WORK-001…004`

## Verifiziert (je einmal erfolgreich gelaufen)
- `python3 -m compileall -q src`
- `PYTHONPATH=src python3 -m unittest discover -s tests -v` → 5 Tests OK
- `PYTHONPATH=src python3 -m unittest tests.test_smoke.StoragePathTest -q` → OK
- `bin/standup --help` (Exit 0), `--version`, ohne Args/mit Text (Skeleton, Exit 1 wie designed)
- Harte Bedingung: `standup` via PATH-Eintrag **und** via Symlink aufrufbar (Wrapper löst Symlinks auf)

## Backlog (alle P0, Muss-Ergebnis-Abdeckung 1:1)
WORK-001 Storage (Muss 3) → WORK-002 Erfassen (Muss 1) ∥ WORK-003 Abruf (Muss 2) → WORK-004 E2E (Muss 4 + Durchstich-Nachweis)

## Caveats
- Kein Linter auf dem System verifiziert → Lint im Profil bewusst „nicht konfiguriert".
- Skeleton-Exit-Codes für capture/show sind 1 („noch nicht implementiert") — gewollt ehrlich, wird durch WORK-002/003 ersetzt.
