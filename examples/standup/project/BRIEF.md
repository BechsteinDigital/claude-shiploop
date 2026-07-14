# Produktbrief: standup — Worklog-CLI

Status: FREIGEGEBEN
Erstellt: 2026-07-11 · Zuletzt geändert: 2026-07-11
Änderungen am Kernvertrag nur mit expliziter User-Freigabe.

## Kernvertrag

- **Kernidee (genau 1 Satz):** Ein CLI-Tool, das mit einer Zeile pro Tag deinen Arbeitsverlauf festhält und dir vor dem Standup den letzten Arbeitstag zurückgibt.
- **Zielnutzer:** Der User selbst als erster Nutzer — arbeitet in einem Team mit täglichem Standup, ist auf Linux/bash schnell an der Konsole (entwicklertypische, git-getaktete Arbeitsweise).
- **Kernproblem:** Der User vergisst regelmäßig, was er zuletzt gearbeitet hat, und steht im Daily Standup unvorbereitet da. Das Erfassen muss minimalen Aufwand kosten, sonst wird es nicht durchgehalten.
- **Wertfilter:** Stärkt diese Änderung direkt mindestens ein Muss-Ergebnis oder die Kernidee? Wenn nein → Eintrag in `project/IDEAS.md`, nicht bauen.
- **Erweiterungsbudget:** max. 1 aktive Erweiterung pro Milestone — und nur, wenn sie keine Eskalationsregel auslöst.

### Muss-Ergebnisse (MVP-Definition, prüfbar)
1. Einen Eintrag für heute mit einem einzigen Befehl erfassen (eine Zeile Freitext).
2. Mit einem Befehl den letzten Arbeitstag *mit Eintrag* abrufen — Ausgabe zeigt Datum + Text. „Letzter Arbeitstag" = letzter Tag, an dem tatsächlich etwas eingetragen wurde (Wochenende/Urlaub/Feiertag fallen automatisch raus, kein Kalender nötig).
3. Einträge bleiben dauerhaft erhalten (überleben Terminal-Schließen und Neustart) in einer menschenlesbaren lokalen Datei im Home-Verzeichnis.
4. Mehrfaches Erfassen am selben Tag ist möglich — neue Einträge werden angehängt, nicht überschrieben.

### Explizite Nicht-Ziele
- Kein Web-Frontend und keine GUI.
- Keine Team-/Mehrbenutzer-Funktion.
- Keine Cloud-Synchronisation.
- Keine KI-gestützte Wochenzusammenfassung in v1 (siehe IDEAS.md; nur mit expliziter Freigabe aktivierbar).
- Kein Editieren oder Löschen bereits erfasster Einträge.

## Kontext
- Auslöser / Motivation: User geht wiederholt unvorbereitet ins Daily Standup, weil er den letzten Arbeitstag nicht mehr präsent hat.
- Bestehende Alternativen und warum sie nicht reichen: Kompletter Neustart, nichts existiert. Gedächtnis/ad-hoc reicht erwiesenermaßen nicht; das Tool soll das Erinnern mit minimalem Erfassungsaufwand abnehmen.

## Rahmenbedingungen
- Zeithorizont: Keine feste Deadline, aber zügig — lauffähige erste Version in wenigen Arbeitssitzungen.
- Budget-/Kostengrenzen: v1 komplett kostenlos und rein lokal. Keine bezahlten Dienste/APIs. Kostenpflichtige Erweiterungen (z. B. KI-Zusammenfassung) nur mit expliziter Extra-Freigabe des Users (Kosten + API-Key).
- Technische Vorgaben des Users: Agent entscheidet Sprache/Verpackung/Datenformat. **Harte Bedingung:** Das Tool muss als einzelnes Kommando `standup` direkt im bash aufrufbar sein — ohne vorherige Aktivierung (kein venv-Aktivieren, kein Sourcen bei jeder Nutzung). Zielplattform: Linux + bash. Datenablage: menschenlesbare Datei im Home-Verzeichnis, konkreter Pfad = Agent-Entscheidung.
- Rechtliches / Compliance / Datenschutz: Rein lokal, nur eigene Daten, keine Weitergabe nach außen — keine besonderen Anforderungen.

## Autonomievertrag
Der Agent arbeitet ohne Rückfragen und entscheidet selbst. Ausnahmen (Pflicht-Eskalation an den User):
1. Eine Änderung am Kernvertrag wäre nötig.
2. Geld ausgeben, externe Accounts anlegen, nach außen deployen oder veröffentlichen.
3. Rechtliche oder sicherheitsrelevante Grauzone.
4. Derselbe Blocker besteht nach 2 dokumentierten Lösungsanläufen weiter.

Alles andere: entscheiden, in `project/DECISIONS.md` loggen, weiterarbeiten.

Deployment-Grenze: Autonomie endet an lokaler Lauffähigkeit. Der Agent baut, testet und macht das Tool lokal lauffähig, veröffentlicht aber nichts (kein Paket-Upload, kein Publish) ohne Freigabe.

Milestone-Verhalten: Nach jedem Milestone kurz berichten und direkt weiterarbeiten — kein Stopp zur Zwischenabnahme.

## Erfolgskriterien (aus User-Sicht)
Der User bewertet das Projekt als gelungen, wenn beide Kriterien erfüllt sind:
1. Er geht kein Standup mehr unvorbereitet hinein, weil er in Sekunden sieht, was er zuletzt gemacht hat.
2. Das Tool wird zur echten Gewohnheit — tägliche Nutzung über Wochen hinweg. Wenn die Nutzung nach ~2 Wochen einschläft, gilt das Projekt als Fehlschlag.
