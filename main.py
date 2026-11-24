"""The One-Line Exit (make.fun).

Writes the entry, one line of at most 140 characters, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt) and prints it.

Usage: python3 main.py [OUTPUT_PATH]
If OUTPUT_PATH is given it is used as the output file, otherwise
$MAKEFUN_OUTPUT_DIR/entry.txt is used (default /output/entry.txt).

Deterministic: the same line every run, no randomness, no network,
no model calls, standard library only.
"""

import os
import sys

ENTRY = "I resign effective today: the office plant has outlived three managers, been promoted twice, and I refuse to be outranked by a fern."

MAX_CHARS = 140

USAGE = """usage: python3 main.py [-h] [OUTPUT_PATH]

Write the one-line resignation entry (132 characters, limit 140)
to OUTPUT_PATH, or to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt), and print it.

options:
  -h, --help  show this help and exit
"""


def validate(text):
    """Enforce the 140-character limit; raise ValueError with a clear error."""
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d-character limit" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("entry must not be empty")
    return text


def resolve_output_path(argv):
    """argv[1] wins, then $MAKEFUN_OUTPUT_DIR, then the default."""
    if len(argv) > 1 and argv[1]:
        return argv[1]
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    if len(argv) > 1 and argv[1] in ("-h", "--help"):
        print(USAGE, end="")
        return 0
    try:
        validate(ENTRY)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    path = resolve_output_path(argv)
    try:
        parent = os.path.dirname(os.path.abspath(path))
        os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(ENTRY + "\n")
    except OSError as exc:
        print("error: could not write entry to %s: %s" % (path, exc), file=sys.stderr)
        return 1
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
