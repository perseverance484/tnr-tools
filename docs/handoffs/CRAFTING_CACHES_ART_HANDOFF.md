# Crafting caches — icon handoff for the visual design agent

> **SUPERSEDED (2026-10-13)** by `docs/handoffs/CRAFTING_CACHES_IMAGE_GEN_HANDOFF.md`, which has the final name (Sage's Strongbox), ready-to-run prompts and the spec values. It is kept for history.

- **From:** Fable / Claude Code
- **To:** the visual design agent (ChatGPT, visual-asset partner)
- **Date:** 2026-10-13
- **Repository:** `perseverance484/tnr-tools`
- **Branch:** `claude/crafting-recipe-census-pln5za`. The exact SHA is in the message that hands
  this file over.

## 1. What is needed

Three **item icons**, one for each new chest. Names approved by dauntless on 2026-10-13:

| Chest | It feeds | Contents (for art direction only) |
| --- | --- | --- |
| **Medicine Inro** | The four pills: Chakra Pill II, Stamina Pill II, Small Health Pill, Pill Pack | Herbs and beast parts: Galecrest Sage, Glimmer Dust, Mosswolf Tuft, Moonlight Antlers, Sunroot |
| **Shinobi Tool Pouch** | Five kunai (Katon, Wave, Ikazuchi, Stonefall, Zephyrfang) and Robber's Friend | Iron Ore plus each kunai's reagent pair (feathers, leaves, scales, spines, moss, thorns) |
| **Sage's Strongbox** | The Legendary consumables: Mona's Mermaid Song, Solider Pill, Enemy Pill, Forbidden Jutsu Scroll: Nexus and Rebirth | Rare relic reagents: Cracked Auditory Core, Tempest Thorn, Lunaris Bloom, Heart of Kuraokami, Fujin's Breath, Voidshade Petal, Parchment Core |

Loot tables are still being balanced. Don't draw specific contents spilling out of the
container, because they may change.

## 2. Authority and process (read first)

- **Every number comes from the spec.** That is the `ICON` target and `house_style` in
  `skills/producing-tnr-art/data/25x_DATA_art_spec.json`. It covers delivered and minimum width,
  aspect, format, byte ceiling, chroma key and padding. This handoff deliberately restates none of
  them.
- **Process:** `skills/producing-tnr-art/SKILL.md` and `references/prompts.md`.
  - Generate the first icon. Get it approved, which **locks the icon style**. Then generate the
    other two to match it.
  - Keep prompts short and concrete.
  - After three failed blind re-descriptions, switch to reference-image prompting.
- **Subject rule warning.** The spec records that generators "reliably fail on packaging formats".
  Each subject below is therefore described as **one concrete, holdable object with a distinctive
  silhouette**, not as "a chest" or "a bag of stuff".
- **Padding.** Keep the small transparent margin the spec asks for, so the game's rarity frame
  shows behind the icon. The chests are planned as COMMON rarity.

## 3. Subject briefs

The three icons are a **set**. Use the same camera, the same lighting, and a shared dark lacquer
and wood palette, with one accent colour per icon that tells them apart at a glance.

### Medicine Inro
- **Object:** a traditional Japanese inrō. It is a small stacked lacquered case of three or four
  tiers, closed by a cord running through the tiers and an ojime bead. It hangs from a netsuke
  toggle.
- **Look:** dark lacquer. A **muted jade or teal** accent picks out a simple herb-leaf crest on
  the front tier.
- **Reads as:** medicine, pills, a field apothecary.

### Shinobi Tool Pouch
- **Object:** a stiff, flapped leather hip pouch with a belt loop. The tips of two or three kunai
  rings and handles stick out from under the flap. The kunai are part of the pouch, not loose
  objects.
- **Look:** dark leather, iron rivets and buckle. The accent is **steel and copper** on the
  buckle and the kunai rings.
- **Reads as:** thrown weapons, kunai making.

### Sage's Strongbox
- **Object:** a compact iron-banded hardwood strongbox with a heavy lock plate. Paper ofuda seal
  strips are pasted across the lid seam.
- **Look:** near-black wood with **aged gold** bands. The single allowed restrained glow accent
  (house style) may be a faint rim on the seal strips. Optional.
- **Reads as:** rare, sealed, Legendary-tier reagents, without looking like a Legendary *weapon*.

**Avoid:** open lids showing contents, loose items around the object, text or kanji legible
enough to be wrong, glows that spread into the background (see the glow section of `prompts.md`
about chroma key bleed), and full-bleed composition.

## 4. Delivery

- **Filenames.** Use these exact names, and deliver them inside a code block. They become
  `@img:` references in the manifest. A corrected image gets a fresh suffix (`_b`, `_c`) and never
  reuses a name (spec `filenames.correction_rule`).
  ```
  icon-medicine-inro.webp
  icon-shinobi-tool-pouch.webp
  icon-sages-strongbox.webp
  ```
- **Ledger.** Record the slug, type, output filename, pixel dimensions and KB for each file, per
  spec `filenames.ledger`.
- **QC.** Run the processing and pre-upload QC in `references/processing.md` before handing over.
- **Binaries.** Return the files to dauntless or the operator. Don't commit generated binaries
  unless the art workflow for this task says so.

## 5. Out of scope

- Loot-table values, item descriptions and in-game text, which Fable will draft separately.
- Any live upload or push. dauntless performs those through the builder.
- The Ghost Ship work.
- Scene art or avatars.

## 6. Open items for dauntless before the icons are final

- Approve the first (style-locking) icon before the other two are generated.
- Confirm the accent colours (jade, steel/copper, gold) or name different ones. This is art
  direction, so it is dauntless's call.
