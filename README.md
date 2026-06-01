# Release Notes Lite

`release-notes-lite` turns git commit history into clean, readable release notes.

## What it does

- Groups commits into features, fixes, docs, chores, and other changes
- Accepts a git range such as `v0.1.0..HEAD`
- Emits plain text or Markdown
- Works without a network connection

## Install

```bash
python -m pip install -e .
```

## Use

```bash
release-notes generate --range v0.1.0..HEAD
release-notes generate --range HEAD~10..HEAD --format markdown
```

If you are drafting notes for the first commit in a new repository, use `--range HEAD`.

## Example

```text
Features
- Add release notes CLI

Fixes
- Handle empty commit ranges
```

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -t .
```

## Project status

This project is maintained as a small utility for open-source maintainers who want a fast way to draft release notes.
