# Projektprofil (technisch)

Gepflegt von `autonomous-setup`. Rollen-Skills lesen Kommandos und Regeln NUR hier — nie raten,
nie aus anderen Projekten übernehmen. Ein Kommando steht erst hier, wenn es einmal erfolgreich lief.

## Stack
- Sprache(n): Python 3 (System-Interpreter `/usr/bin/python3`, 3.14) — ausschließlich stdlib
- Framework(s) / Runtime: keine; CLI via `argparse`, Wrapper `bin/standup` (bash)
- Paketmanager: keiner (bewusst: keine Dependencies, kein venv)
- Begründung: siehe `project/DECISIONS.md` ADR-001, ADR-002

## Kommandos (verifiziert am 2026-07-11)
- Setup: keins nötig (Repo klonen genügt; nur `python3` vorausgesetzt)
- Build: `python3 -m compileall -q src` (Syntax-Check; kein echter Build-Schritt)
- Test (gezielt): `PYTHONPATH=src python3 -m unittest tests.test_smoke.StoragePathTest -q` (Muster: `tests.<modul>.<Klasse>`)
- Test (voll): `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- Lint / Format: nicht konfiguriert (kein Linter auf dem System verifiziert — nicht raten)
- Start / Run: `bin/standup --help` · `bin/standup` · `bin/standup <freitext>`

## Architektur-Kurzbild
- Schnitt / Schichten: dünner Dispatcher (`cli.py`) → Fachmodule (`capture.py`, `show.py`) → Persistenz (`storage.py`)
- Modul- bzw. Verzeichnisgrenzen: `src/standup/` Code · `tests/` unittest · `bin/` Wrapper · `project/` Steuerung — Fachlogik nie in `cli.py` oder `bin/`
- Subsysteme (für Auditor-Fan-out): storage (Format/Pfad/Append) · capture (Erfassen) · show (Abruf) · cli/wrapper (Aufrufbarkeit)

## Qualitätsregeln
Defaults — projektspezifische Regeln hier ergänzt:
- Dateien klein halten (< ~500 Zeilen bevorzugt).
- Fehler nie stumm schlucken; kritische Pfade loggen.
- Keine Secrets im Code oder in Commits.
- Tests belegen Verhalten — Testgrün allein ist kein DONE-Beweis.
- Doku behauptet nie mehr als Code + Tests belegen.
- Öffentliche Schnittstellen dokumentieren.
- **Projekt:** nur Python-stdlib — jede neue Dependency ist eine ADR-pflichtige Entscheidung.
- **Projekt:** Tests berühren nie `~/.standup.log` — immer `STANDUP_FILE` auf tmp-Pfad setzen.
- **Projekt:** Worklog-Datei nur append-only öffnen; Einträge werden nie überschrieben/gelöscht (Nicht-Ziel im Brief).

## Risiko-Muster (für Diff-Scan)
Default-Regex plus projektspezifisch `HOME|expanduser|unlink|truncate|"w"`-Schreibmodi auf der Datendatei:
`(auth|secur|crypt|secret|password|token|payment|lock|mutex|thread|async|concurren|migration|schema|config|deploy|public|export|HOME|expanduser|truncate|unlink)`
