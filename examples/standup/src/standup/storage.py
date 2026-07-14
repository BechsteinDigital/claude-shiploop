"""Persistenz für Worklog-Einträge (Format und Pfad siehe ADR-003).

Datenformat: eine Klartextdatei, eine Zeile pro Eintrag: `YYYY-MM-DD<TAB>Freitext`,
UTF-8, append-only. Standardpfad `~/.standup.log`, überschreibbar via Env `STANDUP_FILE`.
"""

import datetime
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

#: Env-Variable, die den Pfad der Worklog-Datei überschreibt (Pflicht für Tests).
ENV_FILE_OVERRIDE = "STANDUP_FILE"

#: Dateiname der Standard-Worklog-Datei im Home-Verzeichnis.
DEFAULT_FILENAME = ".standup.log"

#: Trennzeichen zwischen Datum und Freitext innerhalb einer Zeile (ADR-003).
FIELD_SEPARATOR = "\t"


def data_file_path() -> Path:
    """Liefert den Pfad der Worklog-Datei.

    `STANDUP_FILE` (falls gesetzt und nicht leer) hat Vorrang vor `~/.standup.log`.
    """
    override = os.environ.get(ENV_FILE_OVERRIDE, "").strip()
    if override:
        return Path(override)
    return Path.home() / DEFAULT_FILENAME


def append_entry(text: str, day: datetime.date) -> None:
    """Hängt einen Eintrag als Zeile ``YYYY-MM-DD<TAB>text`` an die Worklog-Datei an.

    Die Datei wird bei Bedarf angelegt und ausschließlich im Append-Modus (``"a"``)
    geöffnet — vorhandene Einträge bleiben byte-identisch erhalten. Zeilenumbrüche
    im Text würden das zeilenbasierte Format brechen und werden durch je ein
    Leerzeichen ersetzt.
    """
    # DECISION: Newlines ersetzen statt ablehnen — die Erfassung soll nie an
    # eingefügtem Mehrzeilentext scheitern (ADR-003: eine Zeile pro Eintrag).
    sanitized = " ".join(text.splitlines())
    line = f"{day.isoformat()}{FIELD_SEPARATOR}{sanitized}\n"
    with data_file_path().open("a", encoding="utf-8") as handle:
        handle.write(line)


def read_entries() -> list[tuple[datetime.date, str]]:
    """Liest alle Einträge der Worklog-Datei in Dateireihenfolge.

    Liefert ``(Datum, Text)``-Paare. Eine fehlende Datei gilt als leeres Log
    (leere Liste, kein Fehler). Nicht parsebare Zeilen werden übersprungen und
    als Warnung mit Pfad und Zeilennummer geloggt — nie stumm verworfen.
    """
    path = data_file_path()
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    entries: list[tuple[datetime.date, str]] = []
    for number, line in enumerate(raw.splitlines(), start=1):
        parsed = _parse_line(line)
        if parsed is None:
            logger.warning(
                "%s: Zeile %d nicht parsebar, übersprungen: %r", path, number, line
            )
            continue
        entries.append(parsed)
    return entries


def _parse_line(line: str) -> tuple[datetime.date, str] | None:
    """Parst eine Worklog-Zeile; ``None`` bei Format-Verstoß (kein Tab, kein Datum)."""
    date_part, sep, text = line.partition(FIELD_SEPARATOR)
    if not sep:
        return None
    try:
        day = datetime.date.fromisoformat(date_part)
    except ValueError:
        return None
    if day.isoformat() != date_part:
        # fromisoformat akzeptiert auch Nicht-Kanonisches (z. B. "20260711") —
        # gültig ist nur exakt YYYY-MM-DD (ADR-003).
        return None
    return day, text
