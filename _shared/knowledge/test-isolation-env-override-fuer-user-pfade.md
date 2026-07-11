# Tools, die in User-Pfade schreiben, brauchen ab dem Skeleton einen Env-Override — und alle Bestandstests müssen ihn nutzen

- Status: aktiv
- Kontext: Jedes Tool, das Dateien im Home-/User-Verzeichnis anlegt (Configs, Logs, Datenablagen)
- Regel: Der Pfad ist von der ersten Codezeile an per Env-Variable übersteuerbar (z. B. `STANDUP_FILE`),
  und **jeder** Test — auch Skeleton-/Smoke-Tests aus dem Setup — läuft ausschließlich gegen tmp-Overrides.
  Beim Setup zusätzlich prüfen: Welche Bestandstests brechen, wenn Skeleton-Verhalten echt wird? Diese
  Dateien einer Claim-Zone zuordnen (Niemandsland-Regel).
- Warum: standup-CLI (2026-07-11): Zwei Smoke-Tests aus dem Walking Skeleton liefen ohne Override —
  ein voller Suite-Lauf hat real `~/.standup.log` beschrieben und die Suite war nach Implementierung rot.
  Kostete einen kompletten Fix-Zyklus (WORK-005, ~106k Tokens); vom Review gefangen, nicht vom DEV.
- Anwendung: autonomous-setup (Skeleton-Design + Zonen-Zuordnung der Bestandstests); role-reviewer
  (Isolations-Check als Standard-Prüfpunkt bei Test-Diffs).
