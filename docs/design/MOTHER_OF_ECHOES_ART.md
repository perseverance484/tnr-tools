# The Mother of Echoes: complete art list

- **For:** the director (generation) and Fable (code-built FX, intake, upload manifests). **Prompts:** `docs/handoffs/MOTHER_OF_ECHOES_ART_PROMPTS.md` (codes ME01-ME28).
- **Character and visual bible:** `docs/design/SAYO_BIBLE.md` (DRAFT, pending director approval): who Sayo is, her chakra nature, the six move families as visual grammar, per-move animation specs with an art3 audit, and the palette and consistency rules every new strip is checked against.
- **Records:** ids from the committed results bundles (417, 440, 461-464), collected in `docs/handoffs/mother_of_echoes_record_ids.json`. Art slots: `artPlaceholders` in `harness/skyglass_wreck_sim/mother_of_echoes_spec.json` at `fable/mother-of-echoes-sim@dd7e33ab` (the generator's `SPEC_REF`).
- **Canon:** RUL-2026-11-01-093..095, RUL-2026-11-02-108 (names); cut and not drawn: An Invitation in Glass, Remnant of the Mother Glass, all Salvage art (RUL-2026-11-02-104/-105).
- **Delivery (art QA 2026-11-04):** every strip is delivered at 50 px wide (`primitives/animation.ts` rendition 50, `utils/image.ts` `?width=50`) and pixi stretches it ~3.3x with LINEAR filtering (`combatEffects.ts` never passes nearest). Draw on the 50 px grid in solid 2-3 px clusters with dark outlines; 1 px dithers become haze. Appear and static loops start together; the client never plays `disappearAnimation` (the server spawns it as a visual).
- **Renderer** (theninjarpg@3314d122, pixi, `libs/rendering/scenes/combatEffects.ts`): one square sprite per effect per hex, `tile.height * EFFECT_ANIMATION_HEX_RATIO` (2.5), drawn over the fighters; `staticAssetPath` is stretched to the hex box under them. Marks ride the non-visual `increaseregeneration` carrier (RUL-2026-11-02-101). `docs/design/SKYGLASS_BOSS_ANIMATIONS.md`'s three.js section is stale on this point.
- **Live-game requests:** 0. Nothing here is uploaded; uploads and the record edits are a separate push built after approval.

## Counts

| | director | code | reuse live | total |
|---|---|---|---|---|
| P1 | 18 | 5 | 7 | 30 |
| P2 | 9 | 7 | 1 | 17 |
| P3 | 1 | 1 | 0 | 2 |
| **all** | 28 | 13 | 8 | **49** |

P1 = must have before push/465 publishes; P2 = nice (a placeholder or nothing shows meanwhile); P3 = optional.
"code" rows are built in this repo with Pillow (`art/mother_of_echoes_fx/build_fx.py`); None reuses the Crowned Captain's or the crew's strips (`art/skyglass_boss_fx`): the director keeps those for their own live moves (2026-11-03), so stillness, breathless, lucid, likeness and worn are the uber's own. Every code-built file is already exported and preflighted.

## Recommendation: Sayo is one design in three looks

One design, three files. ME01 (Act I) is generated first and locks her face, build, coat and lancet; ME03 (Act II) and ME04 (Act III) attach the approved ME01 as SUBJECT and change only what each act says (the glass climbs and is etched; then it goes dark and the feelers take her). Players see the same woman change across the fight, which is the story (RUL-094: she succumbs to the Silence), and the act boundary still reads at a glance. One shared file would hide the acts; three separate designs would lose her. Fallback if time runs out: Act II reuses the Act I file (ME03 is P1 but the cheapest to defer).

## Assets

| Asset / slot | What it is | Target | Attaches to | Priority | Source | Source detail |
|---|---|---|---|---|---|---|
| `avatar_moe_sayo_v2.webp` | Sayo, Mother of Echoes: Act I boss | AI_AVATAR | AI `fJLcH1mpB1XHHGtNWwvzD` | P1 | director | ME01 |
| `avatar_moe_silence.webp` | The Silence: Act I boss | AI_AVATAR | AI `IhNR-W1FElTsrWw1KfuQ9` | P1 | director | ME02. Rim-lit proposal `avatar_moe_silence_rim.webp` (art QA 2026-11-04: the pure-black silhouette vanishes on dark boards; `art/mother_of_echoes/rim_silence.py`), switch `SILENCE_RIM` in `push/mother_of_echoes.gen.py`, pending the director |
| `avatar_moe_sayo_stilling.webp` | Sayo, Glasswright of the Stilling: Act II boss | AI_AVATAR | AI `H3pNj2qUWpMpVRINiH6Vn` | P1 | director | ME03 |
| `avatar_moe_saint.webp` | Sayo, Saint of Stillness: Act III boss | AI_AVATAR | AI `k0hgSrghl_KcYs9ATVDJT` | P1 | director | ME04 |
| `avatar_moe_feeler.webp` | A Feeler of the Deep: summon (The Listening) | AI_AVATAR | AI `qFKcwTUkBtRiC-uM_8xG8` | P1 | director | ME05 |
| `avatar_moe_likeness.webp` | Your Likeness: summon (Your Likeness) | AI_AVATAR | AI `zyOeF-rSpeXuMU7A3QQgo` | P1 | director | ME06 |
| `avatar_moe_worn_porter.webp` | The Gate Porter (Worn): summon | AI_AVATAR | AI `wivZbMygCZo6c9pRKWvCI` | P1 | director | ME07 |
| `avatar_moe_worn_hana.webp` | Sister Hana (Worn): summon | AI_AVATAR | AI `g6bNcftMcQ9pV_nMki7Wv` | P1 | director | ME08 |
| `avatar_moe_worn_tomo.webp` | Cadet Tomo (Worn): summon | AI_AVATAR | AI `KhFglnxE7ouIDywet3BPB` | P1 | director | ME09 |
| `scene_moe_heart.webp` | The Heart of the Mother Glass | SCENE_BACKGROUND | quest IBPNwhAzlAJPXoeEnp8gW content, d_open, b_act1, f_lost | P1 | director | ME10 |
| `scene_moe_stilling.webp` | The Heart of the Mother Glass, the Stilling | SCENE_BACKGROUND | quest IBPNwhAzlAJPXoeEnp8gW d_act2, b_act2 | P2 | director | ME11 |
| `scene_moe_impression.webp` | The Heart of the Mother Glass, A Good Impression | SCENE_BACKGROUND | quest IBPNwhAzlAJPXoeEnp8gW d_act3, b_act3, w_clear | P2 | director | ME12 |
| `icon-quest-mother-of-echoes.webp` | Quest icon | ICON (quest.image) | quest `IBPNwhAzlAJPXoeEnp8gW` | P1 | director | ME13 |
| `icon-shard-keel.webp` | Shard of the Keel (dropping live now) | ICON | item `uKnlqlfyE_k1QjLuaVml_` | P1 | director | ME14 |
| `icon-shard-crown.webp` | Shard of the Crown (dropping live now) | ICON | item `4UNvgWIDGD9QpNVtLr1aM` | P1 | director | ME15 |
| `icon-shard-tide.webp` | Shard of the Tide (dropping live now) | ICON | item `KHGZAfQFosLQJ29AN2ymC` | P1 | director | ME16 |
| `icon-shard-ledger.webp` | Shard of the Ledger (dropping live now) | ICON | item `cGrmhfe88ACBvFk2XqvSu` | P1 | director | ME17 |
| `icon-variant-token-heartglass.webp` | Heartglass token (VT base, window motif) | ICON | item `FmQgVG5IX3q607wcHcOGy` | P1 | director | ME18 |
| `icon-variant-token-remainder.webp` | The Remainder token (VT base, window motif) | ICON | item `xCAtBCvbA2-TTV2eSe-jx` | P1 | director | ME19 |
| `icon-variant-heartglass-approved.webp` | Heartglass variant (final, director-approved) | ICON (item-variant image) | itemVariant `s_UZJAJ2LR_qDTKAu7l5-` | P1 | director | live since push/468 |
| `icon-variant-the-remainder.webp` | The Remainder variant (live since push/468) | ICON (item-variant image) | itemVariant `f1trw5TAP7ItE-E7eh8b0` | P1 | director | ME20 |
| `jutsu_moe_fam_lancet.webp` | Glass Lancet (jutsu family icon) | JUTSU_ICON | Covers: Glass Lancet `0g0Iy9PKsIVC6ggG1Exz2`; The Glass Remembers `G_b5yaxm6GMOuQ3eaofKb`; Lucid `IOUn-UrO1gwbi4uJdwYDp` | P2 | director | ME21 |
| `jutsu_moe_fam_refraction.webp` | Refraction (jutsu family icon) | JUTSU_ICON | Covers: Refraction `yxP6zO2NmjwqnrnvNXipC`; Far Refraction `HIftLq_RQJkIUUqGgBPTE`; Facet `eYzXEQI-Vz3gSIDfP2sX3`; Refraction Breaks `qjtaZInyr1nZ5lZmSA_SS`; Far Refraction Breaks `OTcP-08or5bUKwcMjc54K`; Facet Breaks `xlmvVot9xaetibexfyc31`; Lucid Refraction `KfXRK6rC3bt4kpdtdJHDb`; Every Name in the Glass `LhyIGAqoerbh3tFbcPrdx`; The Names Flood In `4_dlB0conB-C6sfYqiU6Q` | P2 | director | ME22 |
| `jutsu_moe_fam_etching.webp` | Etching (jutsu family icon) | JUTSU_ICON | Covers: Etching: Rime `lkcsor1I5A8gD038ncrBW`; Etching: Ember `eovhl9XyDQq1N19lDwr77`; Etching: Seam `Pr7i3DK5KiRQRePy8Xw41`; Etching: Heart `nNUaP5r8r7UxYNiAtuF0l`; Etching: Hail `2pU7fdUPQPQQjyd19JDWA`; Recast: Rime `Avu4B2M_9_SE0-Oqqhplw`; Recast: Ember `I5lwaFCaVSH6cpxAPHvFA`; Recast: Seam `54nmWiFXqvFW7u0vSG5zK`; Recast: Heart `-MtfLHClmIwSSGBIw9O7X`; Recast: Hail `lmlhn5p68Oszhj16wKbvx` | P2 | director | ME23 |
| `jutsu_moe_fam_glassfall.webp` | Glassfall (jutsu family icon) | JUTSU_ICON | Covers: Shatterfall `RcMx3MCHD7dyJw_12mr_7`; Shatterfall Gives Way `cxqu1ljkSisTgPBLgYtJa`; Glassfall: First Pane `kzxTPUJ8TYJFTggSKw3zr`; Glassfall: Second Pane `6IMcG7R_uhfROlANlYmDB`; Glassfall: Last Pane `H0MMi_Stpzk8zm4HqDEbF`; Glassfall: Opening Pane `pp40FDDTbGMdwrDFTNyiF`; Glassfall: Heart Recast `3ytuMbHhF4bcE2zrePnlR` | P2 | director | ME24 |
| `jutsu_moe_fam_hush.webp` | The Hush (jutsu family icon) | JUTSU_ICON | Covers: The Hush `kfzxZHje97anmOwwph84l`; The Hush, Unbridled `VqSpJhDUvjxLP5OtjI1mc`; The Hush Rises `F5qD1aXjt-kPQ6IR7nDoo`; Hush Where They Refused `AMNfIbTUiKsnvNfZGpAf1`; No One Is Mended `BA9V_vlnJZhA0V2tY4Ov_`; The Quiet `w6eHg1zFOrP1AhlwtyfZV`; The Long Hush `2erO3JCcfpXixrGz0NmhH`; The Glass Falls Quiet `KIwfifD8OGNVbs9I8O6Rw`; Stillness `A8c_3evIw6fOfnmKIkTgb`; Nothing Moves `scGyJW-F0Mqga4FXnj4Jf`; The Held Breath `3ShDcIL5dzj_8w60Qoo9h`; Breathless Pull `83mLMXND-9sAyN5WfmzQo`; The Listening `mqko5kLLXqGAVr6MVoKY0`; The Listening, Unbridled `q0QcFoX4HIhxO0cpYTL2N`; Cradle `DFcbOLSvYssjLzTHo_dw0`; Grasp `zHNAEQ1xmDSOzFVEqeJlS` | P2 | director | ME25 |
| `jutsu_moe_fam_echoes.webp` | Echoes (jutsu family icon) | JUTSU_ICON | Covers: Your Likeness `foDwd-hL5krmhFHsPtQtc`; Your Own Strike `nkNryj61h6qB3azifb8h4`; Raise the Gate Porter `l1TpeIKJyNDzQQkI1Az1K`; Raise Sister Hana `BeOpXT1M_7oRkwYCcXk6Z`; Raise Cadet Tomo `yzI6KIOPzy6P2B0U6Cqyp`; Doorward Sweep `x4aJMqXJ3kvyr0bKUZaZj`; Worn Mending `tEAiiOTcd7rTgu-nJySPv`; Cadet's Tether `rC9J4ZrjMfftPa4UmlBoV` | P2 | director | ME26 |

### Animations (the 18 named `moe_*` slots plus `tg_etch`)

| Slot | What it is | Target | Jutsu | Priority | Source | Source detail |
|---|---|---|---|---|---|---|
| `tg_etch` | Etching mark, still tile (staticAssetPath, under the characters) | STATIC tile | Etching: Rime `lkcsor1I5A8gD038ncrBW`; Etching: Ember `eovhl9XyDQq1N19lDwr77`; Etching: Seam `Pr7i3DK5KiRQRePy8Xw41`; Etching: Heart `nNUaP5r8r7UxYNiAtuF0l`; Etching: Hail `2pU7fdUPQPQQjyd19JDWA` | P1 | code | `art/mother_of_echoes_fx/exports/tile_moe_etch_v3.webp` (v3, art QA: the v2 1 px Bayer haze became a screen door after the 50 px CDN rendition, so the region is tinted by sparse solid 2x2 score chips; lattice unchanged) |
| `tg_etch` | Etching mark, loop (staticAnimation) | ANIMATION | same 5 Etchings | P1 | code | `anim_moe_etch_glint_v1.webp` (built now) |
| `tg_etch` | Etching mark, appear / disappear | ANIMATION | same 5 Etchings | P1 | code (push/478) | appear `anim_moe_etch_appear_v1.webp` (a white scribe spark cuts the lattice out, the cut flares gold); no disappear (see Custom set) |
| `moe_recast` | Recast hit: the lattice flashes back, glass blades rise and shatter | ANIMATION (appear) | Recast: Rime `Avu4B2M_9_SE0-Oqqhplw`; Recast: Ember `I5lwaFCaVSH6cpxAPHvFA`; Recast: Seam `54nmWiFXqvFW7u0vSG5zK`; Recast: Heart `-MtfLHClmIwSSGBIw9O7X`; Recast: Hail `lmlhn5p68Oszhj16wKbvx` | P1 | code | `anim_moe_recast_v1.webp` (built now; pairs with tg_etch) |
| `moe_refraction` | Refraction / Facet breaks (heavy-mark payoff) | ANIMATION (appear) | Refraction Breaks `qjtaZInyr1nZ5lZmSA_SS`; Far Refraction Breaks `OTcP-08or5bUKwcMjc54K`; Facet Breaks `xlmvVot9xaetibexfyc31`; Lucid Refraction `KfXRK6rC3bt4kpdtdJHDb` | P1 | code (push/478) | `anim_moe_refraction_blast_v1.webp` (was the live Eruption) |
| `moe_shatterfall` | Shatterfall Gives Way | ANIMATION (appear) | Shatterfall Gives Way `cxqu1ljkSisTgPBLgYtJa` | P1 | code (push/478) | `anim_moe_shatterfall_v1.webp` (was the live Crystal Shard) |
| `moe_glassfall` | Glassfall panes (hit, then the next pane is marked) | ANIMATION (appear) | Glassfall: First Pane `kzxTPUJ8TYJFTggSKw3zr`; Glassfall: Second Pane `6IMcG7R_uhfROlANlYmDB`; Glassfall: Last Pane `H0MMi_Stpzk8zm4HqDEbF`; Glassfall: Opening Pane `pp40FDDTbGMdwrDFTNyiF`; Glassfall: Heart Recast `3ytuMbHhF4bcE2zrePnlR` | P1 | code (push/478) | `anim_moe_glassfall_v1.webp` (was the live Crystal Shard) |
| `moe_flood` | The Names Flood In (heavy field payoff) | ANIMATION (appear) | The Names Flood In `4_dlB0conB-C6sfYqiU6Q` | P1 | director + code | `anim_moe_flood_mask_v1.webp`: the director's glass-mask keyframes (ME28b, `art/mother_of_echoes/raw/fx_flood_mask_keys.png`, drawn for the 50 px rendition) animated in `build_fx.py` `build_flood_mask`: rise, hold, eyes-open flash with ember cracks, burst, shards fly. Replaces the live Eruption reuse (2026-11-04) |
| `moe_stillness` | Nothing Moves (control-mark stun payoff) | ANIMATION (appear) | Nothing Moves `scGyJW-F0Mqga4FXnj4Jf` | P1 | code | `anim_moe_still_dark_v2.webp` (v2: a solid ink ring with a crisp 1 px violet edge closes from the rim; no checker halo), the dust stops in the air |
| `moe_breathless` | Breathless Pull (control-mark pull + stun payoff) | ANIMATION (appear) | Breathless Pull `83mLMXND-9sAyN5WfmzQo` | P1 | code | `anim_moe_breath_draw_v1.webp` (built now): breath drawn in from the rim and away upward, a violet lock at the feet; plays only on hit hexes, so the three dry tiles (tg_safe) stay clear |
| `moe_hush_floor` | No One Is Mended floor (healing cut pool) | STATIC tile + ANIMATION | No One Is Mended `BA9V_vlnJZhA0V2tY4Ov_` | P1 | code (push/478) | as tg_linger (custom set); art carried on `healprevent`, not `decreaseheal` (see Custom set) |
| `moe_guard_open` | Guard open: the Recast weakness on SAYO (the weakness targets SELF: her guard opens) | ANIMATION (static loop) | Recast: Rime `Avu4B2M_9_SE0-Oqqhplw`; Recast: Ember `I5lwaFCaVSH6cpxAPHvFA`; Recast: Seam `54nmWiFXqvFW7u0vSG5zK`; Recast: Heart `-MtfLHClmIwSSGBIw9O7X`; Recast: Hail `lmlhn5p68Oszhj16wKbvx` | P2 | code | `anim_moe_guard_open_v2.webp` (v2, art QA: a bold cracked ring of etched gold glass round her portrait, plates push out and flare white on the beat; v1's splinters were invisible) |
| `moe_quiet` | The Quiet hit | ANIMATION (appear) | The Quiet `w6eHg1zFOrP1AhlwtyfZV` | P2 | code | `anim_moe_quiet_v1.webp` |
| `moe_lancet` | Glass Lancet hit | ANIMATION (appear) | Glass Lancet `0g0Iy9PKsIVC6ggG1Exz2` | P2 | code | `anim_moe_lancet_v2.webp` (v2: thick outlined needle, white impact star held 2 frames) |
| `moe_enrage` | The Glass Remembers (round-30 enrage hit) | ANIMATION (appear) | The Glass Remembers `G_b5yaxm6GMOuQ3eaofKb` | P2 | code (push/478) | `anim_moe_enrage_v1.webp` (was the live Eruption) |
| `moe_lucid` | Lucid (Sayo enrage buff aura) | ANIMATION (static loop) | Lucid `IOUn-UrO1gwbi4uJdwYDp` | P2 | code | `anim_moe_lucid_aura_v1.webp` (built now): eight cold skyglass facets circling Sayo alone, white on the beat; keeps her AI-sized portrait clear |
| `moe_likeness` | Your Likeness summon flourish | ANIMATION (appear) | Your Likeness `foDwd-hL5krmhFHsPtQtc` | P2 | code | `anim_moe_likeness_ring_v2.webp` (v2, art QA: frames the summoned avatar instead of drawing a second figure: a silvered-glass ring closes, cracks and bursts into shards) |
| `moe_worn` | Raise the Worn summon flourish | ANIMATION (appear) | Raise the Gate Porter `l1TpeIKJyNDzQQkI1Az1K`; Raise Sister Hana `BeOpXT1M_7oRkwYCcXk6Z`; Raise Cadet Tomo `yzI6KIOPzy6P2B0U6Cqyp` | P2 | code | `anim_moe_worn_ash_v2.webp` (v2: grey-brown ash wells up out of the glass round the summon in solid clusters; v1 was invisible on snow) |
| `moe_feeler` | The Listening summon flourish | ANIMATION (appear) | The Listening `mqko5kLLXqGAVr6MVoKY0`; The Listening, Unbridled `q0QcFoX4HIhxO0cpYTL2N` | P2 | code | `anim_moe_feeler_v2.webp` (v2: ink ripples at the root and bone wisps beside the summoned feeler; no second feeler) |
| `moe_cradle` | Cradle (the Feeler shields its boss) | ANIMATION (static loop) | Cradle `DFcbOLSvYssjLzTHo_dw0` | P2 | code | `anim_moe_cradle_v2.webp` (built in code without ME27: pale feelers braid round her portrait over a violet ink hold; v2 trims the roots so it stays clear of the HP bars two rows down) |
| `moe_lull` | The Glass Falls Quiet (breath between cycles) | ANIMATION (static loop) | The Glass Falls Quiet `KIwfifD8OGNVbs9I8O6Rw` | P3 | code | `anim_moe_lull_v3.webp` (v3: 2x2 motes, twice as many, two dust curtains; v2's 1 px specks vanished under linear filtering). MOVED off the `visual` (dropped by the server at the next action, RUL-2026-11-02-101) onto the same jutsu's `fleeprevent` effect (SELF, 2 rounds) as its staticAnimation: dust drifting beside Sayo for the two rounds between cycles. The visual keeps its live appear/vanish ids |
| `moe_flood` (upgrade) | The Names Flood In, signature version (faces alight) | ANIMATION (appear) | The Names Flood In `4_dlB0conB-C6sfYqiU6Q` | P3 | director | NOT SHIPPED (art QA 2026-11-04): the ME28 faces did not hold up at the 50 px CDN rendition (the 150 px v1 lost its detail; 50 px rebuilds read as blank tiles and stacked into columns across a field). The flood keeps the reuse-live Eruption |

Already wired and live, no work: `tg_heavy`, `tg_control`, `tg_linger`, `tg_safe` (push/431 tiles and loops, `state/skyglass_fx/asset_ids.json`), and the library hits the spec names by id (`dBatQkc1Ts2ask5ZN-A3p` pierce, `FZNt0vFGXlOZeagmPneqc` shove, `I9aYhT5wMB` heal, `bJy2IjRKmAVYEoXUYmXv5` / `k8J4ic-KEz9ewEq1gAszr` appear/vanish). No scene characters: the quest shows the Blank Scene Character by design.

### Custom set (push/478, director 2026-11-05: "we're borrowing a lot of animations from elsewhere in the event instead of making our own")

Every slot that borrowed a live Skyglass or library strip now has its own, built in `art/mother_of_echoes_fx/build_fx.py`
(`CUSTOM`). The event's danger grammar is kept (docs/design/SKYGLASS_BOSS_ANIMATIONS.md readability rules: shape carries
the meaning, colour confirms it), drawn in Sayo's glass: heavy is a ten-sided ring of red-to-yellow ember glass facets
round a near-black ground with four thin cracks; control is fourteen faceted violet glass links round an ink ground
with a closed glass eye (the hush); linger is bile welling up through crazed glass; safe is a cut-glass cyan diamond with
a white four-point star. Payoffs follow anticipation, impact (white frame), follow-through and settle.

| Was (live) | Now | Slots |
|---|---|---|
| Skyglass heavy tile + loop + mark appear/vanish | per act (art3): `tile_moe_heavy_{i,ii,iii}_a3`, `anim_moe_heavy_glint_{i,ii,iii}_a3`, `anim_moe_heavy_appear_{i,ii,iii}_a3` (the v1 strips are retired) | tg_heavy (14 marks: Sayo I in I, The Glass Turns in II, the Saint and The Silence Turns in III) |
| Skyglass control tile + loop + appear/vanish | `tile_moe_control_dark_a3` (art3; both holders are Act III material), `anim_moe_control_glint_v1`, `anim_moe_control_appear_v1` | tg_control (Stillness, The Held Breath); the lull visual's appear |
| Skyglass lingering pool tile + bubbles + appear | `tile_moe_linger_v1` (Acts I-II) or `tile_moe_linger_dark_a3` (the Silence, Act III, No One Is Mended), `anim_moe_linger_glint_v1`, `anim_moe_linger_appear_v1` | tg_linger (the eruption pools), moe_hush_floor |
| Skyglass safe tile + loop + appear/vanish | `tile_moe_safe_v1`, `anim_moe_safe_glint_v1`, `anim_moe_safe_appear_v1` | tg_safe (Every Name in the Glass, The Held Breath) |
| mark appear `bJy2IjRKmAVYEoXUYmXv5` on the Etchings | `anim_moe_etch_appear_v1` | tg_etch |
| Eruption `Z9j8J7ZmAjiaxH2S4nDy8` | `anim_moe_refraction_a3` (Heartglass); The Glass Remembers as the `anim_moe_enrage_w0..3_a3` wave | moe_refraction, moe_enrage |
| Crystal Shard `TAu9k8ifgteP6HBofoKn7` | waves: `anim_moe_glassfall_w0..2_a3`, `anim_moe_shatterfall_w0..4_a3` | moe_glassfall, moe_shatterfall |
| library pierce `dBatQkc1Ts2ask5ZN-A3p` | `anim_moe_grasp_v1` (Grasp), `anim_moe_echo_strike_v1` (Your Own Strike, Doorward Sweep, Cadet's Tether) | summon strikes |
| library shove `FZNt0vFGXlOZeagmPneqc` | `anim_moe_pull_v1` (Breathless Pull, Cadet's Tether), `anim_moe_shove_v1` (Doorward Sweep) | redirection |
| library heal `I9aYhT5wMB` | `anim_moe_mend_v1` | Worn Mending |
| mark vanish `k8J4ic-KEz9ewEq1gAszr` | none (dropped) | every ground mark; the lull visual |

Engine rules applied (docs/design/COMBAT_ANIMATION_ENGINE.md at 2e66800b; theninjarpg@3314d122):
- **No disappear clip on any ground mark** (section 5.3): a ground tag's disappear is re-spawned on whoever stands on it at
  every effect pass (`process.ts:1667-1684`), so it would pop repeatedly on a player in a mark or on the safe hex. A
  `visual` never plays its disappear at all, so the lull's vanish was dead wiring.
- **Art moved off tags that go negative when cast** (section 5.1; `tags.ts` :847/:892/:977/:1062/:1173/:1816; the client
  hides power <= 0, `combatEffects.ts:183-187`, `:215`). An occupant's `fromGround` copy shares the ground effect's id
  (`process.ts:398-411`), so pool art on `decreaseheal` vanished under anyone standing in it, and Cradle's loop on
  `decreasedamagetaken` never rendered. Moved (push/478, 13 jutsu): every eruption pool (Refraction / Far Refraction /
  Facet Breaks, Lucid Refraction, Shatterfall Gives Way, The Names Flood In, the five Glassfall panes) `decreaseheal ->
  increasedamagetaken`; No One Is Mended `decreaseheal -> healprevent`; Cradle `decreasedamagetaken -> clearprevent`.
- Strips stay on the 50 px grid (the CDN `?width=50` rendition, `primitives/animation.ts`), solid 2-3 px clusters, hard
  alpha, 1 px clear frame margin, 9-15 frames (0.45-0.75 s), well under 80 frames.

What the player sees, slot by slot (categories from COMBAT_ANIMATION_ENGINE.md section 1.3):

| Slot (carrier) | Visible? | When | Times drawn |
|---|---|---|---|
| tg_heavy / tg_control / tg_safe / tg_etch marks (`increaseregeneration`, ground, rounds 1) | yes: tile under fighters + loop + appear | cast in round N, on screen for the rest of N and all of N+1, still showing after its eruption in N+1 | appear 2x (client + server visual), 3x on an occupied hex in the cast round; loop and tile 1x |
| tg_linger eruption pools (`increasedamagetaken`, ground, rounds 1) | yes, also under an occupant | with the eruption, for the rest of that round and the next | appear 2x empty / 3x occupied |
| moe_hush_floor (No One Is Mended, `healprevent`, ground) | yes | for its rounds | appear 2x / 3x |
| moe_refraction (instant ground `pierce`; the wave payoffs moved to the visual bands, Art3 below) | yes, as the server visual | the snapshot of the cast | 1x on an empty hex, 2x on an occupied one |
| Grasp, echo strike (character `pierce`, rounds 0) | yes, server visual at the target | the snapshot of the cast | 1x |
| pull / shove (`redirection`) | yes | the snapshot of the cast, at the target's OLD hex (the fighter walks, the clip does not follow) | 1x |
| mend (`heal`, rounds 0) | yes | the snapshot of the cast | 1x |
| Cradle loop (`clearprevent` on Sayo, rounds 1) | yes (was never visible) | while the feeler holds her | loop 1x |
| the lull visual's appear | yes | the snapshot of the cast | 1x |

### Art3 (push/478 rebuilt, director 2026-11-05: "a high end boss fight ... showcase the top end of what our engine is capable of. Pull out all the stops")

Built by `art/mother_of_echoes_fx/build_fx_a3.py` (exports `*_a3.webp`, `moe_fx_a3.json`); wired by
`push/mother_of_echoes.gen.py` (`FX3`, `TG3`, `SLOT3`, `MOSAIC`, `SFX_BY_NAME`, `SCENE_CHARS`). Director decisions, same
day:

1. **Material arc approved, with fixes.** "When she starts out it's Skyglass, crystal, reflections and light. Then she
   gets corrupted by the Silence and it becomes black corrupted shadow moves." Palettes are measured from the approved
   variants: Act I = Heartglass (`art/skyglass_variant_skins/raw/ME40_raw_icon-variant-heartglass_approved.png`: framed
   facets, the heart crown, prismatic glints); Act III = the Remainder (`variant_the_remainder.png`: thorned shards,
   smoke in the glass, glowing crack veins); Act II is the turn. Fixes applied: the ember outer rim stays on heavy in all
   three acts; the Act II heavy and Recast show the Remainder's black cracks and smoke creeping into the Heartglass (it
   does not read as Act I gold); Act III spikes carry brighter teal-cyan veins and edge light for dark boards. A jutsu's
   act is its holders' (`BOSS_ACT`; The Silence and its feeler are Remainder material). The Glass Remembers is one record
   shared by all four bosses, so it has one look: the corrupted wave (the glass remembering what it holds).
2. **Mosaics approved.** The signature payoffs play as a wave: the hit's own appear is blanked and one zero-impact
   `visual` tag per band (target COORDINATES, the cast's own origin, a subset of its tiles, power 2) carries a strip led
   by `band x 3` blank frames. The Glass Remembers: 4 column bands; The Names Flood In: 4 bands out from the field
   centre; Shatterfall Gives Way: 5 bands by rank out from the Saint (CASTER cone); the five Glassfall panes: 3 column
   bands. Engine basis: a COORDINATES tag is stamped only on its own tiles (`actions.ts:1063-1071`; the cast's tiles are
   the union, `util.ts getActionAffectedTiles`), a `visual` has no server duplicate (`process.ts:432`), no occupant copy
   (`:399`) and no gameplay handler, and power 2 is never hidden (`combatEffects.ts:183-187`). Recasts are not mosaicked:
   they are CHARACTER casts, so bands over the etching would draw a payoff where no one is hit and turn a no-target cast
   into a landed one. The sim confirms identical clear rates on a fixed-seed rerun (the tags change no numbers).
3. **Boss auras and act-start flourishes approved**, not as 1-power carriers: a real thematic positive-power buff per
   boss (Act I Sayo, the Silence, Act II Sayo, the Saint), designed and balanced by the sim. The strips
   (`anim_moe_aura_*_a3`, `anim_moe_flourish_*_a3`) ship hidden-then-unhidden with the set and are wired when the buff
   tags land.
4. **Sound: existing in-game SFX, one per cast.** The client plays `appearSfx` once per new effect record
   (`combatEffects.ts:35-41`, `:106`), so a sound on a 100-tile tag plays 100 times. Single-target and CHARACTER casts
   carry it on their art-bearing hit; ground casts on a one-tile `visual` at the caster. Map: Lightning (the Refraction
   payoffs, Lucid), Sword Clash (Recasts), Earth (Glassfall, Shatterfall Gives Way, The Glass Remembers, The Names Flood
   In), Sword (Glass Lancet), Wind (every mark, Breathless Pull), Smoke (the hushes, Nothing Moves, The Quiet, the lull,
   Cradle, every summon), Punch (Grasp, Doorward Sweep, Cadet's Tether, Your Own Strike), Heal (Worn Mending).
5. **Dialog portraits: Sayo only.** SCENE_CHARACTER 2:3 crops (341x512) of the approved avatars: Act I Sayo in
   `d_intro1`, `d_intro2` and `d_open` (not the Silence), the Glasswright in `d_act2`, the Saint in `d_act3`
   (`scene_moe_sayo_a3`, `scene_moe_sayo_stilling_a3`, `scene_moe_saint_a3`). They ride the practice quest edit
   (push/479) and the go-live (push/477, `--art2-from`).

Also replaced: the summon entrances (`moe_feeler`, `moe_likeness`, `moe_worn`) by `anim_moe_rise_*_a3` (the summon
climbs out of cracking glass, bone cords for the feeler), and Recast by `anim_moe_recast_a3` (etched lattice, Heartglass
blades, black cracks race up and shatter).

What the player sees for the new carriers (COMBAT_ANIMATION_ENGINE.md section 1.3 categories):

| Slot (carrier) | Visible? | When | Times drawn |
|---|---|---|---|
| wave bands (`visual`, COORDINATES, rounds 1) | yes | the snapshot of the cast, band k starting k x 150 ms later | 1x per hex (no server duplicate, no occupant copy); the blanked hit draws nothing |
| sound carrier (`visual` at the caster, no art) | sound only | the cast | 1 sound per cast |
| heavy marks per act | as the tg_heavy row above | | |

### Art4: boss entrances, slice mosaics, frequent-move set pieces (director after the live test, 2026-11-05)

**Entrances** ("Boss intro animation was a bit underwhelming but the aura was cool"). `build_fx_a4.py` draws one
30-frame signature entrance per form on the full clip square (anticipation, a 2-frame reveal hold, settle), with the
portrait disc kept clear except for a one-frame rim flash, plus a two-band ring of ground pieces round her hex timed
to land on the reveal: Act I Sayo, Heartglass light spirals in, the fan of framed Heartglass blades opens behind her
with a prismatic burst, a palisade of panes springs up round her; the Silence, the ink spreads and a hooded shadow far
larger than her stands up off the floor with teal veins and bone wisps, shadow tendrils stand up round her, then
smoke; Act II, the gold etch ring is traced and ignites, spokes flare, the Remainder's black cracks creep over it, the
lattice ignites and cracks on the hexes round her; Act III, black glass gathers in and bursts out as thorns with lit
teal veins and bone tendrils, black thorns burst up round her. The approved art3 auras are unchanged.

Finding: no boss jutsu carries a flourish or an aura today. push/478 created them and push/489/496 unhid them, but no
spec effect names them (they were held for the sim's act buffs), so what the tester saw at the start of each act is
the first move's own art. Every boss's first cast also repeats (Sayo I opens with Refraction, the Silence with The
Silence Turns, the Glasswright with her combo, the Saint with Shatterfall or The Quiet), so an entrance on any of them
would replay all act long. The carrier has to be a once-per-act cast: a first rule gated on the absence of the buff it
applies, which is the sim's act buff. The generator wires by slot name: an effect with appearAnimation `moe_entrance`
gets her form's entrance, staticAnimation `moe_aura` her art3 aura, and the cast gains the ring as zero-impact visual
tags at CASTER offsets. CASTER offsets are added to her column and row as written (`targeting.ts:63-70`), so the ring
cannot follow the odd-q stagger: band 0 is the 3 x 3 box round her (her 6 neighbours plus 2 hexes at distance 2, above
or below by her column's parity). The entrance assets (4 after the v2 rework, see "Stacking pass") are created HIDDEN by the final tuning job (`fx4_create_items`,
srcIds `sg498_*`) and unhidden by a follow-up (`art4_unhide_items`); `custom_fx_refs` gives that job the live custom
set by literal id from the push/489 run.

**Slice mosaics** ("you can also have them each play a different frame of a larger animation to make one big
effect"). `build_fx_mosaic.py` draws one composition on a canvas at the clip's own density and cuts it into per-hex
clips. Geometry (section 3.1): tile box hexSize x 0.5 hexSize, columns 0.75 hexSize apart, rows one tile height apart,
odd columns half a row lower (honeycomb-grid offset -1, odd-q, `util.ts:3419`); a clip is 2.5 tile heights square
from the 50 px rendition, so one source pixel is 1/20 tile height on every hex: column pitch 30, row pitch 20,
odd-column drop 10, clip 50 x 50 source px. Each hex carries only the canvas pixels it owns (nearest covered centre in
the hex metric, inside its clip square) plus a 1 px overlap so linear filtering opens no seam. Prototype: Refraction
along row 1, 12 slices: at true size it reads as one continuous line of light running in from both walls, a white
flash, and a palisade of shards crossing hex seams with no visible joins. Timing: all slices of one cast arrive in one
snapshot and start when their own texture is ready (`combatEffects.ts:157-166`, `:212`), so once loaded they start on
the same frame; on the first cast of a battle each waits for its own texture (2.4), and a 0-2 frame stagger reads as a
ripple, not a tear. Limits: BATTLEFIELD patterns know each hex's column parity, so they slice exactly; CASTER and TARGET
patterns do not (her or the target's parity decides which offsets are neighbours), so those keep per-hex pieces;
cost is one asset per distinct slice (a Refraction row: 12; Facet's paired rows: 24).

**Frequent-move set pieces** (Refraction / Far Refraction / Facet marks and Breaks, Lucid Refraction, The Silence
Turns, Stillness, the Hush pools, Etchings, Recasts) are drafted as band waves (`build_fx_a4.py --drafts`) and are
held, with the slice versions, until docs/design/SAYO_BIBLE.md lands (coordinator, 2026-11-05); they will be aligned to
it before they are exported or wired.

## Stacking pass (whole fight, 2026-11-05)

**Brief (coordinator for the director):** know exactly what the player sees each round when several effects play at once,
and cut or re-time anything that clutters or cannot be read, before anything else is wired. Release Friday.

**Method.**
1. Rounds and casts come from the sim, not guesses: seeded traces of the latest spec (`fable/mother-of-echoes-sim` @
   `3eb8abab`, `overrides/moe.params.json` "pass6-live8", read only, run in a private worktree), perfect and real player,
   seeds 1-3, every act; Act III v2 from the prototype's trace (`fable/mother-of-echoes-act3` @ `f064d5dd`, loop L5).
   The player's own kit comes from the director's two logs (`harvests/battle_logs/moe_practice_dauntless_2026-11-05*.txt`:
   Glass Lancet, Grasp, Cradle, Facet, Refraction, Stillness, The Silence Turns against Captain's Decree, Thunderclap
   Strike, Forbidden Chakra Fury, Dragon's Tomb, stances, Chakra Shield, Replacement).
2. Each cast maps to the clips the live build plays (the generator's own `Build` on that spec, the custom set by
   literal id from the push/489 run), with the engine's rules (COMBAT_ANIMATION_ENGINE.md): an effect with rounds R cast
   in round N shows through N+R; appears play once (ground marks 2x / 3x occupied, identical frames, so overdraw
   only matters between different records); static loops and tiles last the effect's life; **all clips draw over every
   fighter, static tiles under them** (3.2); records stack in creation order, newest on top; all AI clips of one
   snapshot start together; the killing blow is not animated.
3. The busiest moments were composited from the real strips at true client scale (132 x 66 px tiles, 165 px clip
   square from the 50 px rendition, linear filtering) on a full 12 x 10 arena, light and dark. Player and library
   strips the session cannot fetch (no CDN access from the shell) use same-size stand-ins, labelled.
   Harness: `scratchpad/custom/stack/` (cooccur.py, composite.py, moments.py); GIFs and key sheets in `stack/gif/`.

**Units.** "Appear-hexes" = hexes on which a one-shot clip starts this round; "loop-hexes" = hexes with a looping clip
on screen (each draws over the fighters for its whole life); "tile-hexes" = static art under the fighters.

### Co-occurrence (per act, the six busiest rounds of each run)

#### Perfect player, seed 1, Act 1 (won, 3 rounds)

Per round: appear-hexes median 56 / max 71; loop-hexes median 69 / max 96 (after the stacking rules: median 33 / max 33); tile-hexes (marks + pools under the fighters) median 69 / max 96.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 1 | Refraction, Glass Lancet, The Hush, Stillness | Wind Release: Whirlwind Demi, Chakra Overflow, _8HEbybzN5QPX8vUG24Tk | 71 | 69 | 63 / 6 |
| 2 | Refraction Breaks, Nothing Moves | Tempest Cleave, Captain's Decree (equivalent | 56 | 96 | 63 / 33 |
| 3 | - | Shrapnel Clone Barrage | 0 | 33 | 0 / 33 |

#### Perfect player, seed 1, Act 2 (won, 30 rounds)

Per round: appear-hexes median 48 / max 80; loop-hexes median 115 / max 186 (after the stacking rules: median 42 / max 53); tile-hexes (marks + pools under the fighters) median 112 / max 184.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 6 | Recast: Seam | Wind Style: Sky Dragon | 80 | 144 | 0 / 142 |
| 11 | Etching: Heart, The Hush Rises, Doorward Sweep | Eclipse Drain, Tempest Cleave | 49 | 151 | 108 / 40 |
| 17 | Recast: Seam | Wind Release: Whirlwind Demi | 80 | 150 | 0 / 148 |
| 18 | Recast: Ember | Chakra Overflow, Earthen Bastion | 72 | 186 | 0 / 184 |
| 28 | Recast: Seam | Shrapnel Clone Barrage, wE1QeldWTjls2Cf43cFjf | 80 | 129 | 36 / 90 |
| 29 | Recast: Rime | tZTvqYWiAc_OrY64nDvIo, Dragon King's Impact, u9mXSgVW_QjkRzCejGXZ1 | 72 | 129 | 0 / 126 |

#### Perfect player, seed 1, Act 3 (won, 56 rounds)

Per round: appear-hexes median 30 / max 240; loop-hexes median 102 / max 397 (after the stacking rules: median 8 / max 24); tile-hexes (marks + pools under the fighters) median 102 / max 396.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 23 | The Names Flood In | Wind Style: Sky Dragon, wE1QeldWTjls2Cf43cFjf | 234 | 376 | 120 / 256 |
| 25 | The Held Breath, Shatterfall | Multi-Layered Gale, Wind Release: Whirlwind Demi | 140 | 378 | 139 / 238 |
| 31 | Breathless Pull, Every Name in the Glass | - | 124 | 381 | 240 / 140 |
| 32 | The Names Flood In | u9mXSgVW_QjkRzCejGXZ1 | 234 | 377 | 120 / 257 |
| 34 | The Held Breath, Shatterfall | - | 140 | 378 | 139 / 238 |
| 41 | The Names Flood In | - | 234 | 377 | 120 / 257 |

#### Real player, seed 1, Act 1 (won, 3 rounds)

Per round: appear-hexes median 56 / max 71; loop-hexes median 69 / max 96 (after the stacking rules: median 33 / max 33); tile-hexes (marks + pools under the fighters) median 69 / max 96.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 1 | Refraction, Glass Lancet, The Hush, Stillness | Wind Release: Whirlwind Demi, Chakra Overflow, _8HEbybzN5QPX8vUG24Tk | 71 | 69 | 63 / 6 |
| 2 | Refraction Breaks, Nothing Moves | Tempest Cleave, Captain's Decree (equivalent | 56 | 96 | 63 / 33 |
| 3 | - | Shrapnel Clone Barrage | 0 | 33 | 0 / 33 |

#### Real player, seed 1, Act 2 (lost, 17 rounds)

Per round: appear-hexes median 49 / max 80; loop-hexes median 111 / max 151 (after the stacking rules: median 38 / max 44); tile-hexes (marks + pools under the fighters) median 108 / max 148.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 4 | Recast: Rime | Shrapnel Clone Barrage, wE1QeldWTjls2Cf43cFjf | 72 | 105 | 36 / 66 |
| 6 | Recast: Seam | Wind Style: Sky Dragon | 80 | 144 | 0 / 142 |
| 10 | Etching: Heart, Etching: Rime, Doorward Sweep | Chakra Overflow, Earthen Bastion, u9mXSgVW_QjkRzCejGXZ1 | 76 | 104 | 72 / 30 |
| 11 | Etching: Heart, The Hush Rises, Doorward Sweep | Eclipse Drain, Tempest Cleave | 49 | 151 | 108 / 40 |
| 16 | Recast: Rime | tZTvqYWiAc_OrY64nDvIo | 72 | 111 | 0 / 108 |
| 17 | Recast: Seam | Wind Release: Whirlwind Demi, Chakra Overflow | 80 | 150 | 0 / 148 |

#### Perfect player, seed 2, Act 1 (won, 23 rounds)

Per round: appear-hexes median 5 / max 109; loop-hexes median 40 / max 122 (after the stacking rules: median 13 / max 41); tile-hexes (marks + pools under the fighters) median 40 / max 120.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 1 | The Hush, Stillness, Refraction, Glass Lancet | Wind Release: Whirlwind Demi, Chakra Overflow, _8HEbybzN5QPX8vUG24Tk | 71 | 69 | 63 / 6 |
| 2 | Nothing Moves, Refraction Breaks | Earthen Bastion, Eclipse Drain | 56 | 96 | 63 / 33 |
| 7 | The Hush, The Listening, Cradle, Grasp, Facet, Glass Lancet | Shrapnel Clone Barrage, wE1QeldWTjls2Cf43cFjf | 64 | 67 | 54 / 12 |
| 8 | Cradle, Facet Breaks | - | 108 | 122 | 54 / 66 |
| 13 | The Hush, Your Likeness, Facet, Stolen Form | Wind Style: Sky Dragon, Captain's Decree (equivalent | 62 | 66 | 54 / 12 |
| 14 | Facet Breaks, Your Own Strike | GNGrfEDnxbRBgOHHCjPX3, Shrapnel Clone Barrage, u9mXSgVW_QjkRzCejGXZ1 | 109 | 120 | 54 / 66 |

Not in the live catalogue (new in this spec, placeholder art or no art): Your Likeness:Stolen Form.

#### Perfect player, seed 2, Act 2 (lost, 18 rounds)

Per round: appear-hexes median 49 / max 80; loop-hexes median 112 / max 151 (after the stacking rules: median 38 / max 44); tile-hexes (marks + pools under the fighters) median 110 / max 148.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 4 | Recast: Rime | - | 72 | 105 | 36 / 66 |
| 6 | Recast: Seam | GNGrfEDnxbRBgOHHCjPX3, Tempest Cleave | 80 | 144 | 0 / 142 |
| 10 | Etching: Heart, Etching: Rime, Doorward Sweep | Chakra Overflow, Earthen Bastion, GNGrfEDnxbRBgOHHCjPX3 | 76 | 104 | 72 / 30 |
| 11 | Etching: Heart, The Hush Rises, Doorward Sweep | Eclipse Drain, Wind Style: Sky Dragon | 49 | 151 | 108 / 40 |
| 16 | Recast: Rime | Wind Release: Whirlwind Demi, tZTvqYWiAc_OrY64nDvIo, Captain's Decree (equivalent | 72 | 111 | 0 / 108 |
| 17 | Recast: Seam | h-mvWaKK5vNNOwS5Y9KQj, Chakra Overflow, Earthen Bastion | 80 | 150 | 0 / 148 |

#### Real player, seed 2, Act 1 (won, 23 rounds)

Per round: appear-hexes median 5 / max 109; loop-hexes median 40 / max 122 (after the stacking rules: median 13 / max 41); tile-hexes (marks + pools under the fighters) median 40 / max 120.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 1 | The Hush, Stillness, Refraction, Glass Lancet | Wind Release: Whirlwind Demi, Chakra Overflow, _8HEbybzN5QPX8vUG24Tk | 71 | 69 | 63 / 6 |
| 2 | Nothing Moves, Refraction Breaks | Earthen Bastion, Eclipse Drain | 56 | 96 | 63 / 33 |
| 7 | The Hush, The Listening, Cradle, Grasp, Facet, Glass Lancet | Shrapnel Clone Barrage, wE1QeldWTjls2Cf43cFjf | 64 | 67 | 54 / 12 |
| 8 | Cradle, Facet Breaks | - | 108 | 122 | 54 / 66 |
| 13 | The Hush, Your Likeness, Facet, Stolen Form | Wind Style: Sky Dragon, Captain's Decree (equivalent | 62 | 66 | 54 / 12 |
| 14 | Facet Breaks, Your Own Strike | GNGrfEDnxbRBgOHHCjPX3, Shrapnel Clone Barrage, u9mXSgVW_QjkRzCejGXZ1 | 109 | 120 | 54 / 66 |

Not in the live catalogue (new in this spec, placeholder art or no art): Your Likeness:Stolen Form.

#### Real player, seed 2, Act 2 (lost, 18 rounds)

Per round: appear-hexes median 49 / max 80; loop-hexes median 112 / max 151 (after the stacking rules: median 38 / max 44); tile-hexes (marks + pools under the fighters) median 110 / max 148.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 4 | Recast: Rime | - | 72 | 105 | 36 / 66 |
| 6 | Recast: Seam | GNGrfEDnxbRBgOHHCjPX3, Tempest Cleave | 80 | 144 | 0 / 142 |
| 10 | Etching: Heart, Etching: Rime, Doorward Sweep | Chakra Overflow, Earthen Bastion, GNGrfEDnxbRBgOHHCjPX3 | 76 | 104 | 72 / 30 |
| 11 | Etching: Heart, The Hush Rises, Doorward Sweep | Eclipse Drain, Wind Style: Sky Dragon | 49 | 151 | 108 / 40 |
| 16 | Recast: Rime | Wind Release: Whirlwind Demi, tZTvqYWiAc_OrY64nDvIo, Captain's Decree (equivalent | 72 | 111 | 0 / 108 |
| 17 | Recast: Seam | h-mvWaKK5vNNOwS5Y9KQj, Chakra Overflow, Earthen Bastion | 80 | 150 | 0 / 148 |

#### Act III v2 prototype (fable/mother-of-echoes-act3 f064d5dd, loop L5 trace), Act 3 (won, 16 rounds)

Per round: appear-hexes median 50 / max 120; loop-hexes median 120 / max 287 (after the stacking rules: median 11 / max 27); tile-hexes (marks + pools under the fighters) median 120 / max 286.

| Round | Boss side casts | Player casts | Appears (hexes) | Loops on screen (hexes) | Marks / pools under (hexes) |
|---|---|---|---|---|---|
| 4 | Facet Breaks, Hold Still | Shrapnel Clone Barrage, u9mXSgVW_QjkRzCejGXZ1 | 108 | 108 | 54 / 54 |
| 8 | Facet Breaks, The Silence Holds Her | Multi-Layered Gale, u9mXSgVW_QjkRzCejGXZ1 | 108 | 108 | 54 / 54 |
| 9 | No One Is Mended | tZTvqYWiAc_OrY64nDvIo, Tempest Cleave | 120 | 174 | 0 / 174 |
| 10 | Etching: Rime, The Hush Rises | Captain's Decree (equivalent, wE1QeldWTjls2Cf43cFjf | 47 | 167 | 36 / 130 |
| 11 | Every Name in the Glass | Shrapnel Clone Barrage, Wind Release: Whirlwind Demi | 120 | 287 | 156 / 130 |
| 12 | The Names Flood In: Rime | Dragon King's Impact, u9mXSgVW_QjkRzCejGXZ1 | 0 | 251 | 120 / 130 |

Not in the live catalogue (new in this spec, placeholder art or no art): Sayo:A Good Impression, Sayo:Every Line Through You, Sayo:Glassfall: First Echo, Sayo:Glassfall: Second Echo, Sayo:Hold Still, Sayo:Remainder Lancet, Sayo:The Names Flood In: Rime, Sayo:The Names Stir, Sayo:The Silence Holds Her.


### Busiest moments, composited and scored

Scores: (a) the hexes dangerous next turn are readable; (b) the player and bosses are findable; (c) the boss's state
(aura, guard, Cradle) reads. ✔ yes, ~ with effort, ✘ no. Coverage = share of the arena under any clip pixel (peak over
the 1.5 s), "3+ clips" = hexes with three or more clip records on them.

| Moment (GIF `stack/gif/<id>_{light,dark}.gif`) | Peak / mean coverage | Clip records | 3+ clips | (a) | (b) | (c) | What breaks |
|---|---|---|---|---|---|---|---|
| m1 Act I opening: Refraction marks + Lancet + Hush pools + Stillness | 28% / 12% | 134 | 9 | ✔ | ~ | ~ | the Stillness field (now 32-36 hexes round the moving Silence) puts 36 violet loops over both bosses; Hush pools land on Refraction lines and their newer tiles cover the mark tile |
| m2 Act I payoff: Refraction Breaks + Nothing Moves + Cradle + Grasp + Lucid | 29% / 14% | 152 | 28 | ~ | ~ | ✘ | Sayo carries Lucid + Cradle + the reflect buff at once; 27 bile pool loops start over last round's marks |
| m3 Act I: Facet (54) + The Silence Turns + likeness strike | 38% / 13% | 157 | 32 | ~ | ✔ | ~ | 54 heavy loops; the Silence Turns ring under the player is one of 61 identical heavy rings |
| m4 Act II: Recast + next Etching + The Glass Turns + Worn | 43% / 20% | 264 | 47 | ~ | ~ | ✘ | the Recast pool is a 40-hex bright bile block for 3 rounds; Hush Rises adds 10 bright pools a cast for 10 rounds; the library shield loop restacks on Sayo every Etching |
| m5 Act III: Every Name (117 heavy + 3 safe) + Breathless Pull on No One Is Mended | **68%** / 27% | 403 | **120** | ~ | ✘ | ✘ | every hex carries a heavy loop over a bile loop; the player and the Saint sit under 3 loops; the three safe diamonds are the only message and compete with 117 rims |
| m6 Act III: The Names Flood In over Every Name and No One Is Mended | **88%** / 58% | 591 | 117 | ✘ | ✘ | ✘ | the flood masks' clip squares overlap the refuge hexes, so the player on a safe hex is under masks for ~0.7 s; after it, 120 hexes bubble bile for 20 rounds |
| m7 Act III: Glassfall Second Pane over the First Pane's pools + Shatterfall pools | 52% / 30% | 303 | 49 | **✘** | ~ | ~ | the next pane's Act III heavy tile (obsidian, teal) disappears into dark pools on the dark board; the pool tile is created after the mark tile in the same cast and covers it where they overlap |
| m8 Act III v2: Silence Holds Her + Hold Still bar + etched stars + echo pane + next lines | 33% / 16% | 107 | 4 | ~ | ✔ | ✔ | two of three etched stars are under the still-floor field and the echo pane's pools; the Hold Still bar (heavy III) sits next to Act I echo lines (heavy I) and reads as part of them |

### Problems, ranked

1. **Persistent pool loops over the whole floor (Act III, Act II).** No One Is Mended lays 120 bile loops for 20 rounds;
   The Names Flood In 117 for 3; the Recasts 32-42 for 3; Hush Rises 10 a cast for 10 rounds. Every later telegraph sits
   under a bubbling field, and every loop draws over the fighters. Act III loop-hexes: median 102, max 397 a round.
2. **Act III telegraphs camouflaged.** The Remainder heavy tile is dark-on-dark beside dark pools; on the dark board the
   next Glassfall pane is unreadable (m7). The Hush Rises / Act II pool and Act III pools also share the bile glint.
3. **Field waves overlap the refuges.** A clip is 2.5 hex heights square, so a band on the hex next to a safe hex paints
   over it (m6). The safe hex, and the player standing on it, vanish for the payoff's length.
4. **Big mark fields as loops.** Every Name (117), The Held Breath (117), Facet (54), the Glassfall marks (36-42),
   Stillness (36), the Etchings (36-42): one loop per hex, all over the fighters. Peak coverage 68% (m5).
5. **Boss state buried.** The approved boss buffs (reflect on the Refraction marks, absorb on the Hush, shield on the
   Etchings and Shatterfall) still carry another event's library strips (`FZNt0vFGXlOZeagmPneqc` shove,
   `VMft99LeB_qQggEw_GrKi` barrier loop). They re-apply every cast and tag stacking is on, so 2-3 out-of-phase loops pile
   on the boss with Lucid and Cradle (m2, m4, m5). The spec at `3eb8abab` also makes the current generator refuse to
   build (an unmapped live strip); the stacking rules blank them.
6. **Stillness now follows the Silence (AOE_SPIRAL_SHOOT, range 3, up to 36 hexes).** A violet field the size of a third of
   the arena moves with her and covers both bosses in Act I (m1).
7. **Telegraph tiles hidden by later tiles.** Static art stacks newest on top: a Hush pool cast after a Refraction mark
   covers it; within one cast the pool effect is created after the next-pane mark (Glassfall) and covers it where they
   overlap.
8. **Hue collisions** (SAYO_BIBLE.md 5.1 grammar): Act III vein teal `#60d6ec` against safe cyan `#98d6e8` in Every Name
   and The Held Breath; ember yellow `#ffce54` on the Act II heavy rim against etch gold `#deb868` (the bible's heavy_ii
   tune, "add gold scoring", would make this worse: use the black crack only); the mend's gold motes against the etch
   (bible); violet `control_appear` on The Glass Falls Quiet, the rest beat (bible rewire).
9. **Act III v2:** the etched stars (lethal memory) can be covered by the still floor and the echo pools; the Hold Still bar
   needs its own read next to the Act I echo lines.

### Rules (visual budget and layering)

Layering priority: **telegraph > threat landing > boss state > flavour.**

1. **Pools: a tile, not a loop, above 10 hexes.** The tile under the fighters carries the warning; the arrival plays once.
   (`STACK_RULES["pool_loop_max"]`; reversible.)
2. **Mark fields: a tile, not a loop, above 30 hexes.** Lines and rings (Refraction 27, the follow rings 7, the Hold Still
   bar 3, safe hexes) keep their loops; fields keep the tile and the arrival. (`STACK_RULES["mark_loop_max"]`.) Where the
   whole board is marked, the loop belongs on the exception (the safe hexes), which keeps theirs.
3. **One payoff family per round on screen.** A field-wide wave (Glass Remembers, Flood, Glassfall, Shatterfall, Recast)
   does not share a round with another field-wide wave; a second big cast in the same snapshot keeps its tiles and drops
   its arrival.
4. **Refuges are never painted.** Pieces next to a safe hex must stay inside their own hex: the slice mosaic does this by
   construction (each hex paints only the pixels it owns), so Flood and the Glassfall panes move to slices first.
5. **Boss state rides one non-stacking carrier per act** (the entrance / aura buff). Recurring buffs carry no loop and no
   library appear.
6. **Telegraph tiles are created last** in their record (the next-pane mark after the pool), so the newest static art on
   a hex is the warning.
7. **Act III marks keep a lit edge:** the ember rim on the Remainder heavy tile must survive a dark pool under it (tune
   `tile_moe_heavy_iii_a3` / `heavy_appear_iii`: the bible's "arrive dark with teal veins" plus a 2 px ember rim).
8. **Every strip passes SAYO_BIBLE.md 5.7 on the stacked board,** not alone: the composite harness is the check.

### Applied now (reversible, visual only, no timing change)

- `push/mother_of_echoes.gen.py`: `Build(stack=True)` applies rules 1, 2 and 5 (loops off pools > 10 and mark fields > 30
  hexes; the library strips on the boss buffs blanked). Opt-in, so push/478 and the jobs that ran regenerate
  unchanged; the final tuning build passes `stack=True`. Effect on the traced runs (loop-hexes a round, median / max):
  Act I 40 / 122 → 13 / 41; Act II 112 / 151 → 38 / 44; Act III 102 / 397 → 8 / 24. After-renders: `stack/gif/*_after_*`.
- Entrances v2 (`anim_moe_entrance_*_a5`, below); the v1 strips and their ground rings are retired before upload.

### Requests for the sim agent (they change records the sim owns; outcomes must be re-confirmed)

- **R1 (rule 6):** reorder effects so a cast's next-pane / next-line mark comes after its pool effect (Glassfall panes,
  Lucid Refraction). Art order only; please confirm a fixed-seed rerun is identical.
- **R2 (problem 7):** keep the Hush's random pools off the current Refraction / Far Refraction lines (exclude those rows
  from `hushField` while a line mark is down, or draw from the off-line rows).
- **R3 (problem 6):** Stillness as the ring at distance 3 (or 2-3) round the Silence instead of the full spiral, so the
  field does not cover both bosses; or accept it with the loop off (applied).
- **R4 (rule 3):** no field-wide payoff in the same snapshot as another (The Held Breath + Shatterfall share rounds in Act
  III; Every Name + Breathless Pull).
- **R5 (rule 5):** one aura-carrying buff per boss that does not re-apply (the entrance carrier), and the recurring buffs
  without art.

### SAYO_BIBLE.md section 6 items that cause clutter or misreads (fix these first)

| Item | Clutter / readability effect | Priority |
|---|---|---|
| The Hush Rises pool (rewire: the bright pool) | bright bile across Act II for 10 rounds a cast, the same glint as the Recast pools | 1 |
| `anim_moe_heavy_appear_iii_a3` (tune) and the Act III heavy tile | the Act III telegraph disappears on dark pools (m7) | 1 |
| `anim_moe_lucid_aura_v1` (redo: duplicate orbit) | stacks with the Act I aura, Cradle and the reflect buff on Sayo (m2) | 2 |
| `anim_moe_control_glint_v1`, `anim_moe_breath_draw_v1` (1-2 px particles) | haze across the 36-hex Stillness field (now loop-off by rule 2) | 2 |
| The Glass Falls Quiet visual (`control_appear`, rewire) | the rest beat reads as a lock | 2 |
| `tile_moe_heavy_ii_a3` (tune) | Act II vs Act I: use the black crack, not gold scoring (etch-gold collision) | 3 |
| `anim_moe_mend_v1` (gold) | gold on a heal next to etch gold | 3 |
| `anim_moe_refraction_a3`, `anim_moe_quiet_v1`, `anim_moe_echo_strike_v1`, `anim_moe_rise_feeler_a3` | quality and material, not clutter | 4 |
| flourishes (`*_flourish_*_a3`) | superseded by the entrances v2 | done |

### Art direction: omens, payoffs, lingering ground (director, 2026-11-05; standing, overrides the per-hex drafts)

The director, on the Lancet and the Refraction line: "it seems you feel obligated to mimic the other set pieces in the
event and create individual tiles. We can paint a picture or tell a story with these. We can animate the ability as it
would appear on the battlefield, and the ground as it would appear in full because of the ability being used. We don't
need to mark each hex as unsafe toxic bubbles or use circles. Omens should use the normal language we've established
with the circles and marks on the ground, but the eruptions and real abilities should be like refraction."

1. **Omens** (telegraph marks, the round before) keep the established ground language: circles and marks on the hex,
   readable and consistent with the rest of Skyglass. Their job is clarity.
2. **Payoffs** (eruptions, breaks, Glassfall, Flood, Recasts, Shatterfall, An Absence's burst, every real ability) are
   painted as one picture of the ability happening across the whole area it affects, sliced across the hexes like the
   Refraction line.
3. **Lingering ground** (pools, No One Is Mended, the Hush, the flood residue, the splatter) shows the floor as it looks
   because the ability happened: one continuous painted surface (stained, frozen, cracked or blackened glass), no per-hex
   bubbles or circles, static or nearly so (stacking rules 1-2), reading "don't stand here" through the material, with
   the area's edge clear, never over a safe hex.

**Honest limits (engine, theninjarpg@3314d122):**
- *Payoffs on fixed board positions* (BATTLEFIELD patterns: the Refraction family, Etchings, Recasts, Glassfall,
  Flood, The Glass Remembers, Every Name) slice exactly: one visual tag per hex (or per column where rows repeat), each
  carrying its own slice; the cost is one asset per distinct slice (a 40-hex Recast region: 40).
- *Payoffs relative to her or the target* (CASTER / TARGET origins: Shatterfall Gives Way, The Silence Turns, An
  Absence, Hold Still): the offsets are added to her column as written, so a neighbour hex sits half a row higher or
  lower by her column's parity and exact slices tear on one of the two parities. What works: one large clip centred
  on the origin (2.5 hex heights, 1.25 hex widths) carrying the whole picture, plus a few overlapping per-hex pieces
  whose art is radially symmetric or vertical, so a half-row shift does not break the image. The picture's reach is
  bounded by that centre clip; beyond it the pieces are separate (they can share a continuous theme, not exact
  pixels).
- *Lingering ground* is static art (`staticAssetPath`) on the lasting effect: one asset per effect, drawn as the same
  tile on every hex of that effect. A per-hex unique painting would need one carrier effect per hex, which changes the
  records the sim owns. What works now: a **lattice-periodic surface**: one tile whose pattern repeats with the hex
  grid's period (column pitch 0.75 hexSize with the odd-column drop, row pitch one tile height), so the floor reads as
  one continuous painted surface across the area with no hex seams, and the area's edge is the hex boundary. Single
  scattered hexes (the Hush's random pools) are a patch of that surface on one hex.
- *Static loops* still draw over the fighters (3.2), so lingering surfaces stay static (rule 1-2); any life in them
  comes from the payoff's settle frames, not a loop.

### Ability quality bar: audit and worklist (director's standing directive, 2026-11-05)

"Every boss ability animation must look as cool as the Refraction slice-mosaic line." Read as a bar, not a technique:
fixed board patterns (BATTLEFIELD origin) are sliced; moves relative to her or the target (CASTER / TARGET origin,
CHARACTER, RANDOM, single-target, summons, auras) get per-hex pieces at the same craft: one strong idea from the bible's
verbs (SAYO_BIBLE.md 3), a clean read at 50 px, the held frame, anticipation → payoff → settle, nothing gaudy, nothing
clipped, and it must pass the stacked board (rules above). Ordered by how often a player sees it: boss casts counted
over the six seeded traces of `3eb8abab` (perfect and real, seeds 1-3) plus the director's two logs.

| # | Move (casts in traces) | Pattern → technique | Now | Verdict | When |
|---|---|---|---|---|---|
| 1 | Glass Lancet (64; every act) | single target → per-hex | `anim_moe_lancet_v2`: readable, generic | **upgrade**: the hand's verb (3.1), a glass needle drawn from the wall, a held glint, one cut | Friday |
| 2 | Refraction / Far Refraction marks (14) | BATTLEFIELD lines → **slice** | per-hex heavy ring + loop | **redo as slices**: light runs in from the walls along the line, the beam holds, the line sets as glass (the Refraction line's arrival) | Friday |
| 3 | Refraction / Far / Facet Breaks, Lucid Refraction (14) | BATTLEFIELD lines → **slice** | radial burst per hex (bible: redo) | **redo as slices**: the prototype line (director: 10/10); Facet mirrored across the hall | Friday |
| 4 | Facet marks (6) | BATTLEFIELD paired rows → **slice** | per-hex | **redo as slices** (paired rows, mirrored run) | Friday |
| 5 | The Hush, Unbridled, Hush Rises, Hush Where They Refused (94) | RANDOM → per-hex | bright bile pool appear, bile loop | **redo**: absence spreading (3.5): a dark pool wells up and closes inward; bible rewire (Hush Rises gets the dark pool); loop off over 10 hexes | Friday |
| 6 | Doorward Sweep, Cadet's Tether, Your Own Strike (62+) | single target → per-hex | one crescent for three actors (bible: redo) | **redo**: the Porter's sweep, Tomo's rope, the likeness's mirror slash | Friday (sweep), post-launch (others) |
| 7 | The Quiet (25) | single target → per-hex | 1 px dotted ring (bible: redo) | **redo**: ink lids closing | Friday |
| 8 | Etchings (75) | BATTLEFIELD regions → **slice** | per-hex lattice cut | **redo as slices**: the scribe carves the region in one sequence (3.3) | Friday |
| 9 | Recasts (46) | BATTLEFIELD regions (ground casts) → **slice** | per-hex `anim_moe_recast_a3` | **redo as slices**: the remembered region breaks as one wave, black cracks creeping (bible open decision 5) | Friday |
| 10 | Shatterfall marks (23) / Shatterfall Gives Way (21) | CASTER cone → per-hex | the Gives Way wave is the bible's quality bar | **keep** the wave; tune the cone's marks (Act III heavy, rule 7) | Friday (marks) |
| 11 | The Held Breath (13), Every Name in the Glass (7) | BATTLEFIELD field + 3 safe → **slice** | per-hex rings over 117 hexes | **redo**: the field as one slice (the floor goes still), the safe hexes stay their own pieces; loops off (rule 2) | post-launch |
| 12 | Grasp (12), Cradle (8) | single target / ally → per-hex | Grasp reads; Cradle loop reads | **keep**, polish post-launch | post-launch |
| 13 | The Silence Turns (6), The Glass Turns (9) | AOE_CIRCLE_SPAWN → per-hex | heavy ring per hex | **upgrade**: dark closes in on the player (draft `close_in`), held, mark lands; flexible for the pending mark + eruption change | Friday |
| 14 | Stillness (6), Nothing Moves (4) | spiral round the Silence / CHARACTER → per-hex | violet field, ink burst | **upgrade**: the ring closes inward (draft `still`), loop off (rule 2) | post-launch |
| 15 | The Glass Falls Quiet (9) | 3 hexes | violet lock on the rest beat (bible: rewire) | **rewire** to a calm cyan breath | Friday (wiring) |
| 16 | Summons: The Listening, Raise the Worn, Your Likeness (32) | EMPTY_GROUND single → per-hex | rises; feeler is Heartglass cyan (bible: tune) | **tune** feeler to Remainder; keep the others | post-launch |
| 17 | Worn Mending (9) | ally → per-hex | gold motes (bible: tune) | **tune** to ash and rose | post-launch |
| 18 | The Names Flood In (6), Glassfall panes (2+), The Glass Remembers | BATTLEFIELD → **slice** | waves (per-hex delays) | **upgrade to slices** (rule 4: refuges never painted) | post-launch |
| 19 | No One Is Mended (2), The Long Hush (2) | BATTLEFIELD field | pool tile; no final-stand art | **add** the Long Hush stand loop (bible missing) | post-launch |
| 20 | Entrances v2, auras | self → per-hex | v2 restrained (this pass); Saint aura shards read as triangles | **tune** the Saint aura; wire with the sim's carrier | with R5 |
| 21 | Act III v2: Hold Still bar, The Silence Holds Her, etched stars, echo panes | TARGET bar / self / BATTLEFIELD | placeholders (Act III heavy, Cradle, etch, glassfall) | Hold Still: its own still-bar piece; echo panes as slices of the act they echo; stars kept clear of fields (problem 9) | with Act III v2 (post-launch unless it ships Friday) |

**At the bar now:** Shatterfall Gives Way's wave, the Refraction line prototype (not wired). **Friday's tuning job:** rows
1-10, 13, 15 (by frequency). **Post-launch:** 11, 12, 14, 16-21. Batches go to the director as GIFs as each finishes.

### Entrances v2 and the slice upgrade

The director judged the first entrances "far too large and gaudy, especially since the bosses spawn in together; they
clip". v2 (`build_fx_a4.py` `entrances2`, `anim_moe_entrance_{sayo1,silence,sayo2,saint}_a5`): 20 frames, inside her own
clip (a build check fails any frame within 2 px of the edge), no ground ring, the bible 3.7 brief and beat: Act I the
fan opens pane by pane round her flanks, the rim heats, a held beat, one white frame, three prismatic 2 x 2 glints; the
Silence's shadow peels up into an ink hood, a held violet rim, frozen dust only; Act II the fan's panes, a black crack
runs through them, a white-gold frame, the gold scores draw and dim; Act III the ink folds into her, held, one teal-white
frame, a small halo of hooked thorns. Both Act I bosses enter on the same tick without crowding
(`scratchpad/custom/review5/`). Wiring is unchanged (`moe_entrance` / `moe_aura` slots; the carrier is the sim's
once-per-act buff, R5). The fixed-position set pieces (Refraction / Far Refraction / Facet marks and breaks, Etchings,
Recasts, Stillness) go to slice mosaics at the Refraction line's standard next, with rule 4 built in.

## Jutsu icons: six families for 53 jutsu

The Skyglass event shipped 4 icons across every AI kit; these are AI-only jutsu nobody equips. Six family icons (ME21-ME26) cover all 53, one technique silhouette each; the per-jutsu `@img:jutsu_moe_*.webp` slots in `artPlaceholders` all point at their family file (one upload per family). The table above lists every jutsu per family with its live id.

## The Etching mark (tg_etch) and its Recast

- **Shape:** a lattice of straight scored lines through each hex's opposite edge midpoints. The lines meet their neighbours' exactly, so a marked region reads as one etched sheet with no hex seams. No ring (heavy, control), no pool (linger), no star (safe).
- **Palette:** warm white into pale gold, a new family for a new threat (a delayed hit you must remember). Ember, violet, bile and cyan stay with their meanings.
- **Loop:** scribe sparks run out along the lattice and the side junctions twinkle on the shared 0.8 s beat, keeping clear of player portraits. A sparse dither tints the region, denser at the centre.
- **Recast pairing:** the Recast hit replays the same lattice in white-gold on its first frames before glass blades rise along it, so the hit reads as the mark coming due. The guard-open loop it leaves uses the same glass and gold.
- **Wiring:** the art push sets `moe_lull` on The Glass Falls Quiet's `fleeprevent` effect (not the `visual`); this is a slot move in the jutsu edit, not a mechanics change. Replace `TG_STANDIN = {"tg_etch": "tg_control"}` in `push/mother_of_echoes.gen.py` with a `TG["tg_etch"]` entry once the two assets are created and unhidden (law 16c).

## Code-built exports and previews

- **Builder:** `art/mother_of_echoes_fx/build_fx.py` (Pillow only). Exports are in `art/mother_of_echoes_fx/exports/` with fresh names (law 32). `moe_fx_v1.json` gives frames, speed (50 ms), use and bytes for each asset create.
- **Preflight:** `artpreflight.py --type STATIC` on the tile and `--type ANIMATION` on the 12 strips: 0 errors, 0 warnings. Reports are in `art/mother_of_echoes_fx/_provenance/`, with `SHA256SUMS`.
- **Previews:** `docs/design/mother_of_echoes_fx/preview.py` renders each export on the battle still at pixi sizes: a 165 px clip on a 132 x 66 hex, tiles stretched to the hex.
  - Outputs: `keys_<asset>.png` and `moe_fx_battle.mp4`.
  - The Etching field is shown beside tg_heavy, tg_control, tg_linger and tg_safe on the light (snow) board, for distinctness and contrast.
  - Breathless Pull plays beside three tg_safe tiles, which it leaves clear. Lucid and the lull are shown on an AI-sized portrait.

## Open questions and limits

1. **ICON scaffold:** `spec.prompt_scaffolds.ICON` asks for a "dark background", but the ICON target pads transparent and preflight requires alpha. The icon cards therefore reuse the Skyglass IC/VT/VS lines (the shards' live siblings). The scaffold needs an art-direction fix.
2. **AI_AVATAR scaffold:** it repeats the accent clause and lists "no props". Sayo's lancet, the Porter's lantern and Tomo's wooden sword may be dropped; check this at raw QC. The Silence and the Feeler are not "ninja characters", so they use the FX raw-layer card.
3. **VT00_approved.png** is not in the repo; the register says VT00 was NOT NEEDED. ME18 and ME19 also attach a delivered VT token as the base, in case the director has no VT00 file.
4. **The Remainder:** ME19's token motif must follow the director's ME20 art, which is in progress.
5. **New palette:** the Etching's gold-white family and the five uber-only strips that replaced the Crownhold reuse are art-direction calls for the director to confirm. `SKYGLASS_BOSS_ANIMATIONS.md` is the canonical owner of the danger language and should gain the tg_etch row when it is approved.
6. **AI portraits:** they are 1.6 hex-heights across (player pins 1.2), so the portrait-clear loops clear player portraits only.
7. **Preview limits:** the battle still is a three.js-era capture rescaled to pixi geometry, and its token is approximate. `artpreflight.py` cannot check per-frame squareness (no `--frames`); `build_fx.py` asserts it.
