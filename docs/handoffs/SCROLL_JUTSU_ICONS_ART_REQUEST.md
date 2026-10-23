# Art request: jutsu icons for the scroll jutsu (10)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude Code, at dauntless's request (2026-10-22)
- **Direction (director, 2026-10-22):** each jutsu taught by a scroll gets a new icon. **Visual theme** (palette,
  material, mood) matches its scroll. **Visual design** (composition, rendering, rules) follows the approved
  jutsu-icon exemplars (BBE, RUL-2026-10-14-001 / RUL-2026-10-17-021). Silhouettes below are proposals; the
  director's visual approval of each raw locks it.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one jutsu per generation session, jutsu target lock).
  Worked examples: `docs/design/blue_blade_eyes/JUTSU_ICON_REGISTER.md`, `docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md`.
  Spec: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `JUTSU_ICON` (opaque allowed).
- **Companions:** scroll plan `docs/design/scroll_icons/SCROLL_ICON_ROADMAP.md`; scroll art request
  `docs/handoffs/SCROLL_ICONS_SET3_ART_REQUEST.md`.
- **Source:** jutsu records from the 2026-10-21 player jutsu census (push/178–181); AI equips from the 2026-10-21 AI
  census; current icons downloaded from the image CDN 2026-10-22 (`docs/design/scroll_icons/sheet_live_scroll_jutsu_2026-10-22.png`).
- **Live-game requests/writes:** 0. Nothing here uploads anything.

**Delivered:** 4/10. Earthen Bastion (`art/jutsu_icons/scroll_jutsu/raws/raw_jutsu_earthen_bastion_v1.png` → `exports/icon_jutsu_earthen_bastion_v1.webp`, opaque 256x256 lossless, `artpreflight --type JUTSU_ICON` clean; near-black ground with base glow, as Poisonous Senbon was accepted), 2026-10-23. Drops of Renewal (`raw_jutsu_drops_of_renewal_v1.png` → `icon_jutsu_drops_of_renewal_v1.webp`; delivered at 256x256 WebP, so the export is a lossless re-encode, not a downscale; preflight clean). Blazing Fang Strike (`raw_jutsu_blazing_fang_strike_v1.png` → `icon_jutsu_blazing_fang_strike_v1.webp`; a serpentine fire dragon with bared fangs, replacing the proposed three fangs; still unique in the set; preflight clean). Celestial Dew (`raw_jutsu_celestial_dew_v1.png` → `icon_jutsu_celestial_dew_v1.webp`; crescent moon, falling dew drop, dome of light, as proposed; preflight clean).

## 1. Why

Every current icon for these jutsu is a small pixel scene of a ninja figure posing (sheet above). At 64 px and below
the technique is a streak next to an actor, which breaks the jutsu-icon standard (no actor; one technique shape).
The scrolls that teach them now each have a distinct colour; the jutsu should read as the same family as their scroll.

## 2. Scope

| In | Out |
|---|---|
| The 7 event jutsu taught by the event scrolls, the 2 forbidden jutsu, Subaku Palace (all inspired by their scrolls). **Open (director):** the six visible EVENT jutsu with no scroll (Black Coffin, Dark Pact, Frictional force, Hogs gone Wild, Moose Cleave, Moose Prime) | **KGK: Black Fang Lance, Flash Step, Veilguard Pulse, KX Hollow Surge**: another staff member's custom contributions (director, push/196 review: "Dont rewrite other staffs custom contributions"); their icons are already a strong family. Bloodline scrolls grant whole bloodlines, not one jutsu. Dragon's Scroll grants an item. |

## 3. Collection-wide visual lock (the exemplar design)

- **Technique first, no actor:** no ninja, face, body, hands or limbs. One dominant technique-specific silhouette,
  one supporting effect, clear direction, dark negative space. Reads as one shape at 32 px.
- **Rendering:** the approved JUTSU_ICON standard (BBE): detailed pixel-art rendering, crisp edges, strong rim light,
  luminous core, high contrast.
- **Background:** full-bleed designed atmosphere in the jutsu's palette (opaque approved; do not fake transparency).
- **Theme from the scroll:** the palette slot of the jutsu's scroll (section 4) is the jutsu's palette. A jutsu
  never uses another scroll's slot (taken slots: `SCROLL_ICONS_SET3_ART_REQUEST.md` section 2).
- **BEE lesson (director, 2026-10-23):** each icon is **one bold emblem that is the ability's metaphor** and fills the
  frame (BEE: a chalice for a tithe, an orb for healing, a skull in miasma for a plague), with the energy itself as the
  subject. Never a diagram of the mechanics (no "broken sword + broken shield" for a debuff). Reference:
  `art/style_refs/jutsu_icons/bee/`.
- **Avoid:** actors/portraits, a scroll (the icon is the technique, not the item), mandatory mandalas or eye emblems,
  text/kanji/runes, frames, franchise insignia, any silhouette reserved for another jutsu below.

## 4. Targets and distinction ledger

Each silhouette is unique in this set; pass the others as **text exclusions**, never as images.

| # | Jutsu (id) | What it does (live effects) | Scroll and palette slot | Unique silhouette (proposal) | Delivery filename |
|---|---|---|---|---|---|
| 1 | Tempest Cleave (`Ul83iTziN__Z0i_UOzZTK`) | area slash: damage, afterburn, target takes more damage | Scroll of Cleave: **steel silver, orange edge** (set-3 recolour) | a **ring of crescent wind-blades** spinning around an empty centre, orange-hot cutting edges | `icon_jutsu_tempest_cleave_v1.webp` |
| 2 | Earthen Bastion (`_zNMEZqIzgjTqXoXQRWz0`) | self: takes less damage, deals more | Scroll of Bastion: **earth brown, molten orange cracks** | a **tall faceted stone rampart** of rising rock shards, orange light in the cracks | `icon_jutsu_earthen_bastion_v1.webp` |
| 3 | Drops of Renewal (`-7jaNkJCvt3ByWhPJSw3E`) | self: absorbs damage into health, deals more | Scroll of Renewal: **aqua water, green leaves, gold glints** | **one large water droplet** drawing a spiral of smaller drops and two leaves into it | `icon_jutsu_drops_of_renewal_v1.webp` |
| 4 | Blazing Fang Strike (`l3oXmqSJ7L-r4XI9IBIyh`) | piercing strike with afterburn | Scroll of Blazing: **fang red-orange flame** | **a serpentine fire dragon with bared fangs** (delivered 2026-10-23; was "three flaming fangs") | `icon_jutsu_blazing_fang_strike_v1.webp` |
| 5 | Celestial Dew (`2vNeMhph6A9Ld--WXa35O`) | self: heal and shield | Scroll of Celestial Dew: **pearl white, pale blue starlight** | a **crescent moon** letting fall **one glowing dew drop** onto a soft dome of light | `icon_jutsu_celestial_dew_v1.webp` |
| 6 | Hollow Veil (`GAhckNCW8xUES4YGTJPGL`) | on the target: deals less damage; absorb | Scroll of Hollow Veil: **ash grey, bone white** (set-3 redo) | a **drifting translucent veil** with a hollow empty centre, frayed ash edges | `icon_jutsu_hollow_veil_v1.webp` |
| 7 | Aegis of Shadows (`XS08zZhUhK615Dle4j3f3`) | on the target: deals less damage, takes more | Scroll of Shadows: **oxblood crimson on black** | **renamed Abyss of Shadows** (director, 2026-10-23). **The engulfing wave:** a towering wall of shadow with glowing oxblood edges curls over the top of the frame like a breaking wave, its inside a black void: the moment of being swallowed. One emblem filling the frame, BEE-style; no props | `icon_jutsu_abyss_of_shadows_v1.webp` |
| 8 | Ethereal Nexus (`iktsCP-RjIhlYlsTg-JTN`), forbidden | damage, lifesteal, target takes more damage | Forbidden Nexus: **magenta seals**, black chain accents | **three magenta energy streams converging into a knot**, a thin red life-thread drawn back out | `icon_jutsu_ethereal_nexus_v1.webp` |
| 9 | Ethereal Rebirth (`K0t6Z-Q4lau1jFt8Tkpot`), forbidden | damage, absorb, target deals less damage | Forbidden Rebirth: **emerald green seals**, black chain accents | an **emerald phoenix-like ember rising** out of a cracked seal ring (no bird head detail needed) | `icon_jutsu_ethereal_rebirth_v1.webp` |
| 10 | Subaku Palace (`jELEiw5W3N4m2R3oJm3Pk`) | area spiral; stats buff/debuff | Demon Scroll: Subaku Palace (new, set-3 #11): **rust sandstone with demon gold** | a **demonic pagoda gate** silhouette of rust sandstone, a gold-lit spiral sigil on the ground before it | `icon_jutsu_subaku_palace_v1.webp` |

Aegis of Shadows is being renamed **Abyss of Shadows** (director, 2026-10-23): it no longer shields the user; it curses
the target (deals less damage, takes more, 2 rounds). The icon follows the new name; the rename and new texts go in a
separate text ticket (`docs/design/jutsu_overhaul/ABYSS_OF_SHADOWS_TEXT.md`). Delivery filename
`icon_jutsu_abyss_of_shadows_v1.webp`.

## 5. References per session (attach as real image bytes, one or two files, never a collage)

1. **Design exemplar (always):** `art/style_refs/jutsu_icons/bbe/icon_bbe_ice_shackles_v2.webp`. Composition,
   rendering and material quality **only**: do not copy its X-chain layout or its icy palette.
2. **Theme reference:** the jutsu's scroll art, for **palette and material only** ("do not draw a scroll"):
   - Bastion, Renewal, Blazing, Celestial Dew: `art/item_icons/event_scrolls/raws/raw_scroll_of_<name>_v1.png`.
   - Aegis of Shadows: `art/item_icons/event_scrolls/raws/raw_scroll_of_shadows_b.png`.
   - Tempest Cleave, Hollow Veil: `art/item_icons/event_scrolls/raws/raw_scroll_of_{cleave,hollow_veil}_b.png`.
   - Ethereal Nexus / Rebirth: `art/item_icons/event_scrolls/raws/raw_forbidden_scroll_{nexus,rebirth}_v1.png`.
   - Subaku Palace: `art/item_icons/event_scrolls/raws/raw_demon_scroll_subaku_palace_v1.png` (set-3 #11, delivered).

## 6. Prompt template

~~~text
Target: the jutsu "<name>". One square 1:1 game jutsu icon.

What it does: <effects, plain words, from section 4>.

Reference 1 (design exemplar): match its COMPOSITION, PIXEL-ART RENDERING and finish quality: one dominant
technique silhouette, one supporting effect, strong rim light, luminous core, high contrast. Do NOT copy its layout,
subject or icy colours.
Reference 2 (theme): use its PALETTE and MATERIALS only. Do NOT draw a scroll.

Subject: <unique silhouette from section 4>. Palette: <slot from section 4>.

Full-bleed designed background in the same palette, dark enough that the silhouette reads at 32 px.

Avoid: any person, ninja, face, hands or body; a scroll; text, kanji, runes; frames, mandalas, eye emblems;
these silhouettes reserved for other jutsu: <list the other nine silhouettes>.

Generate ONE image. Do not upload or process it.
~~~

## 7. Order, QC and delivery

1. Event jutsu whose scroll is final: Earthen Bastion, Drops of Renewal, Blazing Fang Strike, Celestial Dew, Aegis of
   Shadows.
2. Tempest Cleave and Hollow Veil once their set-3 scrolls are approved.
3. Ethereal Nexus, then Ethereal Rebirth (after the forbidden scroll pair); Subaku Palace after its new scroll (set-3 #11).

Raw QC per icon: no actor; one dominant silhouette matching its row; palette inside its slot; no reserved silhouette;
reads at 125, 64 and 32 px. Two wrong-subject results in one session: close it and start clean.

Deliver each director-approved original under its exact filename (corrections `_b`, `_c`), square, 1024 px or more,
with a ledger row (filename, jutsu, pixel size, bytes). Do not process or upload: Fable does intake, preflight
(`artpreflight.py --type JUTSU_ICON`) and the ticket.

## 8. Ticket conditions (Fable)

- **Combined ticket (director, 2026-10-22):** these jutsu icons go in the **same** manifest as scroll icons set 3
  (`SCROLL_ICONS_SET3_ART_REQUEST.md`): one suggest-mode manifest for the scroll items, the Colored Jewel and these jutsu.
- **One suggest-mode manifest** for all delivered icons, one suggestion per jutsu, `image` only, `injectableInBattle`
  re-sent at its live value (law 20), from a fresh capture of the ten jutsu taken just before the build.
- **Open text suggestions:** the round-2 text suggestions on Aegis of Shadows, Blazing Fang Strike, Celestial Dew,
  Subaku Palace and Tempest Cleave were resolved by the director (2026-10-23); no open suggestion blocks the ticket.
- **Earthen Bastion is equipped by an AI (War Commander, 2026-10-21 census).** Director, 2026-10-22: "Include it. I'll
  reequip later." It goes in the combined ticket like the others; approving its suggestion edits the jutsu and severs
  War Commander's link (laws 18, 60), and the director re-equips War Commander afterwards. The ticket note says so.
