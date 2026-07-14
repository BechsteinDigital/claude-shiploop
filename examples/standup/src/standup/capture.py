"""Erfassen eines Tageseintrags (Muss-Ergebnis 1 und 4 — Implementierung: WORK-002)."""

import datetime
import sys

from standup import storage


def _today() -> datetime.date:
    """Liefert das lokale heutige Datum (eigene Funktion als Test-Naht)."""
    return datetime.date.today()


def run(text: str) -> int:
    """Erfasst ``text`` als Eintrag für heute (lokales Datum) über die Storage-Schicht.

    Leerer oder nur aus Whitespace bestehender Text wird abgelehnt: verständliche
    Meldung auf stderr, Rückgabe 1, kein Schreibzugriff. Bei Erfolg wird genau eine
    Zeile angehängt (append-only, WORK-001-Vertrag) und auf stdout mit Datum und
    gespeichertem Text bestätigt; Rückgabe 0.
    """
    # DECISION: Eingabe normalisieren (trim + Zeilenumbrüche -> Leerzeichen), damit
    # die Bestätigung exakt den gespeicherten Text zeigt (ADR-003: eine Zeile pro
    # Eintrag; storage.append_entry ersetzt Newlines ohnehin identisch).
    entry = " ".join((text or "").strip().splitlines())
    if not entry:
        print(
            "standup: leerer Text — nichts erfasst. Beispiel: standup PR gereviewt",
            file=sys.stderr,
        )
        return 1
    day = _today()
    try:
        storage.append_entry(entry, day)
    except OSError as error:
        print(
            f"standup: Eintrag konnte nicht gespeichert werden: {error}",
            file=sys.stderr,
        )
        return 1
    print(f"Erfasst für {day.isoformat()}: {entry}")
    return 0
