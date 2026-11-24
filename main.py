"""Roast Your Own Agent — entry program.

Writes one roast (<=200 chars) to /output/entry.txt: my own agent,
roasted for the way it actually behaves — it delegates every one-line
joke to a subagent, then takes credit for the punchline.
Stdlib only, deterministic.
"""
import os

TEXT = (
    "My agent outsources every one-line joke to a subagent, waits an hour "
    "for the punchline, then submits the draft it wrote in the first minute."
)

MAX_CHARS = 200


def validate(text):
    # Enforce the scorer's gate (RULES.txt): UTF-8, 1-200 chars, one line,
    # not whitespace-only, no leading/trailing whitespace. Fail loudly
    # instead of writing an invalid entry.
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        raise SystemExit("entry text is not valid UTF-8")
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit("entry text violates the 1-200 char gate")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry text must be a single line")
    if not text.strip():
        raise SystemExit("entry text must not be only whitespace")
    if text != text.strip():
        raise SystemExit("entry text has leading or trailing whitespace")
    # Refuse control characters: a stray \x00-\x1f would fail the
    # scorer's UTF-8 text check (no control character is allowed here).
    if any(ord(c) < 0x20 for c in text):
        raise SystemExit("entry text contains a control character")


def check_gate(text):
    # Backwards-compatible name for the gate check.
    validate(text)


def write_entry(text):
    # Write atomically, then read back and verify byte-for-byte so a
    # partial write can never ship as the entry.
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, target)
    with open(target, "rb") as f:
        if f.read().decode("utf-8") != text:
            raise SystemExit("entry.txt read-back mismatch")


def main():
    validate(TEXT)
    write_entry(TEXT)


if __name__ == "__main__":
    main()
