"""Tests für das Erfassen (WORK-002: `standup <text>` schreibt Tageseintrag).

Alle Tests setzen `STANDUP_FILE` auf einen tmp-Pfad — `Path.home()` wird nie beschrieben.
Das "Heute"-Datum wird über die Test-Naht `capture._today` fixiert (deterministisch).
"""

import contextlib
import datetime
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from standup import capture, storage

#: Fixiertes "Heute" für deterministische Zeilen-Asserts.
TODAY = datetime.date(2026, 7, 11)


class CaptureTestCase(unittest.TestCase):
    """Basis: frisches tmp-Worklog pro Test, festes Datum via `capture._today`."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.file_path = Path(tmp.name) / "worklog.log"
        env = mock.patch.dict(
            os.environ, {storage.ENV_FILE_OVERRIDE: str(self.file_path)}
        )
        env.start()
        self.addCleanup(env.stop)
        today = mock.patch.object(capture, "_today", return_value=TODAY)
        today.start()
        self.addCleanup(today.stop)

    def run_capture(self, text) -> tuple[int, str, str]:
        """Ruft `capture.run(text)` auf und liefert (Exit-Code, stdout, stderr)."""
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = capture.run(text)
        return code, stdout.getvalue(), stderr.getvalue()


class CaptureSuccessTest(CaptureTestCase):
    def test_writes_exactly_one_line_and_returns_zero(self) -> None:
        code, _, stderr = self.run_capture("PR gereviewt")
        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(
            self.file_path.read_text(encoding="utf-8"),
            "2026-07-11\tPR gereviewt\n",
        )

    def test_second_capture_same_day_appends_instead_of_overwriting(self) -> None:
        first, _, _ = self.run_capture("erster Eintrag")
        second, _, _ = self.run_capture("zweiter Eintrag")
        self.assertEqual((first, second), (0, 0))
        self.assertEqual(
            self.file_path.read_text(encoding="utf-8"),
            "2026-07-11\terster Eintrag\n2026-07-11\tzweiter Eintrag\n",
        )

    def test_confirmation_on_stdout_names_date_and_text(self) -> None:
        code, stdout, _ = self.run_capture("PR gereviewt")
        self.assertEqual(code, 0)
        self.assertIn("2026-07-11", stdout)
        self.assertIn("PR gereviewt", stdout)


class CaptureNormalizationTest(CaptureTestCase):
    def test_strips_surrounding_whitespace_before_storing(self) -> None:
        code, stdout, _ = self.run_capture("  Deploy vorbereitet  ")
        self.assertEqual(code, 0)
        self.assertEqual(
            self.file_path.read_text(encoding="utf-8"),
            "2026-07-11\tDeploy vorbereitet\n",
        )
        self.assertIn("Deploy vorbereitet", stdout)

    def test_multiline_text_is_confirmed_exactly_as_stored(self) -> None:
        code, stdout, _ = self.run_capture("Zeile eins\nZeile zwei")
        self.assertEqual(code, 0)
        self.assertEqual(
            self.file_path.read_text(encoding="utf-8"),
            "2026-07-11\tZeile eins Zeile zwei\n",
        )
        self.assertIn("Zeile eins Zeile zwei", stdout)


class CaptureRejectionTest(CaptureTestCase):
    def assert_rejected_without_write(self, text) -> None:
        code, stdout, stderr = self.run_capture(text)
        self.assertNotEqual(code, 0)
        self.assertEqual(stdout, "")
        self.assertNotEqual(stderr.strip(), "", "Ablehnung braucht stderr-Meldung")
        self.assertFalse(self.file_path.exists(), "Ablehnung darf nicht schreiben")

    def test_empty_text_is_rejected(self) -> None:
        self.assert_rejected_without_write("")

    def test_whitespace_only_text_is_rejected(self) -> None:
        self.assert_rejected_without_write("   \n\t  ")

    def test_none_is_rejected_defensively(self) -> None:
        self.assert_rejected_without_write(None)


class CaptureStorageErrorTest(CaptureTestCase):
    def test_oserror_yields_stderr_message_and_nonzero_exit(self) -> None:
        with mock.patch.object(
            storage, "append_entry", side_effect=OSError("Platte voll")
        ):
            code, stdout, stderr = self.run_capture("Eintrag")
        self.assertNotEqual(code, 0)
        self.assertEqual(stdout, "")
        self.assertIn("Platte voll", stderr)


class TodayHelperTest(unittest.TestCase):
    def test_today_helper_returns_local_date(self) -> None:
        before = datetime.date.today()
        value = capture._today()
        after = datetime.date.today()
        self.assertIn(value, {before, after})


if __name__ == "__main__":
    unittest.main()
