---
name: autonomous-loop
description: Use when ein aufgesetztes Projekt (project/BRIEF.md freigegeben, PROFILE/STATE/Backlog vorhanden) autonom weitergebaut werden soll — Orchestrierung von CEO/PO/DEV/REVIEWER-Zyklen mit parallelen Agenten, ohne User-Eingaben. Auch zum Fortsetzen nach Unterbrechung oder Handoff.
---

# Autonomer Delivery-Loop

## Grundsatz
Der Loop orchestriert Rollen als Subagenten und arbeitet ohne User-Eingaben bis MVP-Gate,
Eskalationskriterium oder Kontextdruck. Der Kernvertrag in `project/BRIEF.md` ist die Verfassung;
`project/STATE.md` der einzige Zustandsspeicher.

## Zyklus (wiederholen)

1. **Sync:** `STATE.md` lesen; Zyklus-Zähler inkrementieren (Basis für Cooling-off) und gegen das Zyklus-Cap prüfen — Cap erreicht → Runaway-Stop (siehe Stop-Bedingungen), kein weiterer Zyklus. Offene Merges, Blocker, Review-Ergebnisse einarbeiten.
2. **CEO-Tick** (inline nach `role-ceo`): nächste WORK-Items bis WIP-Limit aktivieren, Gates bewerten. Kein neuer Grund → keine Umpriorisierung.
3. **PO-Schritt** (nach `role-po`): aktivierte Items zu Karten schneiden — mit Akzeptanzkriterien, Claim-Grenzen und **disjunkten Claim-Zonen**. Ideen-Triage über `project/IDEAS.md`.
4. **DEV-Fan-out (parallel):** je Karte ein DEV-Subagent, alle in **einem** Aufruf-Block. Kontext **einbetten statt lesen lassen**: WORK-Karte und Profil-Auszug (Kommandos, Qualitätsregeln) stehen wörtlich im Prompt — der Subagent liest nur noch seinen Rollen-Skill. **Modellwahl nach Karten-Komplexität:** S/M → ein Modell unterhalb des Orchestrators (z. B. Sonnet); L oder „heikel" → Orchestrator-Modell. Der Orchestrator prüft die Einstufung vor dem Spawn: Risiko-Regex-Treffer in der Claim-Zone, Gate-Relevanz oder Security-/Nebenläufigkeits-Bezug überstimmen eine niedrigere PO-Einstufung nach oben — nie nach unten. Zonen nicht sicher disjunkt oder > 2 parallele DEVs → Worktree-Isolation pro Agent. Parallele DEVs fahren nur gezielte Tests ihrer Zone plus Regressionscheck der Fundament-Module — der volle Suite-Lauf gehört dem Orchestrator nach dem Merge (sonst testet jeder gegen halbfertige Nachbarzonen).
5. **Review-Pipeline (risikobasiert):** sobald ein DEV fertig ist, Reviewer-Subagent nach `role-reviewer` starten — nicht auf die langsamste Karte warten. **Voll-Review** (Gate-relevant → Orchestrator-Modell, sonst eine Stufe darunter) bei: Produktionscode, Gate-Paketen, Risiko-Regex-Treffern im Diff oder enthaltenen Status-Claims. **Light-Review** (kleines Modell) bei Trivialpaketen (nur Tests/Doku, kleiner Diff): Zonen-Check, Akzeptanz-Abgleich, gezielte Tests, kompaktes Claim-Audit — ohne Muster-Stichprobe.
6. **Fix-Schleife:** Findings/`BLOCKED` → gezielter Fix-Lauf (gleiche Karte, gleiche Zone). **Max. 2 Anläufe pro Blocker**, dann greift der Autonomievertrag (Eskalation oder DEFER mit ADR). Findings in Dateien **außerhalb aller Zonen** (Niemandsland, z. B. Bestands- oder Skeleton-Tests): nie vom DEV mitfixen lassen — PO schneidet sofort eine eigene Fix-Karte mit eigener Zone, die vor dem Merge der blockierten Pakete läuft.
7. **Merge sequenziell:** ein Paket nach dem anderen mergen — davor pro Paket der mechanische Check,
   ausgeführt auf dem Paket-Branch mit sauberem Orchestrator-Tree (eigene `project/`-Änderungen wie
   `STATE.md`/`IDEAS.md` vorher committen, damit nur Paket-Änderungen im Check landen):
   `<skills-dir>/_shared/scripts/merge-check.sh <base> --zone <karten-zone>… --allow project/backlog/<WORK-NNN>.md --allow project/PROFILE.md --test-cmd "<voll-Test aus PROFILE>"`
   — `<skills-dir>` ist der Installationsort dieser Skills (projektlokal `.claude/skills/`, global `~/.claude/skills/`).
   **Kein breites `--allow project/`:** das würde DEV-Änderungen an `STATE.md`, `BRIEF.md` oder `IDEAS.md`
   durchwinken. Erlaubt sind nur die eigene Karte (Evidenz) und `PROFILE.md` (Kommando-Pflege);
   für Sonderfälle kennt der Check `--deny` (überstimmt Zone und Allow).
   `FAIL` blockiert den Merge hart (Zonen-Verletzung → Finding + Fix-Karte; rote Suite → Fix-Schleife) — kein Ermessen.
   Die **volle Suite läuft genau einmal pro Paket: hier, über den Check** — DEV und Reviewer testen nur gezielt, Doppelläufe sind gestrichen. Karte auf FERTIG inkl. Evidenz, `STATE.md` aktualisieren.
8. **Ideen einsammeln:** `IDEEN`/`FOLLOW-UP` aus allen DEV-Outputs nach `project/IDEAS.md` übertragen — nur eintragen, Bewertung erst im PO-Schritt des **nächsten** Zyklus (Cooling-off).
9. **Stop-Check** (siehe unten), sonst nächster Zyklus.

## Fokus-Regeln (hart)
- **Wertfilter:** Nichts wird gebaut, was nicht ein Muss-Ergebnis stärkt oder als Erweiterung durch die PO-Triage ging.
- **Cooling-off:** Keine Idee wird im selben Zyklus geboren und gebaut.
- **Ideen-Ketten-Regel:** Ideen, die bei der Umsetzung einer Erweiterung entstehen (2. Ordnung), werden in diesem Projektlauf nie aktiviert — nur notiert.
- **Erweiterungsbudget** aus dem Brief ist ein Hard Cap pro Milestone.
- Muss-Ergebnisse schlagen Erweiterungen: solange ein P0 offen ist, wird keine Erweiterung aktiviert.

| Rationalisierung | Realität |
|---|---|
| „Der DEV-Agent ist eh gerade in der Datei" | Gelegenheit ist kein Wert. Zone gilt; Idee in den Trichter. |
| „Nur diese eine Erweiterung noch, dann MVP" | So entsteht Idee-auf-Idee. Budget und P0-Regel gelten. |
| „Das Review dauert zu lange, ich merge direkt" | Ungeprüfte Claims sind die teuerste Abkürzung. Pipeline einhalten. |
| „Ich frage den User kurz, ist ja nur eine Kleinigkeit" | Autonomievertrag gilt: entscheiden, loggen, weiter. |

## Eskalation an den User (einzige Unterbrechungsgründe)
Genau die Kriterien aus dem Autonomievertrag in `project/BRIEF.md`:
Kernvertrags-Änderung nötig · Geld/Accounts/Deployment/Veröffentlichung · Rechts-/Sicherheits-Grauzone ·
Blocker nach 2 Anläufen. Eskalation = kompakte Entscheidungsvorlage (Lage, Optionen, Empfehlung), kein Log-Dump.

## Retro am Milestone-/MVP-Gate (Pflicht vor dem Report)
Max. **3–5 Learnings destillieren** — je: Regel in einem Satz, Warum (Beleg), Anwendung. Quellen:
Review-Findings, Blocker, revidierte ADRs. Projektspezifisches nach `project/LEARNINGS.md`;
Generalisierbares zusätzlich als eigene Datei in die globale Wissensbasis
(`$SKILLS_KNOWLEDGE_DIR`, sonst Default `~/Projekte/Skills/_shared/knowledge/`;
existiert keins von beiden → nur projektlokal; Format siehe deren README).
Kein Verlaufsprotokoll, keine Duplikate von Regeln, die bereits in Skills stehen — nur Destillat.

## Stop-Bedingungen
- **MVP-Gate:** alle Muss-Ergebnisse durch Review-Verdicts belegt → Retro, dann Abschlussreport (siehe unten), dann stoppen. Kein Weiterbauen an Erweiterungen ohne neuen Auftrag.
- **Eskalationskriterium erfüllt** → Entscheidungsvorlage an den User.
- **Runaway-Guard:** Zyklus-Cap aus `STATE.md` erreicht (Default 15 pro Milestone) → Stop mit Entscheidungsvorlage: was fertig ist, was hängt, warum es nicht konvergiert; Optionen: Cap erhöhen, Scope schneiden, DEFER. Das Cap wird nie stillschweigend erhöht — auch nicht um „nur einen" Zyklus. Bewusst kein Token-Budget: nicht messbar, wäre Pseudo-Mechanik.
- **Kontextdruck:** Handoff nach `_shared/templates/HANDOFF.template.md` schreiben (inkl. offener Worktrees/Branches), sauber beenden. Fortsetzung: dieser Skill, Schritt 1.

## Output-Disziplin
Während der Zyklen keine Chat-Narration; Verlauf steht in `project/log/` und `STATE.md`.
An den User gehen nur: Milestone-/MVP-Report, Eskalations-Vorlagen und der Abschlussreport
(erreichte Muss-Ergebnisse mit Evidenz, getroffene ADRs, offene NACH-MVP-Ideen, bekannte Grenzen).

## Rote Flaggen
- Zwei DEV-Agenten mit überlappenden Zonen ohne Worktree → Merge-Chaos vorprogrammiert
- `STATE.md` und Realität widersprechen sich → erst Sync reparieren, dann weiterarbeiten
- Ein Zyklus ohne einen einzigen Review → Claims ungeprüft, Stop
- Erweiterung aktiv, während ein P0 offen ist → Verstoß gegen Fokus-Regeln
