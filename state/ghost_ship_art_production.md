# Ghost Ship / Skyglass art production

**Baseline:** live main verified 2026-10-01 at `df17803a9c4222025dba7e68c1919a372835fcd6`.
**Lead:** Content Designer / Art Director during crew revision; Image Production resumes after direction review. **Status:** quest icon LOCKED; Deck Warden `_a` REJECTED for direction; revised elite/cursed roster proposed.
**Branch:** `chatgpt/ghost-ship-skyglass-art-20261001`. No live-game API requests or writes; only captured image URLs fetched.

## Direction and sequence

Follow `state/ghost_ship_retheme_design.md`, the shared-pool migration, and the current art spec. Forbidden shinobi warship, dark timber/iron seal lattice, pale white-blue Skyglass; crew are reconstructed chakra impressions. Tragic military duty without mortal life. Captain and Crowned Captain are increasingly stable, not increasingly decomposed. Skyglass Serum is approved.

2026-10-01 correction: all personnel aboard the top-secret project at its disappearance were high-level operatives. The curse must be immediately visible, not reduced to ordinary shinobi with small glowing cracks. Read `state/ghost_ship_crew_direction.md` before further generation. Its proposed specialist duties and silhouettes await review; the approved premise is recorded in RUL-2026-10-01-003.

1. Quest listing icon, shared by Gather and Hunt.
2. Revised Deck Warden AI avatar prototype: elite boarding-security chief, archaic specialist armor and a major readable reconstruction failure. Preserve a glimpse of the unaged human face. Follow the pending revised brief after direction review; the ordinary-guard `_a` treatment is superseded.
3. Remaining AI avatars/props, one at a time: Oathkeeper, Wayfinder, Arsenal Keeper, Sentinel, First Blade, The Captain, Crowned Captain, Core Horror, Seal Charge, Core Canister. Captain pair shares identity; hazards share core/seal construction.
4. Scene portraits from locked Oathkeeper/Captain identities; then Deck, Lower Hull, Chart Room, Hold, Helm, Cache Site backgrounds. Reserve lower left; compose backgrounds at 3:2.
5. Skyglass Crown, matching fragment, Skyglass Serum item icons. Reassess the fragment only after Crown lock.

These are production recommendations, not new content or final visual approvals. No work on a bespoke 29-jutsu icon set. Core Rupture is a shared signature; art is optional only if the eventual shared record requires it.

## Captured-art audit

Sources: `harvests/inbox/tnr_results_1790826101573.json`, `tnr_results_1790826836406.json`, `tnr_results_1790828718767.json`. All 41 capture rows have successful full-body persistence; all three journals are DONE/success with zero mutation items. Audited 29 image-bearing direct records, 28 unique image URLs (both quests use the same icon). Individual style references were inspected separately; human audit contact sheets were not generation references.

| Asset | Recommendation | Observed reason |
|---|---|---|
| Existing quest icon | Fully regenerate | Green ghost faces around a conventional sailing ship and whirlpool; no Skyglass engineering. |
| Deck Warden, Oathkeeper, Wayfinder, Arsenal Keeper, First Blade, Captain pair | Fully regenerate | Skeletal undead, pirate hats/coats, decorative gold, green fire; incompatible identities and costume. |
| Core Horror | Fully regenerate | Encrusted wooden undead body with green light; rebuild as a damaged human impression held together by hull timber/cable/seals. |
| Sentinel | Fully regenerate; preserve broad silhouette idea only | Shell/stone construct is relevant, but horned monster/green magic treatment needs the new seal-frame language. |
| Seal Charge, Core Canister | Fully regenerate | Literal red TNT/dynamite. Both 256px avatars are below the 320px minimum. |
| Oathkeeper/Captain/Crowned Captain scene portraits | Fully regenerate | Same pirate/undead conflict. Captain portrait is 522,252 bytes, above the 450KiB working ceiling. |
| All six backgrounds | Fully regenerate at 3:2 | All are 512x512 JPEG, stretched by scene client. Hold is treasure-piled; helm lacks control architecture. Deck/lower-hull/cache staging can inform new composition, not serve as ready exports. |
| Blank Scene Character | Reuse unchanged | Intentional transparent suppressor, not missing artwork. |
| Mystery Chest, Ornate Chest | Reuse shared reward art | Generic existing rewards outside the rename set; do not reskin shared records as Ghost Ship-specific supplies. |
| Fragment of the Skyglass Crown | Potential minor retheme | Pale crown fragment with white flame could become crystalline sealwork; must match the new Crown. Current PNG needs WebP export. |
| The Skyglass Crown | Fully regenerate | Central skull and ornate flame crown conflict with a crystalline command interface. |
| Skyglass Serum | Fully regenerate | Skull bottle and warm amber pirate treatment; use a pre-modern sealed restorative vial with restrained Skyglass cues. |
| Ghostly Sovereign's Diadem | Obsolete for this workstream | Legacy attachment slated for removal; image is a generic landscape placeholder. Do not redesign or delete the standalone record. |
| Legacy-only jutsu art | No production | 29-jutsu rename plan superseded; 37 legacy-only jutsu are unequip/retirement candidates, not deletion targets. |

`shotlist.py` was run against the extracted Gather quest: 57 objectives, six wired backgrounds, three real portraits plus the blank suppressor. It flags missing top-level `content.sceneBackground`; plan a deliberate global scene using the final Deck/entry plate. Existing wiring being reported SATISFIED does not imply visual suitability. No push manifest or new @img wiring was authored.

## Locked ship reference and scene continuity

dauntless approved the processed icon on 2026-10-01: “Approved. Need to remain faithful to this ship design when making scene art.” This is the canonical vessel design for all scene art, not merely a palette reference (RUL-2026-10-01-002).

Preserve its deep reinforced timber hull, iron ribs/bands, two unequal battened charcoal sails, conductive rigging, caged mid-deck Skyglass structure, bow crystal housing, keel crystal and angular underside sealwork. The approved view has the bow at right and stern at left; maintain the same physical arrangement when changing viewpoint, not a mirrored or redesigned vessel. Stern afterimage fragments and the restrained levitation ripple remain supporting cues.

Use the approved source pixels as an individual reference for ship scenes. Do not add masts, replace the sail plan, move the crystal structures, or substitute a generic galleon. Interior scenes may reveal unseen construction, but must carry the same timber/iron structure, crystal geometry and seal-lattice engineering. Compare every background against the approved ship during QC. Preserve the locked icon unchanged.

Repository reference files: `art/ghost_ship/icon_ghost_ship_skyglass_d.webp` (approved export) and `art/ghost_ship/references/ghost_ship_skyglass_locked_source_d.webp` (1254x1254 final chroma source, lossless WebP with exact decoded RGB pixel equality verified against the generated PNG; design reference only, not a game upload). Reference SHA-256: `6d96257b9f4d9db2cbdec1cf986b4a5bfada68199e898ae4e06e5bfd580e9b2d`.

## Quest icon lock and QA

- File: `icon_ghost_ship_skyglass_d.webp`
- Target: ICON, via `quest.image` raw URL; no new gameAsset record.
- Export: 248x248, 63,048 bytes (61.6 KiB), lossless WebP, actual alpha.
- SHA-256: `9edcb347e9f7a180cdfd45571eddc2de0486a843cf35c3caad1a36d0e8a1dda0`
- Retained artifact: `libfile_b9b44d02e72c81918592acb62ff9b316`, exact filename above.
- Acceptance: **LOCKED by dauntless 2026-10-01**. Exact approved bytes and ship continuity are preserved.
- Built-in image generation used. Final chroma source 1254x1254; rawqc ACCEPT, key coverage 54.5%, border purity 100%. Source reduced with nearest-neighbor to spec-recommended 256px before bundled key/crop/pad/export.
- `chroma.py --target ICON --qc ...` and `artpreflight.py --type ICON --spec ... --json`: **0 errors, 0 warnings**, 0% partial-alpha edges. Native dark composite and 125px client-size view inspected. Silhouette/crystal keel remain readable; thin rigging becomes secondary texture.
- Earlier opaque/native-alpha exports are superseded and not deliverables. The opaque 256px export encountered the preflight alpha requirement; native alpha exceeded the soft-edge limit. Final flat-chroma generation resolves both without changing tool code or spec.

Reference pack `style_refs.py verify --repo-root .`: 18/18 references, 2,223,333 bytes, provenance proven. Pack contains scene characters/backgrounds, no ICON or AI_AVATAR selector. Inspected Commander Okabe, Winter Crow, Pale Fang, Old Ghost and Canal Frontage for calibration; character references did not enter icon generation.

Session bootstrap: lawmap 0 errors/5 pre-existing warnings; doctrine and pack projections current. The unrelated session parity adapter crashes on this capture-only bundle's `checks:null` (`validate.py:201`, TypeError). This is recorded, not reported green; capture success and art checks were verified independently. No tooling repair attempted.

Ghost Ship roadmap validates. `validate --all` reports an unrelated pre-existing One Perfect Crop missing evidence path (`push/54_one_perfect_crop_launch_final.json`); the same failure is present at baseline. Do not edit that workstream in this art task.

## Rejected Deck Warden prototype and historical QA

- File: `art/ghost_ship/avatar_deck_warden_skyglass_a.webp`
- Target: AI_AVATAR, existing Deck Warden AI record's avatar; no gameAsset record.
- Export: 614x614, 144,720 bytes (141.3 KiB), lossless WebP, actual alpha.
- SHA-256: `0a762a7f43770de08c3516a9faf3d67b243f80e1ac556d980ed096ea8d842304`
- Retained artifact: `libfile_c80cfd855230819188dc5b0096d6a4c9`.
- Disposition: **REJECTED / SUPERSEDED by dauntless's direction correction, 2026-10-01**. It reads as an ordinary enemy shinobi, not an elite operative of a cursed classified project. Retained for provenance only; do not package or use as a style anchor. No remaining avatars generated.
- Built-in image generation; original 1254x1254. `rawqc.py --scaffold deck_warden_skyglass_a`: ACCEPT, lime coverage 77.8%, border purity 100%. Reduced to recommended 640x640 with nearest-neighbor before bundled crop/pad/export.
- `chroma.py --target AI_AVATAR --spec ... --qc ...`: exact square 614x614; background 320,086px, holes 24px, remapped 15px. `artpreflight.py --type AI_AVATAR --spec ... --json`: **0 errors, 0 warnings**, 0% partial-alpha edges.
- Historical native/320px QC found complete hands/feet, a youthful human face, layered black wrap clothing/iron plates, a practical hook and clean pale-blue edges. It missed the central direction failure: the ordinary silhouette and tiny reconstruction cues did not communicate the classified elite crew or cursed condition. Technical PASS is not artistic acceptance. The next candidate must pass the visual tests in `state/ghost_ship_crew_direction.md` before handover.
- NINJA selector rerun and all four individual references inspected: Commander Okabe for facial/near detail only; Winter Crow, Pale Fang and Old Ghost for costume, silhouette and edge discipline. New asset-class generation carried no ship/scene image context.

## Resume

Quest icon accepted. Deck Warden `_a` rejected for direction. Present the complete proposed roster/visual reset in `state/ghost_ship_crew_direction.md`; settle that direction before generating replacement `_b`. Do not ask to lock `_a` again. The replacement still requires normal technical QC and visual acceptance before proceeding to remaining avatars. Preserve the locked ship design in later scenes.

## Superseded Deck Warden prompt record (do not reuse)

Create ONE original TNR game AI avatar, square 1:1, full body head to feet, centered with generous clean margins. Single ninja character in a compact dynamic combat guard, weight shifted and knees slightly bent. Crisp pixel lineart, flat cel shading, limited palette, soft even lighting, camera at eye level, flat 3/4 view, no low angle and no foreshortening, both arms held within the subject's own silhouette and touching nothing, at most one restrained elemental glow accent, as rim light on edges only.

SUBJECT: Deck Warden, a reconstructed chakra impression of a young adult male shinobi naval guard from an ancient forbidden warship. A plainly human youthful face, weary focused eyes of normal size, pale natural skin, short black hair tied close at the nape, no headwear. Obsolete practical military uniform: near-black layered cross-wrap tunic, short neck cowl, small rectangular iron lamellar chest and shoulder plates, wrapped forearms, close leather utility harness, plain buckled belt, short split cloth tassets, dark gathered trousers, shin wraps and simple split-toe footwear. Compact hooked iron boarding tool secured at the belt, not a hook hand. Premodern cloth, iron, rope and leather. One very restrained icy-white-blue accent along a few armor seam edges. Small angular discontinuities at one sleeve edge and one calf show incomplete chakra reconstruction, edged by pale geometric seal strokes; most of the body is solid and stable, anatomically intact. A tragic soldier still following orders. No skeleton, no corpse, no fantasy pirate.

TNR rendering calibration: articulated dark armor plates, broad flat cloth shadow shapes and fine pixel-edged contours; face and hands have clear adult anatomy, like a carefully painted game figure with pixel discipline, never chunky low-resolution sprite art. Near-black garment base with ONE accent colour per character. Cel shading with restrained painterly depth. Defined shadow shapes, flat mid-tones, no airbrush gradients and no bloom. Grounded adult proportions. Not chibi, not anime-scaled eyes.

TRUE SOLID FLAT pure lime-green #00FF00 chroma field covering the entire canvas and every opening between limbs and equipment, no shadow on the green. Hard opaque pixel boundaries, not transparency or checkerboard. No aura, halo, light field, glow disc, green spill, fog, diffuse ghost glow or floating dust. No scenery, floor, ship, furniture or extra props. No text, UI, watermark, labels, frame, asset sheet, grid, multiple characters, headband, forehead protector, clan symbol, village mark, real-world logo, tricorn, pirate coat, skull, bones, treasure, gold ornament, modern clothing, zippers or firearms.

## Quest icon prompt record

Built-in image generation. Initial generation:

Create one finished square TNR Ghost Ship quest-listing icon, 1024x1024. Open square pixel-art icon, crisp pixel lineart, flat cel shading, limited palette, soft even lighting, dark background, strong readable silhouette, no frame, no text. Subject: ONE ancient experimental shinobi warship suspended in empty night air, complete compact three-quarter broadside silhouette. Dark timber armored hull with iron reinforcement ribs, two short masts with broad charcoal battened sails, a few clear chakra-conductive rigging lines. Pale icy-white and blue Skyglass crystal control structure embedded into the ship; restrained carved seal channels connect it along the keel and illuminate the underside. The white-blue seals are abstract geometric engineering marks, never lettering. A subtle short broken ripple beneath the keel suggests levitation, no ocean beneath it. Faint fractured afterimage of one trailing hull edge suggests a vessel materializing. The ship fills most of the square with clear breathing room; simple major forms must read at 125px. Tragic, mysterious, militarized, pre-modern Japanese-inspired forbidden engineering. Readable dark wood and metal planes, localized Skyglass highlights, hard pixel clusters and clean shadow shapes. Background near-black muted midnight blue, quiet and uncluttered. No people, no crew, no skulls or bones, no ghost faces, no pirate imagery, no flags, no treasure, no cannons, no gold ornament, no Western galleon castle, no moon, no whirlpool, no scenic horizon, no modern technology, no neon outlines, no bloom, no airbrush gradients, no blur, no decorative border, no words, no labels, no UI, no watermark, no asset sheet, no grid, no franchise insignia. This is an individual quest icon, not a scene background or a character.

Final isolation edit used the initial image as its sole reference:

Production isolation edit of the supplied warship icon. Preserve the ship's design, dark timber armor, charcoal battened sails, pale icy white-blue Skyglass crystals, carved hull channels and three-quarter silhouette. Put it on a TRUE SOLID FLAT pure #00FF00 lime green chroma field filling the ENTIRE square canvas, INCLUDING every opening through the rigging and between silhouette fragments. No gradient, no texture and no shadow on the green. Make the ship 82 percent of the canvas width and height, all edges well inside the canvas. Crisp pixel lineart, flat cel shading, limited palette. Hard opaque pixel boundaries, ZERO semi-transparent glow; crystal light is contained INSIDE the crystal and seal shapes only. Simplify the dissolving stern into a few substantial angular chunks and the levitation ripple into two short solid pale-blue marks. No tiny debris speckles, no outer aura, halo, bloom, fog or light field. Retain the single complete ship, no people, no pirate symbols, no text, no border, no frame, no multiple views. Square 1:1 canvas, true solid #00FF00 background.
