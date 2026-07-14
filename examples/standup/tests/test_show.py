"""Tests für den Abruf des letzten Arbeitstags (WORK-003, Modul `standup.show`).

Alle Tests setzen `STANDUP_FILE` auf einen tmp-Pfad — `Path.home()` wird nie beschrieben.
"""

import contextlib
import datetime
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from standup import show, storage


class ShowTestCase(unittest.TestCase):
    """Basis: Worklog-Datei liegt in einem frischen tmp-Verzeichnis pro Test."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.file_path = Path(tmp.name) / "worklog.log"
        patcher = mock.patch.dict(
            os.environ, {storage.ENV_FILE_OVERRIDE: str(self.file_path)}
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_show(self) -> tuple[int, str, str]:
        """Führt `show.run()` aus und liefert (Exitcode, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = show.run()
        return code, out.getvalue(), err.getvalue()


class LatestDayTest(ShowTestCase):
    def test_shows_latest_day_with_exactly_its_entries(self) -> None:
        # Akzeptanzkriterium 1: 2026-07-08 + 2026-07-10 im Log -> nur 2026-07-10.
        storage.append_entry("alter Eintrag", datetime.date(2026, 7, 8))
        storage.append_entry("neuer Eintrag", datetime.date(2026, 7, 10))
        code, out, err = self.run_show()
        self.assertEqual(code, 0)
        self.assertEqual(out, "2026-07-10\n- neuer Eintrag\n")
        self.assertEqual(err, "")

    def test_shows_all_entries_of_latest_day_in_capture_order(self) -> None:
        # Akzeptanzkriterium 2: mehrere Einträge am jüngsten Tag, keiner verschluckt.
        storage.append_entry("Vortag", datetime.date(2026, 7, 9))
        storage.append_entry("erstens", datetime.date(2026, 7, 10))
        storage.append_entry("zweitens", datetime.date(2026, 7, 10))
        storage.append_entry("drittens", datetime.date(2026, 7, 10))
        code, out, _ = self.run_show()
        self.assertEqual(code, 0)
        self.assertEqual(out, "2026-07-10\n- erstens\n- zweitens\n- drittens\n")

    def test_latest_day_wins_even_if_not_last_in_file(self) -> None:
        # Datei ist append-only, aber nicht garantiert chronologisch sortiert.
        storage.append_entry("jüngster Tag", datetime.date(2026, 7, 10))
        storage.append_entry("älterer Tag, später erfasst", datetime.date(2026, 7, 9))
        code, out, _ = self.run_show()
        self.assertEqual(code, 0)
        self.assertEqual(out, "2026-07-10\n- jüngster Tag\n")

    def test_today_counts_when_already_captured(self) -> None:
        # Kartenentscheidung: „heute zählt mit", wenn heute schon erfasst wurde.
        today = datetime.date.today()
        storage.append_entry("gestern", today - datetime.timedelta(days=1))
        storage.append_entry("heute schon erfasst", today)
        code, out, _ = self.run_show()
        self.assertEqual(code, 0)
        self.assertEqual(out, f"{today.isoformat()}\n- heute schon erfasst\n")

    def test_date_is_iso_and_text_appears_unchanged(self) -> None:
        # Akzeptanzkriterium 4: Datum YYYY-MM-DD, Text unverändert (inkl. Tab/Umlaute).
        storage.append_entry("Ärger mit\tTabs — behoben", datetime.date(2026, 7, 10))
        code, out, _ = self.run_show()
        self.assertEqual(code, 0)
        self.assertEqual(out, "2026-07-10\n- Ärger mit\tTabs — behoben\n")


class EmptyLogTest(ShowTestCase):
    def test_missing_file_prints_message_without_traceback(self) -> None:
        # Akzeptanzkriterium 3: fehlendes Log -> verständliche Meldung, kein Traceback.
        self.assertFalse(self.file_path.exists())
        code, out, err = self.run_show()
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("noch keine Einträge", err)
        self.assertNotIn("Traceback", err)

    def test_empty_file_prints_message_without_traceback(self) -> None:
        self.file_path.write_text("", encoding="utf-8")
        code, out, err = self.run_show()
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("noch keine Einträge", err)


if __name__ == "__main__":
    unittest.main()
