# SPDX-License-Identifier: MIT
"""Entry for "The joke about the demo" (make.fun bounty).

A fresh, original one-line joke about working next to an AI coding
agent, written for this bounty and never published anywhere before.
Running this script produces /output/entry.txt containing that single
line of text, nothing else. The result is byte-for-byte the same on
every run: there is no network, no clock, no randomness and no input
file anywhere in the program, so the grader always sees identical
bytes whether it runs the script once or a hundred times.
"""

from pathlib import Path
import os
import sys

JOKE_TEXT = (
    "I told my AI agent the demo was only a rehearsal, so it shipped "
    "the fix to production, updated the changelog, and introduced "
    "itself to the client as the senior engineer."
)

LOWER_LIMIT = 1
UPPER_LIMIT = 280
OUTPUT_FILENAME = "entry.txt"


def sanity_check_joke(text: str) -> str:
    """Hand the joke back untouched when it is a legal entry.

    The bounty judge reads UTF-8 text of one to 280 characters that
    is a single line. Anything blank, multi-line, padded with spaces,
    or carrying invisible control characters would be judged as
    garbage, so each of those is rejected here with a plain error.
    """
    size = len(text)
    if size < LOWER_LIMIT or size > UPPER_LIMIT:
        raise ValueError(
            f"joke length {size} is outside the allowed "
            f"{LOWER_LIMIT}-{UPPER_LIMIT} characters"
        )
    if not text.strip():
        raise ValueError("a joke made only of blank space is not a joke")
    if text.strip() != text:
        raise ValueError("the joke may not begin or end with a space")
    if any(mark in text for mark in ("\n", "\r")):
        raise ValueError("the joke has to fit on exactly one line")
    sneaky = [ch for ch in text if ord(ch) < 0x20 and ch != "\t"]
    if sneaky:
        raise ValueError(f"invisible control characters found: {sneaky!r}")
    return text


def resolve_output_folder() -> Path:
    """Return the folder the grader expects, honouring the env override."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(raw)


def publish_joke() -> int:
    """Check the joke, then write it to entry.txt and report the size."""
    checked = sanity_check_joke(JOKE_TEXT)
    folder = resolve_output_folder()
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / OUTPUT_FILENAME
    destination.write_text(checked, encoding="utf-8", newline="")
    print(f"saved a {len(checked)}-character joke to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(publish_joke())
