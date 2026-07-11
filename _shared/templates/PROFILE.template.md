# Projektprofil (technisch)

Gepflegt von `autonomous-setup`. Rollen-Skills lesen Kommandos und Regeln NUR hier — nie raten,
nie aus anderen Projekten übernehmen. Ein Kommando steht erst hier, wenn es einmal erfolgreich lief.

## Stack
- Sprache(n): …
- Framework(s) / Runtime: …
- Paketmanager: …
- Begründung: siehe `project/DECISIONS.md` ADR-…

## Kommandos (verifiziert am <Datum>)
- Setup: `…`
- Build: `…`
- Test (gezielt): `…`
- Test (voll): `…`
- Lint / Format: `…`
- Start / Run: `…`

## Architektur-Kurzbild
- Schnitt / Schichten: …
- Modul- bzw. Verzeichnisgrenzen: …
- Subsysteme (für Auditor-Fan-out): …

## Qualitätsregeln
Defaults — projektspezifische Regeln hier ergänzen oder überschreiben:
- Dateien klein halten (< ~500 Zeilen bevorzugt).
- Fehler nie stumm schlucken; kritische Pfade loggen.
- Keine Secrets im Code oder in Commits.
- Tests belegen Verhalten — Testgrün allein ist kein DONE-Beweis.
- Doku behauptet nie mehr als Code + Tests belegen.
- Öffentliche Schnittstellen dokumentieren.

## Risiko-Muster (für Diff-Scan)
Projektspezifisch anpassen. Default-Regex:
`(auth|secur|crypt|secret|password|token|payment|lock|mutex|thread|async|concurren|migration|schema|config|deploy|public|export)`
