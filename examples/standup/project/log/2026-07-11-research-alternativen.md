# Research: Alternativen (2026-07-11, setup, aus Modellwissen — kein WebSearch nötig)

## Bestandsaufnahme
- **jrnl** (Python-CLI-Journal): mächtig, aber pip/pipx-Installation nötig (Reibung, verletzt tendenziell „kein venv-Gefrickel"), kein eingebautes „letzter Arbeitstag mit Eintrag"-Kommando.
- **doing** (Ruby-Gem): ähnliche Idee, Ruby-Toolchain als Abhängigkeit, mehr Konzept (Tags, Sections) als gebraucht.
- **git log**: deckt nur Code-Arbeit ab, über viele Repos verstreut, kein Freitext („Meeting mit X" fehlt).
- **taskwarrior/timewarrior**: Task-/Zeiterfassung, nicht Worklog; deutlicher Overhead.
- **Plain-Text-Datei + Alias**: nah dran, aber „letzter Tag *mit* Eintrag" (Wochenende/Urlaub überspringen) fehlt — genau der Kern.

## Ergebnis
Keine Alternative liefert die Kombination aus (a) Null-Setup, (b) einem einzigen Kommando `standup`,
(c) „letzter Arbeitstag mit Eintrag"-Logik, (d) menschenlesbarer lokaler Datei. **Kernvertrag bestätigt.**

## Ideen-Fund (→ IDEAS.md, nicht Scope)
- Auto-Erfassung aus git-Commits des Tages (I-002 eingetragen).
