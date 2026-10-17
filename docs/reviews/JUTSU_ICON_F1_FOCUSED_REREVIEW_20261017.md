# Focused Re-Review — JUTSU_ICON F1 correction

**Date:** 2026-10-17  
**Repository:** `perseverance484/tnr-tools`, branch `ccr-0a13c59a-q1el4g`  
**Originating review:** `chatgpt/review-jutsu-icon-alpha-20261016@0763effd1986115a156ae8c5fdc0614565bcbebb`, finding F1 (copied verbatim to `docs/reviews/JUTSU_ICON_OPAQUE_PREFLIGHT_INDEPENDENT_REVIEW_20261016.md`)  
**Final verdict:** **PASS WITH NOTES** at frozen SHA `fe3712129c3bd86f10bdf9e7eadf2539ebd10d70`  
**Live-game requests/writes:** 0/0. **Credentials:** none.

## Process deviation (director decision)

The normal loop is a ChatGPT focused re-review. ChatGPT ran out of tokens, so dauntless directed that the work be finished without it. The focused re-review was performed instead by a **separate Claude reviewer agent**. It had no access to the author's reasoning, worked read-only from the frozen SHAs, and ran its own probes, fuzzing and gates. This is a substitute for the cross-model review, not an equivalent. Only F1 was in scope; the remainder of the original review (spec split, alpha policy, `--max-bytes`) was already verified by ChatGPT and was not re-litigated.

## Round 1 — correction `122a6f069545af84cf04a969039bd4b1e206c133` (author `0f67148`): CHANGES REQUESTED

The correction made `jutsu` a whole-token match and refused when the name carried `item`/`img_` evidence. It closed every F1 reproduction, and its new selftests failed 9/20 against `382dbf3`. But the same class-boundary hole remained:

- **F1-R1 (moderate, blocking).** The house item convention is `icon_<name>` / `icon-<name>`: all 11 tracked item icons in `art/` use it, and none carries an `item` token. So `icon_jutsu_scroll.webp`, `icon-jutsu-scroll.webp`, `icon_forbidden_jutsu_tome.webp` and `quest_icon_jutsu_seal.webp` still inferred JUTSU_ICON, and an opaque RGB file passed clean. CLI: `icon_jutsu_scroll.webp` exited 0; with `--type ICON` it exited 1 with `[alpha]`.
- **F1-R2 (minor).** Variant item markers were not treated as evidence. `items_jutsu_icon`, `scroll_items_jutsu_icon`, `item01_jutsu_scroll`, `item2_jutsu_icon`, `x_img_jutsu_icon`, `jutsu_item2`, `img-jutsu_scroll` and `jutsu_scroll item` all inferred JUTSU_ICON and passed opaque.
- **Notes:** `weapon_*`/`bloodline_*` jutsu names inferred JUTSU_ICON (bloodline recommended as evidence). Basename-only inference was confirmed consistent with base.

## Round 2 — correction `fe3712129c3bd86f10bdf9e7eadf2539ebd10d70` (author `57ae672` + bot zip rebuild): PASS WITH NOTES

**Change.** JUTSU_ICON inference is now **allow-listed** instead of deny-listing item markers. `jutsu_icon_verdict()` works as follows:

1. Strips image extensions repeatedly.
2. Splits the name on `_ - . space`.
3. Requires exactly one `jutsu` token.
4. Drops a trailing `icon` only for a `…_jutsu_icon` suffix.
5. Refuses if the remaining tokens hit any `TYPE_HINTS` pattern, or contain `item|img|icon|bloodline` anywhere.

An ambiguous result returns None and never falls through. `SPECIALISES` was removed. The spec is unchanged (`git diff --quiet 382dbf3 fe37121 -- …/25x_DATA_art_spec.json` exits 0). `check_file`, `alpha_policy`, the residual-key check and `--max-bytes` are not in the diff.

**Verification by the reviewer:**

- Every F1, R1 and R2 reproduction now refuses (`[type]`), or stays ICON with `[alpha]` (`icon_ninjutsu_manual`).
- Valid names still infer JUTSU_ICON and pass opaque: `ice_shackles_jutsu_icon`, `glacial_volley_jutsu`, `arctic-frost-jutsu`, `Ice.Shackles.Jutsu`, `fire_jutsu_v2`, `jutsu`, `ice shackles jutsu`.
- **Fuzz, 300,000 random names:**
  - inference is identical to base `f083dde` for every name without a `jutsu` token;
  - 0 inferred JUTSU_ICON names carry `item`, `img` or `bloodline`, or `icon` outside the trailing suffix;
  - no `jutsu`-token name infers any target other than JUTSU_ICON.
- **Selftest at fe37121:** 98 passed, 0 failed, exit 0. **The same selftest against the 122a6f0 validator:** 80 passed, 18 failed. All 14 R1/R2 inferred cases and the 3 new CLI cases fail, so the tests detect the defect.
- **Explicit types unchanged:**
  - `--type ICON` on an opaque file exits 1 with `[alpha]`;
  - `--type JUTSU_ICON` on an opaque file exits 0;
  - keyed jutsu icons still get `[spill]`/`[soft_edges]`;
  - the `--max-bytes` boundary holds: a file of N bytes fails at N and passes at N+1.
- The dist zip's spec, `artpreflight.py`, selftest and `SKILL.md` are byte-identical to the branch.
- **Gates at the fe37121 worktree root:**

  | gate | exit | result |
  |---|---|---|
  | `doctrinemap.py .` | 0 | 0 errors / 0 warnings |
  | `render_doctrine.py --check` | 0 | all projections current |
  | `build_packs.py --check` | 0 | all packs and TOCs current |
  | `lawmap.py .` | 0 | 0 errors / 5 warnings |

  The 5 lawmap warnings (16d, 18, 37, 61, 69) are identical at base.
- **Author-side check:** all 133 tracked images in the repository infer the same target as at base.

**Notes (non-blocking):**

- **N1.** Item-like words that are not class markers still allow-list: `forbidden_jutsu_scroll`, `jutsu_scroll`, `weapon_jutsu_icon`, `reward_jutsu_chest`. These cannot be told apart from jutsu names (`kunai_jutsu`) without a vocabulary list. Inference is a convenience and `--type` is authoritative. Item icons should follow the `icon_<name>` convention (which now refuses) or be run with `--type ICON`.
- **N2.** Fail-closed side effect: jutsu names containing another target's hint now refuse and need `--type`, for example `spinning_blade_jutsu` (`pin`), `animal_summon_jutsu` (`anim`), `silicon_jutsu` (`icon`) and `portrait_jutsu`. This is the safe direction and was judged acceptable.
- **N3.** `ISOLATED_ART_GENERATION.md` says "`<name>_jutsu[_icon]` style". The code also accepts a leading `jutsu_<name>` token. This is cosmetic; `SKILL.md` states the exact rule.

**Not verified:** `rawqc.py` (out of scope); browser, live-game, CDN and rarity-frame behaviour.

## Integration

Integrated into `main` via PR at head `fe37121` plus this docs-only review-record commit. The skillpack workflow is not triggered by `docs/**`, so the reviewed code and the bundle are unchanged by the record commit.
