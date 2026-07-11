---
name: autonomous-setup
description: Use when ein freigegebener Produktbrief (project/BRIEF.md, Status FREIGEGEBEN) existiert und das Projekt ohne weitere User-Eingaben aufgesetzt werden soll — Research, Tech-Entscheidungen, Scaffold, Backlog. Nicht verwenden, solange der Brief fehlt oder ENTWURF ist (→ project-onboarding).
---

# Autonomes Setup

## Grundsatz
Ab hier **keine Fragen an den User**. Jede offene Entscheidung wird selbst getroffen und in
`project/DECISIONS.md` als ADR geloggt. Einzige Ausnahmen: die Eskalationskriterien aus dem
Autonomievertrag in `project/BRIEF.md`.

## Vorbedingung
`project/BRIEF.md` existiert mit Status FREIGEGEBEN. Sonst abbrechen und `project-onboarding` verlangen.

## Phasen

### 1. Research (timeboxed, parallel)
Zuerst die globale Wissensbasis lesen (`$SKILLS_KNOWLEDGE_DIR`, sonst Default
`~/Projekte/Skills/_shared/knowledge/`; existiert keins von beiden → überspringen) —
dokumentierte Learnings aus früheren Projekten ersetzen Recherche und verhindern Wiederholungsfehler.

Dann parallele read-only Subagenten in einem Aufruf-Block, je Frage einer:
- **Alternativen:** Was existiert bereits? Was macht es nicht gut genug? (bestätigt/schärft den Kernvertrag)
- **Tech-Optionen:** 2–3 Stack-Kandidaten passend zu Muss-Ergebnissen, Zielumgebung und Kostenrahmen — mit Trade-offs, nicht mit Gewinner
- **Risiken:** rechtliche, technische und Kosten-Fallen der Domäne

Ergebnisse nach `project/log/<datum>-research-<thema>.md`. Research-Funde, die neue Features
nahelegen, gehen in `project/IDEAS.md` — **nie** direkt in den Scope.

### 2. Entscheiden
Stack, Architektur-Schnitt und Projektstruktur festlegen: je ein ADR in `project/DECISIONS.md`
(Entscheidung, Alternativen, Begründung, Umkehrkosten). Bei Gleichstand entscheidet: geringste
Komplexität für die Muss-Ergebnisse — nicht die interessanteste Technologie.

### 3. Scaffold
- Repo initialisieren (falls nicht vorhanden), Grundgerüst gemäß ADRs, `.gitignore`, minimale README.
- `project/PROFILE.md` nach `_shared/templates/PROFILE.template.md` anlegen.
  **Jedes Kommando (Build, Test, Lint, Run) erst eintragen, nachdem es einmal erfolgreich lief.**
- Ein Walking Skeleton reicht: baubar, testbar, startbar. Keine Feature-Implementierung im Setup.

### 4. Backlog
- Je Muss-Ergebnis aus dem Brief mindestens eine WORK-Karte (`project/backlog/`, Template beachten): P0 = kritischer Pfad zum MVP.
- Karten klein und mit disjunkten Claim-Zonen schneiden, wo möglich — das ermöglicht dem Loop Parallelarbeit.
- `project/STATE.md` und `project/IDEAS.md` aus den Templates initialisieren.

### 5. Abschluss
Erster Commit (Scaffold + project/-Artefakte). Kurzer Setup-Report in `project/log/`.
Danach direkt `autonomous-loop` starten — nicht auf Bestätigung warten.

## Rote Flaggen
- „Ich frag den User kurz, welche Sprache er lieber mag" → Verstoß: entscheiden, loggen, weiter.
- Research dauert länger als das Scaffold → Timebox verletzt, Entscheidungen mit vorhandenem Wissen treffen.
- Kommandos im Profil, die nie ausgeführt wurden → Profil lügt, Loop bricht später.
- Setup implementiert schon Features → gehört in WORK-Karten und den Loop.
