from __future__ import annotations

from collections import OrderedDict

from .generator import CATEGORY_ORDER, CommitItem


def format_text(commits: list[CommitItem]) -> str:
    grouped = _group_commits(commits)
    lines: list[str] = []
    for category in CATEGORY_ORDER:
        items = grouped.get(category, [])
        if not items:
            continue
        lines.append(category.capitalize())
        for item in items:
            lines.append(f"- {item.subject}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def format_markdown(commits: list[CommitItem]) -> str:
    grouped = _group_commits(commits)
    lines: list[str] = ["# Release Notes", ""]
    for category in CATEGORY_ORDER:
        items = grouped.get(category, [])
        if not items:
            continue
        lines.append(f"## {category.capitalize()}")
        lines.append("")
        for item in items:
            lines.append(f"- {item.subject}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _group_commits(commits: list[CommitItem]) -> OrderedDict[str, list[CommitItem]]:
    grouped: OrderedDict[str, list[CommitItem]] = OrderedDict((category, []) for category in CATEGORY_ORDER)
    for commit in commits:
        grouped[commit.category].append(commit)
    return grouped
