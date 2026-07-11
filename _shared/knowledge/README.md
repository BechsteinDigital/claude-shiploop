# Globale Wissensbasis (Erfahrungswissen)

Projektübergreifendes, destilliertes Lernen der Skill-Suite. **Kanonischer Ort ist genau dieses
Verzeichnis** (`~/Projekte/Skills/_shared/knowledge/`) — `install.sh` kopiert es bewusst NICHT in
Projekte, damit es nur eine Wahrheit gibt. Skills lesen/schreiben direkt hier; existiert der Pfad
auf einer Maschine nicht, degradieren sie auf projektlokales `project/LEARNINGS.md`.

## Was hierher gehört
- Generalisierbare Regeln aus Retros (Milestone-/MVP-Gate des `autonomous-loop`)
- Wiederkehrende Review-Finding-Muster, Blocker-Ursachen, revidierte Entscheidungen
- Bewährte Setup-/Stack-Muster mit Beleg

## Was NICHT hierher gehört
- Projektzustand (lebt in `project/STATE.md` — nie spiegeln)
- Regeln, die bereits in einem Skill kodifiziert sind (dann gehören sie in den Skill)
- Verlaufsprotokolle, Session-Transkripte, Rohdaten — Wissensbasen verrotten durch Rauschen

## Format
Eine Datei pro Learning, kebab-case, nach `LEARNING.template.md`. Max. 3–5 neue Einträge pro Retro.
Widerlegte Einträge nicht löschen, sondern oben mit `Status: widerlegt durch <datei/beleg>` markieren.

## Skalierungspfad
Wächst die Basis über einige hundert Einträge, kommt ein semantischer Index davor (Empfehlung:
Graphiti/Zep als MCP — temporaler Knowledge Graph). Die Markdown-Dateien bleiben dann die Quelle,
der Graph ist nur Index — analog graphify über Code.
