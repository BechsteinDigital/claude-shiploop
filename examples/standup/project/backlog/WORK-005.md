# WORK-005: Smoke-Tests auf implementiertes Verhalten umstellen + isolieren

- Priorität: P0 (blockiert Merge von WORK-002/003)
- Status: FERTIG (Review: APPROVED, Zyklus 2)
- Bezug: Review-Findings High aus WORK-002/003-Reviews (Zyklus 2); Voraussetzung für deren AK5 „volle Suite grün"
- Claim-Zone (Dateien/Ordner, exklusiv während DEV): `tests/test_smoke.py`

## Problem
`tests/test_smoke.py` stammt aus dem Walking Skeleton: zwei Tests asserten Skeleton-Verhalten
(„nicht implementiert", Exit 1) und sind seit WORK-002/003 rot. Schwerer: Die CLI-Smoke-Tests
setzen kein `STANDUP_FILE` — ein voller Suite-Lauf schreibt/liest die echte `~/.standup.log`
(Verstoß gegen PROFILE-Regel; real aufgetreten und bereinigt).

## Ziel dieses Pakets
Beide veralteten Smoke-Tests prüfen das implementierte Verhalten (Dispatch an capture/show mit
echtem Effekt) und laufen wie alle anderen Tests ausschließlich gegen `STANDUP_FILE`-tmp-Pfade.

## Nicht Teil dieses Pakets
- Keine Änderungen an `src/standup/*` oder anderen Testdateien.
- Keine neuen E2E-Szenarien (WORK-004).

## Akzeptanzkriterien (prüfbar, diff-fähig)
1. Kein Test in `tests/test_smoke.py` läuft ohne `STANDUP_FILE`-tmp-Override; `Path.home()`/reale `~/.standup.log` wird nie berührt.
2. Die zwei Dispatch-Tests asserten implementiertes Verhalten (capture: Eintrag landet in tmp-Datei, Exit 0; show: Ausgabe des jüngsten Tages bzw. Leermeldung).
3. `PYTHONPATH=src python3 -m unittest discover -s tests -v` komplett grün.

## Claim-Grenzen
- erlaubt: „Suite grün, Smoke-Tests isoliert"
- nicht erlaubt: Status-Aussagen zu WORK-002/003 (macht der Orchestrator nach Merge)

## Evidenz (von DEV / Reviewer gefüllt)
- Tests: 31/31 grün (unittest discover, 2026-07-11, Reviewer-verifiziert); ~/.standup.log vor/nach Lauf nicht vorhanden.
