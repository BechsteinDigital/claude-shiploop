# WORK-006: show.run() — OSError-Behandlung analog capture

- Priorität: P1
- Status: OFFEN
- Bezug: Review-Finding Medium aus WORK-003-Review (Muster-Stichprobe: Abweichung vom Mehrheitsmuster)
- Claim-Zone (Dateien/Ordner, exklusiv während DEV): `src/standup/show.py`, `tests/test_show.py`

## Problem
`show.run()` ruft `storage.read_entries()` ohne `OSError`-Behandlung auf — nicht lesbare Datei
(z. B. Permissions) erzeugt einen rohen Traceback. `capture.py` übersetzt `OSError` dagegen in
stderr-Meldung + Exit 1 (Mehrheitsmuster).

## Ziel dieses Pakets
`OSError` in `show.run()` wie in `capture.run()` behandeln: verständliche stderr-Meldung, Exit 1,
kein Traceback. Ein Test für den Fehlerpfad.

## Akzeptanzkriterien (prüfbar, diff-fähig)
1. Nicht lesbare Worklog-Datei → stderr-Meldung mit `standup: `-Präfix, Exit 1, kein Traceback.
2. Volle Suite grün.

## Claim-Grenzen
- erlaubt: „Fehlerpfad-Muster vereinheitlicht"
- nicht erlaubt: keine

## Evidenz (von DEV / Reviewer gefüllt)
- Tests: …
