from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass(frozen=True)
class CommitItem:
    sha: str
    subject: str
    category: str


CATEGORY_ORDER = ("features", "fixes", "docs", "chore", "other")


def generate_release_notes(root: Path, revision_range: str) -> list[CommitItem]:
    commits = _read_commits(root, revision_range)
    return [CommitItem(sha=sha, subject=subject, category=_categorize(subject)) for sha, subject in commits]


def _read_commits(root: Path, revision_range: str) -> list[tuple[str, str]]:
    command = ["git", "-C", str(root), "log", "--format=%H%x00%s", revision_range]
    try:
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(exc.stderr.strip() or exc.stdout.strip() or f"git log failed for range {revision_range}") from exc
    output = completed.stdout.strip()
    if not output:
        return []

    commits: list[tuple[str, str]] = []
    for line in output.splitlines():
        sha, subject = line.split("\x00", 1)
        commits.append((sha, subject))
    return commits


def _categorize(subject: str) -> str:
    lower = subject.lower()
    if lower.startswith(("feat:", "feature:", "add ")):
        return "features"
    if lower.startswith(("fix:", "bugfix:", "patch:")):
        return "fixes"
    if lower.startswith(("docs:", "doc:")):
        return "docs"
    if lower.startswith(("chore:", "build:", "ci:", "refactor:", "test:")):
        return "chore"
    return "other"
