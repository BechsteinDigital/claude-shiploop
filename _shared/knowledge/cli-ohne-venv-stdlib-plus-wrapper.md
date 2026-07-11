# CLI-Tools ohne Aktivierungs-Reibung: System-Interpreter + stdlib + dünner Shell-Wrapper

- Status: aktiv
- Kontext: Neues CLI-Tool auf Linux/macOS, Anforderung „direkt aufrufbar, kein venv/Sourcen"
- Regel: Erst prüfen, ob der System-Interpreter (z. B. `python3`) plus Standardbibliothek reicht;
  Aufrufbarkeit über einen dünnen Shell-Wrapper in `bin/` (löst eigenen Pfad auf, ruft `python3 -m <paket>`),
  Installation = PATH-Eintrag oder Symlink. Dependencies erst einführen, wenn ein Muss-Ergebnis sie erzwingt.
- Warum: standup-CLI (2026-07-11): stdlib-only + Wrapper erfüllte die harte User-Bedingung ohne
  Paketmanager, venv oder Install-Schritt; Setup→MVP in 3 Zyklen ohne einen einzigen Dependency-Konflikt.
- Anwendung: autonomous-setup bei der Stack-Entscheidung (ADR); PO beim Schnitt der Aufrufbarkeits-Pakete.
