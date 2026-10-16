# Blood-Enchanted Eyes — Eight-Jutsu Showcase Readiness

**Status:** PREPARED / **SHOWCASE NOT READY** (2026-10-15).  
**Workstation:** `chatgpt/bee-jutsu-art-studio-20261014`.  
**Workflow owner:** `docs/workflows/JUTSU_ICON_SHOWCASE.md`.  
**Reference layout:** director-provided 2 x 4 BBE screenshot `1000018422.png` (layout only; source is JPEG despite extension, 1536 x 854). See workflow for exact hash and framing rules.  
**No live requests or writes. No production upload.**

**Roster-size scope:** this preparation document is **BEE-specific**. Blood-Enchanted Eyes happens to have **eight** jutsu in the pinned historical roster, so its showcase uses the BBE-style **4 + 4** layout. **Do not generalize that count, grid, or 1536 x 854 canvas to other bloodlines.** Many A-rank bloodlines have five jutsu; S-rank rosters vary. Future bloodline studios determine N from their own verified jutsu roster and follow the adaptive procedure in `docs/workflows/JUTSU_ICON_SHOWCASE.md` (e.g. **3 + 2 centered** for five, pending director acceptance).

## Intended final presentation

For BEE's verified eight-jutsu roster specifically, a landscape **1536 x 854** contact sheet of exactly **eight** currently accepted BEE jutsu icons, **four square tiles per row**, on a plain dark navy/charcoal background. Each icon gets one label directly below: `<Approved jutsu name> <actual WebP size in decimal kB to one decimal>`. No title banner, decorative border, rarity card, guessed bytes, weapons/character embellishments, or image-generation changes to existing art.

**Frozen row-major display order**, following the BEE historical jutsu roster rather than the order the artworks happened to be generated:

| Position | Jutsu | Current raw approval at preparation | Accepted source (SHA-256 prefix) |
| --- | --- | --- | --- |
| R1C1 | Ring of Spilled Blood | APPROVED | `1000018474.png` (`a686b372`) |
| R1C2 | Crimson Tithe | APPROVED | `1000018475.png` (`eeae4826`) |
| R1C3 | Sanguine Plague | APPROVED — corruption front | `1000018488.png` (`4a48079a`) |
| R1C4 | Reaper's Embrace | APPROVED — scythe | `1000018481.png` (`0b972708`) |
| R2C1 | Unholy Enhancement | **OPEN — not approved** | Previous `1000018480.png` withdrawn; latest `1000018490.png` needs rework |
| R2C2 | Crimson Impact | APPROVED | `1000018482.png` (`85617e35`) |
| R2C3 | Hemocure | APPROVED — vitality bubble | `1000018489.png` (`bdb157eb`) |
| R2C4 | Thousand Strike | APPROVED — needle storm | `1000018487.png` (`6a6fead5`) |

**Decision to preserve:** director disliked Unholy Enhancement's previous upward power eruption because of confusion with Crimson Impact; current replacement target is savage, broken radiating waves with intentional broad shadow wavefronts, **not** lumps/debris, smooth vitality-bubble arcs or an explosion. The latest rework `1000018490.png` (conversation JPEG RGB 1536 x 1536, 426,476 bytes, SHA-256 `27069f2d73dfaa76332dae0f953d2e6c113b6c3f492324f231559b0337e422bf`) received critical director feedback on its shadow anatomy; **not approved**, not a style reference. This attachment's received-byte metadata is recorded here as review evidence; the actual binary is conversation-bound, not Git-pinned.

## Final showcase gate — current facts

| Gate | Current state | Needed |
| --- | --- | --- |
| Raw visual approvals | **7/8** | Director accepts a replacement Unholy Enhancement candidate |
| Exact accepted originals | 7 received as conversation files, SHA-256 in `SOURCE_EVIDENCE.json`; not Git-pinned | Reattach/read exact 8 current sources at production; hash-check |
| Final 256px exports | **0/8 current-revision WebPs verified in studio** | Process each approved original per current art spec, version filenames, record bytes/hash/codec |
| Historical processed file | Old Ring `icon_bee_ring_of_spilled_blood_v1.webp` exists as prior-version evidence only | Exclude it from current final family and size captions |
| Small-size family comparison | Individually reviewed informally; **no final processed 125/64/32 family QC** | Side-by-side processed icons at 125/64/32 and confusion checks |
| Shared ICON alpha preflight | **Known unresolved contract mismatch** for intentionally opaque jutsu artwork | Run/report actual gate; do not treat as green or fake transparency |
| Labeled showcase + manifest | **NOT GENERATED** | Deterministically composite from final WebPs after N/N approvals/export QC |
| Whole-set director signoff | **NOT REQUESTED** | Show final 2 x 4 with verified names and file sizes; request explicit family acceptance |
| Final package / live | **NO final package, NO live action** | Separate export package, QC/readback as authorized; user controls upload |

The old BBE reference montage is an example of **showcase presentation only**. Its pictured icon art and reported file sizes are not BEE inputs or evidence that BBE had eight final accepted files; its own closeout documents an unfinished revision. Never borrow the blue crystalline rendering for the red BEE family.

## Final workstation closure action

Once the last Unholy image is approved, the Art Studio should:

1. Re-open this readiness ledger and current `SOURCE_EVIDENCE.json` at live verified SHAs; update the roster to **8/8 current raw approvals**, not older superseded visuals.
2. Intake/process/hash **eight current versions**, inspect their WebPs at 125/64/32 and record all per-file codec/byte/preflight results.
3. Compose `bee_jutsu_icon_showcase_v1.png` and `bee_jutsu_icon_showcase_v1.manifest.json` in **BEE's eight-only 4 x 2 layout**, with actual processed byte-derived captions.
4. Show the complete family to the director for explicit **showcase-level acceptance**; rework and rebuild if any icon is confusing, missing or mislabeled.
5. Record the accepted showcase image/manifest SHA-256, exact 8-input archive or ZIP integrity, export/QC verdicts and unresolved upload contract issue in a family closeout document. **A showcase approval is not preflight clearance or live publication.**

**Ownership boundary:** Art Studio may design/review/produce the composite from accepted data; any new generalized showcase builder/script or validator change is separate Lane A implementation, normally Fable-owned and independently reviewed.
