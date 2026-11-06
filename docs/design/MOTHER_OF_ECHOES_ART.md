# The Mother of Echoes: complete art list

- **For:** the director (generation) and Fable (code-built FX, intake, upload manifests). **Prompts:** `docs/handoffs/MOTHER_OF_ECHOES_ART_PROMPTS.md` (codes ME01-ME28).
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
or below by her column's parity). The 12 assets are created HIDDEN by the final tuning job (`fx4_create_items`,
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
