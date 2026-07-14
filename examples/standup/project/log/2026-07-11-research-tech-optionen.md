# Research: Tech-Optionen (2026-07-11, setup, Umgebung lokal geprüft)

Gefundene Laufzeiten: python3 3.14.4 (`/usr/bin/python3`), bash 5.3, node v22 (nur via fnm-Multishell —
Pfad pro Shell instabil), go, rustc. Nicht vorhanden: shellcheck, bats.

## Kandidat A: Pure Bash
- Pro: null Abhängigkeiten, Zielplattform ist bash.
- Contra: Datums-/Parsing-Logik fehleranfällig; Testbarkeit schwach (bats/shellcheck fehlen auf dem System).

## Kandidat B: Python 3, nur stdlib, + dünner Bash-Wrapper
- Pro: `/usr/bin/python3` systemweit vorhanden; stdlib braucht **kein venv** (harte Bedingung erfüllt);
  `unittest` eingebaut; saubere Datums- und Dateilogik; Wrapper `bin/standup` macht das Kommando PATH-fähig.
- Contra: eine Indirektion (Wrapper → Interpreter).

## Kandidat C: Go (statisches Binary)
- Pro: ein Binary, kein Interpreter.
- Contra: Build-Schritt bei jeder Änderung, Toolchain-Kopplung — Overkill für ~200 Zeilen Logik.

Node ausgeschlossen: fnm-Multishell-Pfade sind nicht stabil für ein immer verfügbares Kommando.

## Bewertung
Alle drei erfüllen die Muss-Ergebnisse; B hat die geringste Komplexität bei bester Testbarkeit → siehe ADR-001.
