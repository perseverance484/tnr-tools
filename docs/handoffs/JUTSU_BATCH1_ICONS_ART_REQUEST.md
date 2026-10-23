# Art request: jutsu upgrade batch 1 icons (10)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude Code, at dauntless's request (2026-10-23)
- **Direction (director, 2026-10-23):** the ten most-used NORMAL jutsu not yet upgraded get a premium icon, as the event
  jutsu did (`docs/design/jutsu_overhaul/PRIORITY_TARGETS_2026-10-23.md`). The silhouettes below are proposals; the
  director's visual approval of each raw locks it.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one jutsu per generation session). Spec:
  `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `JUTSU_ICON` (opaque allowed). Worked example of this
  exact direction: `docs/handoffs/SCROLL_JUTSU_ICONS_ART_REQUEST.md` (all ten delivered and approved 2026-10-23).
- **Text it must echo:** `docs/design/jutsu_overhaul/BATCH1_TEXT_DRAFTS.md` (draft; the icon follows the battle line's image).
- **Current icons:** `art/jutsu_icons/batch1/originals_live/` (predecessor record for the director; **never attach to a
  generation session**).
- **Delivery:** raws to `art/jutsu_icons/batch1/raws/`, exports (256x256 lossless WebP) to `art/jutsu_icons/batch1/exports/`.
- **Live-game requests/writes:** 0.

**Delivered:** 0/10.

## 1. Why

All ten current icons are the old style: a posed ninja in a full landscape scene. At 32 to 64 px the technique is a smudge
next to an actor. Together these ten are used about 240,000 times in battle (public stats, 2026-10-23); they are among the
icons players see most.

## 2. Collection-wide visual lock

- **One bold emblem that is the ability's metaphor** (the BEE lesson): the energy or object itself is the subject, filling
  the frame and glowing against dark space. Never a diagram of the mechanics. Reference: `art/style_refs/jutsu_icons/bee/`.
- **No actor:** no ninja, face, body, hands or limbs (the Clone Technique emblem is two chakra flames, not two people).
- **Bounded emblem:** a shape glowing against dark negative space, never a texture that fills the frame edge to edge.
  Check every raw at 32 px before approving.
- **Rendering:** the approved JUTSU_ICON standard: detailed pixel art, crisp edges, strong rim light, luminous core, high
  contrast; full-bleed dark atmosphere in the jutsu's palette.
- **Avoid:** text, kanji, runes, frames, scrolls, franchise insignia, mandatory mandalas or eye emblems, and every
  silhouette reserved below or in the scroll-jutsu set (razor-wind ring, stone rampart, droplet spiral, fire dragon,
  crescent moon with dew, black sun, hooded ash shroud, magenta vortex, green flame pillar, demon palace) and the starter
  set (three senbon, chakra afterimage, ember shield, crescent cut with shock rings, spectral chains, venom dread-mask).
  The set already has three spirals; **none of these ten is a spiral or vortex.**

## 3. Targets and distinction ledger

Pass the other silhouettes as **text exclusions**, never as images.

| # | Jutsu (id) | What it does (live) | Palette | Unique silhouette (proposal) | Delivery filename |
|---|---|---|---|---|---|
| 1 | Chakra Overflow (`e2eC-x4UXc5m6QexNbx8w`) | self: attacks hit far harder, short time | white-gold over deep chakra blue | **a brimming orb of chakra cracking open**, white-gold light bursting through its fissures and spilling over its rim like a breaking dam | `icon_jutsu_chakra_overflow_v1.webp` |
| 2 | Summoning: Titanoboa (`ZeqpsECJ882inNKUu0t3d`) | summons the great serpent, several rounds | emerald scales, gold eyes, blood-red seal | **the Titanoboa's head rearing from one thick coil**, fangs bared, golden eyes, a faint blood-red summoning ring beneath | `icon_jutsu_titanoboa_v1.webp` |
| 3 | Crimson Vein (`GGms9iTcZq_gICEuZYF2Q`) | target takes more damage; user steals life | crimson and blood-red on black | **a single needle of crimson chakra** trailing a branching web of glowing veins, like lightning made of blood | `icon_jutsu_crimson_vein_v1.webp` |
| 4 | Abyssal Wraith (`57JrAbfLuAliey0TgH2uM`) | genjutsu damage | violet and sickly teal ghostfire on black | **a shrieking wraith skull** rising out of a cracked black pit, hollow glowing eyes, a tail of ghostfire | `icon_jutsu_abyssal_wraith_v1.webp` |
| 5 | Clone Technique (`clh4d6phm0000tb0h7wo71p2z`) | full-strength clone, short time | pale chakra blue, white smoke | **one chakra flame splitting into two identical twin flames** in a crack of white smoke | `icon_jutsu_clone_technique_v1.webp` |
| 6 | Faint Shadow (`GnuyzNIf-Mdu41dnQv5dH`) | genjutsu damage; user hits harder | indigo and pale silver | **a cracked mask of shadow** with thin whisper-wisps curling from its mouth and eyes into the dark | `icon_jutsu_faint_shadow_v1.webp` |
| 7 | Body Flicker (`y39RtS7NN7TdqOgyT52gr`) | move, burst of chakra around the landing point | leaf green, white speed streaks, pale blue burst | **a burst of swirling leaves around a starburst impact flash**, sharp speed streaks converging on it | `icon_jutsu_body_flicker_v1.webp` |
| 8 | Terra Shift (`CLlN7iJPGCGRIDbJTo4P5`) | move, earth burst around the landing point; user takes less damage | amber dust, brown and gray stone | **a boulder fist bursting up through cracked earth**, rock shards flung outward in a ring of amber dust (not a rampart) | `icon_jutsu_terra_shift_v1.webp` |
| 9 | Crescent Strike (`sER45bYNHRP6GDk7Zl2Ez`) | move, blade sweep around the landing point | moon silver and steel blue | **a crescent moon forged from a sword blade**, its cutting edge blazing silver against a pale moon disc (not the starter's crescent cut with shock rings) | `icon_jutsu_crescent_strike_v1.webp` |
| 10 | Rotting Bite (`69LbdTR46ecbDsKoP0Lsy`) | damage; user heals from damage dealt | sickly green and bruise black | **a phantom bone jaw biting shut**, sickly green rot dripping from the fangs and creeping outward in veins | `icon_jutsu_rotting_bite_v1.webp` |

## 4. Ticket (when delivered)

One suggest-mode suggestion per jutsu carries its icon and its approved text together (as push/219 did), re-sending
`injectableInBattle` at its live value (law 20; Chakra Overflow is live `true`). AI equips: the 2026-10-21 census finds only
Tyrant King and Tyrant Guard holding Chakra Overflow, unequipped (no link to sever); push/224 reads the 26 AIs the
census lacks.
