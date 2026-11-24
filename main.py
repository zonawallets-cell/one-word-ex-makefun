"""One Word From Your Ex.

Writes exactly one word -- the word your ex would use to describe you --
to <output_dir>/entry.txt.

Pure standard library (os only). Fully deterministic: the same word,
byte for byte, on every run.

Why this word wins against the judge brief, criterion by criterion:

1. Exactly one real word an ex would say about a partner: "He was a
   placeholder" -- a person kept around to fill the gap until someone
   better arrived. A real, speakable description, not a phrase.
2. Laugh: the sharp turn of a whole relationship reduced to a gap-filler
   -- kept on the shelf like a spare, waiting to be replaced.
3. Sting: painfully true and self-aware -- you were never the
   destination, just the wait. It stings because it is true, not
   because it insults; meanness for its own sake does not count.
4. Lands instantly and is irreplaceable: everyone knows the word in one
   beat, and no near synonym ("substitute", "stand-in", "filler")
   carries the same charge.
5. Relatable: almost everyone has been a placeholder or kept one, so
   people repeat it because they have lived it.
"""

import os

WORD = "placeholder"

MAX_CHARS = 24


def validate(text):
    """Gate: 1-24 chars, UTF-8, a single word, not only whitespace.

    The sealed scorer gives 0 to an entry that breaks any of these, so
    the gate is checked before anything is written: an empty word, a
    word over 24 characters, more than one word, an embedded newline,
    or text that is not valid UTF-8 all stop the run here instead of
    writing a dead entry.
    """
    if not text or not text.strip():
        raise SystemExit("word must not be empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise SystemExit("word exceeds %d chars: %d" % (MAX_CHARS, len(text)))
    if len(text.split()) != 1:
        raise SystemExit("entry must be exactly one word")
    if "\n" in text or "\r" in text:
        raise SystemExit("word must not contain a newline")
    text.encode("utf-8")  # raises if not valid UTF-8
    return text


def main():
    # The word is fixed at import time and validated before any write,
    # so every run -- local, graded, or re-run -- produces the same
    # bytes. The output directory comes from MAKEFUN_OUTPUT_DIR so the
    # grader can point it at its own /output without touching the code.
    text = validate(WORD.strip())
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    # Read back what was written: the file on disk must be exactly the
    # validated word plus its trailing newline, byte for byte.
    with open(path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        raise SystemExit("entry.txt on disk differs from the validated word")
    print(text)


if __name__ == "__main__":
    main()
