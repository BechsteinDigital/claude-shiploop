# WORK-003: Abruf — `standup` zeigt letzten Arbeitstag mit Eintrag

- Priorität: P0
- Status: FERTIG (Review: APPROVED WITH FOLLOW-UPS, Zyklus 2)
- Bezug: Muss-Ergebnis #2 aus BRIEF (letzter Arbeitstag *mit Eintrag*, Datum + Text)
- Claim-Zone (Dateien/Ordner, exklusiv während DEV): `src/standup/show.py`, `tests/test_show.py`
- Abhängigkeit: WORK-001 (Storage) muss FERTIG sein

## Problem
`show.run()` ist Skeleton. Der eigentliche Produktwert — „was habe ich zuletzt gemacht?" — fehlt.

## Ziel dieses Pakets
`standup` (ohne Argumente) zeigt den jüngsten Tag, der Einträge hat, mit Datum und **allen**
Einträgen dieses Tages. „Letzter Arbeitstag" = letztes Datum mit Eintrag — Wochenende/Urlaub
fallen automatisch raus, kein Kalender (Brief-Definition).

## Nicht Teil dieses Pakets
- Keine Änderungen an `storage.py` oder `capture.py`.
- Kein Zeitraum-/History-Abruf (z. B. „letzte Woche") — wäre Idee für IDEAS.md.
- Definition offen lassen, ob „heute" ausgeschlossen wird? Nein — Entscheidung hier: **heute zählt mit**,
  wenn heute schon erfasst wurde (einfachste Regel; ADR ergänzen, falls DEV abweicht).

## Akzeptanzkriterien (prüfbar, diff-fähig)
1. Log mit Einträgen an 2026-07-08 und 2026-07-10 → Ausgabe zeigt `2026-07-10` und genau dessen Einträge (alle, in Erfassungsreihenfolge), Exit 0.
2. Mehrere Einträge am jüngsten Tag → alle werden angezeigt, keiner verschluckt.
3. Leeres/fehlendes Log → verständliche Meldung („noch keine Einträge"), Exit ≠ 0 ist erlaubt, aber kein Traceback.
4. Datumsformat in der Ausgabe ist `YYYY-MM-DD` und der Text erscheint unverändert.
5. Tests ausschließlich über `STANDUP_FILE`-tmp-Pfade; volle Suite grün.

## Claim-Grenzen
- erlaubt nach erfolgreicher Umsetzung: „Abruf implementiert und getestet (Modulebene)"
- nicht erlaubt: „Muss-Ergebnis 2 erfüllt" ohne E2E-Nachweis über das echte Kommando (WORK-004)

## Evidenz (von DEV / Reviewer gefüllt)
- Tests: 7/7 test_show grün (DEV + Reviewer unabhängig); volle Suite nach WORK-005 31/31 grün.
- Review: Smoke-Findings → WORK-005; Medium-Finding (OSError-Handling in show.run) → Follow-up WORK-006.
- Claim-Grenze eingehalten: kein Claim auf Muss-Ergebnis 2 (erst WORK-004).
