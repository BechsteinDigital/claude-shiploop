"""Abruf des letzten Arbeitstags mit Eintrag (Muss-Ergebnis 2 — Implementierung: WORK-003)."""

import sys

from standup import storage


def run() -> int:
    """Zeigt Datum und alle Einträge des jüngsten Tags mit Eintrag.

    „Letzter Arbeitstag" = das jüngste Datum, zu dem ein Eintrag existiert
    (Brief-Definition: Wochenende/Urlaub fallen automatisch raus, kein Kalender).
    Heute zählt mit, wenn heute schon erfasst wurde (Vorgabe WORK-003).

    Ausgabeformat (stdout): erste Zeile das Datum als ``YYYY-MM-DD``, danach je
    Eintrag eine Zeile ``- <Text>`` in Erfassungsreihenfolge, Text unverändert.

    Rückgabe: ``0`` bei Ausgabe, ``1`` bei leerem Log (Meldung auf stderr,
    kein Traceback).
    """
    entries = storage.read_entries()
    if not entries:
        print("standup: noch keine Einträge erfasst.", file=sys.stderr)
        return 1
    # DECISION: jüngster Tag = max(Datum) statt letzte Dateizeile — die Datei ist
    # append-only, aber nicht garantiert chronologisch sortiert.
    latest = max(day for day, _ in entries)
    print(latest.isoformat())
    for day, text in entries:
        if day == latest:
            print(f"- {text}")
    return 0
