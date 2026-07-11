# Autonomous Delivery Skills

Projekt- und sprachunabhängige Skill-Suite für Claude Code: vom Idee-Pitch über autonomes Setup
bis zum parallelen, selbstkontrollierten Delivery-Loop.

Entstanden als Generalisierung der `sdk-*`-Skills aus dem VoIP-Projekt — ohne deren
Hardcodings (.NET-Kommandos, CORE-Karten, projektfeste Pfade, doppelte Budget-Quellen).

## Ablauf

```
Pitch ──▶ project-onboarding ──▶ autonomous-setup ──▶ autonomous-loop ──▶ MVP-Report
          (einziger inter-        (Research, Stack,     (CEO→PO→DEV∥DEV→REVIEWER,
           aktiver Schritt)        Scaffold, Backlog)     Ideen-Trichter, Gates)
```

## Skills

| Skill | Zweck |
|---|---|
| `project-onboarding` | Pitch-Interview bis Definition of Ready; erzeugt freigegebenen Brief inkl. Kernvertrag und Autonomievertrag |
| `autonomous-setup` | Bootstrapping ohne Rückfragen: Research, ADRs, Scaffold, Backlog |
| `autonomous-loop` | Orchestriert Rollen als (parallele) Subagenten bis MVP-Gate |
| `role-ceo` | Portfolio-Entscheidungen, Gates, WIP, Anti-Thrash |
| `role-po` | Paket-Zuschnitt, Akzeptanzkriterien, Claim-Zonen, **Ideen-Triage (Wertfilter)** |
| `role-dev` | Implementiert genau ein Paket, silent, Evidenz-Output |
| `role-reviewer` | Delta-Review: Akzeptanz, Claim-Audit, Zonen-Check |
| `role-auditor` | Zustands-Audit per parallelem read-only Fan-out |

## Projekt-Artefakte (im Zielprojekt, von den Skills erzeugt)

```
project/
  BRIEF.md        Produktbrief + Kernvertrag + Autonomievertrag (Verfassung)
  PROFILE.md      Stack, verifizierte Kommandos, Qualitätsregeln (einzige Kommando-Quelle)
  STATE.md        einziger Zustandsspeicher (WIP, Milestone, Budget, Zyklus)
  DECISIONS.md    ADR-light-Log autonomer Entscheidungen
  IDEAS.md        Ideen-Trichter mit Triage-Regeln
  LEARNINGS.md    Retro-Destillat dieses Projekts (Gate-Pflicht)
  backlog/        WORK-Karten (inkl. Claim-Zone + Komplexität)
  log/            Research-, Audit-, Zyklus-Logs
```

## Design-Prinzipien
1. **Eine Quelle pro Wahrheit:** Kommandos nur in `PROFILE.md`, Zustand nur in `STATE.md` — keine Snapshot-Duplikate, die driften.
2. **Fokus als Mechanik, nicht als Appell:** Wertfilter, Cooling-off, Ideen-Ketten-Regel, Erweiterungsbudget — Verbote allein halten keinen autonomen Loop auf Kurs.
3. **Autonomie mit Vertrag:** Eskalation an den User nur über explizit vereinbarte Kriterien; alles andere wird entschieden und geloggt.
4. **Parallelität über Claim-Zonen:** disjunkte Dateizonen je Paket; bei Unsicherheit Worktree-Isolation.
5. **Claims brauchen Evidenz:** Doku darf nie mehr behaupten als Code + Tests belegen (aus der sdk-Suite übernommen — deren stärkstes Element).
6. **Modell-Hierarchie:** Teure Tokens dorthin, wo geurteilt wird (Orchestrator, PO-Schnitt, Gate-Reviews); günstige dorthin, wo ausgeführt wird (DEV/Review nach Karten-Komplexität, Auditor-Fan-out). Die Kartenqualität macht kleine Modelle sicher — deshalb wird am PO nie gespart.
7. **Erfahrungswissen als Destillat:** Retro am Milestone-Gate → max. 3–5 Learnings nach `project/LEARNINGS.md`, Generalisierbares in die globale KB `_shared/knowledge/` (nur am Master-Ort, wird nicht mitinstalliert). Setup und Reviews lesen sie — jedes Projekt startet mit der Erfahrung aller vorherigen.

## Installation in ein Projekt

```bash
./install.sh /pfad/zum/projekt
```

Kopiert alle Skills + `_shared/` nach `<projekt>/.claude/skills/`. Alternativ für globale
Nutzung in alle Projekte: `./install.sh --global` (legt sie unter `~/.claude/skills/` ab).
Die Skills referenzieren die Skripte in `_shared/scripts/` relativ zum Installationsort —
beide Varianten funktionieren.

Liegt dieses Master-Repo nicht unter `~/Projekte/Skills`, die globale Wissensbasis per
Env-Variable bekanntmachen: `export SKILLS_KNOWLEDGE_DIR=<repo>/_shared/knowledge`.

**Betriebshinweis:** Die Claude-Code-Session immer **im Zielprojekt** starten — Subagenten können
außerhalb des Session-Roots nicht schreiben. Für den autonomen Loop brauchen DEV-Subagenten einen
Permission-Mode ohne interaktive Prompts (`acceptEdits`/`bypassPermissions`), sonst blockiert
jeder Write, während niemand zusieht.

E2E-validiert am 2026-07-11: kompletter Durchlauf Pitch → Interview → Setup → 3 Loop-Zyklen
(2 DEVs parallel) → MVP-Gate mit einem realen Projekt (`standup`-CLI, 36/36 Tests).
