"""Read player-facing text out of docs/design/SKYGLASS_TEXT.md, verbatim (the file says: "Generators copy from here;
they do not paraphrase").

    block("item:Tide Chart.description")      -> the fenced block (or inline code) under that target heading
    table("### 5.1 The 12 Skyglass variants")  -> the first markdown table after that heading, as lists of cells

Cells keep their text with surrounding backticks removed. Nothing here invents or edits wording; a missing target is
an error, never an empty string.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_PATH = os.path.join(ROOT, "docs/design/SKYGLASS_TEXT.md")
_LINES = None


def lines():
    global _LINES
    if _LINES is None:
        _LINES = open(TEXT_PATH, encoding="utf-8").read().split("\n")
    return _LINES


def block(target):
    """The text for `target`: the fenced block that follows the `**`target`**` heading line, or the inline code on
    the heading line itself (`**`target`**: `text``)."""
    L = lines()
    head = "**`" + target + "`**"
    hits = [i for i, l in enumerate(L) if l.startswith(head)]
    if len(hits) != 1:
        raise KeyError(f"SKYGLASS_TEXT.md: {len(hits)} headings for {target!r}")
    i = hits[0]
    rest = L[i][len(head):]
    m = re.match(r"\s*(?:\([^)]*\))?\s*:\s*`(.*)`\s*$", rest)
    if m:
        return m.group(1)
    j = i + 1
    while j < len(L) and not L[j].startswith("```"):
        if L[j].startswith("**`"):
            raise KeyError(f"SKYGLASS_TEXT.md: no block under {target!r}")
        j += 1
    k = j + 1
    while k < len(L) and not L[k].startswith("```"):
        k += 1
    if j >= len(L) or k >= len(L):
        raise KeyError(f"SKYGLASS_TEXT.md: unterminated block under {target!r}")
    return "\n".join(L[j + 1:k])


def choices(target):
    """The `- `choice[n]`: `text`` bullets under a dialog target, in order."""
    L = lines()
    head = "**`" + target + "`**"
    i = next(i for i, l in enumerate(L) if l.startswith(head))
    out, j, seen_block = [], i + 1, False
    while j < len(L):
        l = L[j]
        if l.startswith("**`") or l.startswith("#"):
            break
        m = re.match(r"- `choice\[(\d+)\]`: `([^`]*)`(?:\s+\([^)]*\))?\s*$", l)
        if m:
            out.append(m.group(2))
        j += 1
    return out


def _cells(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return [c[1:-1] if len(c) >= 2 and c[0] == "`" and c[-1] == "`" else c for c in cells]


def table(heading, after=None):
    """Rows (without the header and rule) of the first table after the line starting with `heading` (and, if given,
    after the first later line starting with `after`)."""
    L = lines()
    i = next(i for i, l in enumerate(L) if l.startswith(heading))
    if after:
        i = next(j for j in range(i, len(L)) if L[j].startswith(after))
    while not L[i].startswith("|"):
        i += 1
    rows = []
    i += 2  # header + rule
    while i < len(L) and L[i].startswith("|"):
        rows.append(_cells(L[i]))
        i += 1
    return rows
