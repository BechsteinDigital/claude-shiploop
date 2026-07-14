# Ideen-Trichter

Jede neue Idee landet HIER — nie direkt im Code. Bewertung nur durch PO (role-po).

## Triage-Regeln
- **JETZT** nur wenn: Kernbeitrag ≥ 2 **und** Aufwand ≤ M **und** Erweiterungsbudget frei
  **und** die Idee mindestens einen vollen Zyklus hier lag (Cooling-off).
- **Ideen 2. Ordnung** (entstanden bei Umsetzung einer bereits akzeptierten Erweiterung): nie JETZT — immer NACH-MVP oder NIE.
- Kernbeitrag 3 + Aufwand L → CEO-Gate; falls Kernvertrag betroffen → User-Eskalation.

Kernbeitrag: 0 = keiner · 1 = indirekt · 2 = stärkt ein Muss-Ergebnis direkt · 3 = Kernidee ohne sie unvollständig

| ID | Idee | Herkunft (user/research/dev/2.Ordnung) | Kernbeitrag 0–3 | Aufwand S/M/L | Eingetragen (Zyklus) | Entscheidung JETZT/NACH-MVP/NIE | Begründung |
|----|------|----------------------------------------|-----------------|---------------|----------------------|--------------------------------|------------|
| I-001 | KI-gestützte Wochenzusammenfassung für den Teamlead (LLM/API) | user (Onboarding) | 1 | M | Onboarding | NACH-MVP + User-Freigabe | Explizites Nicht-Ziel v1 im Brief; löst Eskalationsregel 2 aus (Kosten, externe API, Daten nach außen). Details unten. |
| I-002 | Auto-Erfassung aus git-Commits des Tages (`standup --from-git` o. ä.) | research (Setup, Alternativen-Analyse) | 1 | M | Setup | NACH-MVP | PO-Triage Zyklus 1: Kernbeitrag 1 < 2 → kein JETZT; zudem P0 offen (keine Erweiterung, solange P0 offen). |
| I-003 | Suite-weiter Isolations-Guard: gemeinsames Test-Setup erzwingt STANDUP_FILE | dev (WORK-005, Zyklus 2) | 1 | S | Zyklus 2 | offen (Triage frühestens Zyklus 3, Cooling-off) | Würde Wiederholung des Smoke-Isolations-Fehlers strukturell verhindern. |
| I-004 | Leermeldung von `standup` nennt das Erfassungs-Kommando (UX-Hinweis) | dev (WORK-003, Zyklus 2) | 1 | S | Zyklus 2 | offen (Triage frühestens Zyklus 3, Cooling-off) | Kleiner Onboarding-Gewinn für neue Nutzer, kein Muss-Ergebnis. |

## Details

### I-001 — KI-gestützte Wochenzusammenfassung
- **Idee:** Freitags automatisch einen kleinen Wochenbericht für den Teamlead generieren, aus den erfassten Tageseinträgen, per LLM/API.
- **Warum geparkt:** Nicht Teil des Kerns; berührt eine externe API. Löst Eskalationsregel 2 aus (Geld ausgeben / externer Account / Daten nach außen). Steht daher explizit als Nicht-Ziel der v1 im Brief.
- **Aktivierungsbedingung:** Nur mit expliziter Extra-Freigabe des Users, inkl. Zustimmung zu Kosten und Bereitstellung eines API-Keys. Zählt gegen das Erweiterungsbudget (max. 1 Erweiterung pro Milestone).
- **Offene Punkte für später:** Anbieter/Modell, Kostenrahmen, wohin der Bericht geht (Ausgabe im Terminal vs. Datei vs. Versand), Datenschutz bei Weitergabe an Dritte.
