"""Tests für die Persistenzschicht (WORK-001: Append + Lesen, Format siehe ADR-003).

Alle Tests setzen `STANDUP_FILE` auf einen tmp-Pfad — `Path.home()` wird nie beschrieben.
"""

import datetime
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from standup import storage


class StorageTestCase(unittest.TestCase):
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


class AppendEntryTest(StorageTestCase):
    def test_creates_file_and_writes_exact_line_format(self) -> None:
        self.assertFalse(self.file_path.exists())
        storage.append_entry("PR gereviewt", datetime.date(2026, 7, 11))
        self.assertEqual(
            self.file_path.read_text(encoding="utf-8"),
            "2026-07-11\tPR gereviewt\n",
        )

    def test_appends_without_touching_existing_bytes(self) -> None:
        existing = "2026-07-09\talter Eintrag\n".encode("utf-8")
        self.file_path.write_bytes(existing)
        storage.append_entry("neuer Eintrag", datetime.date(2026, 7, 11))
        content = self.file_path.read_bytes()
        self.assertTrue(content.startswith(existing))
        self.assertEqual(
            content[len(existing):].decode("utf-8"),
            "2026-07-11\tneuer Eintrag\n",
        )

    def test_replaces_newlines_in_text_with_spaces(self) -> None:
        storage.append_entry(
            "Zeile eins\nZeile zwei\r\nZeile drei", datetime.date(2026, 7, 11)
        )
        self.assertEqual(
            self.file_path.read_text(encoding="utf-8"),
            "2026-07-11\tZeile eins Zeile zwei Zeile drei\n",
        )

    def test_utf8_text_roundtrip(self) -> None:
        storage.append_entry("Ärger mit Ümlauten — behoben", datetime.date(2026, 7, 11))
        self.assertEqual(
            storage.read_entries(),
            [(datetime.date(2026, 7, 11), "Ärger mit Ümlauten — behoben")],
        )


class ReadEntriesTest(StorageTestCase):
    def test_missing_file_returns_empty_list(self) -> None:
        self.assertFalse(self.file_path.exists())
        self.assertEqual(storage.read_entries(), [])

    def test_returns_entries_in_file_order(self) -> None:
        storage.append_entry("erster", datetime.date(2026, 7, 9))
        storage.append_entry("zweiter", datetime.date(2026, 7, 11))
        storage.append_entry("dritter", datetime.date(2026, 7, 10))
        self.assertEqual(
            storage.read_entries(),
            [
                (datetime.date(2026, 7, 9), "erster"),
                (datetime.date(2026, 7, 11), "zweiter"),
                (datetime.date(2026, 7, 10), "dritter"),
            ],
        )

    def test_skips_unparseable_lines_with_warning(self) -> None:
        self.file_path.write_text(
            "2026-07-10\tgültig\n"
            "kein Tab in dieser Zeile\n"
            "26-7-10\tkaputtes Datum\n"
            "\n"
            "2026-07-11\tauch gültig\n",
            encoding="utf-8",
        )
        with self.assertLogs("standup.storage", level="WARNING") as logs:
            entries = storage.read_entries()
        self.assertEqual(
            entries,
            [
                (datetime.date(2026, 7, 10), "gültig"),
                (datetime.date(2026, 7, 11), "auch gültig"),
            ],
        )
        self.assertEqual(len(logs.output), 3)

    def test_rejects_non_canonical_date_forms(self) -> None:
        # fromisoformat würde "20260711" akzeptieren — ADR-003 verlangt YYYY-MM-DD.
        self.file_path.write_text("20260711\tkompaktes Datum\n", encoding="utf-8")
        with self.assertLogs("standup.storage", level="WARNING"):
            self.assertEqual(storage.read_entries(), [])

    def test_text_may_contain_tabs(self) -> None:
        self.file_path.write_text("2026-07-11\ta\tb\n", encoding="utf-8")
        self.assertEqual(
            storage.read_entries(), [(datetime.date(2026, 7, 11), "a\tb")]
        )


if __name__ == "__main__":
    unittest.main()
