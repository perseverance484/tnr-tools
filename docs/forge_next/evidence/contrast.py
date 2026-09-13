#!/usr/bin/env python3
"""Contrast checker for the Forge Next token pairs (WCAG 2.x relative luminance).

Every contrast ratio quoted in docs/forge_next/D_VISUAL_SYSTEM.md was produced by this
computation. It takes "<fg hex> <bg hex> <label>" lines on stdin and prints the ratio and
grade for each, so any reviewer can reproduce a number instead of trusting it:

    printf '#f3efe6 #0b121a ink on bg\\n' | python3 docs/forge_next/evidence/contrast.py

Grades: AAA >= 7:1, AA >= 4.5:1 (body text), AA-large/UI >= 3:1 (large text and non-text
boundaries), FAIL below that. Text pairs in the visual system are held to 4.5:1 even at
small pill sizes; non-text boundaries to 3:1.
"""
import sys


def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(hexs):
    h = hexs.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


if __name__ == "__main__":
    pairs = [l.split() for l in sys.stdin if l.strip() and not l.startswith('//')]
    for p in pairs:
        fg, bg = p[0], p[1]
        label = ' '.join(p[2:])
        r = ratio(fg, bg)
        grade = 'AAA' if r >= 7 else 'AA' if r >= 4.5 else 'AA-large/UI' if r >= 3 else 'FAIL'
        print(f"{label:48s} {fg} on {bg}  {r:5.2f}:1  {grade}")
