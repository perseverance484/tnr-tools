# Skyglass weekend 3: Stolen Stores band setup (draft for the director's review)

Built 2026-11-14 ~16:00Z. Nothing was run and nothing was written to the game. The TNR connector would not sign in
for this session, so the live state was taken from the repo (perseverance484/tnr-tools main 2e28c2b) and the release
thread's notes, not from a live read.

## Files
- `00_clone_plan.json`: 3 clones of the original Wreck Sighted `_zp1l7Y9a_77pgonAdsYx` (hidden event). Connector, or the
  Clone button in the quest editor. Then regenerate with the three ids:
  `python3 stolen_stores_band.gen.py --page-id A --ws-low-id B --ws-high-id C`
- `01_stolen_stores_band_build.json`: Forge, your tab. New 30-80 page, both Wreck Sighted copies, Stolen Stores as the 81+ page.
- `02_release_flips.json`: Forge. Unhide the new page and copies, hide last week's copies.
- `03_wreck_gates_direct_save.json`: Wreck gates to the new copies. Not Forge (Forge refuses dungeon edits): connector
  direct save, or the dungeon editor.

## Stolen Stores as it stands (from the repo, not a live read)
`AgGR962c3XNo6Pr0up2qT`: published Nov 8 (518), levels 1-100, no prerequisite, startsAt 2026-11-21, endsAt 2026-11-24,
no Wreck Salvage on its orders. Confirmed against 517/518 and the release thread's 00:38Z live read.

## Changes vs this week (Rotted Heading)
- Clone source is the original Wreck Sighted. Last week's source (First Page) was deleted Nov 14.
- Copies match what 615 wrote to this week's live copies (your 9:40 AM CT run, 3/3 read back): 609's top-level
  fields plus 615's whole content block, reward included. 614 was refused because it sent the scene steps only.
- Copies get startsAt 2026-11-21 and endsAt 2026-11-24 (this week's had none). This closes them at the weekend's end
  and lets the release flips run Wednesday without anything opening early.
- Stolen Stores: level 81-100, needs the new 81+ copy, 3 Wreck Salvage per order, rewards and rules lines updated.
  Its five challenges and rewards are unchanged from the draft you saw Nov 8.
- New 30-80 page "The Watch Log: Stolen Stores (Shallows)": Rotted Galley x2 (Galley Stores), Low Tide/Night Watch x2
  (Medicine Inro), Split Hold or Broken Stern x1 (Tide Chart), any trade x1 (Archive Chart Case), dailies x5 (Sealed
  Treasury), 3 salvage each, Skyglass Token for all five. Beachcombing is no longer its own challenge (still counts as
  a daily).

## Icon prompts (attach ref_style_skyglass_icons.png)
1. The Watch Log: Stolen Stores. Game item icon in the same hand-painted style as the attached icons: a dented,
   salt-crusted tin ration box lying open at a 3/4 angle, a folded page of a ship's log tucked under its lid, the
   page's edge showing short struck-through brush rows. A few pale cyan skyglass flecks in the salt; a faint green rot
   stain at one corner of the page. Thick dark ink outlines, cel shading with a few highlight steps, weathered texture,
   cool blue-black and dull tin palette with one pale cyan accent. Single object, centered, small even margin, square
   1024x1024, transparent background. No readable text, letters or numbers, no UI, no frame, no surface or shadow, no
   glow halo, no second object.
2. The Watch Log: Stolen Stores (Shallows). Same style: a narrow strip torn from the bottom of a ship's log page,
   soaked and curling, lying across a wet coil of rope, its few brush rows run and struck through, one tiny pale cyan
   skyglass shard caught in the rope. Water drips from the torn edge. Thick dark ink outlines, cel shading, cool
   blue-black palette with one pale cyan accent. Single object, centered, small even margin, square 1024x1024,
   transparent background. No readable text, letters or numbers, no UI, no frame, no surface or shadow, no glow halo,
   no second object.
The Wreck Sighted copies keep the Ghost Ship icon already on them.
