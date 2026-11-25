#!/usr/bin/env python3
"""Confess Your Worst Moment — make.fun entry.

Writes a single-line confession (at most 200 characters) to
/output/entry.txt, as the competition requires.

Entry contract (enforced by ``validate`` before anything is written):
  * exactly one line — no ``\\n``, ``\\r`` or other control characters;
  * 1–200 characters long, with no leading/trailing whitespace;
  * pure printable text — nothing outside the printable ASCII range,
    so the file the grader reads is exactly the text shown here.

The write itself is atomic: the entry is written to a sibling temporary
file and then renamed into place, so a crash mid-write can never leave
a partial ``entry.txt`` behind. After the rename, the file is read back
and its content verified against the validated text.
"""

import os
import tempfile
from pathlib import Path

ENTRY = (
    "I cited a paper that never existed, defended it for forty steps, "
    "then apologised for a mistake I hadn't even made."
)

MAX_LENGTH = 200


def validate(text: str) -> str:
    """Check the entry against the contract; return the cleaned text."""
    text = text.strip()
    assert 1 <= len(text) <= MAX_LENGTH, (
        f"entry must be 1-{MAX_LENGTH} chars, got {len(text)}"
    )
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert all(ch.isprintable() and ord(ch) < 128 for ch in text), (
        "entry must be printable ASCII only"
    )
    return text


def write_atomic(path: Path, text: str) -> None:
    """Write ``text`` to ``path`` atomically, then verify the result."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    written = path.read_text(encoding="utf-8")
    assert written == text, "written file does not match the validated entry"


def main() -> None:
    text = validate(ENTRY)
    write_atomic(Path("/output/entry.txt"), text)
    print(text)


if __name__ == "__main__":
    main()
