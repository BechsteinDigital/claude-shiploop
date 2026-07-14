# WORK-002: Erfassen — `standup <text>` schreibt Tageseintrag

- Priorität: P0
- Status: FERTIG (Review: APPROVED WITH FOLLOW-UPS, Zyklus 2)
- Bezug: Muss-Ergebnis #1 aus BRIEF (Eintrag für heute mit einem einzigen Befehl); Append-Verhalten aus Muss-Ergebnis #4
- Claim-Zone (Dateien/Ordner, exklusiv während DEV): `src/standup/capture.py`, `tests/test_capture.py`
- Abhängigkeit: WORK-001 (Storage) muss FERTIG sein

## Problem
`capture.run()` ist Skeleton („noch nicht implementiert", Exit 1). Der Kern-Erfassungspfad fehlt.

## Ziel dieses Pakets
`standup <freitext…>` erfasst den Text als Eintrag für heute (lokales Datum) über die
Storage-Schicht: Bestätigung auf stdout, Exit 0. Mehrfaches Erfassen am selben Tag hängt an.

## Nicht Teil dieses Pakets
- Keine Änderungen an `storage.py` (bei Bedarf: neue WORK-Karte statt stillem Mitbauen).
- Kein Abruf-Verhalten (WORK-003), kein Editieren/Löschen.
- Keine Änderungen am CLI-Dispatch (`cli.py` steht, UX per ADR-005).

## Akzeptanzkriterien (prüfbar, diff-fähig)
1. `capture.run("PR gereviewt")` schreibt genau eine Zeile `<heute>\tPR gereviewt` in die Datei aus `storage.data_file_path()` und gibt 0 zurück.
2. Zwei Aufrufe am selben Tag ergeben zwei Zeilen mit demselben Datum — nichts wird überschrieben.
3. Leerer/nur-Whitespace-Text wird abgelehnt: verständliche Meldung auf stderr, Exit ≠ 0, kein Schreibzugriff.
4. Erfolgsmeldung auf stdout nennt Datum und erfassten Text (Nutzer sieht, was gespeichert wurde).
5. Tests ausschließlich über `STANDUP_FILE`-tmp-Pfade; volle Suite grün.

## Claim-Grenzen
- erlaubt nach erfolgreicher Umsetzung: „Erfassen implementiert und getestet (inkl. Append am selben Tag auf Modulebene)"
- nicht erlaubt: „Muss-Ergebnis 1/4 erfüllt" ohne E2E-Nachweis über das echte Kommando (WORK-004)

## Evidenz (von DEV / Reviewer gefüllt)
- Tests: 10/10 test_capture grün (DEV + Reviewer unabhängig); volle Suite nach WORK-005 31/31 grün.
- Review: 2 Findings außerhalb der Zone (stale Smoke-Tests + fehlende Isolation) → behoben via WORK-005.
- Claim-Grenze eingehalten: kein Claim auf Muss-Ergebnis 1/4 (erst WORK-004).
