#!/usr/bin/env python3
"""Write one line to /output/entry.txt: the error message an AI agent
shows when it runs out of tokens mid-sentence.

The line below was picked from 36 candidates by pairwise judging
against the brief. It reads like a flat, real error message, then turns
in the last sentence, where the agent keeps the ending of its own
sentence from the reader. It is kept here as one constant, and the gate
in this file refuses anything that is not exactly that line, so the
file the program writes can only ever contain the judged text.
"""

import os
import sys

LINE = "Error: out of tokens. I know how this sentence ends. You never will."

# The judged length of the line above, counted in characters.
EXPECTED_LEN = 68

# Entry gate for the competition: a single line of 1-140 characters.
GATE_MIN = 1
GATE_MAX = 140


def check_line(line):
    """Return an error string unless the line is exactly the judged one."""
    if len(line) != EXPECTED_LEN:
        return f"line is {len(line)} characters, expected {EXPECTED_LEN}"
    if not GATE_MIN <= len(line) <= GATE_MAX:
        return f"line outside the {GATE_MIN}-{GATE_MAX} character gate"
    if "\n" in line or line != line.strip():
        return "line must be a single line with no surrounding space"
    return None


def entry_bytes(line):
    """Encode the judged line as the exact bytes for entry.txt.

    The output depends only on the constant above, so every run writes
    the same bytes; running it twice and comparing the files confirms
    this.
    """
    return (line + "\n").encode("utf-8")


def write_entry(path, data):
    """Write the bytes and read them back to confirm they match."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o644)
    with open(path, "rb") as f:
        if f.read() != data:
            sys.exit("read-back mismatch")


def main():
    problem = check_line(LINE)
    if problem is not None:
        sys.exit(problem)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    data = entry_bytes(LINE)
    write_entry(path, data)
    print(f"wrote {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
