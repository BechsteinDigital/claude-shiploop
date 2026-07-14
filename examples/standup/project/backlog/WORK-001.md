# WORK-001: Storage — Append & Lesen der Worklog-Datei

- Priorität: P0
- Status: FERTIG (Review: APPROVED, Zyklus 1)
- Bezug: Muss-Ergebnis #3 aus BRIEF (dauerhafte, menschenlesbare Datei im Home-Verzeichnis)
- Claim-Zone (Dateien/Ordner, exklusiv während DEV): `src/standup/storage.py`, `tests/test_storage.py`

## Problem
`storage.py` enthält nur die Pfadauflösung. Es gibt keine Funktionen, um Einträge dauerhaft
anzuhängen und wieder zu lesen — das Fundament für Erfassen (WORK-002) und Abruf (WORK-003) fehlt.

## Ziel dieses Pakets
Persistenzschicht gemäß ADR-003: `append_entry(text, day)` hängt eine Zeile
`YYYY-MM-DD<TAB>text` (UTF-8, append-only) an die Worklog-Datei an; `read_entries()` liefert die
Einträge als (Datum, Text)-Paare in Dateireihenfolge. Fehlende Datei = leeres Log, kein Fehler.

## Nicht Teil dieses Pakets
- Keine CLI-Anbindung (bleibt Skeleton), kein Erfassen/Abruf-Verhalten (WORK-002/003).
- Kein Editieren/Löschen von Einträgen (Nicht-Ziel im Brief).
- Keine Locking-/Multiprozess-Mechanik (ein Nutzer, lokal).

## Akzeptanzkriterien (prüfbar, diff-fähig)
1. `append_entry` legt die Datei bei Bedarf an und hängt an — vorhandene Zeilen bleiben byte-identisch erhalten (append-only, Schreibmodus `"a"`).
2. Zeilenformat exakt `YYYY-MM-DD<TAB>text\n`; Newlines im Text werden ersetzt oder abgelehnt (keine kaputten Zeilen), Verhalten getestet.
3. `read_entries` liest 0..n Einträge korrekt, toleriert fehlende Datei (leeres Ergebnis) und überspringt nicht parsebare Zeilen ohne Absturz — mit Log/Hinweis, nicht stumm.
4. Alle Tests nutzen `STANDUP_FILE` auf einen tmp-Pfad; `Path.home()` wird in keinem Test real beschrieben.
5. `PYTHONPATH=src python3 -m unittest discover -s tests -v` grün.

## Claim-Grenzen
- erlaubt nach erfolgreicher Umsetzung: „Persistenzschicht implementiert und getestet (Append + Lesen)"
- nicht erlaubt: „Muss-Ergebnis 3 erfüllt" (erst mit CLI-Durchstich + E2E-Nachweis in WORK-004), jede DONE-Aussage über Erfassen/Abruf

## Evidenz (von DEV / Reviewer gefüllt)
- Tests: `PYTHONPATH=src python3 -m unittest discover -s tests -v` → 14/14 grün (9 neue Storage-Tests); vom Reviewer unabhängig ausgeführt und bestätigt.
- Review: APPROVED, 1 Low-Finding (Leereingabe → als Prüfpunkt bereits in WORK-002 Kriterium 3 abgedeckt).
- Caveats: `read_entries()` liefert `(datetime.date, str)` — Vertrag für WORK-002/003. Kein Locking (Nicht-Ziel).
- Claim-Grenze eingehalten: „Persistenzschicht implementiert und getestet" — KEIN Claim auf Muss-Ergebnis 3 (erst nach WORK-004).
