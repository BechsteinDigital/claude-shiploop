"""Dünner CLI-Dispatcher (UX siehe ADR-005).

- `standup <freitext…>`  -> Eintrag für heute erfassen (standup.capture)
- `standup`              -> letzten Arbeitstag mit Eintrag anzeigen (standup.show)

Dieses Modul enthält bewusst keine Fachlogik — nur Argument-Parsing und Dispatch.
"""

import argparse
from typing import Optional, Sequence

from standup import __version__, capture, show


def build_parser() -> argparse.ArgumentParser:
    """Erzeugt den Argument-Parser für das Kommando `standup`."""
    parser = argparse.ArgumentParser(
        prog="standup",
        description=(
            "Worklog-CLI: eine Zeile pro Tag festhalten, "
            "vor dem Standup den letzten Arbeitstag abrufen."
        ),
        epilog=(
            "Ohne Argumente: letzten Arbeitstag mit Eintrag anzeigen. "
            "Freitext, der mit '-' beginnt, mit '--' abtrennen."
        ),
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Freitext des heutigen Eintrags; ohne Text wird der letzte Arbeitstag angezeigt.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI-Einstieg. Gibt den Prozess-Exitcode zurück."""
    args = build_parser().parse_args(argv)
    if args.text:
        return capture.run(" ".join(args.text))
    return show.run()
