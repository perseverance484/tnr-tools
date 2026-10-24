# Jutsu icon overhaul: art direction for regeneration

- **For:** the art director
- **From:** Fable / Claude Code, at the director's request (2026-10-24): "Write up a design document for handoff to the art
  director to regenerate the images."
- **Scope:** **35 of the 36 jutsu icons being reworked** in the icon overhaul. Replacement Technique is handled in its own
  session and is not covered here. Section 5.8 adds a people version of Crystal Sphere (a kept icon) for comparison. They ship together in one batch with the 15 icons
  kept unchanged (RUL-2026-10-23-008).
- **Sources:** director scores and notes (`docs/design/icon_overhaul/ICON_SCORES.md`); staff review in Discord, from Aven, zaruza and Keo
  (`docs/design/icon_overhaul/STAFF_FEEDBACK.md`); each jutsu's live name, data and battle text (public reads of 2026-10-23,
  `harvests/inbox/tnr_results_1792732003454.json`); the side-by-side cards `docs/design/icon_overhaul/review/NN_<slug>.png`
  (old icon on the left, our reverted icon on the right).
- **Roles (director, 2026-10-24):** the art director **only makes the art**. Claude Code handles everything else: intake and
  processing of raws, previews and comparison sheets, export and preflight, jutsu text rewrites, and the batch manifest.
- **Status:** direction for regeneration. Where this document proposes a subject, it is a proposal: art direction and final
  acceptance are the director's (CLAUDE.md section 10). Open decisions are listed in section 4.
- **Live-game requests/writes:** 0. Credentials: none.

## 1. What happened

Our first premium pass replaced 51 jutsu icons. Players disliked many of them, so all 51 were reverted (push/227). The
director scored every one and opened a staff review. The 15 icons that worked go back unchanged; the other 36 are
regenerated (35 in this document, plus Replacement Technique in its own session). The review gives a clear picture of what works and what does not.

## 2. The overriding rule: depict the move

**Director, 2026-10-24:** "A big mistake we've made with all our icons is they are too abstract. They don't convey the move at
all. They compress down to the same amorphous blobs at size. They need to depict the actual move, the lore, the actual thing
being done. Visual design needs to be better."

Every icon shows **the jutsu being done**: who does it, what they do, to whom or where, with what, at the moment it lands.
The battle text is the script. Energy, glow and particles are only the medium of the move, never the subject. Section 5
states each move in one bold sentence; draw that sentence.

### 2.1 Visual design

| # | Principle | In practice |
|---|---|---|
| V1 | **The 45 px name test.** | Shrunk to 45 px, a player can say what is happening in five words ("a ninja throws poison needles", "stone walls close around him"). If it shrinks to a blob, it fails. |
| V2 | **Silhouette first.** | The action reads as a flat black shape at 32 px: a figure, a weapon, a dragon, a wall, a wave. Design the silhouette before the detail; check it in grayscale and blurred. |
| V3 | **One moment, the peak.** | The instant of release or impact: the needles leaving the hand, the plates slamming shut, the fist meeting the face. Not before, not after. |
| V4 | **Concrete things.** | Draw real objects and bodies: senbon, logs, chains, stone plates, a trident, a water dragon, a fist. Abstract swirls, bursts, orbs and halos do not count as a subject. |
| V5 | **Big and few.** | One or two main shapes filling 60 to 75 percent of the tile; a figure is at least half the tile's height. Few secondary shapes; no texture filling the whole frame. |
| V6 | **A clear line of action.** | One readable direction of motion, usually a diagonal; the eye travels from the source of the move to its target. |
| V7 | **Value and colour structure.** | A dark, simple background in two or three values; the subject is the brightest, highest-contrast area. Two or three hues plus one accent. |
| V8 | **Lore over decoration.** | Details come from the jutsu's lore (a bloodline's weapon, a summon's design, the element's real material), not generic sparkle. |

### 2.2 The formula and layouts (from the deep dive)

Full analysis and sources: `docs/design/icon_overhaul/VISUAL_DESIGN_DEEP_DIVE.md`.

**One actor, one action, one moment, two to four big shapes, one light.** At most two actors plus one prop or effect;
crop to the smallest slice that tells the move; design the silhouette first; three value bands; one glow source, on the
move's energy; a flat or two-tone background tinted by the family; off-centre diagonal action, never a centred radial
burst. For figure icons, prefer a **dark figure against the brightest energy** (backlit): it is the most readable
arrangement in our own 45 px test.

Every move in section 5 is tagged with a layout, so siblings differ at 45 px:

| Code | Layout | How it is framed |
|---|---|---|
| **A** Strike | user (or their fist or weapon) from one side, target on the other, impact flash at contact; diagonal |
| **B** Projectile | thrower small in a lower corner or out of frame; the projectile big on a diagonal, about to hit |
| **C** Self-power | figure centred and braced, the effect forming on or around the body; backlit |
| **D** Affliction | target silhouette afflicted; the source above or to one side |
| **E** Summon | small user, huge creature looming behind; the scale contrast is the message |
| **F** Eruption | low camera; the effect erupting from the ground around or in front of the user |
| **G** Movement | figure in motion with a trail from where they were; the origin visible |

### 2.3 Rules from the review (apply to every icon)

| # | Rule | Evidence |
|---|---|---|
| R1 | **Premium TNR pixel art,** in the game's house style (`app/src/libs/imagePrompts.ts`): retro 32-bit pixel art, hard pixel edges, no gradients or blur, sharp contrast, rim light from the top-left, dramatic angles; figures with mature proportions in twisted, foreshortened action poses; exterior outlines; 16–24 colours. Not painterly, not glossy, not photo-real. | The most common note: Poisonous Senbon, Searing Might, Charge 4 Explosion, Inferno Cataclysm, all Aerathiel, four Vaporia. Drops of Renewal: "too realistic". |
| R2 | **It must read as a skill icon at 45 px.** One dominant subject; the background supports it and never takes over. Fewer, larger shapes. | Earthen Bastion "too busy/noisy"; Subaku Palace "doesn't read clearly as a skill icon"; Blue Blade Eyes: "I let the backgrounds take over"; Aven: "very bright and very busy". |
| R3 | **Show what the jutsu does** (section 2). Use its battle text. A generic shield, bubble, explosion or swirl loses the skill. | Blast Shield "a generic shield with a recolor"; Atomic Shield "a generic bubble"; Howitzer Crash "lacks skill identity"; Ethereal Rebirth "reads as poisonous energy". |
| R4 | **Distinct from every other icon,** in the family and across families, at thumbnail size. Check silhouette, palette and motion against the icons in section 3. | Abyss of Shadows vs BEE; Ethereal Nexus vs Shakunetsu Sakura; Death's March, Windshear Decay and Atomic Shield look alike; Surfing Strike vs Azure Dragon Palm; Tempest Cleave "looks like a shuriken skill". |
| R5 | **Keep the family palette** of the bloodline. | Atomic Shield: "colour scheme is wrong for Aera... loses most of the teal". |
| R6 | **Keep what players loved in the old icon.** The old icon is often the subject reference. | Icebound Might's looming summon; the older Tempest Cleave. |
| R7 | **Restraint with glow.** One glow source per icon, on the move's energy; no ambient halos. Attention matches importance. | Aven on Aerathiel: "too much going on when there's always a glowing aspect". See also decision D2. |
| R8 | **Tile rules (game source):** square, opaque, full-bleed; rounded corners and a border clip the tile; jutsu lists cover the **bottom-left and bottom-right corners** with 28 px badges, so nothing important goes there; nothing touches the edges. | `combat/page.tsx`, `CombatActions.tsx`, `ContentImage.tsx` at 107d7a8; JUTSU_ICON spec. |
| R9 | **No text,** kanji, runes, letters or numbers; no franchise insignia (village headbands, Sharingan, Rasengan, Susano'o armor copied from the anime); no UI or frames. | House rules. |

## 3. Icons that stay (the quality bar, and what to stay away from)

These 15 are kept unchanged. Use them as **style references** for rendering quality, and as **exclusions**: no reworked icon
may look like them at 45 px.

| Kept icon | Its look (reserved) | File |
|---|---|---|
| Blood-Enchanted Eyes ×8 (Crimson Impact, Crimson Tithe, Hemocure, Reaper's Embrace, Ring of Spilled Blood, Sanguine Plague, Thousand Strike, Unholy Enhancement) | crimson and black on black: blood burst, chalice, blood orb, scythe, blood spiral, smoke skull, needle rain, red veins | `art/style_refs/jutsu_icons/bee/` |
| Crystal Essence ×5 (Crystal Cave, Crystal Sphere, Kōsai Shippū, Prism, Summoning: Jade) | faceted crystal, gold light, prismatic | `art/jutsu_icons/crystal_essence/exports/` |
| Blazing Fang Strike | golden fire dragon coiling up | `art/jutsu_icons/scroll_jutsu/exports/icon_jutsu_blazing_fang_strike_v1.webp` |
| Celestial Dew | water crescent moon dripping into a pool | `art/jutsu_icons/scroll_jutsu/exports/icon_jutsu_celestial_dew_v1.webp` |

These are references for **rendering quality** only, not for concept: several of them are abstract themselves, which is
what section 2 now rules out for the reworks.

Practical consequence: **red-on-black circles and spirals belong to BEE**; **faceted crystal belongs to Crystal Essence**;
**a dragon belongs to Blazing Fang Strike and Azure Dragon Palm**; **a crescent belongs to Celestial Dew**.

## 4. Open decisions (director)

| # | Decision | Options | Default in this document |
|---|---|---|---|
| D1 | **People in icons.** **Decided (director, 2026-10-24): "Confirmed, show people wherever the move needs them."** | settled | Section 5 shows the user or the target wherever the move needs them. The five comparisons (Poisonous Senbon, Blast Shield, Decaying Touch, Ethereal Nexus, Crystal Sphere) keep a people and a no-people version. Figures: silhouette-first, readable at 45 px, original designs, no face close-ups, no franchise looks. |
| D2 | **Glow by tier** (Aven's proposal): basic D-rank jutsu without glowing effects; bloodline, forbidden, event and special jutsu keep the glow. | adopt / do not adopt | Not adopted until the director decides. Briefs for the four Normal jutsu note where it would change them. |
| D3 | **Surfing Strike vs Azure Dragon Palm:** flip one so the wave and the dragon move in opposite directions (zaruza), or a new wave composition. | flip / redraw | Redraw with the wave moving left to right, low and horizontal; the dragon faces left. |
| D4 | **Battle text vs new art.** Abyss of Shadows' text describes a crimson corona, and Ethereal Rebirth's text describes green flame, but the new direction moves both off those colours. | Claude Code's job, not the art director's | Art follows the new direction. Claude Code drafts text that matches the approved art and puts it to the director with the batch. |
| D5 | **Charge 4 Explosion's "C4" shape:** the explosions spelling C4 were called "unique and creative" (Keo: "neat and very to the point"), but they are letters (R9). | keep the C4 shape / drop it | Two candidates: one with, one without. |
| D6 | **Aerathiel palette.** The director's note: "color scheme is wrong for Aera... loses most of the teal". Keo: "lets change the color scheme to a bit more earthy tones? it is a dust element jutsu... just an updated version of current would do wonders, just with a color change." | teal particle energy / earthy dust tones / both as candidates | Teal, from the director's note, with one earthy-dust candidate per icon for comparison. |
| D7 | **Crystal Essence stays unchanged?** RUL-2026-10-23-008 keeps all five ("unless someone says something"). Keo has said something: Crystal Cave "looks just like stalagmites... maybe make it more cave-y"; Crystal Sphere "update old version to have this shell but put a person in the middle"; Kōsai Shippū "hard to tell which direction it's going"; Prism "the beam... more on the nose and rainbowed"; Summoning: Jade "love this, keep"; overall "more jewel tones beyond emerald and sapphire". | keep all five / rework some | Keep all five (the ruling) until the director reopens any. Kōsai Shippū's text is wrong regardless ("recoiling damage", but it has no recoil effect): Claude Code fixes it in the batch. |
| D8 | **Searing Might: keep the icon, rename the jutsu?** Keo: "it looks more like a shield which given the jutsus effects work. Maybe we use the icon, but change the jutsu name?" The director scored ours 2/10 ("too literal with the shield... doesn't read as premium pixel art"). | rework the icon (this document) / keep a shield and rename | Rework, as briefed in 5.3. A rename is a text change for Claude Code if the director wants it. |

## 5. Direction by family

Each entry gives what the jutsu does (live data), the score and feedback, and the move to depict. **Reference roles**
follow the isolated-generation protocol: at most two attached references per generation, each marked *subject*,
*element* or *style*. "Old" and "ours" mean the two images on the jutsu's review card.

### 5.1 Event (6)

Event icons are each unique; no shared palette. Avoid BEE red (R4).

| Jutsu | Does | Score and feedback | The move to depict |
|---|---|---|---|
| **Abyss of Shadows** (`XS08zZhUhK615Dle4j3f3`) | A rank, 40 AP, one opponent at range 5: they deal less and take more damage. Text: a black sun blooms above the target; shadow wisps spiral down and drag them in. | 8/10. The circle and red/black palette overlap BEE (Ring of Spilled Blood, Hemocure). Aven: "a little too red... darker colours". Director: move it off dark red. Keo: "yes i like". | `[D]` **The user raises a hand; a black sun blooms above the target; shadow tendrils pour from its rim, coil around the target and drag them upward.** Frame: black sun at the top with a cold violet-silver corona, tendrils descending, the target's silhouette caught and lifting off the ground at lower centre. Palette black, indigo, violet, a thin silver rim. No red. |
| **Drops of Renewal** (`-7jaNkJCvt3ByWhPJSw3E`) | A rank, 40 AP, self: absorbs damage as healing and hits harder. Text: a shimmering rain gathers in slow, glowing spirals and returns wounds as life. | 6/10. "Too realistic... the drop looks like water instead of restorative energy." Keo: "i like, but would like it to be more rain like if possible". | `[C]` **The user kneels with face lifted while glowing rain falls and gathers around them in slow spirals; their wounds close into light.** Old = subject (the hooded figure praying under drops), upgraded: a fine rain of teal-green light, spiralling around the figure, a few motes rising from them. Restorative light, not glassy water. Keo: "more rain like". |
| **Earthen Bastion** (`_zNMEZqIzgjTqXoXQRWz0`) | A rank, 40 AP, self: takes less damage, hits harder. Text: stone plates tear free and slam shut around the user, veined with molten light. | 4/10. "Doesn't read well as a skill icon. Too busy/noisy." Keo: "i like but not sure the direction... It looks kinda like a rock formation, which in itself isnt bad." | `[C]` **The user drives a heel into the ground and stone plates tear up and slam shut around them, veined with molten light.** The figure braced low at centre, four or five big plates rising around and closing over them like a fortress, thin molten seams. It reads as a defence closing around a person, not a rock formation. Dark plain background, little debris. |
| **Hollow Veil** (`GAhckNCW8xUES4YGTJPGL`) | A rank, 40 AP, one opponent: they deal less damage; the user absorbs. Text: an ash-gray veil settles over the target like a funeral shroud and hollows them out. | 9/10. "Very good. Maybe a little silhouette upgrade." Keo: "yes!" | `[D]` **An ash-gray veil drifts over the target and settles like a funeral shroud, hollowing them out.** Ours = element (its shroud): the shroud draped over a target's silhouette whose own glow drains out through it, leaving a dark hollow where the chest was. Firm outer contour. |
| **Subaku Palace** (`jELEiw5W3N4m2R3oJm3Pk`) | A rank, 40 AP, ground spiral: buffs allies' damage, weakens enemies'. Text: a burning-gold sigil spirals out; red sandstone gates carved with snarling faces tear free of the ground. | 6/10. "Good enough rendering but doesn't read clearly as a skill icon." Keo: "PRETTY PALACE!!" | `[F]` **The user presses a palm to the earth; a burning-gold sigil spirals outward and red sandstone gates carved with snarling faces tear up from the ground.** Two candidates. **A:** old = subject, upgraded: the kneeling user, the gold sigil spiralling from the palm, the gates rising around it. **B** (Keo liked ours): the palace rising from the spiralling sigil, with the user's palm on the sigil in the foreground so the move reads. |
| **Tempest Cleave** (`Ul83iTziN__Z0i_UOzZTK`) | A rank, 60 AP, ring around the user: damage, burning wounds, enemies take more damage. Text: the user turns once and the air becomes a blade; a howling ring of razor wind. | 0/10, **do not reuse ours at all**. "Looks like a shuriken skill... not intimidating enough, wrong shape and art direction." Keo liked ours but "can see shuriken look of it" and suggested a "Rasen-shuriken style"; the director's 0/10 stands, and a Rasenshuriken is franchise imagery (R9). | `[F]` **The user plants their feet and turns once; the air becomes a blade and a ring of razor wind erupts outward, carving everything in reach.** A fighter mid-spin at the centre, a howling ring of blue-white wind blades bursting out around them, debris sliced in the ring, storm sky. Use the director's older version for the wind (`docs/design/icon_overhaul/refs/08_tempest_cleave_older_version.png`, element). No radial shuriken blades, nothing from ours. |

### 5.2 Forbidden (2)

Forbidden jutsu are the rarest; they should feel the most powerful. The two must not look alike.

| Jutsu | Does | Score and feedback | The move to depict |
|---|---|---|---|
| **Ethereal Nexus** (`iktsCP-RjIhlYlsTg-JTN`) | S rank, 60 AP, one opponent: damage with lifesteal; they take more damage. Text: fire, water, earth and wind spiral together into one blinding knot of chakra. | 3/10. "Looks like a Shakunetsu Sakura skill and doesn't reflect the ability." Keo: "not sure how to fix it beyond maybe just updating old version?" | `[A/B]` **People vs no people** (director). The move: fire, water, earth and wind spiral together between the user's hands into one blinding knot, which tears into the target and drinks from the wound. **A, no people:** the four elements drawn as their real materials (a lick of flame, a rope of water, stone shards, wind streaks) twisting into one white-hot knot that is striking forward, life-light streaming back from the impact. **B, people:** old = subject, upgraded: the white-haired fighter holding the knot between their hands, drawing light from the kneeling foe. No pink or magenta. |
| **Ethereal Rebirth** (`K0t6Z-Q4lau1jFt8Tkpot`) | S rank, 60 AP, one opponent: damage; the user absorbs and deals less. Text: the user cracks open the seal on their soul and remakes themselves. | 0/10. "Reads more like poisonous energy explosion than an ethereal rebirth. Bad direction and quality." Director: "spinning energy... more light blues"; multiple colours: "Sure". Keo: "it looks kinda necro summoning. not a huge fan of it for ER, but could possibly use it for something else?" | `[C]` **The user breaks the seal on their own soul; the elements burn through them and their body unmakes and remakes itself.** A figure at the centre, a seal cracking on the chest, the body half dissolving into spinning light-blue energy and half reforming, rings of that energy turning around them, soft prismatic edges (director: "spinning energy... more light blues"; multiple colours allowed). Not a necromantic summoning (Keo), not green poison. |

### 5.3 Normal (4)

Basic D-rank jutsu that every player sees. If the director adopts D2, these lose most of their glow.

| Jutsu | Does | Score and feedback | The move to depict |
|---|---|---|---|
| **Poisonous Senbon** (`H9XLJiU1YEro03QJ2mH8q`) | D rank, 60 AP, one opponent: damage. Text: a handful of poison-laced senbon. | 5/10. "Decent idea but... doesn't read as TNR premium pixel art." Keo: "i like it, maybe do... a person throwing them? so old style updated?" | `[B]` **People vs no people** (director). The move: a flick of the wrist sends poison-laced senbon into the target. **A, no people:** three senbon in flight on a diagonal, poison beading off the tips, the lead needle about to strike a wooden training post or the edge of a target, so they are clearly thrown weapons in flight. **B, people:** old = subject, upgraded: the kunoichi mid-throw, the glowing senbon leaving her hand on the same diagonal. |
| **Searing Might** (`clh4d6q1j0008tb0hzthddb6m`) | D rank, 40 AP, self: takes less damage. Text: chakra ignites the user's core into a controlled blaze that reinforces muscles and pathways, a shield of inner strength. | 2/10. "A little too literal with the shield. Art doesn't read as premium pixel art." Keo: the shield fits the effect; keep the icon and rename the jutsu? (D8) | `[C]` **The user ignites their core; the blaze spreads through their body and hardens into a shield of inner strength.** Old = subject, upgraded: a warrior braced in a guard stance, fire racing along their arms and torso and hardening into plates of ember-armour. See D8 for the rename alternative (keeping a shield). |
| **Soul Shackles** (`clh4d6psu0004tb0hsa5cshh6`) | D rank, 60 AP, a line of opponents: damage. Text: cursed chakra chains are hurled, pierce defenses and latch onto the target's spirit. | 4/10. "Where are the shackles going? They just stop midair. Might be better if the shackles were just spread straight across the icon." Keo: "looks neat af. Maybe we can make the 'soul' a bit more noticeable?" | `[B]` **The user hurls cursed chakra chains that pierce the target and latch onto their spirit.** Chains running straight across the icon from one side to the other, hooked through a target's silhouette, pulling a large, clearly visible ghostly soul half out of their body (Keo: make the soul noticeable). Purple and spectral. |
| **Venomous Phobia.** (`9oirFnLa0wejelNYpewq6`) | D rank, 40 AP, one opponent: they take more damage. Text: an airborne toxin seeps into the mind; illusions of venomous creatures. | 7/10. "Pretty good actually. Might need a better silhouette." Keo: "i like it. would keep". | `[D]` **An airborne toxin seeps into the target's mind; hallucinated venomous creatures crawl over them.** A target clutching their head as green mist curls around them and takes the shape of snakes and spiders closing in. Ours (the fanged miasma mask) is the alternative if the director prefers to keep it (7/10; Keo: keep). |

### 5.4 Bakuhatsu (5)

Explosion release. Palette: orange, gold and white-hot light on dark smoke. Must read as **explosions**, never lava or plain
fire (R3).

| Jutsu | Does | Score and feedback | The move to depict |
|---|---|---|---|
| **Blast Shield** (`Awyd1k1-tw4uzn-PLbcdP`) | D rank, 40 AP, ring around the user: a barrier; takes less damage. Text: a massive explosion around the user neutralises incoming attacks. | 6/10. "Reads as a generic shield with a recolor. Could use the actual blast/shockwave. It also kicks up a physical barrier of earth around the user in a circle." Keo: "i like it. its very similar [to the old]. maybe we just add the person in the middle?" | `[C]` **People vs no people** (director). The move: a massive explosion around the user neutralises incoming attacks and throws up a ring of earth. Both: a shockwave dome bursting outward, a ring of upheaved earth slabs around its base, incoming kunai or a strike blown apart at its edge. **A, no people:** a white-hot core at the centre. **B, people:** a ninja braced at the centre, as in the old icon. |
| **Charge 4 Explosion** (`rOqCTqNBSW_A-QYesFBw9`) | C rank, 40 AP, one opponent: burning wounds; both sides deal and take more damage. Text: the battlefield covered in explosive chakra; small explosions all around. | 4/10. "Unique and creative but not high quality or premium." Keo: "neat and very to the point. lol". | `[F]` **The user covers the battlefield with explosive chakra; small explosions go off all around.** Glowing chakra charges stuck across cracked ground, detonating one after another in a chain towards the viewer, the nearest one bursting. See D5 for the C4 shape. |
| **Howitzer Crash** (`hW4IV1Hp59BqVFx0u-gTd`) | B rank, 60 AP, area at range 5: the user moves, deals damage, and weakens defenses. Text: explodes the space behind them to launch at the opponent, then detonates on arrival. | 6/10. "Decent execution but lacks any real pop or skill identity." Keo: "love". | `[G→A]` **The user explodes the space behind them, launches at the opponent and detonates on arrival.** A figure rocketing forward on a diagonal, a blast erupting behind their feet, fist first into an impact burst at upper right. Two explosions on one line: the launch and the hit. |
| **Inferno Cataclysm** (`FTTl_wnTlbvOfOyiGCc-b`) | A rank, 60 AP, ground spiral: heavy damage, recoil to the user. Text: the user slams their hands into the ground and the heat erupts. | 6/10. "Visuals don't look premium and reads more like a lava skill than an explosion skill." Keo: "works for me!" | `[F]` **The user slams both hands into the ground and the heat erupts.** The figure crouched at the bottom, palms on the ground, a white-hot blast column and fireball erupting in front of them, a shockwave ring racing across the ground. Blast and smoke, no lava. |
| **Kinetic Nova** (`y8y01n9jz16bz5EBzl4wr`) | A rank, 60 AP, area: damage and a wound. Text: a ball of chakra flung at the target explodes, showering the area in tiny explosions. | 9/10. "Pretty good. Maybe a little polish." Keo: "nail on head. dont change". | `[B]` **The user flings a ball of chakra that explodes, showering the area in tiny explosions.** Ours = subject, light polish only: make the chakra ball visible at the heart of the burst so it reads as one ball exploding into many. Keeping ours untouched is the alternative (Keo: "dont change"). |

### 5.5 Aerathiel (5)

The weakest family in the director's scores: four of five at 1/10. Every icon needs the family look rebuilt: **teal and
cyan particle energy with pale gold accents on deep navy** (use the old icons for palette, R5; see D6 for Keo's earthy dust
alternative), premium pixel art (R1), restrained glow (R7), and five clearly different silhouettes (R4). Today three of them
are teal swirls; that must not happen again. Keo rated ours more kindly ("thats not to say i dont like updated ones
purposed. cuz i REALLY do."); the director's scores set the direction.

| Jutsu | Does | Score and feedback | The move to depict |
|---|---|---|---|
| **Atomic Shield** (`FGSJC-7Zd0BYh7-tvsUdH`) | D rank, 40 AP, self: reflects damage, hits harder. Text: a translucent barrier made of the particles around them. | 1/10. "Doesn't have premium pixel art, color scheme is wrong for Aera. Loses most of the teal and particle barrier aspects for a generic bubble." Keo: "a good update from old style". | `[C]` **The user creates a translucent barrier of particles to defend from all attacks.** The user inside a shell of fine particles in a lattice, an incoming kunai or blast deflecting off it with a reflected spark. Not a bubble. |
| **Death's March** (`UgYXqNIJNjLGkAS5b5udH`) | B rank, 60 AP, area: damage; they take more damage. Text: a radiant chakra tunnel envelops the target; the enemy's form crumbles. | 1/10. Same art style issue; "too similar to Windshear Decay and Atomic Shield". Keo: "old style is... neat, but to me doesnt fit the jutsu. but the new icon looks great". | `[D]` **The user envelops the target in a radiant chakra tunnel; the target's body crumbles into dust.** A vertical tunnel of light bearing down on a target silhouette whose body is breaking apart into rising particles. Straight and vertical, not swirling. |
| **Decaying Touch** (`Zr6Zo2NcXxWuL13ufQsHw`) | B rank, 60 AP, one opponent: damage, recoil to the user. Text: a dust cloud; the user's touch, then the body becomes dust. | 1/10. Same art style issue; "hand looks unnatural". Keo: "i like the old version, so maybe update that style?" | `[A]` **People vs no people** (director). The move: the user dashes through a dust cloud, places a hand on the target, and the target turns to dust. **A, no people:** a glowing palm-print burned onto a crumbling stone figure or armour piece, dust pouring from the cracks. **B, people:** old = subject, upgraded: the user's palm on the target, whose body crumbles into dust. |
| **Particle Cannon** (`egtCp5UC5pRwxz7egJm7J`) | A rank, 60 AP, one opponent: damage, a wound. Text: fingers weave a triangle; a radiant orb unfurls into a brilliant beam. | 4/10. "Decent execution on this one but needs an art style improvement." Keo: "pretty similar" [to the old]. | `[B]` **The user's fingers weave a triangle; a radiant orb unfurls into a brilliant beam.** Old = subject: two hands forming a triangle, the beam firing out through it at an angle. Keep ours' beam strength. |
| **Windshear Decay** (`VmoEzExhfgtzme2b5RuzJ`) | A rank, 40 AP, area: enemies deal less, take more, and attacks are redirected. Text: a torrent of razor-sharp wind slashes tears towards the target. | 1/10. Same art style issue; "resembles Death's March and Atomic Shield too much". Keo: "i like it". | `[B]` **Hand seals summon Fūjin's winds; a torrent of razor-wind slashes tears towards the target.** Long straight wind slashes ripping across the frame towards a target silhouette, cuts opening in their cloak and fragments shearing off. Straight lines, not a curl. |

### 5.6 Vaporia (5)

Boil release: fire and water together. Staff like the family (zaruza: "looks so solid and encompasses the names of the
jutsu so well"; Keo liked all five concepts); the asks are premium art (R1), **water that clearly reads as water**, in water
drops (Aven: beaded, droplet texture; Keo on Drowning Strike: "hard to tell its water"), and telling Surfing Strike apart from
Azure Dragon Palm (D3). Keep the concepts and restyle the five together so they match.

| Jutsu | Does | Score and feedback | The move to depict |
|---|---|---|---|
| **Azure Dragon Palm** (`pBsG-Jw4TTkSjxfqzjG6b`) | A rank, 60 AP, one opponent: piercing damage, heals the user. Text: a water dragon encases the user like armour; every strike is mirrored by the dragon. | 6/10. "Needs more premium art." Keo: "dragon is good. and fits". | `[E/A]` **A water dragon encases the user like armour; each palm strike they land is mirrored by the dragon.** Old = subject, upgraded: the fighter thrusting a palm forward, the water dragon coiled around them and striking in the same direction. Dragon faces left (D3). Water in beaded droplets. |
| **Drowning Strike** (`eZqJ9qJ_f43VRg_HhRiyb`) | D rank, 60 AP, ground spiral: damage; they take more damage. Text: a fist of scorching water strikes and floods the target. | 6/10. "Needs more premium art." Keo: "its good, but hard to tell its water". | `[A]` **The user's fist, covered in scorching water, strikes the target in the face.** A fist sheathed in boiling water punching forward into a splash of spray and steam, clearly water (blue, beaded). Old = element (the punch through a ring of water). |
| **Liquid Ember Shell** (`fWb24FYrbTqYvE9GIEA49`) | B rank, 40 AP, one opponent: burning wounds, lifesteal, the user hits harder. Text: fire and water merge into a molten liquid shell that absorbs attacks. | 8/10. "May just need updating to the same art style as the others." Keo: "its good, just dont like the steam from it, it looks weird". | `[C]` **Fire and water merge into a molten liquid shell around the user that absorbs attacks.** The user inside a shell of water with embers churning through it, an incoming strike splashing off. No steam plume (Keo). |
| **Scorch Break** (`6v7dfraXRVo5K3NbgixzT`) | B rank, 60 AP, area: damage, reflect. Text: chakra in the palms turns to steaming liquid; a flurry of searing punches. | 6/10. "Needs more premium art." Keo: "the breaking of the waves with a fire punch is great!" | `[A]` **Steaming-liquid fists, a flurry of searing punches.** Ours = subject (Keo: "the breaking of the waves with a fire punch is great!"): a burning fist driving through a wall of water that breaks apart around it. |
| **Surfing Strike** (`M-iPxOupEp35-KptpG4DV`) | A rank, 60 AP, area: the user moves, deals damage, takes less damage. Text: a torrent floods the battlefield; the user glides over the steaming surface. | 6/10. "Needs more premium art. Resembles the Azure dragon a bit too much at thumbnail size." Keo: "i like the wave style of it. would keep". | `[G]` **The user floods the battlefield and glides over the boiling surface, scalding the target.** A rider on a low wave moving left to right with a long steaming wake (Keo: keep the wave style). Wide and flat, opposite direction to the dragon (D3). |

### 5.7 Blue Blade Eyes (8)

All eight scored 8/10 with one shared flaw: "The background is too noisy and makes the skill icon too difficult to make out"
(Aven: "very bright and very busy"; Keo: "all BBE is a go for me... if we darken the background to make the foreground pop
more would fix it"). Keep each concept where it already shows the move (ours = subject), make it concrete where it does not (section 2), and
fix the treatment: **a dark, calm navy
background**, the ice subject brightest, fewer stray shards. Palette: icy white and blue on deep navy.

| Jutsu | Does | The move to depict |
|---|---|---|
| **Arctic Frost** (`0tPhVC7G21Ej99YSICtJO`) | A rank, 40 AP: the blade is encased in ice; lifesteal. | `[C]` **The user chills the blade, encasing it in ice.** A sword gripped in a hand, ice crystallising up the blade and a sweeping arc of frost from its swing. Dark calm background. |
| **Blade Resonance** (`TFRsEeV-VacukUUop-dtN`) | A rank, 60 AP: a blade of ice disrupts the target's defenses. | `[A]` **A blade of ice strikes the target, disrupting their defences.** The ice blade striking, resonance rings bursting outward from the point of impact. Dark calm background. |
| **Blue Crimson** (`bxIPWiqiEaCmPYfAysB5a`) | C rank, 60 AP, area: the user flickers around the target. | `[G]` **The user vanishes and reappears around the target, faster and faster.** Afterimages of the user ringing a target, slash trails linking them. Dark calm background. |
| **Glacial Volley** (`Bw2OBS92Xi-4YlfErS632`) | B rank, 60 AP: ranks of ice lances volley at the target. | `[B]` **The user raises the trident; ranks of ice lances form in the air, all aimed at the target, then volley.** The trident raised in the lower corner, rows of ice lances hanging in the air and loosing towards the far side. Dark calm background. |
| **Ice Shackles** (`Aff56oo9BFTcoLLeEyOja`) | B rank, 60 AP: frost locks the target in blue ice; stun. | `[D]` **The trident levels; frost races up the target, locking joint after joint.** A target encased in blue ice from the ground up to the chest, ice chains locking the arms. Dark calm background. |
| **Icebound Might** (`YGBz7eIDvLwWXSVFEcK9j`) | B rank, 60 AP, area: ice armour; a shield; enemies deal less. | `[E]` **The user plants the trident and ice armour closes over them.** Old = subject: the towering ice guardian looming over the user, full figure visible, an original design (not anime Susano'o armour). Dark calm background. |
| **Quintessential Flake** (`dXOjSl1vNp5G5BsFrNPkh`) | C rank, 40 AP: the user moves; the area freezes. | `[F]` **The user drives the Blue Blade energy down and the ground around the target freezes.** The blade point striking the ground, ice spreading outward across it in a bold snowflake pattern. Dark calm background. |
| **Sapphire Command** (`gIEy7THAZdXgcak5zs5U6`) | C rank, 40 AP: a pulse of Blue Blade chakra freezes the target's flow. | `[D]` **A pulse of Blue Blade chakra sweeps across the battlefield and freezes the target's chakra flow.** A wave of ice-blue light passing through a target silhouette, frost spreading through their body. Dark calm background. |

### 5.8 People-vs-no-people comparison: Crystal Sphere (1)

Crystal Sphere is a kept icon (section 3, D7), so ours is already the **no-people version**. Only the **people version** is
generated, so the director can compare the two.

| Jutsu | Does | Feedback | The move to depict |
|---|---|---|---|
| **Crystal Sphere** (`zKK0rjIJqbpSiTw7McDAv`) | Crystal Essence. See its review card (#40). | 10/10, kept. Keo: "update old version to have this shell but put a person in the middle?" | `[C]` **People version only:** our crystal dome (ours = subject: its shell, facets and the deflected fiery blast), with **a fighter braced inside it**, as in the old icon. Same palette and lighting as ours. |

Person rule for B: one clear figure (two only where the old icon's story needs the target), readable at 45 px, original design, no face close-up, no franchise look.

## 6. How to produce them

**Art director:**

1. **One jutsu per isolated generation session** (`docs/workflows/ISOLATED_ART_GENERATION.md`). Each brief carries the jutsu
   target lock (id and name above), the move to depict and its layout code, the family palette, section 2 (the move rule, V1–V8, the formula and R1–R9), and
   the section 3 exclusions.
2. **References:** at most two per generation, each with its role stated. Typical pair: the jutsu's old or ours image
   (*subject* or *element*, as the table says) plus one kept icon from section 3 (*style* only). Pull the images from the
   review cards or `docs/design/icon_overhaul/src/NN_<slug>_original|_ours`.
3. **Fail fast before returning a raw:** fails the 45 px name test (V1); abstract blob instead of the move; background busier than the subject; looks like a section 3
   icon or a family sibling; text or insignia; anatomy errors.
4. **Return the raw images only,** named `raw_<slug>_<candidate>.png`. Do not process, crop, upscale, key or upload them.

**Claude Code** (everything after the raw):

5. Intake into `art/jutsu_icons/overhaul_2026_10/candidates/<slug>/`; the acceptance gates of the deep dive (section 7:
   name test, silhouette, family lineup, bar test, safe area, pixel integrity, backgrounds); previews in context next to the
   old icon; old / new sheets for the staff thread.
6. After the director picks: processing into real pixel art (snap to one grid, 16–24 colours, clean stray pixels; deep dive
   section 6.4), export (256 px lossless WebP), `artpreflight --type JUTSU_ICON`.
7. Text: drafts for any jutsu whose name, description or battle text no longer matches its approved art (Abyss of Shadows
   and Ethereal Rebirth at least), plus Kōsai Shippū, whose battle text claims recoil it does not have (Keo), and a Searing
   Might rename if the director chooses it (D8); all for the director's approval.
8. The batch manifest once all 36 are approved: the 36 new icons, the 15 kept icons, any approved text, and the AI
   unequip/re-equip cycle where an equipped jutsu changes (`docs/design/icon_overhaul/BATCH_PLAN.md`).

**Suggested order:** the families with the clearest direction and the most to gain:
Aerathiel, Forbidden, then Event, Normal, Bakuhatsu, Vaporia, and Blue Blade Eyes last (a treatment fix on approved
concepts).
