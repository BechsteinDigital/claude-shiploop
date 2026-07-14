"""Smoke-Tests: CLI-Dispatch mit echtem Effekt (capture/show) + Pfadauflösung.

Alle Tests laufen ausschließlich gegen `STANDUP_FILE`-tmp-Pfade — die reale
`~/.standup.log` wird nie berührt (PROFILE-Regel). Auch der Default-Pfad-Test
arbeitet gegen ein gemocktes Home-Verzeichnis.
"""

import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from standup import cli, storage


class SmokeTestCase(unittest.TestCase):
    """Basis: `STANDUP_FILE` zeigt für jeden Test auf ein frisches tmp-Worklog."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp_dir = Path(tmp.name)
        self.file_path = self.tmp_dir / "worklog.log"
        env = mock.patch.dict(
            os.environ, {storage.ENV_FILE_OVERRIDE: str(self.file_path)}
        )
        env.start()
        self.addCleanup(env.stop)

    def run_cli(self, argv: list[str]) -> tuple[int, str, str]:
        """Ruft `cli.main(argv)` auf und liefert (Exit-Code, stdout, stderr)."""
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli.main(argv)
        return code, stdout.getvalue(), stderr.getvalue()


class CliSmokeTest(SmokeTestCase):
    def test_help_exits_zero(self) -> None:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as ctx:
                cli.main(["--help"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertIn("standup", buf.getvalue())

    def test_text_args_dispatch_to_capture_with_effect(self) -> None:
        code, stdout, stderr = self.run_cli(["PR", "gereviewt"])
        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        content = self.file_path.read_text(encoding="utf-8")
        self.assertEqual(content.count("\n"), 1, "genau eine Zeile erwartet")
        self.assertTrue(
            content.endswith(f"{storage.FIELD_SEPARATOR}PR gereviewt\n"),
            f"Eintrag fehlt oder Format falsch: {content!r}",
        )
        self.assertIn("PR gereviewt", stdout)

    def test_no_args_dispatches_to_show_latest_day_or_empty_message(self) -> None:
        # Leeres Log: Leermeldung auf stderr, Exit 1, kein stdout.
        code, stdout, stderr = self.run_cli([])
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("keine Einträge", stderr)

        # Nach Erfassung: Datum des jüngsten Tags + Eintrag, Exit 0.
        code, _, _ = self.run_cli(["Standup", "vorbereitet"])
        self.assertEqual(code, 0)
        stored_date = self.file_path.read_text(encoding="utf-8").split(
            storage.FIELD_SEPARATOR
        )[0]
        code, stdout, stderr = self.run_cli([])
        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        lines = stdout.splitlines()
        self.assertEqual(lines[0], stored_date)
        self.assertIn("- Standup vorbereitet", lines[1:])


class StoragePathTest(SmokeTestCase):
    def test_env_override_wins(self) -> None:
        with mock.patch.dict(os.environ, {storage.ENV_FILE_OVERRIDE: "/tmp/wl.log"}):
            self.assertEqual(storage.data_file_path(), Path("/tmp/wl.log"))

    def test_default_is_dotfile_in_home(self) -> None:
        # Default-Auflösung ohne Override testen, aber gegen gemocktes tmp-Home —
        # das reale Home-Verzeichnis wird nie referenziert oder berührt.
        with mock.patch.object(Path, "home", return_value=self.tmp_dir):
            with mock.patch.dict(os.environ, {}, clear=False):
                os.environ.pop(storage.ENV_FILE_OVERRIDE, None)
                self.assertEqual(
                    storage.data_file_path(),
                    self.tmp_dir / storage.DEFAULT_FILENAME,
                )


if __name__ == "__main__":
    unittest.main()
