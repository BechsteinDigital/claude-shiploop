# claude-shiploop

[English](README.md) · **Deutsch**

[![CI](https://github.com/BechsteinDigital/claude-shiploop/actions/workflows/ci.yml/badge.svg)](https://github.com/BechsteinDigital/claude-shiploop/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Projekt%20unterst%C3%BCtzen-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/bechsteindigital)

**Autonome Delivery-Skills für Claude Code — Idee pitchen, MVP bekommen.**
Projekt- und sprachunabhängige Skill-Suite: vom Idee-Pitch über autonomes Setup
bis zum parallelen, selbstkontrollierten Delivery-Loop — mit Verträgen, Gates und Evidenzregeln
statt Hoffnung.

<p align="center">
  <img src="docs/demo.svg" alt="Replay eines echten shiploop-Laufs: Pitch → Onboarding → Setup → 3 Loop-Zyklen mit parallelen DEV-Agenten → MVP-Gate, 36/36 Tests" width="800">
</p>

**End-to-End validiert, Artefakte inklusive:** Die Demo oben ist das Replay eines echten
Durchlaufs — Pitch → Interview → Setup → 3 Loop-Zyklen (2 DEVs parallel) → MVP-Gate
(`standup`-CLI, 36/36 Tests). Die unbearbeiteten Projekt-Artefakte liegen in
[`examples/standup`](examples/README.md), und die CI führt dessen Testsuite bei jedem Push aus.

## Ablauf

```
Pitch ──▶ project-onboarding ──▶ autonomous-setup ──▶ autonomous-loop ──▶ MVP-Report
          (einziger inter-        (Research, Stack,     (CEO→PO→DEV∥DEV→REVIEWER,
           aktiver Schritt)        Scaffold, Backlog)     Ideen-Trichter, Gates)
```

Du pitchst eine Idee und beantwortest einmal das Onboarding-Interview. Alles danach läuft
autonom: Die Suite recherchiert, wählt einen Stack, scaffoldet das Projekt, schneidet
Arbeitspakete und orchestriert Rollen-Agenten parallel bis zum MVP-Gate — eskaliert wird nur
über Kriterien, denen du explizit zugestimmt hast.

## Quickstart

**Als Plugin (empfohlen):** in Claude Code ausführen

```
/plugin marketplace add BechsteinDigital/claude-shiploop
/plugin install claude-shiploop@bechstein-digital
```

**Oder per Install-Skript:**

```bash
git clone https://github.com/BechsteinDigital/claude-shiploop.git
cd claude-shiploop
./install.sh /pfad/zum/projekt    # oder: ./install.sh --global
```

Danach die Claude-Code-Session **im Zielprojekt** starten und die Idee pitchen —
`project-onboarding` übernimmt ab dort.

## Bedienung

Die ganze Kette läuft **nach dem Pitch von selbst**: Onboarding übergibt an Setup, Setup startet
den Loop — den nächsten Schritt tippst du nie. Deine einzigen Eingaben: der Pitch, die
Interview-Antworten und eine kurze Freigabe.

### 0 · Session starten (einmalig, im Zielprojekt)

```bash
cd /pfad/zum/projekt
claude --permission-mode bypassPermissions   # oder normal starten und Shift+Tab drücken
```

Der Loop läuft unbeaufsichtigt: DEV-Agenten schreiben Dateien **und** führen Tests/Build aus,
ohne dass jemand an der Tastatur sitzt. Im `default`-Modus blockiert jeder Write und jedes
Kommando an einem Prompt — gib ihm also einen nicht-interaktiven Modus (`bypassPermissions` oder
eine vorab freigegebene Allowlist in `.claude/settings.json`). Shift+Tab wechselt den Modus live.

Das Modell steckt in jedem Skill (Frontmatter) — du musst keins setzen. Für sehr lange Läufe ggf.
eine 1M-Kontext-Session: `/model opus[1m]`.

### 1 · Pitch (der einzige interaktive Schritt)

Beschreib einfach die Idee — `project-onboarding` lädt von selbst — oder ruf es explizit auf:

```
/project-onboarding
```

Es spiegelt die Idee zurück, führt das Interview (≤ 4 Fragen pro Runde: Kern → Scope → Rahmen →
Autonomie), prüft die Definition of Ready und schreibt `project/BRIEF.md`. **Du gibst den Brief
explizit frei** — diese Freigabe ist das Tor zur Autonomie.

### 2 · Setup + Loop (automatisch)

Mit der Freigabe startet `autonomous-setup` sofort (Research → ADRs → Scaffold → Backlog) und
ruft dann direkt `autonomous-loop` auf. Ab hier laufen die Rollen als (parallele) Subagenten:
CEO → PO → DEV ∥ DEV → REVIEWER, Ideen-Trichter, Gates. Keine Rückfragen — Entscheidungen werden
als ADRs geloggt. Du siehst nur: Milestone-/Gate-Reports, Eskalations-Memos und den finalen
MVP-Report.

### 3 · Wenn es zu dir zurückkommt

- **Eskalation** — nur bei den Kriterien aus dem Autonomievertrag (Kernvertrags-Änderung,
  Geld/Accounts/Deployment, rechtliche/Sicherheits-Grauzone, Blocker nach 2 Versuchen). Du
  bekommst ein kompaktes Entscheidungs-Memo; antworte in der nächsten Nachricht, dann läuft es
  weiter.
- **MVP-Gate erreicht** — Retro + Final-Report, dann Stopp (kein Gold-Plating).
- **Kontextdruck / Runaway-Cap** — es schreibt einen Handoff und stoppt sauber.

### 4 · Einen Lauf fortsetzen

Nach Handoff, Unterbrechung oder in einer neuen Session auf einem bereits aufgesetzten Projekt:

```
/autonomous-loop
```

Es liest `project/STATE.md` und macht dort weiter, wo es aufgehört hat.

### Eine einzelne Rolle starten (optional)

Die Rollen funktionieren auch standalone — praktisch für ein einmaliges Audit oder das erneute
Ausführen einer Karte:

```
/role-auditor payments               # Zustands-Audit (optional: auf ein Subsystem beschränken)
/role-dev WORK-042                    # genau eine freigegebene Karte umsetzen
/role-reviewer WORK-042 main HEAD     # Delta-Review eines Pakets
```

Im Loop werden sie für dich orchestriert; die Argumente oben sind nur für die direkte Nutzung.

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

## Warum das hier und keine lose Skill-Sammlung?

Die meisten Skill-Sammlungen sind Werkzeugkisten — fahren musst du selbst. Diese Suite ist ein
Betriebsmodell:

- **Autonomie mit Vertrag:** Eskalation an den User nur über explizit vereinbarte Kriterien;
  alles andere wird entschieden und geloggt.
- **Fokus als Mechanik, nicht als Appell:** Wertfilter, Cooling-off, Ideen-Ketten-Regel,
  Erweiterungsbudget — Verbote allein halten keinen autonomen Loop auf Kurs.
- **Claims brauchen Evidenz:** Doku darf nie mehr behaupten als Code + Tests belegen.
- **Parallelität über Claim-Zonen:** disjunkte Dateizonen je Paket; bei Unsicherheit
  Worktree-Isolation.

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

1. **Eine Quelle pro Wahrheit:** Kommandos nur in `PROFILE.md`, Zustand nur in `STATE.md` —
   keine Snapshot-Duplikate, die driften.
2. **Fokus als Mechanik, nicht als Appell:** Wertfilter, Cooling-off, Ideen-Ketten-Regel,
   Erweiterungsbudget — Verbote allein halten keinen autonomen Loop auf Kurs.
3. **Autonomie mit Vertrag:** Eskalation an den User nur über explizit vereinbarte Kriterien;
   alles andere wird entschieden und geloggt.
4. **Parallelität über Claim-Zonen:** disjunkte Dateizonen je Paket; bei Unsicherheit
   Worktree-Isolation.
5. **Claims brauchen Evidenz:** Doku darf nie mehr behaupten als Code + Tests belegen.
6. **Modell-Hierarchie:** Teure Tokens dorthin, wo geurteilt wird, günstige, wo ausgeführt wird —
   in jedem Skill-Frontmatter verdrahtet. Opus für Onboarding, Setup, Loop, CEO, PO und Auditor;
   DEV und Reviewer tragen `inherit`, damit der Loop je Karte wählt: Sonnet für S/M-Arbeit, Opus
   für große/sensible Karten und Gate-Reviews, Haiku für Light-Reviews. Die Kartenqualität macht
   kleine Modelle sicher — deshalb wird am PO nie gespart.
7. **Erfahrungswissen als Destillat:** Retro am Milestone-Gate → max. 3–5 Learnings nach
   `project/LEARNINGS.md`, Generalisierbares in die globale KB `_shared/knowledge/` (nur am
   Master-Ort, wird nicht mitinstalliert). Setup und Reviews lesen sie — jedes Projekt startet
   mit der Erfahrung aller vorherigen.

## Installations-Details

```bash
./install.sh /pfad/zum/projekt    # kopiert Skills + _shared/ nach <projekt>/.claude/skills/
./install.sh --global             # installiert nach ~/.claude/skills/ für alle Projekte
```

Die Skills referenzieren die Skripte in `_shared/scripts/` relativ zum Installationsort —
beide Varianten funktionieren.

Die globale Wissensbasis bleibt in diesem Repo (eine Quelle, wird nie in Projekte installiert).
`install.sh` schreibt ihren absoluten Pfad in die Installation (`_shared/knowledge.path`), damit
die Skills sie aus jedem Projekt finden — kein fester Clone-Ort nötig. Wird das Repo verschoben:
`./install.sh` erneut ausführen oder per `export SKILLS_KNOWLEDGE_DIR=<repo>/_shared/knowledge`
übersteuern.

Bei Installation als Plugin gibt es kein `knowledge.path` (der Plugin-Cache ist flüchtig):
Learnings bleiben dann projektlokal — außer man clont dieses Repo und setzt `SKILLS_KNOWLEDGE_DIR`.

**Betriebshinweis:** Die Claude-Code-Session immer **im Zielprojekt** starten — Subagenten können
außerhalb des Session-Roots nicht schreiben. Für den autonomen Loop brauchen DEV-Subagenten einen
Permission-Mode ohne interaktive Prompts (`acceptEdits`/`bypassPermissions`), sonst blockiert
jeder Write, während niemand zusieht.

## Lizenz

[MIT](LICENSE)
