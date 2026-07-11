---
name: project-onboarding
description: Use when der User eine neue Projekt- oder Produktidee pitcht, ein neues Projekt starten will oder ein Onboarding-Interview verlangt — auch bei vagen Ideen („ich hab da eine Idee für eine App"). Einziger interaktiver Skill der Suite; danach läuft alles autonom.
---

# Projekt-Onboarding (Pitch-Interview)

## Ziel
Aus einem Pitch alle Informationen herausfragen, bis autonomes Arbeiten möglich ist — festgehalten
als freigegebener `project/BRIEF.md`. Das ist die **letzte** Gelegenheit für Fragen an den User;
danach übernimmt `autonomous-setup` ohne Rückfragen.

## Ablauf

### 1. Pitch spiegeln
Idee in 2–3 eigenen Sätzen zurückspiegeln (Kernidee, vermuteter Nutzer, vermutetes Problem).
Erst wenn der User die Spiegelung bestätigt oder korrigiert hat, mit dem Interview beginnen.

### 2. Interview in Runden
Fragen mit `AskUserQuestion` stellen (max. 4 pro Runde), pro Runde ein Themenblock,
Runden bauen aufeinander auf. Fragenkatalog: `references/interview-guide.md` — dort
Runde und Formulierung an die Antworten anpassen, nicht mechanisch abarbeiten.

Reihenfolge: **A Kern** (Problem, Nutzer, Erfolg) → **B Scope** (Muss-Ergebnisse, Nicht-Ziele,
kleinste liefernswerte Version) → **C Rahmen** (Zeit, Kosten, Tech-Vorgaben, Plattform) →
**D Autonomie** (Eskalationsregeln, Erweiterungsbudget, Deployment-Grenzen).

Regeln:
- Nach jeder Runde kurz zusammenfassen, was jetzt feststeht.
- „Weiß nicht" → selbst einen Default vorschlagen und nur bestätigen lassen — nie nachbohren.
- Technische Detailfragen nur, wenn der User erkennbar technisch ist; sonst Wirkung statt Technik erfragen.
- Keine Suggestivfragen, die den Scope vergrößern („Wollen Sie nicht auch noch …?"). Das Interview
  existiert, um den Kern zu schärfen, nicht um Features zu sammeln.
- Spontane Feature-Einfälle — egal ob vom User („Oh, und X wäre auch cool!") oder vom Interviewer:
  kurz bestätigen, als Kandidat für `project/IDEAS.md` und ggf. als Nicht-Ziel notieren, **nicht vertiefen**,
  zurück zum Kern. Nur wenn der User darauf besteht, dass es zum Kern gehört, wird es als Muss-Ergebnis-Kandidat behandelt.

### 3. Definition of Ready prüfen
Checkliste in `references/interview-guide.md#definition-of-ready`. Jeder offene Punkt → gezielte
Nachfrage-Runde oder markierter Default. Nicht loslegen, solange ein Punkt weder beantwortet noch
als bestätigter Default gedeckt ist.

### 4. Brief schreiben und freigeben lassen
`project/BRIEF.md` nach `_shared/templates/BRIEF.template.md` erstellen (Status: ENTWURF),
dem User die Kernpunkte kompakt zeigen und **explizite Freigabe** einholen. Erst nach Freigabe:
Status auf FREIGEGEBEN setzen.

### 5. Übergabe
Nach Freigabe sofort `autonomous-setup` starten. Ab hier keine Fragen mehr an den User —
der Autonomievertrag im Brief regelt die einzigen Ausnahmen.

## Rote Flaggen
- Interview startet ohne bestätigte Spiegelung
- Mehr als ~4 Runden ohne Zwischenfazit → User ermüdet, Defaults vorschlagen
- Muss-Ergebnisse, die nicht prüfbar formuliert sind („soll gut aussehen")
- Setup startet, obwohl der Brief noch ENTWURF ist
