from __future__ import annotations

from contextlib import redirect_stdout
from contextlib import redirect_stderr
from io import StringIO
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from release_notes_lite.cli import main
from release_notes_lite.formatting import format_markdown, format_text
from release_notes_lite.generator import CommitItem, generate_release_notes


class ReleaseNotesTests(unittest.TestCase):
    def test_groups_commits_by_category(self) -> None:
        commits = [
            CommitItem(sha="1", subject="feat: add CLI", category="features"),
            CommitItem(sha="2", subject="fix: handle empty range", category="fixes"),
            CommitItem(sha="3", subject="docs: update README", category="docs"),
        ]

        text = format_text(commits)
        markdown = format_markdown(commits)

        self.assertIn("Features", text)
        self.assertIn("- feat: add CLI", text)
        self.assertIn("## Fixes", markdown)
        self.assertIn("- docs: update README", markdown)

    def test_generate_release_notes_uses_git_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fake_output = "abc123\x00feat: add release notes\n"

            with patch("subprocess.run") as run_mock:
                run_mock.return_value.stdout = fake_output
                notes = generate_release_notes(root, "v0.1.0..HEAD")

            self.assertEqual(len(notes), 1)
            self.assertEqual(notes[0].category, "features")

    def test_cli_prints_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with patch("release_notes_lite.cli.generate_release_notes") as generator_mock:
                generator_mock.return_value = [CommitItem(sha="1", subject="feat: add CLI", category="features")]
                buffer = StringIO()
                with redirect_stdout(buffer):
                    exit_code = main(["generate", "--range", "v0.1.0..HEAD", "--root", str(root)])

            self.assertEqual(exit_code, 0)
            self.assertIn("feat: add CLI", buffer.getvalue())

    def test_cli_reports_git_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with patch("release_notes_lite.cli.generate_release_notes") as generator_mock:
                generator_mock.side_effect = RuntimeError("git log failed")
                buffer = StringIO()
                error_buffer = StringIO()
                with redirect_stdout(buffer), redirect_stderr(error_buffer):
                    exit_code = main(["generate", "--range", "HEAD~1..HEAD", "--root", str(root)])

            self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
