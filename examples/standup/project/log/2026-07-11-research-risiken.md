# Research: Risiken (2026-07-11, setup)

## Rechtlich / Datenschutz
- Keine: rein lokal, eigene Daten, keine Weitergabe. Erst relevant, falls I-001 (KI-Zusammenfassung)
  aktiviert wird → dann greift Eskalationsregel 2 (bereits im Brief verankert).

## Technisch
1. **Datenverlust/-korruption:** Append-only-Schreibmodus, ein Nutzer, eine Datei → Risiko gering;
   Tests dürfen nie die echte Home-Datei berühren → Env-Override `STANDUP_FILE` (ADR-003).
2. **Tagesgrenze:** „Tag" = lokales Datum zum Erfassungszeitpunkt. Arbeit nach Mitternacht landet am
   Folgetag — bewusst simpel, kein Kalender (im Brief so gedeckt).
3. **PATH-/Installationsreibung:** verletzt die harte Bedingung, wenn der Wrapper Symlinks nicht auflöst
   → `readlink -f` im Wrapper; Installationsweg nur dokumentieren, nicht ausführen (Vorgabe Testumgebung).
4. **Format-Lock-in:** zeilenbasiertes Klartextformat → Migrationskosten minimal.

## Kosten
- Null. Keine externen Dienste, keine Abhängigkeiten.

## Produktrisiko (Erfolgskriterium 2)
- Gewohnheitsbildung scheitert an Reibung → Abruf muss argumentlos funktionieren (`standup` ohne Args),
  Erfassung einzeiliger Freitext ohne Anführungszeichen-Zwang wo möglich (ADR-005).
