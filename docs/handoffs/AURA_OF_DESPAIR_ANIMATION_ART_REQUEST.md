# Art request: Aura of Despair field animation layers

- **For:** the art director (Art Director role, then Image Production)
- **From:** Fable / Claude, at dauntless's request (2026-10-26)
- **Status:** PROPOSAL. Direction (section 3) awaits director approval before any generation.
- **Companion:** `HELLFIRE_HARVEST_ANIMATION_ART_REQUEST.md`. Same Rider, same route, same intake; the two must read as
  one boss but never as the same move.
- **Jutsu:** Aura of Despair `N8V10pCnF7sEdrRs-mIdG`, equipped on the Headless Rider (`eaMN5CfciNlxfezSKemJ6`): target
  GROUND, method AOE_SPIRAL_SHOOT, range 5, cooldown 5, 100 AP (his whole turn). Effects (push/262 read):
  enemies on the tiles pay +100% pool cost for 4 rounds and take +30% damage for 4 rounds; the Rider takes 40% less
  damage for 2 rounds. His rule 3 (after Candle Lit Aura and Hellfire Harvest).
- **Style reference (attach, style only):** `art/halloween_headless_rider/headless_rider_avatar.webp`, his lantern in
  particular. Scene palette: `headless_rider_horror_04_river.webp`.
- **Roles, protocol, spec:** as the Hellfire Harvest request (art director paints layers; Claude Code animates by script;
  one layer per fresh session; `STATIC` and `ANIMATION` targets). **Live-game requests/writes:** 0.

## 1. What it uses now

| Slot | Current | Problem |
|---|---|---|
| appear, static loop and disappear | one unindexed animation `yCPTIR4Kk-sopCgSYZVeR` in all three slots | the same clip at cast, on loop and at the end, so nothing marks the field starting or ending |
| static tile | "Shadow Field 2" `dKEJjYMI4asyfvH9hsQUZ` | a generic dark wash, the sibling of the field Hellfire Harvest is dropping |
| appear sound | "Clear" `mOSkDnYv4hchkPbhdpTDd` | a cleanse chime on a curse |
| text | "New jutsu description" / "%user uses %jutsu on %target" | placeholders |

Only the pool-cost effect carries visuals; the damage-taken curse and the Rider's own shield show nothing.

## 2. How the game draws it

The spiral pattern marks a cluster of tiles around the target for 4 rounds. On each marked tile: the static still sits
under the units; the static loop plays continuously on top; the appear plays once at cast and the disappear once when the
4 rounds end. All at 50 px per tile (`libs/threejs/combat.ts` 610-680). So the field is a patch of the board, not the
whole board, and it has a visible start, a living middle and an end.

## 3. Direction (director to approve)

**The idea:** Hellfire Harvest is his fire. Aura of Despair is his **lantern**: cold, dead light that drains the will to
fight. Low, heavy, slow, where Hellfire is fast and bright.

**Palette:** night ink `#08080d`, grave grey `#2e2d3a`, mist bone `#cfc6b8` at low opacity, and one accent: **dull
lantern red** `#7a1a1f` to `#c3141b`, never orange. No fire, no flame shapes; that is Hellfire Harvest's.

**Appear "Lantern Spill"** (~10 frames): a lantern's glow flares at the tile centre, then a ring of black-red mist pours
outward along the ground and settles.

**Static tile "Despair Mist"** (still): low black mist pooled on the ground, a faint dull-red light under it, two or three
dark wisps; edges fade to clear so marked tiles merge into one patch.

**Static loop "Wailing Wisps"** (6-8 frames, loops): the mist rolls slowly; a pale wisp rises and, for a frame or two,
shows a hollow wailing face before it thins away. Subtle: units stay readable.

**Disappear "Gutter Out"** (~6 frames): the red light dims like a lantern running out of oil and the mist sinks into the
ground.

**Sound:** "Clear" removed from the curse; a fitting sound is requested separately (none in the current library fits).

## 4. Deliverables (each on a fully transparent canvas; nothing else on it)

| Layer | What | Size |
|---|---|---|
| **M1 MIST POOL** | the static tile: low black mist pooled on the ground seen from above, faint dull-red underlight, edges fading to clear | 1024 x 1024 |
| **L1 LANTERN FLARE** | a burst of dull red lantern light, round, soft-edged but no painted disc (rim and rays only), no lantern object | 1254 x 1254 |
| **R1 MIST RING** | a ring of black-red mist spreading along the ground, seen from slightly above, empty middle | 1254 x 1254 |
| **W1 WISPS** | 6-8 separate pale smoke wisps, mixed sizes, two of them showing a hollow wailing face, spaced apart | 1254 x 1254 |
| **D1 GUTTER** | the red underlight alone, as a soft flat glow under mist, for the dimming frames | 1254 x 1254 |

Rules as the Hellfire Harvest request: Rider-avatar pixel rendering; glow as rim light, never a painted disc or panel;
real transparency; no text, runes or symbols; faces only in W1, hollow and simple.

## 5. Intake (Claude Code)

1. Raws to `art/halloween_headless_rider/aura_of_despair/raws/`; raw QC per layer.
2. **M1** to the `STATIC` target (256 x 256 lossless, circle-safe), `artpreflight.py --type STATIC`.
3. Three strips by script (appear from L1 + R1; static loop from W1 over M1's mist; disappear from D1 + M1), 112 px
   square frames, lossless, under 460,800 bytes each, `artpreflight.py --type ANIMATION`.
4. Preview GIF: the spiral patch on a hex board over the River background, through cast, two loop cycles and the end.
5. Manifest (rides with the Hellfire Harvest art manifest): four hidden gameAsset creates in `HeadlessRiderHorror`; the
   Rider unequip; the jutsu edit (appear, static, loop, disappear on the pool-cost effect; "Clear" sound removed; real
   description and battle line); the re-equip (law 18/60, two runs).

## 6. Director decisions

1. Lantern / despair direction and the dull-red accent (distinct from Hellfire's orange).
2. The wailing faces in the loop.
3. Text: proposed description "The Rider raises his lantern and its dead light spills across the ground. Those it
   touches feel their strength drain away, and every blow lands harder." Battle line "%user raises a guttering lantern
   and dead light spills across the ground around %target."
