# WORK-004: E2E-Nachweis — Persistenz & Mehrfacherfassung über das echte Kommando

- Priorität: P0
- Status: FERTIG (Review: APPROVED, Zyklus 3, MVP-Gate)
- Bezug: Muss-Ergebnis #4 aus BRIEF (Mehrfacherfassung am selben Tag); Nachweis-Schlussstein für Muss-Ergebnisse #1–#3
- Claim-Zone (Dateien/Ordner, exklusiv während DEV): `tests/test_e2e.py`
- Abhängigkeit: WORK-002 und WORK-003 müssen FERTIG sein

## Problem
Modultests belegen Bausteine, aber kein Muss-Ergebnis ist über das echte Kommando `bin/standup`
(neuer Prozess, wie der Nutzer es aufruft) nachgewiesen. Ohne diesen Durchstich darf laut
Claim-Regeln kein „MVP erfüllt" behauptet werden.

## Ziel dieses Pakets
End-to-End-Tests, die `bin/standup` als Subprozess mit `STANDUP_FILE` auf tmp-Pfad aufrufen und
den kompletten Nutzerpfad belegen: erfassen → nochmals erfassen → neuer Prozess → Abruf.

## Nicht Teil dieses Pakets
- Keine Änderungen an `src/standup/*` — gefundene Bugs als Befund an PO/neue Karte, nicht still fixen.
- Keine Installation ins System (PATH/Symlink bleibt Doku, Vorgabe Testumgebung).

## Akzeptanzkriterien (prüfbar, diff-fähig)
1. E2E: `bin/standup eintrag eins` → Exit 0; Datei enthält 1 Zeile mit heutigem Datum.
2. E2E: zweiter Aufruf `bin/standup eintrag zwei` → 2 Zeilen, gleicher Tag, Reihenfolge erhalten (Muss #4).
3. E2E: **neuer** Subprozess `bin/standup` (ohne Args) zeigt heutiges Datum + beide Texte → belegt Persistenz über Prozessgrenzen (Muss #3) und Abruf (Muss #2).
4. E2E: Log mit älterem Datum + Lücke (Wochenend-Simulation) → Abruf zeigt das jüngste Datum mit Eintrag.
5. Alle E2E-Tests laufen in der vollen Suite (`python3 -m unittest discover`) grün und berühren `~/.standup.log` nicht.

## Claim-Grenzen
- erlaubt nach erfolgreicher Umsetzung: „Muss-Ergebnisse 1–4 E2E über das echte Kommando nachgewiesen (MVP-Verhalten belegt)"
- nicht erlaubt: Aussagen über Gewohnheitsbildung/Erfolgskriterien des Users (nur der User kann das bewerten); „installiert" (Installation ist dokumentiert, nicht ausgeführt)

## Evidenz (von DEV / Reviewer gefüllt)
- Tests: 5 E2E-Tests via subprocess über `bin/standup`, volle Suite 36/36 grün (DEV + Reviewer unabhängig verifiziert, 2026-07-11); reale `~/.standup.log` entsteht nie (STANDUP_FILE- + HOME-Override, Cleanup-Assert).
- MVP-Gate: Reviewer bestätigt Muss-Ergebnisse 1–4 je mit konkretem Testbeleg (siehe Review Zyklus 3). Caveat Muss #3: Home-Default-Pfad prinzipbedingt nur modulgetestet (test_smoke.StoragePathTest).
