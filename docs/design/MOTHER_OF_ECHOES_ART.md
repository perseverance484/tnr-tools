# The Mother of Echoes: complete art list

- **For:** the director (generation) and Fable (code-built FX, intake, upload manifests). **Prompts:** `docs/handoffs/MOTHER_OF_ECHOES_ART_PROMPTS.md` (codes ME01-ME28).
- **Records:** ids from the committed results bundles (417, 440, 461-464), collected in `docs/handoffs/mother_of_echoes_record_ids.json`. Art slots: `artPlaceholders` in `harness/skyglass_wreck_sim/mother_of_echoes_spec.json` at `fable/mother-of-echoes-sim@dd7e33ab` (the generator's `SPEC_REF`).
- **Canon:** RUL-2026-11-01-093..095, RUL-2026-11-02-108 (names); cut and not drawn: An Invitation in Glass, Remnant of the Mother Glass, all Salvage art (RUL-2026-11-02-104/-105).
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
"code" rows are built in this repo with Pillow (`art/mother_of_echoes_fx/build_fx.py`); 4 of them re-export director-drawn Skyglass boss strips that were never uploaded. Every code-built file is already exported and preflighted.

## Recommendation: Sayo is one design in three looks

One design, three files. ME01 (Act I) is generated first and locks her face, build, coat and lancet; ME03 (Act II) and ME04 (Act III) attach the approved ME01 as SUBJECT and change only what each act says (the glass climbs and is etched; then it goes dark and the feelers take her). Players see the same woman change across the fight, which is the story (RUL-094: she succumbs to the Silence), and the act boundary still reads at a glance. One shared file would hide the acts; three separate designs would lose her. Fallback if time runs out: Act II reuses the Act I file (ME03 is P1 but the cheapest to defer).

## Assets

| Asset / slot | What it is | Target | Attaches to | Priority | Source | Source detail |
|---|---|---|---|---|---|---|
| `avatar_moe_sayo.webp` | Sayo, Mother of Echoes: Act I boss | AI_AVATAR | AI `fJLcH1mpB1XHHGtNWwvzD` | P1 | director | ME01 |
| `avatar_moe_silence.webp` | The Silence: Act I boss | AI_AVATAR | AI `IhNR-W1FElTsrWw1KfuQ9` | P1 | director | ME02 |
| `avatar_moe_sayo-stilling.webp` | Sayo, Glasswright of the Stilling: Act II boss | AI_AVATAR | AI `H3pNj2qUWpMpVRINiH6Vn` | P1 | director | ME03 |
| `avatar_moe_saint.webp` | Sayo, Saint of Stillness: Act III boss | AI_AVATAR | AI `k0hgSrghl_KcYs9ATVDJT` | P1 | director | ME04 |
| `avatar_moe_feeler.webp` | A Feeler of the Deep: summon (The Listening) | AI_AVATAR | AI `qFKcwTUkBtRiC-uM_8xG8` | P1 | director | ME05 |
| `avatar_moe_likeness.webp` | Your Likeness: summon (Your Likeness) | AI_AVATAR | AI `zyOeF-rSpeXuMU7A3QQgo` | P1 | director | ME06 |
| `avatar_moe_worn-porter.webp` | The Gate Porter (Worn): summon | AI_AVATAR | AI `wivZbMygCZo6c9pRKWvCI` | P1 | director | ME07 |
| `avatar_moe_worn-hana.webp` | Sister Hana (Worn): summon | AI_AVATAR | AI `g6bNcftMcQ9pV_nMki7Wv` | P1 | director | ME08 |
| `avatar_moe_worn-tomo.webp` | Cadet Tomo (Worn): summon | AI_AVATAR | AI `KhFglnxE7ouIDywet3BPB` | P1 | director | ME09 |
| `scene_bg_moe_heart_of_the_mother_glass.webp` | The Heart of the Mother Glass | SCENE_BACKGROUND | quest IBPNwhAzlAJPXoeEnp8gW content, d_open, b_act1, f_lost | P1 | director | ME10 |
| `scene_bg_moe_the_stilling.webp` | The Heart of the Mother Glass, the Stilling | SCENE_BACKGROUND | quest IBPNwhAzlAJPXoeEnp8gW d_act2, b_act2 | P2 | director | ME11 |
| `scene_bg_moe_a_good_impression.webp` | The Heart of the Mother Glass, A Good Impression | SCENE_BACKGROUND | quest IBPNwhAzlAJPXoeEnp8gW d_act3, b_act3, w_clear | P2 | director | ME12 |
| `quest_icon_mother_of_echoes.webp` | Quest icon | ICON (quest.image) | quest `IBPNwhAzlAJPXoeEnp8gW` | P1 | director | ME13 |
| `icon-shard-of-the-keel.webp` | Shard of the Keel (dropping live now) | ICON | item `uKnlqlfyE_k1QjLuaVml_` | P1 | director | ME14 |
| `icon-shard-of-the-crown.webp` | Shard of the Crown (dropping live now) | ICON | item `4UNvgWIDGD9QpNVtLr1aM` | P1 | director | ME15 |
| `icon-shard-of-the-tide.webp` | Shard of the Tide (dropping live now) | ICON | item `KHGZAfQFosLQJ29AN2ymC` | P1 | director | ME16 |
| `icon-shard-of-the-ledger.webp` | Shard of the Ledger (dropping live now) | ICON | item `cGrmhfe88ACBvFk2XqvSu` | P1 | director | ME17 |
| `icon-variant-token-heartglass.webp` | Heartglass token (VT base, window motif) | ICON | item `FmQgVG5IX3q607wcHcOGy` | P1 | director | ME18 |
| `icon-variant-token-the-remainder.webp` | The Remainder token (VT base, window motif) | ICON | item `xCAtBCvbA2-TTV2eSe-jx` | P1 | director | ME19 |
| `icon-variant-heartglass.webp` | Heartglass variant (final) | ICON (item-variant image) | itemVariant `s_UZJAJ2LR_qDTKAu7l5-` | P1 | reuse live | already on the variant since push/417; nothing to do |
| `icon-variant-the-remainder.webp` | The Remainder variant (director in progress) | ICON (item-variant image) | itemVariant `f1trw5TAP7ItE-E7eh8b0` | P1 | director | ME20 |
| `jutsu_moe_fam_lancet.webp` | Glass Lancet (jutsu family icon) | JUTSU_ICON | Covers: Glass Lancet `0g0Iy9PKsIVC6ggG1Exz2`; The Glass Remembers `G_b5yaxm6GMOuQ3eaofKb`; Lucid `IOUn-UrO1gwbi4uJdwYDp` | P2 | director | ME21 |
| `jutsu_moe_fam_refraction.webp` | Refraction (jutsu family icon) | JUTSU_ICON | Covers: Refraction `yxP6zO2NmjwqnrnvNXipC`; Far Refraction `HIftLq_RQJkIUUqGgBPTE`; Facet `eYzXEQI-Vz3gSIDfP2sX3`; Refraction Breaks `qjtaZInyr1nZ5lZmSA_SS`; Far Refraction Breaks `OTcP-08or5bUKwcMjc54K`; Facet Breaks `xlmvVot9xaetibexfyc31`; Lucid Refraction `KfXRK6rC3bt4kpdtdJHDb`; Every Name in the Glass `LhyIGAqoerbh3tFbcPrdx`; The Names Flood In `4_dlB0conB-C6sfYqiU6Q` | P2 | director | ME22 |
| `jutsu_moe_fam_etching.webp` | Etching (jutsu family icon) | JUTSU_ICON | Covers: Etching: Rime `lkcsor1I5A8gD038ncrBW`; Etching: Ember `eovhl9XyDQq1N19lDwr77`; Etching: Seam `Pr7i3DK5KiRQRePy8Xw41`; Etching: Heart `nNUaP5r8r7UxYNiAtuF0l`; Etching: Hail `2pU7fdUPQPQQjyd19JDWA`; Recast: Rime `Avu4B2M_9_SE0-Oqqhplw`; Recast: Ember `I5lwaFCaVSH6cpxAPHvFA`; Recast: Seam `54nmWiFXqvFW7u0vSG5zK`; Recast: Heart `-MtfLHClmIwSSGBIw9O7X`; Recast: Hail `lmlhn5p68Oszhj16wKbvx` | P2 | director | ME23 |
| `jutsu_moe_fam_glassfall.webp` | Glassfall (jutsu family icon) | JUTSU_ICON | Covers: Shatterfall `RcMx3MCHD7dyJw_12mr_7`; Shatterfall Gives Way `cxqu1ljkSisTgPBLgYtJa`; Glassfall: First Pane `kzxTPUJ8TYJFTggSKw3zr`; Glassfall: Second Pane `6IMcG7R_uhfROlANlYmDB`; Glassfall: Last Pane `H0MMi_Stpzk8zm4HqDEbF`; Glassfall: Opening Pane `pp40FDDTbGMdwrDFTNyiF`; Glassfall: Heart Recast `3ytuMbHhF4bcE2zrePnlR` | P2 | director | ME24 |
| `jutsu_moe_fam_hush.webp` | The Hush (jutsu family icon) | JUTSU_ICON | Covers: The Hush `kfzxZHje97anmOwwph84l`; The Hush, Unbridled `VqSpJhDUvjxLP5OtjI1mc`; The Hush Rises `F5qD1aXjt-kPQ6IR7nDoo`; Hush Where They Refused `AMNfIbTUiKsnvNfZGpAf1`; No One Is Mended `BA9V_vlnJZhA0V2tY4Ov_`; The Quiet `w6eHg1zFOrP1AhlwtyfZV`; The Long Hush `2erO3JCcfpXixrGz0NmhH`; The Glass Falls Quiet `KIwfifD8OGNVbs9I8O6Rw`; Stillness `A8c_3evIw6fOfnmKIkTgb`; Nothing Moves `scGyJW-F0Mqga4FXnj4Jf`; The Held Breath `3ShDcIL5dzj_8w60Qoo9h`; Breathless Pull `83mLMXND-9sAyN5WfmzQo`; The Listening `mqko5kLLXqGAVr6MVoKY0`; The Listening, Unbridled `q0QcFoX4HIhxO0cpYTL2N`; Cradle `DFcbOLSvYssjLzTHo_dw0`; Grasp `zHNAEQ1xmDSOzFVEqeJlS` | P2 | director | ME25 |
| `jutsu_moe_fam_echoes.webp` | Echoes (jutsu family icon) | JUTSU_ICON | Covers: Your Likeness `foDwd-hL5krmhFHsPtQtc`; Your Own Strike `nkNryj61h6qB3azifb8h4`; Raise the Gate Porter `l1TpeIKJyNDzQQkI1Az1K`; Raise Sister Hana `BeOpXT1M_7oRkwYCcXk6Z`; Raise Cadet Tomo `yzI6KIOPzy6P2B0U6Cqyp`; Doorward Sweep `x4aJMqXJ3kvyr0bKUZaZj`; Worn Mending `tEAiiOTcd7rTgu-nJySPv`; Cadet's Tether `rC9J4ZrjMfftPa4UmlBoV` | P2 | director | ME26 |

### Animations (the 18 named `moe_*` slots plus `tg_etch`)

| Slot | What it is | Target | Jutsu | Priority | Source | Source detail |
|---|---|---|---|---|---|---|
| `tg_etch` | Etching mark, still tile (staticAssetPath, under the characters) | STATIC tile | Etching: Rime `lkcsor1I5A8gD038ncrBW`; Etching: Ember `eovhl9XyDQq1N19lDwr77`; Etching: Seam `Pr7i3DK5KiRQRePy8Xw41`; Etching: Heart `nNUaP5r8r7UxYNiAtuF0l`; Etching: Hail `2pU7fdUPQPQQjyd19JDWA` | P1 | code | `art/mother_of_echoes_fx/exports/tile_moe_etch_v1.webp` (built now; replaces the tg_control stand-in in push/mother_of_echoes.gen.py TG_STANDIN) |
| `tg_etch` | Etching mark, loop (staticAnimation) | ANIMATION | same 5 Etchings | P1 | code | `anim_moe_etch_glint_v1.webp` (built now) |
| `tg_etch` | Etching mark, appear / disappear | ANIMATION | same 5 Etchings | P1 | reuse live | `bJy2IjRKmAVYEoXUYmXv5` / `k8J4ic-KEz9ewEq1gAszr` (as every live mark, push/431) |
| `moe_recast` | Recast hit: the lattice flashes back, glass blades rise and shatter | ANIMATION (appear) | Recast: Rime `Avu4B2M_9_SE0-Oqqhplw`; Recast: Ember `I5lwaFCaVSH6cpxAPHvFA`; Recast: Seam `54nmWiFXqvFW7u0vSG5zK`; Recast: Heart `-MtfLHClmIwSSGBIw9O7X`; Recast: Hail `lmlhn5p68Oszhj16wKbvx` | P1 | code | `anim_moe_recast_v1.webp` (built now; pairs with tg_etch) |
| `moe_refraction` | Refraction / Facet breaks (heavy-mark payoff) | ANIMATION (appear) | Refraction Breaks `qjtaZInyr1nZ5lZmSA_SS`; Far Refraction Breaks `OTcP-08or5bUKwcMjc54K`; Facet Breaks `xlmvVot9xaetibexfyc31`; Lucid Refraction `KfXRK6rC3bt4kpdtdJHDb` | P1 | reuse live | Skyglass Blast - Eruption `Z9j8J7ZmAjiaxH2S4nDy8` (dt_heavy) |
| `moe_shatterfall` | Shatterfall Gives Way | ANIMATION (appear) | Shatterfall Gives Way `cxqu1ljkSisTgPBLgYtJa` | P1 | reuse live | Skyglass Blast - Crystal Shard `TAu9k8ifgteP6HBofoKn7` (dt_shard) |
| `moe_glassfall` | Glassfall panes (hit, then the next pane is marked) | ANIMATION (appear) | Glassfall: First Pane `kzxTPUJ8TYJFTggSKw3zr`; Glassfall: Second Pane `6IMcG7R_uhfROlANlYmDB`; Glassfall: Last Pane `H0MMi_Stpzk8zm4HqDEbF`; Glassfall: Opening Pane `pp40FDDTbGMdwrDFTNyiF`; Glassfall: Heart Recast `3ytuMbHhF4bcE2zrePnlR` | P1 | reuse live | Crystal Shard `TAu9k8ifgteP6HBofoKn7` (dt_shard) |
| `moe_flood` | The Names Flood In (heavy field payoff) | ANIMATION (appear) | The Names Flood In `4_dlB0conB-C6sfYqiU6Q` | P1 | reuse live | Eruption `Z9j8J7ZmAjiaxH2S4nDy8` (dt_heavy); optional signature upgrade below |
| `moe_stillness` | Nothing Moves (control-mark stun payoff) | ANIMATION (appear) | Nothing Moves `scGyJW-F0Mqga4FXnj4Jf` | P1 | code | `anim_moe_stillness_v1.webp`: re-export of `anim_chain_wrap_v1.webp` (violet lock; RUL-2026-10-30-061 item 10 already chose it as the violet blast) |
| `moe_breathless` | Breathless Pull (control-mark pull + stun payoff) | ANIMATION (appear) | Breathless Pull `83mLMXND-9sAyN5WfmzQo` | P1 | code | `anim_moe_breathless_v1.webp`: re-export of `anim_command_absolute_v1.webp` (chains lock, seal stamps) |
| `moe_hush_floor` | No One Is Mended floor (healing cut pool) | STATIC tile + ANIMATION | No One Is Mended `BA9V_vlnJZhA0V2tY4Ov_` | P1 | reuse live | Lingering Pool tile `PoG_KDERWlvyj7MsKSDW2` (staticAssetPath), bubbles `qlGYJizxxxdd794Jea6lB` (staticAnimation), appear `bJy2IjRKmAVYEoXUYmXv5`: map as tg_linger |
| `moe_guard_open` | Guard open: the Recast weakness on the hit player | ANIMATION (static loop) | Recast: Rime `Avu4B2M_9_SE0-Oqqhplw`; Recast: Ember `I5lwaFCaVSH6cpxAPHvFA`; Recast: Seam `54nmWiFXqvFW7u0vSG5zK`; Recast: Heart `-MtfLHClmIwSSGBIw9O7X`; Recast: Hail `lmlhn5p68Oszhj16wKbvx` | P2 | code | `anim_moe_guard_open_v1.webp` (built now; portrait-clear) |
| `moe_quiet` | The Quiet hit | ANIMATION (appear) | The Quiet `w6eHg1zFOrP1AhlwtyfZV` | P2 | code | `anim_moe_quiet_v1.webp` (built now) |
| `moe_lancet` | Glass Lancet hit | ANIMATION (appear) | Glass Lancet `0g0Iy9PKsIVC6ggG1Exz2` | P2 | code | `anim_moe_lancet_v1.webp` (built now) |
| `moe_enrage` | The Glass Remembers (round-30 enrage hit) | ANIMATION (appear) | The Glass Remembers `G_b5yaxm6GMOuQ3eaofKb` | P2 | reuse live | Eruption `Z9j8J7ZmAjiaxH2S4nDy8` |
| `moe_lucid` | Lucid (Sayo enrage buff aura) | ANIMATION (static loop) | Lucid `IOUn-UrO1gwbi4uJdwYDp` | P2 | code | `anim_moe_lucid_v1.webp`: re-export of `anim_crown_aura_v1.webp` (shard ring, portrait-clear) |
| `moe_likeness` | Your Likeness summon flourish | ANIMATION (appear) | Your Likeness `foDwd-hL5krmhFHsPtQtc` | P2 | code | `anim_moe_echo_rise_v1.webp`: re-export of `anim_recall_v1.webp` (an echo pulled from the glass) |
| `moe_worn` | Raise the Worn summon flourish | ANIMATION (appear) | Raise the Gate Porter `l1TpeIKJyNDzQQkI1Az1K`; Raise Sister Hana `BeOpXT1M_7oRkwYCcXk6Z`; Raise Cadet Tomo `yzI6KIOPzy6P2B0U6Cqyp` | P2 | code | same file as moe_likeness |
| `moe_feeler` | The Listening summon flourish | ANIMATION (appear) | The Listening `mqko5kLLXqGAVr6MVoKY0`; The Listening, Unbridled `q0QcFoX4HIhxO0cpYTL2N` | P2 | code | `anim_moe_feeler_v1.webp` (built now) |
| `moe_cradle` | Cradle (the Feeler shields its boss) | ANIMATION (static loop) | Cradle `DFcbOLSvYssjLzTHo_dw0` | P2 | director | ME27 raw layer, then animated in code (not built yet) |
| `moe_lull` | The Glass Falls Quiet (breath between cycles) | ANIMATION (static loop) | The Glass Falls Quiet `KIwfifD8OGNVbs9I8O6Rw` | P3 | code | `anim_moe_lull_v1.webp` (built now). Rides a `visual` effect, which the server drops at the next action (RUL-2026-11-02-101), so it is barely seen |
| `moe_flood` (upgrade) | The Names Flood In, signature version (faces alight) | ANIMATION (appear) | The Names Flood In `4_dlB0conB-C6sfYqiU6Q` | P3 | director | ME28 raw layer, animated in code; optional |

Already wired and live, no work: `tg_heavy`, `tg_control`, `tg_linger`, `tg_safe` (push/431 tiles and loops, `state/skyglass_fx/asset_ids.json`), and the library hits the spec names by id (`dBatQkc1Ts2ask5ZN-A3p` pierce, `FZNt0vFGXlOZeagmPneqc` shove, `I9aYhT5wMB` heal, `bJy2IjRKmAVYEoXUYmXv5` / `k8J4ic-KEz9ewEq1gAszr` appear/vanish). No scene characters: the quest shows the Blank Scene Character by design.

## Jutsu icons: six families for 53 jutsu

The Skyglass event shipped 4 icons across every AI kit; these are AI-only jutsu nobody equips. Six family icons (ME21-ME26) cover all 53, one technique silhouette each; the per-jutsu `@img:jutsu_moe_*.webp` slots in `artPlaceholders` all point at their family file (one upload per family). The table above lists every jutsu per family with its live id.

## The Etching mark (tg_etch) and its Recast

- **Shape:** a lattice of straight scored lines through each hex's opposite edge midpoints. The lines meet their neighbours' exactly, so a marked region reads as one etched sheet with no hex seams. No ring (heavy, control), no pool (linger), no star (safe).
- **Palette:** warm white into pale gold, a new family for a new threat (a delayed hit you must remember). Ember, violet, bile and cyan stay with their meanings.
- **Loop:** scribe sparks run out along the lattice and the side junctions twinkle on the shared 0.8 s beat, keeping clear of player portraits. A sparse dither tints the region, denser at the centre.
- **Recast pairing:** the Recast hit replays the same lattice in white-gold on its first frames before glass blades rise along it, so the hit reads as the mark coming due. The guard-open loop it leaves uses the same glass and gold.
- **Wiring:** replace `TG_STANDIN = {"tg_etch": "tg_control"}` in `push/mother_of_echoes.gen.py` with a `TG["tg_etch"]` entry once the two assets are created and unhidden (law 16c).

## Code-built exports and previews

- **Builder:** `art/mother_of_echoes_fx/build_fx.py` (Pillow only). Exports are in `art/mother_of_echoes_fx/exports/` with fresh names (law 32). `moe_fx_v1.json` gives frames, speed (50 ms), use and bytes for each asset create.
- **Preflight:** `artpreflight.py --type STATIC` on the tile and `--type ANIMATION` on the 11 strips: 0 errors, 0 warnings. Reports are in `art/mother_of_echoes_fx/_provenance/`, with `SHA256SUMS`.
- **Previews:** `docs/design/mother_of_echoes_fx/preview.py` renders each export on the battle still at pixi sizes: a 165 px clip on a 132 x 66 hex, tiles stretched to the hex.
  - Outputs: `keys_<asset>.png` and `moe_fx_battle.mp4`.
  - The Etching field is shown beside tg_heavy, tg_control, tg_linger and tg_safe for the distinctness check.

## Open questions and limits

1. **ICON scaffold:** `spec.prompt_scaffolds.ICON` asks for a "dark background", but the ICON target pads transparent and preflight requires alpha. The icon cards therefore reuse the Skyglass IC/VT/VS lines (the shards' live siblings). The scaffold needs an art-direction fix.
2. **AI_AVATAR scaffold:** it repeats the accent clause and lists "no props". Sayo's lancet, the Porter's lantern and Tomo's wooden sword may be dropped; check this at raw QC. The Silence and the Feeler are not "ninja characters", so they use the FX raw-layer card.
3. **VT00_approved.png** is not in the repo; the register says VT00 was NOT NEEDED. ME18 and ME19 also attach a delivered VT token as the base, in case the director has no VT00 file.
4. **The Remainder:** ME19's token motif must follow the director's ME20 art, which is in progress.
5. **New palette:** the Etching's gold-white family and the four re-exported boss strips are art-direction calls for the director to confirm. `SKYGLASS_BOSS_ANIMATIONS.md` is the canonical owner of the danger language and should gain the tg_etch row when it is approved.
6. **AI portraits:** they are 1.6 hex-heights across (player pins 1.2), so the portrait-clear loops clear player portraits only.
7. **Preview limits:** the battle still is a three.js-era capture rescaled to pixi geometry, and its token is approximate. `artpreflight.py` cannot check per-frame squareness (no `--frames`); `build_fx.py` asserts it.
