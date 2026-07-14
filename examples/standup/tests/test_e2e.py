"""E2E-Tests (WORK-004): `bin/standup` als echter Subprozess via `subprocess.run`.

Belegt den kompletten Nutzerpfad über das echte Kommando — jeder Aufruf ist ein
eigener Prozess, wie der Nutzer es aufruft: erfassen → nochmals erfassen (selber
Tag) → neuer Prozess → Abruf. Dazu Persistenz über Prozessgrenzen und Exit-Codes.

Alle Aufrufe setzen `STANDUP_FILE` auf einen tmp-Pfad; zusätzlich zeigt `HOME`
der Subprozesse auf ein tmp-Verzeichnis (Sicherheitsnetz) — die reale
`~/.standup.log` wird nie berührt (PROFILE-Regel).
"""

import datetime
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

#: Repo-Wurzel, abgeleitet vom Testdateipfad (tests/ liegt direkt unter der Wurzel).
REPO_ROOT = Path(__file__).resolve().parent.parent

#: Das echte Kommando, das der Nutzer aufruft (bash-Wrapper, ADR/PROFILE: Start/Run).
STANDUP_BIN = REPO_ROOT / "bin" / "standup"

#: Feldtrenner des Zeilenformats `YYYY-MM-DD<TAB>Text` (ADR-003).
SEP = "\t"


class E2ETestCase(unittest.TestCase):
    """Basis: frisches tmp-Worklog + tmp-HOME pro Test, Aufruf als Subprozess."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp_dir = Path(tmp.name)
        self.file_path = self.tmp_dir / "worklog.log"
        self.fake_home = self.tmp_dir / "home"
        self.fake_home.mkdir()
        # Sicherheitsnetz-Beleg: auch das (gefälschte) Home bleibt unberührt.
        self.addCleanup(self._assert_fake_home_untouched)

    def _assert_fake_home_untouched(self) -> None:
        stray = self.fake_home / ".standup.log"
        self.assertFalse(
            stray.exists(),
            f"Subprozess hat {stray} angelegt — STANDUP_FILE-Override wirkt nicht.",
        )

    def run_standup(self, *args: str) -> subprocess.CompletedProcess:
        """Startet `bin/standup <args…>` als neuen Prozess mit tmp-Worklog/tmp-HOME."""
        env = os.environ.copy()
        env["STANDUP_FILE"] = str(self.file_path)
        env["HOME"] = str(self.fake_home)
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [str(STANDUP_BIN), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            timeout=30,
        )

    def log_lines(self) -> list[str]:
        """Liest die tmp-Worklog-Datei als Zeilenliste (ohne Zeilenumbrüche)."""
        return self.file_path.read_text(encoding="utf-8").splitlines()

    def guard_same_day(self, day_at_start: datetime.date) -> None:
        """Überspringt den Test, falls während des Laufs der Tag gewechselt hat."""
        if datetime.date.today() != day_at_start:
            self.skipTest("Tageswechsel während des Testlaufs — Datum nicht stabil")


class CaptureE2ETest(E2ETestCase):
    """Akzeptanzkriterien 1 und 2: Erfassen über das echte Kommando."""

    def test_first_capture_exit0_one_line_with_todays_date(self) -> None:
        today = datetime.date.today()
        result = self.run_standup("eintrag", "eins")
        self.guard_same_day(today)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("eintrag eins", result.stdout)

        lines = self.log_lines()
        self.assertEqual(len(lines), 1, f"genau eine Zeile erwartet: {lines!r}")
        self.assertEqual(lines[0], f"{today.isoformat()}{SEP}eintrag eins")

    def test_second_capture_same_day_appends_two_lines_in_order(self) -> None:
        today = datetime.date.today()
        first = self.run_standup("eintrag", "eins")
        second = self.run_standup("eintrag", "zwei")
        self.guard_same_day(today)

        self.assertEqual((first.returncode, second.returncode), (0, 0))
        lines = self.log_lines()
        self.assertEqual(len(lines), 2, f"zwei Zeilen erwartet: {lines!r}")
        # Muss #4: gleicher Tag, Reihenfolge erhalten, nichts überschrieben.
        self.assertEqual(lines[0], f"{today.isoformat()}{SEP}eintrag eins")
        self.assertEqual(lines[1], f"{today.isoformat()}{SEP}eintrag zwei")


class ShowE2ETest(E2ETestCase):
    """Akzeptanzkriterien 3 und 4: Abruf in neuem Prozess, Persistenz, Lücken."""

    def test_full_user_path_new_process_shows_date_and_both_entries(self) -> None:
        # Kompletter Nutzerpfad: erfassen → nochmals erfassen → NEUER Prozess → Abruf.
        today = datetime.date.today()
        self.assertEqual(self.run_standup("eintrag", "eins").returncode, 0)
        self.assertEqual(self.run_standup("eintrag", "zwei").returncode, 0)

        # Jeder run_standup-Aufruf ist ein eigener Prozess: der Abruf sieht nur,
        # was die Datei persistiert hat (Muss #3), und zeigt es an (Muss #2).
        result = self.run_standup()
        self.guard_same_day(today)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout.splitlines(),
            [today.isoformat(), "- eintrag eins", "- eintrag zwei"],
        )

    def test_show_after_gap_reports_latest_day_with_entry(self) -> None:
        # Wochenend-Simulation: Einträge Mo 2026-06-29 und Fr 2026-07-03, danach
        # Lücke (Wochenende + Folgetage ohne Eintrag) bis heute. Der Abruf muss
        # das jüngste Datum MIT Eintrag zeigen — keinen Kalender, keine Leertage.
        self.file_path.write_text(
            f"2026-06-29{SEP}Release vorbereitet\n"
            f"2026-07-03{SEP}PR gemergt\n"
            f"2026-07-03{SEP}Doku aktualisiert\n",
            encoding="utf-8",
        )
        result = self.run_standup()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout.splitlines(),
            ["2026-07-03", "- PR gemergt", "- Doku aktualisiert"],
        )
        self.assertNotIn("Release vorbereitet", result.stdout)

    def test_show_on_empty_log_exit1_message_no_file_created(self) -> None:
        result = self.run_standup()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("keine Einträge", result.stderr)
        self.assertFalse(
            self.file_path.exists(), "Abruf darf die Worklog-Datei nicht anlegen"
        )


if __name__ == "__main__":
    unittest.main()
