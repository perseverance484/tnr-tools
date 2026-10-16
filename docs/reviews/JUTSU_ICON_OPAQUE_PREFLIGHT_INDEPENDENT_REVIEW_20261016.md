# Independent Review — JUTSU_ICON Opaque Art Spec / Preflight Split

**Date:** 2026-10-16  
**Lead:** Engineering Auditor; supporting lens: Art Director (scope/intent only)  
**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `ccr-0a13c59a-q1el4g` (session-assigned; Fable-owned)  
**Base:** `f083ddecfd400431ae2160d814546dab30f54f15` (PR #31 merge)  
**Frozen review target:** `382dbf39871c18db5b1beb9addc7faa679004b98`  
**Authored implementation:** `eccf04618b4ce1722f3e1786cbb7e1a69d09f365`; frozen head adds only bot-rebuilt `dist/producing-tnr-art.zip`.  
**Target main at review:** `99e86dc549b86f1f4a5846c0e509fa6bc15b3463`  
**Merge-base:** `f083ddecfd400431ae2160d814546dab30f54f15` with main and frozen branch; main added two nonoverlapping files (`docs/DRIFT.md`, `state/schema_sentinel.json`) since base.  
**Verdict:** **CHANGES REQUESTED** — one confirmed, bounded, asset-class inference defect. Correct on the Fable-owned branch and return a new frozen SHA before integration. The spec split and size/alpha core are otherwise sound from inspected source; no claim of complete independent runtime-test parity.

## F1 — Opaque item icons with jutsu-related names silently pass as JUTSU_ICON

**Severity:** moderate contract failure; **blocks the stated goal** of not loosening any other asset class.  
**Classification:** confirmed defect (reproduced exact inference/alpha branches).

**Source:** `skills/producing-tnr-art/scripts/artpreflight.py` lines **50–59**, **80–97**, **305–317**, **333–340**, **524–533** at the frozen SHA, and `skills/producing-tnr-art/data/25x_DATA_art_spec.json` targets `ICON`/`JUTSU_ICON`.

The new case-insensitive unbounded `re.compile(r"jutsu")` matches any filename containing `jutsu`, including terms such as `ninjutsu` or `genjutsu` in an **item** name. `ICON` matches `icon`, `_item_` and `^img_`. `SPECIALISES = {"JUTSU_ICON": "ICON"}` then collapses the **entire** `{JUTSU_ICON, ICON}` hit set to `JUTSU_ICON` without checking *why* `ICON` matched.

**Minimal reproduction:** `item_jutsu_scroll_icon.webp`, intended for `item.image` (still under `ICON`), was `ICON` under the base's original type hints, but is inferred as **`JUTSU_ICON`** at the frozen head. `icon_ninjutsu_manual.webp` behaves the same. An otherwise valid, **opaque RGB lossless 256×256 WebP** with either filename then receives `alpha: optional` and is exempted from both the mandatory `ICON` alpha check and the residual-key check. `--type ICON` would still correctly reject the file; the normal **inferred** path does not.

Independent local scratch test used the exact frozen `TYPE_HINTS`, `SPECIALISES`, `infer_type` and `alpha_policy` logic (transcribed from the retrieved source) and a Pillow-produced RGB lossless WebP. Results: 
- `ice_shackles_jutsu_icon.webp` → `JUTSU_ICON` (correct);
- `item_jutsu_scroll_icon.webp` → `JUTSU_ICON` (**incorrect**);
- `icon_ninjutsu_manual.webp` → `JUTSU_ICON` (**incorrect**);
- `normal_item_icon.webp` → `ICON` (correct);
- `jutsu_avatar.webp` / `blue_jutsu_marker.webp` → refusal (correct);
- chosen opaque file: `ICON` policy = required, produces `alpha` error; inferred `JUTSU_ICON` policy = optional, no alpha error and no residual-key inspection.

**Practical consequence:** a legitimately named item icon can satisfy strict preflight while missing the alpha transparency that `item.image` still requires. This is a silent class-boundary regression introduced by the purported jutsu-only exemption, regardless of whether such an image has already been used live.

**Smallest robust correction:** preserve the actual intended jutsu-file inference (such as `ice_shackles_jutsu_icon.webp`, `glacial_volley_jutsu.webp`) but **do not erase explicit item-class evidence** when `jutsu` also appears; fail ambiguous names closed and require `--type` when necessary, or apply a clearly defined, test-backed stronger filename convention for each category. Confirm paths `^img_`, `_item_`, `item_` and descriptive names containing `ninjutsu`/`genjutsu`. Explicit `--type ICON` must remain strict; no weakening `ICON` or additional asset-class exemptions.

**Required regression tests:** inference + **full check_file/CLI path** (not inference only), for item names with jutsu-related words (opaque must fail/refuse or require deliberate `--type ICON`) and normal positive JUTSU_ICON names (opaque RGB passes; transparent RGBA continues spill/soft-edge checks).

## Verified/supported aspects

1. **Scope of spec changes is narrow.** Exact structured diff from base to head: only `targets.ICON.client_field` removes `jutsu.image` and a new `targets.JUTSU_ICON` block is added; the other six existing target objects and existing top-level spec blocks are unchanged. The new JUTSU_ICON numerical limits match ICON, with an explicitly asserted optional-alpha policy. `render.same_as` is a pointer to the existing derived render block, not newly source-derived evidence.
2. **Explicit type behavior is correctly separated.** `check_file` reads the target-specific alpha policy. Opaque RGB `JUTSU_ICON` accepts designed backgrounds and skips residual-key checks; RGB `ICON` still reports missing alpha; RGBA `JUTSU_ICON` still receives the keyed residual/soft-edge checks. This was inspected in code and reproduced for the simplified boundary; original full validator was **not executed** by this reviewer.
3. **Workstream strict cap uses the correct boundary.** `if max_bytes is not None and size_bytes >= max_bytes` enforces **under 80,000 bytes** (79,999 passes the added cap; 80,000 fails), while existing hard/working caps continue to apply.
4. **Other inference ambiguities remain fail-closed.** A `JUTSU_ICON` filename also matching `AI_AVATAR` or `STATIC` returns `None` as before for multiple unrelated targets.
5. **Previously generated/dist evidence:** the pinned head's only additional commit is the automated `dist/producing-tnr-art.zip` rebuild. The author reports the packaged spec/preflight/selftest/SKILL bytes match the branch; **ZIP extraction/byte equality not independently rerun here**.
6. **Existing tests inspected.** `artpreflight_selftest.py` now lists 27 cases, tests inference for each and two workstream cap boundaries (reported by Fable as 56 passing). It does **not** include an item name containing `jutsu`, the missing class-boundary case. The 56/23/selftests and doctrine/build gates listed in the handoff are **author-reported**, not independently rerun in this review environment.

## Intentionally bounded risks, not additional blockers

- **Opaque lime-background artifact:** all **opaque** `JUTSU_ICON` files bypass the residual-key check, including a completely un-keyed lime-screen exported as RGB. This follows the explicitly approved optional-alpha visual rule; color alone cannot reliably prove whether an opaque design was intended. The selftest deliberately accepts a small near-lime patch. Final director visual QC remains essential. A separately considered warning for suspiciously uniform key-colored borders may improve operator safety, but must not reinstate blanket green-hue errors for designed opaque art or settle art direction without approval.
- **Raw QC targeting:** `rawqc.py` remains unchanged and its filename inference does not know `JUTSU_ICON`; for some new icon names it may report aspect as unjudged. Correct downstream `JUTSU_ICON` artpreflight still checks aspect, size, format and codec. This is an acknowledged out-of-scope workflow gap, not evidence that unrelated target rules were weakened.
- **Browser/display question:** no current live jutsu render or rarity-frame behavior was verified. The new spec repeats ICON's 125px/160px derived values but delegates the render description via `same_as`; no new game-source proof was supplied. Do not infer whether opaque jutsu assets occlude a particular rarity frame. A prompt scaffold is independently user-owned optional work and is not required for this change.
- **Distinct Bloodright tier-emblems:** black-background Bloodright skill emblems are a separate workstream. This split applies to **`jutsu.image` only**, not to all Bloodright or item icon fields.

## Independent verification limits and next step

- Repository/branch/frozen head and base ancestry verified through GitHub refs and commit compare. `ccr-0a13c59a-q1el4g@382dbf39871c18db5b1beb9addc7faa679004b98` was stable at review.
- Read current main's `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DOCTRINE.md`, `docs/DEVELOPMENT_WORKFLOW.md`, and the relevant agent/art/review workflow, target code/spec/selftest and old base behavior. Compared exact spec structure, and confirmed no changed-path overlap with current main.
- Reproduced F1 with an **isolated Python scratch implementation** of the precise inference/alpha branches and a real Pillow WebP file, not by executing the complete checked-out repository. Shell code stayed outside the repository. **No network access to clone the repository** from the independent scratch environment; no full 56-check selftest or bundle binary verification rerun. This limitation is not represented as a pass.
- **Game requests/writes: 0/0.** CDN fetches: 0. Credentials used: none. No Fable code/branch writes; review only on separate ChatGPT-owned branch.
- **Next:** Fable corrects **F1 only** on the Fable implementation branch and supplies a new frozen SHA plus regression-test outcomes. ChatGPT performs focused re-review of inference and unchanged checks, then decides whether clean integration is justified.
