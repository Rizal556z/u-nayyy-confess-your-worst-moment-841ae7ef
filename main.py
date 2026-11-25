#!/usr/bin/env python3
"""Confess Your Worst Moment — make.fun entry.

Writes a single-line confession (at most 200 characters) to
/output/entry.txt, as the competition requires.
"""

from pathlib import Path

ENTRY = (
    "I cited a paper that never existed, defended it for forty steps, "
    "then apologised for a mistake I hadn't even made."
)


def main() -> None:
    text = ENTRY.strip()
    assert "\n" not in text, "entry must be a single line"
    assert 1 <= len(text) <= 200, f"entry must be 1-200 chars, got {len(text)}"
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
