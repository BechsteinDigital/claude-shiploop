# standup — Worklog-CLI

Hält mit einer Zeile pro Tag deinen Arbeitsverlauf fest und gibt dir vor dem Daily Standup
den letzten Arbeitstag mit Eintrag zurück. Rein lokal, keine Abhängigkeiten (Python-3-stdlib).

**Status:** Walking Skeleton — CLI startbar, Fachlogik in Arbeit (siehe `project/backlog/`).

## Nutzung (Ziel-UX)

```bash
standup PR #42 gereviewt, Deployment vorbereitet   # Eintrag für heute erfassen (anhängend)
standup                                            # letzten Arbeitstag mit Eintrag anzeigen
standup --help
```

Freitext, der mit `-` beginnt, mit `--` abtrennen: `standup -- -rc2 getestet`.

## Installation

Voraussetzung: Linux, bash, `python3` (≥ 3.9, nur Standardbibliothek — **kein venv, kein pip**).

Das Kommando ist der Wrapper `bin/standup` in diesem Repository. Eine der beiden Varianten genügt:

```bash
# Variante A: PATH-Eintrag (in ~/.bashrc)
export PATH="$PATH:/home/dbechstein/Projekte/skills-e2e-test/bin"

# Variante B: Symlink in ein Verzeichnis, das bereits im PATH liegt, z. B.:
ln -s /home/dbechstein/Projekte/skills-e2e-test/bin/standup ~/.local/bin/standup
```

Der Wrapper löst Symlinks selbst auf; danach funktioniert `standup` in jeder neuen Shell
ohne Aktivierung. (In dieser Testumgebung wird die Installation bewusst nicht ausgeführt,
nur dokumentiert.)

## Datenablage

Alle Einträge liegen menschenlesbar in `~/.standup.log` — eine Zeile pro Eintrag:
`YYYY-MM-DD<TAB>Freitext`. Pfad überschreibbar über die Env-Variable `STANDUP_FILE`.

## Entwicklung

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v   # Tests
python3 -m compileall -q src                              # Syntax-Check
bin/standup --help                                        # Start
```

Projektsteuerung (Brief, Entscheidungen, Backlog): `project/`.
