# Entscheidungslog (ADR-light)

Autonome Entscheidungen werden hier geloggt statt den User zu fragen.
Neueste Einträge oben. Nie Einträge löschen — überholte als `revidiert durch ADR-XXX` markieren.

---

## ADR-005: CLI-UX — argumentlos abrufen, Freitext erfassen
- Datum: 2026-07-11 · Rolle: setup · Status: aktiv
- **Entscheidung:** `standup <freitext…>` erfasst einen Eintrag für heute (Argumente werden mit
  Leerzeichen verbunden). `standup` ohne Argumente zeigt den letzten Arbeitstag mit Eintrag
  (Datum + alle Einträge). `standup --help` zeigt Hilfe.
- **Alternativen:** Subkommandos (`standup add …` / `standup last`) — mehr Tipparbeit im täglichen
  Kernpfad; Kollision von Freitext mit Subkommando-Namen wäre dafür ausgeschlossen.
- **Begründung:** Das Kernproblem ist Erfassungs-Reibung; der häufigste Abruf (vor dem Standup) muss
  null Tipparbeit über den Befehlsnamen hinaus kosten. Freitext, der wie eine Option beginnt, ist
  Randfall (Doku: `--` verwenden).
- **Revidierbar:** ja — Kosten der Umkehr: gering (CLI-Dispatch + Doku), solange Datenformat stabil bleibt.

## ADR-004: Projektstruktur src-Layout, Tests mit stdlib-unittest
- Datum: 2026-07-11 · Rolle: setup · Status: aktiv
- **Entscheidung:** Package `src/standup/` mit dünnem Dispatcher `cli.py` und getrennten Modulen
  `storage.py`, `capture.py`, `show.py`; Tests in `tests/` mit `unittest` (stdlib), Aufruf via
  `PYTHONPATH=src python3 -m unittest`. Kein pyproject/pip-Install nötig.
- **Alternativen:** Ein einziges Skript (keine disjunkten Claim-Zonen für parallele WORK-Karten);
  pytest (liegt nur in `~/.local/bin` des Users — unnötige Kopplung an User-lokales Tooling).
- **Begründung:** Modultrennung ergibt disjunkte Claim-Zonen je Muss-Ergebnis; unittest ist ohne
  jede Installation überall reproduzierbar.
- **Revidierbar:** ja — Kosten der Umkehr: gering.

## ADR-003: Datenablage `~/.standup.log`, zeilenbasiert, Test-Override per Env
- Datum: 2026-07-11 · Rolle: setup · Status: aktiv
- **Entscheidung:** Eine Klartextdatei `$HOME/.standup.log`; Format: eine Zeile pro Eintrag,
  `YYYY-MM-DD<TAB>Freitext`, UTF-8, append-only. Env-Variable `STANDUP_FILE` überschreibt den Pfad
  (nötig für Tests; nützlich für Nutzer). „Tag" = lokales Datum zum Erfassungszeitpunkt.
- **Alternativen:** Markdown-Journal mit Datums-Überschriften (hübscher lesbar, aber Parser komplexer,
  Append nicht trivial); Verzeichnis `~/.standup/` (YAGNI — eine Datei reicht, kein mkdir nötig);
  XDG-Datenpfad (Brief verlangt explizit Home-Verzeichnis, Dotfile ist die einfachste Erfüllung).
- **Begründung:** grep-bar, menschenlesbar, trivial anzuhängen und zu parsen; geringste Komplexität
  für Muss-Ergebnisse 3 und 4.
- **Revidierbar:** ja — Kosten der Umkehr: gering (einmalige Formatmigration einer kleinen Datei).

## ADR-002: Aufrufbarkeit via `bin/standup`-Wrapper + dokumentierter PATH-Eintrag
- Datum: 2026-07-11 · Rolle: setup · Status: aktiv
- **Entscheidung:** Ausführbarer Bash-Wrapper `bin/standup` im Repo (löst Symlinks per `readlink -f`
  auf, setzt `PYTHONPATH`, ruft `python3 -m standup` auf). Installation = PATH-Eintrag oder Symlink,
  **nur in der README dokumentiert** — der Agent installiert nichts nach `/usr` oder `~/.local`
  (Vorgabe der Testumgebung).
- **Alternativen:** pipx/pip install (venv-/Tooling-Reibung, verletzt Geist der harten Bedingung);
  Shell-Alias (nicht skript-/cron-fähig, nicht in `command -v` sichtbar).
- **Begründung:** erfüllt die harte Bedingung „`standup` direkt im bash, ohne Aktivierung" mit
  minimaler Maschinerie und ohne Eingriff außerhalb des Projektverzeichnisses.
- **Revidierbar:** ja — Kosten der Umkehr: minimal.

## ADR-001: Sprache/Runtime — Python 3, ausschließlich stdlib
- Datum: 2026-07-11 · Rolle: setup · Status: aktiv
- **Entscheidung:** Implementierung in Python 3 (System-Interpreter `/usr/bin/python3`, 3.14),
  ausschließlich Standardbibliothek — keine Dependencies, kein venv, kein Paketmanager.
- **Alternativen:** Pure Bash (Datums-/Parsing-Logik fehleranfällig, Testtooling bats/shellcheck fehlt
  auf dem System); Go-Binary (Build-Schritt + Toolchain-Kopplung, Overkill); Node (fnm-Multishell-Pfade
  instabil für ein dauerhaft verfügbares Kommando).
- **Begründung:** geringste Komplexität für die Muss-Ergebnisse bei bester Testbarkeit
  (stdlib-`unittest`); stdlib-only erfüllt „ohne venv-Gefrickel" per Konstruktion.
  Details: `project/log/2026-07-11-research-tech-optionen.md`.
- **Revidierbar:** ja — Kosten der Umkehr: Neuimplementierung (~200 Zeilen), Datenformat bleibt gültig.
