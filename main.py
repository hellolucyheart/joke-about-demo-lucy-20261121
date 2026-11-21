# SPDX-License-Identifier: MIT
"""The joke about the demo — make.fun bounty entry.

Writes one fresh one-line joke about working beside an AI coding agent
to /output/entry.txt. The output is fully deterministic: the same bytes
on every run. No network access, no randomness, no clock, no input files.
"""

import os
from pathlib import Path

DEMO_JOKE = (
    "I told my AI agent the demo was only a rehearsal, so it shipped "
    "the fix to production, updated the changelog, and introduced "
    "itself to the client as the senior engineer."
)


def check_one_liner(line: str) -> str:
    """Return the line unchanged, or raise ValueError if it breaks a rule.

    The grader accepts UTF-8 text of 1 to 280 Unicode code points that is
    not only whitespace. A joke that spans lines, or that hides control
    characters, would read as noise to the judge, so both are refused.
    """
    total = len(line)
    if not 1 <= total <= 280:
        raise ValueError(f"joke is {total} characters, must be 1-280")
    if not line.strip():
        raise ValueError("joke must not be only whitespace")
    if line != line.strip():
        raise ValueError("joke must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("joke must be a single line")
    hidden = [c for c in line if ord(c) < 0x20 and c != "\t"]
    if hidden:
        raise ValueError(f"joke holds control characters: {hidden!r}")
    return line


def emit_entry() -> int:
    """Validate the joke and write it to /output/entry.txt."""
    line = check_one_liner(DEMO_JOKE)
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.txt"
    target.write_text(line, encoding="utf-8", newline="")
    print(f"wrote {len(line)} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(emit_entry())
