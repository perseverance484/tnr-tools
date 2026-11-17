# Studio sessions, jutsu-icon families and art lookup

Condensed routing for the ruling-backed art workflows. The full protocols stay authoritative:
`docs/workflows/ISOLATED_ART_GENERATION.md` (P0 A-F gates, RUL-2026-10-19-003),
`docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md` (ZIP-first, RUL-2026-10-17-020/021),
`docs/workflows/JUTSU_ICON_SHOWCASE.md` (deterministic gallery), `docs/workflows/JUTSU_ART_LOOKUP.md`,
`docs/workflows/ART_PRODUCTION.md` (general flow and live boundary). Change those only with a director ruling.

## Two kinds of session

| Session | Does | Never does |
|---|---|---|
| **Studio** (persistent) | reads repo state, keeps the register and ledger, writes one brief per asset, intakes, processes, QCs, packages, records | generate images, change accepted art, touch the live game |
| **Isolated generation** (new conversation per asset) | one brief + at most two individual reference images, one candidate at a time, director approval, returns the original | other assets, sheets or collages, processing, publishing |

Two wrong-subject results in one generation conversation: close it and restart clean. Never feed rejected images or
a contact sheet back as conditioning. Pass the actual image bytes; a URL or filename proves nothing.

## Jutsu icons (`JUTSU_ICON` target)

- **Target lock before rendering:** exact bloodline and jutsu id and name, what the technique does, one dominant
  silhouette, camera and motion axis, one secondary effect, every sibling's reserved silhouette as an exclusion, and the
  role of each reference (identity, style or material only, true subject). Composition first, palette second.
- **Fail fast on pixels:** reject wrong technique, generic effect or wrong camera before asking the director. Check at
  125, 64 and 32 px.
- Designed opaque backgrounds are allowed (RUL-2026-10-14-001): never key them, never fabricate alpha.
- Style exemplars: `scripts/style_refs.py select --target JUTSU_ICON [--family BBE|BEE]`, style or material only.

### ZIP-first family studio (`scripts/jutsu_studio.py`)

```
python3 scripts/jutsu_studio.py doctor                                  # can this runtime run the pinned preflight?
python3 scripts/jutsu_studio.py intake PACK.zip --out WORK/intake [--roster roster.json]
python3 scripts/jutsu_studio.py lock-check locks.json
python3 scripts/jutsu_studio.py attempts attempts.json --locks locks.json
python3 scripts/jutsu_studio.py compare candidate.png sibling1.png sibling2.png --out cmp.png  # 125/64/32
python3 scripts/jutsu_studio.py finalize approved.json --out DIR --locks locks.json --attempts attempts.json
python3 scripts/jutsu_studio.py audit-gallery gallery.png --manifest gallery.json --exports DIR
```

N is the verified roster, not the ZIP's file count; an ambiguous id match is `MAPPING_REQUIRED` (ask, never guess).
The orientation index is studio-only, never a generator reference. `finalize` always runs `artpreflight.py --type
JUTSU_ICON`; the verdict is **canonical** only when the script and spec match `data/preflight_pins.json`. With
mismatched pins it still runs and reports **NON_CANONICAL** when the checks pass (FAIL when they fail). **NOT_RUN**
means the preflight did not execute (script or dependency missing, per `doctor`, or skipped by `--stop-after export`). Keep the three states distinct in every report.
Opening prompt for a new family: `docs/design/jutsu_icon_studio/START_PROMPT.md`.

## Finding existing art

```
python3 scripts/jutsu_art.py verify                 # repo root; always first
python3 scripts/jutsu_art.py lookup "Name" [--json]
python3 scripts/jutsu_art.py image-url "Name"
python3 scripts/jutsu_art.py search fang [--all]
```

Exact normalized names only; a miss lists suggestions it never selects. For live records use the TNR connector with
`select` (for example `jutsu.getAll {name}` then `gameAsset.get {id}` for a clip's name, frames, speed and host).

## Art requests to an outside art partner

Write the brief in `docs/handoffs/<NAME>_ART_REQUEST.md`, then give the director one copy-ready prompt that points at
it. Ask for painted sources (layers or key poses on a 1254 px transparent canvas) rather than finished sheets, state
palette hexes, sizes, what must not appear, and how the pieces will be assembled. Intake returned ZIPs into their own
empty folder, read their HANDOFF note, then copy the sources into the repo's `art/.../raws/`.
