# Director prompt: village bloodline scroll icons

- **For:** the art director, to paste into a generation session
- **Brief:** `docs/handoffs/VILLAGE_BLOODLINE_SCROLL_ICONS_ART_REQUEST.md` (RUL-2026-10-20-005)
- **Status:** approved for main by dauntless, 2026-10-20
- **Live-game requests/writes:** 0

~~~text
You are the art director's generation session for The Ninja RPG. Task: six new item icons for the
village bloodline scrolls.

Read first (repo perseverance484/tnr-tools, branch main):
- docs/handoffs/VILLAGE_BLOODLINE_SCROLL_ICONS_ART_REQUEST.md  (approved brief, RUL-2026-10-20-005)
- docs/workflows/ISOLATED_ART_GENERATION.md                     (one asset per session, P0 gates)
- skills/producing-tnr-art/data/25x_DATA_art_spec.json, target ICON

What to make: one closed handscroll silhouette for all six scrolls (Oblivion Seal, Shinseina Ki,
Arashima, Taiyo Kami, Aerathiel, Hyouga Yui). Each is told apart only by its palette, cord and one
element effect, as given in section 4 of the brief. No text, kanji, symbols or glyphs anywhere.

How:
1. Start with icon 1, Oblivion Seal. One image per session. Attach
   art/crafting_caches/icon-shinobi-tool-pouch.webp as a style/material reference only. Use the
   section 6 style clause, negative and subject line, and a transparent background (otherwise a
   lime #00FF00 key; use magenta #FF00FF for the green Shinseina Ki scroll).
2. Show icon 1 to the director and wait. Its approval locks the style and the scroll silhouette.
3. Make icons 2-6 one session at a time, each with the tool pouch plus approved icon 1 as
   references. Pass no other images: not the current shared scroll icon, and not the Bloodright
   glyph art.
4. Raw QC before handing anything back: square; one complete closed scroll; no writing, symbols or
   glyphs; no halo or glow disc; not sitting on a surface; background flat or transparent. Two
   wrong-subject results in one session means close it and start clean.

Deliver: each approved original under its exact section 2 filename
(icon-village-scroll-<slug>.webp; a correction gets _b, _c), plus a ledger row per file (filename,
type ICON, pixel size, bytes). Do not upload anything to the game. Intake, preflight and the
review-desk ticket happen afterwards in the studio.
~~~
