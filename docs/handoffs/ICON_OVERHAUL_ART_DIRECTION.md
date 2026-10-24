# Jutsu icon overhaul: art direction for regeneration

- **For:** the art director
- **From:** Fable / Claude Code, at the director's request (2026-10-24): "Write up a design document for handoff to the art
  director to regenerate the images."
- **Scope:** the **36 jutsu icons being reworked** in the icon overhaul. They ship together in one batch with the 15 icons
  kept unchanged (RUL-2026-10-23-008).
- **Sources:** director scores and notes (`docs/design/icon_overhaul/ICON_SCORES.md`); staff review in Discord
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
director scored every one and opened a staff review. The 15 icons that worked go back unchanged; the 36 below are
regenerated. The review gives a clear picture of what works and what does not.

## 2. Rules from the review (apply to every icon)

| # | Rule | Evidence |
|---|---|---|
| R1 | **Premium TNR pixel art.** Detailed pixel art with crisp edges, clean readable forms, strong rim light. Not painterly, not glossy, not photo-real. | The most common note: Poisonous Senbon, Searing Might, Charge 4 Explosion, Inferno Cataclysm, all Aerathiel, four Vaporia. Drops of Renewal: "too realistic". |
| R2 | **It must read as a skill icon at 45 px.** One dominant subject; the background supports it and never takes over. Fewer, larger shapes. | Earthen Bastion "too busy/noisy"; Subaku Palace "doesn't read clearly as a skill icon"; Blue Blade Eyes: "I let the backgrounds take over"; Aven: "very bright and very busy". |
| R3 | **Show what the jutsu does.** Use its battle text. A generic shield, bubble, explosion or swirl loses the skill. | Blast Shield "a generic shield with a recolor"; Atomic Shield "a generic bubble"; Howitzer Crash "lacks skill identity"; Ethereal Rebirth "reads as poisonous energy". |
| R4 | **Distinct from every other icon,** in the family and across families, at thumbnail size. Check silhouette, palette and motion against the icons in section 3. | Abyss of Shadows vs BEE; Ethereal Nexus vs Shakunetsu Sakura; Death's March, Windshear Decay and Atomic Shield look alike; Surfing Strike vs Azure Dragon Palm; Tempest Cleave "looks like a shuriken skill". |
| R5 | **Keep the family palette** of the bloodline. | Atomic Shield: "colour scheme is wrong for Aera... loses most of the teal". |
| R6 | **Keep what players loved in the old icon.** The old icon is often the subject reference. | Replacement Technique ("players missed the old one"); Icebound Might's looming summon; the older Tempest Cleave. |
| R7 | **Restraint with glow.** Glow is for the subject's energy, not on every surface. | Aven on Aerathiel: "too much going on when there's always a glowing aspect". See also decision D2. |
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

Practical consequence: **red-on-black circles and spirals belong to BEE**; **faceted crystal belongs to Crystal Essence**;
**a dragon belongs to Blazing Fang Strike and Azure Dragon Palm**; **a crescent belongs to Celestial Dew**.

## 4. Open decisions (director)

| # | Decision | Options | Default in this document |
|---|---|---|---|
| D1 | **People in icons.** The staff thread leaned towards no people ("I *think* so"; Jutsu Masters cover people renders), but Replacement Technique was asked for as a faithful upgrade of the old icon, which shows a ninja. | a) no people anywhere; b) no people except where the old icon's figure is the identity (Replacement Technique, Icebound Might's summon) | b). Where a brief needs a body part (a fist, a palm), it is formed of the element, not a human hand. |
| D2 | **Glow by tier** (Aven's proposal): basic D-rank jutsu without glowing effects; bloodline, forbidden, event and special jutsu keep the glow. | adopt / do not adopt | Not adopted until the director decides. Briefs for the five Normal jutsu note where it would change them. |
| D3 | **Surfing Strike vs Azure Dragon Palm:** flip one so the wave and the dragon move in opposite directions (zaruza), or a new wave composition. | flip / redraw | Redraw with the wave moving left to right, low and horizontal; the dragon faces left. |
| D4 | **Battle text vs new art.** Abyss of Shadows' text describes a crimson corona, and Ethereal Rebirth's text describes green flame, but the new direction moves both off those colours. | Claude Code's job, not the art director's | Art follows the new direction. Claude Code drafts text that matches the approved art and puts it to the director with the batch. |
| D5 | **Charge 4 Explosion's "C4" shape:** the explosions spelling C4 were called "unique and creative", but they are letters (R9). | keep the C4 shape / drop it | Two candidates: one with, one without. |

## 5. Direction by family

Each entry gives what the jutsu does (live data), the score and feedback, and the proposed subject. **Reference roles**
follow the isolated-generation protocol: at most two attached references per generation, each marked *subject*,
*element* or *style*. "Old" and "ours" mean the two images on the jutsu's review card.

### 5.1 Event (6)

Event icons are each unique; no shared palette. Avoid BEE red (R4).

| Jutsu | Does | Score and feedback | Proposed subject |
|---|---|---|---|
| **Abyss of Shadows** (`XS08zZhUhK615Dle4j3f3`) | A rank, 40 AP, one opponent at range 5: they deal less and take more damage. Text: a black sun blooms above the target; shadow wisps spiral down and drag them in. | 8/10. The circle and red/black palette overlap BEE (Ring of Spilled Blood, Hemocure). Aven: "a little too red... darker colours". Director: move it off dark red. | A **black sun high in the frame** with a cold violet-silver corona, and **shadow tendrils pouring down** from it; vertical composition, not a full-frame ring. Palette: black, deep indigo and violet, a thin silver rim. No red. |
| **Drops of Renewal** (`-7jaNkJCvt3ByWhPJSw3E`) | A rank, 40 AP, self: absorbs damage as healing and hits harder. Text: a shimmering rain gathers in slow, glowing spirals and returns wounds as life. | 6/10. "Too realistic... the drop looks like water instead of restorative energy." | A **drop of restorative energy**, stylised and luminous (teal-green light, not glassy water), with small healing motes rising in a gentle spiral. Not a crescent (Celestial Dew), not leaves. |
| **Earthen Bastion** (`_zNMEZqIzgjTqXoXQRWz0`) | A rank, 40 AP, self: takes less damage, hits harder. Text: stone plates tear free and slam shut around the user, veined with molten light. | 4/10. "Doesn't read well as a skill icon. Too busy/noisy." | **Four or five large stone plates locked together** into one fortress shape, front-on, thin molten seams between them; dark plain background; almost no flying debris. One silhouette. |
| **Hollow Veil** (`GAhckNCW8xUES4YGTJPGL`) | A rank, 40 AP, one opponent: they deal less damage; the user absorbs. Text: an ash-gray veil settles over the target like a funeral shroud and hollows them out. | 9/10. "Very good. Maybe a little silhouette upgrade." | **Refine ours** (ours = subject): the ash-gray shroud arching over an empty dark hollow, with a firmer outer contour and a darker, cleaner hollow so it reads at 45 px. |
| **Subaku Palace** (`jELEiw5W3N4m2R3oJm3Pk`) | A rank, 40 AP, ground spiral: buffs allies' damage, weakens enemies'. Text: a burning-gold sigil spirals out; red sandstone gates carved with snarling faces tear free of the ground. | 6/10. "Good enough rendering but doesn't read clearly as a skill icon." | **Two red sandstone gates with snarling faces** rising from a burning-gold sigil on the ground, seen close; the old icon's demon gates are the identity (old = subject). Not a whole pagoda palace. |
| **Tempest Cleave** (`Ul83iTziN__Z0i_UOzZTK`) | A rank, 60 AP, ring around the user: damage, burning wounds, enemies take more damage. Text: the user turns once and the air becomes a blade; a howling ring of razor wind. | 0/10, **do not reuse ours at all**. "Looks like a shuriken skill... not intimidating enough, wrong shape and art direction." | Start from the **older version** the director supplied (`docs/design/icon_overhaul/refs/08_tempest_cleave_older_version.png`, subject): a **blue-white slicing whirlwind** with lightning and cloud curls, storm-dark and intimidating. No radial blade shapes. |

### 5.2 Forbidden (2)

Forbidden jutsu are the rarest; they should feel the most powerful. The two must not look alike.

| Jutsu | Does | Score and feedback | Proposed subject |
|---|---|---|---|
| **Ethereal Nexus** (`iktsCP-RjIhlYlsTg-JTN`) | S rank, 60 AP, one opponent: damage with lifesteal; they take more damage. Text: fire, water, earth and wind spiral together into one blinding knot of chakra. | 3/10. "Looks like a Shakunetsu Sakura skill and doesn't reflect the ability." | **Four elemental streams** (fire red-orange, water blue, earth amber, wind pale green) **braiding into one white-hot knot**. Compact and dense, like a fist of light. No pink or magenta. |
| **Ethereal Rebirth** (`K0t6Z-Q4lau1jFt8Tkpot`) | S rank, 60 AP, one opponent: damage; the user absorbs and deals less. Text: the user cracks open the seal on their soul and remakes themselves. | 0/10. "Reads more like poisonous energy explosion than an ethereal rebirth. Bad direction and quality." Director: "spinning energy... more light blues"; multiple colours: "Sure". | **Spinning restorative energy rising**: an open ring or halo of light-blue energy turning upward, edged with soft prismatic colours, with motes ascending. Open and expanding (rebirth), unlike Nexus's tight knot. No green flame. |

### 5.3 Normal (5)

Basic D-rank jutsu that every player sees. If the director adopts D2, these lose most of their glow.

| Jutsu | Does | Score and feedback | Proposed subject |
|---|---|---|---|
| **Poisonous Senbon** (`H9XLJiU1YEro03QJ2mH8q`) | D rank, 60 AP, one opponent: damage. Text: a handful of poison-laced senbon. | 5/10. "Decent idea but... doesn't read as TNR premium pixel art." | Keep ours' idea (ours = element): **three senbon flying on a diagonal** with poison beading off their tips. Rendered as premium pixel art on a dark green-black background rather than a void. |
| **Replacement Technique** (`clh4d6pok0002tb0hx1bxro6l`) | D rank, 20 AP, move to an empty tile. Text: vanishes in a puff of smoke, leaving a decoy, and reappears elsewhere. | 3/10. "Players missed the old one... try working the two together." Director: "faithfully upgrade the old icon." | **Already briefed:** `docs/handoffs/REPLACEMENT_TECHNIQUE_REWORK_SESSION_PROMPT.md` (old scene of the ninja leaping from the log, upgraded, plus our smoke puff and swap trail). |
| **Searing Might** (`clh4d6q1j0008tb0hzthddb6m`) | D rank, 40 AP, self: takes less damage. Text: chakra ignites the user's core into a controlled blaze that reinforces muscles and pathways, a shield of inner strength. | 2/10. "A little too literal with the shield. Art doesn't read as premium pixel art." | **Inner fire, not an object:** a white-hot core whose flames flow outward along curving pathways into a protective aura, like armour made of heat. No shield shape, and no veins (Unholy Enhancement). |
| **Soul Shackles** (`clh4d6psu0004tb0hsa5cshh6`) | D rank, 60 AP, a line of opponents: damage. Text: cursed chakra chains are hurled, pierce defenses and latch onto the target's spirit. | 4/10. "Where are the shackles going? They just stop midair. Might be better if the shackles were just spread straight across the icon." | **Spectral purple chains running straight across the icon,** edge to edge on a slight diagonal, one link snaring a torn wisp of soul flame at the centre. |
| **Venomous Phobia.** (`9oirFnLa0wejelNYpewq6`) | D rank, 40 AP, one opponent: they take more damage. Text: an airborne toxin seeps into the mind; illusions of venomous creatures. | 7/10. "Pretty good actually. Might need a better silhouette." | **Refine ours** (ours = subject): the fanged mask of green and purple miasma, with a clearer outer shape and a calmer background. |

### 5.4 Bakuhatsu (5)

Explosion release. Palette: orange, gold and white-hot light on dark smoke. Must read as **explosions**, never lava or plain
fire (R3).

| Jutsu | Does | Score and feedback | Proposed subject |
|---|---|---|---|
| **Blast Shield** (`Awyd1k1-tw4uzn-PLbcdP`) | D rank, 40 AP, ring around the user: a barrier; takes less damage. Text: a massive explosion around the user neutralises incoming attacks. | 6/10. "Reads as a generic shield with a recolor. Could use the actual blast/shockwave. It also kicks up a physical barrier of earth around the user in a circle." | A **shockwave dome bursting outward** from the centre, with a **ring of upheaved earth slabs** thrown up around its base as a wall. Explosion light behind the slabs. |
| **Charge 4 Explosion** (`rOqCTqNBSW_A-QYesFBw9`) | C rank, 40 AP, one opponent: burning wounds; both sides deal and take more damage. Text: the battlefield covered in explosive chakra; small explosions all around. | 4/10. "Unique and creative but not high quality or premium." | Explosive **chakra charges scattered across cracked ground, detonating in a chain**, the nearest one bursting. Premium rendering. See D5 for the C4 shape. |
| **Howitzer Crash** (`hW4IV1Hp59BqVFx0u-gTd`) | B rank, 60 AP, area at range 5: the user moves, deals damage, and weakens defenses. Text: explodes the space behind them to launch at the opponent, then detonates on arrival. | 6/10. "Decent execution but lacks any real pop or skill identity." | **Two explosions on one diagonal:** a launch blast at lower left and a blazing projectile streaking to an impact burst at upper right. The streak is the hero. |
| **Inferno Cataclysm** (`FTTl_wnTlbvOfOyiGCc-b`) | A rank, 60 AP, ground spiral: heavy damage, recoil to the user. Text: the user slams their hands into the ground and the heat erupts. | 6/10. "Visuals don't look premium and reads more like a lava skill than an explosion skill." | A **towering detonation**: a white-hot blast column rising into a billowing fireball, with a shockwave ring racing across the ground. Smoke and blast light, no molten rivers or lava cracks. |
| **Kinetic Nova** (`y8y01n9jz16bz5EBzl4wr`) | A rank, 60 AP, area: damage and a wound. Text: a ball of chakra flung at the target explodes, showering the area in tiny explosions. | 9/10. "Pretty good. Maybe a little polish." | **Polish ours** (ours = subject): the cluster burst, with a clearer central blast and less clutter at the edges. |

### 5.5 Aerathiel (5)

The weakest family: four of five at 1/10. Every icon needs the family look rebuilt: **teal and cyan particle energy with
pale gold accents on deep navy** (use the old icons for palette, R5), premium pixel art (R1), restrained glow (R7), and five
clearly different silhouettes (R4). Today three of them are teal swirls; that must not happen again.

| Jutsu | Does | Score and feedback | Proposed subject |
|---|---|---|---|
| **Atomic Shield** (`FGSJC-7Zd0BYh7-tvsUdH`) | D rank, 40 AP, self: reflects damage, hits harder. Text: a translucent barrier made of the particles around them. | 1/10. "Doesn't have premium pixel art, color scheme is wrong for Aera. Loses most of the teal and particle barrier aspects for a generic bubble." | A **shell of fine teal particles** held in a hexagonal lattice, a strike glancing off it with a reflected spark. Clearly made of particles; not a bubble and not a swirl. |
| **Death's March** (`UgYXqNIJNjLGkAS5b5udH`) | B rank, 60 AP, area: damage; they take more damage. Text: a radiant chakra tunnel envelops the target; the enemy's form crumbles. | 1/10. Same art style issue; "too similar to Windshear Decay and Atomic Shield". | A **straight vertical tunnel of teal light** bearing down, with matter breaking apart into rising particles at its base. Vertical and still, not swirling. |
| **Decaying Touch** (`Zr6Zo2NcXxWuL13ufQsHw`) | B rank, 60 AP, one opponent: damage, recoil to the user. Text: a dust cloud; the user's touch, then the body becomes dust. | 1/10. Same art style issue; "hand looks unnatural". | A **single point of teal contact** in a cloud of drifting dust, from which disintegration cracks spread outward and crumble into motes. No hand. |
| **Particle Cannon** (`egtCp5UC5pRwxz7egJm7J`) | A rank, 60 AP, one opponent: damage, a wound. Text: fingers weave a triangle; a radiant orb unfurls into a brilliant beam. | 4/10. "Decent execution on this one but needs an art style improvement." | Keep ours' idea (ours = element): a **beam firing through a triangle of light**, in the rebuilt family style; the beam leaves the frame at an angle rather than straight at the viewer. |
| **Windshear Decay** (`VmoEzExhfgtzme2b5RuzJ`) | A rank, 40 AP, area: enemies deal less, take more, and attacks are redirected. Text: a torrent of razor-sharp wind slashes tears towards the target. | 1/10. Same art style issue; "resembles Death's March and Atomic Shield too much". | **Straight razor-wind slashes crossing** the frame (three to five long blade-strokes of teal air), with fragments shearing off. Straight lines, not a curl. |

### 5.6 Vaporia (5)

Boil release: fire and water together. Staff like the family ("looks so solid and encompasses the names of the jutsu so
well"); the asks are premium art (R1), **water that looks like water drops** (Aven: beaded, droplet texture), and telling
Surfing Strike apart from Azure Dragon Palm (D3). Restyle together so the five match.

| Jutsu | Does | Score and feedback | Proposed subject |
|---|---|---|---|
| **Azure Dragon Palm** (`pBsG-Jw4TTkSjxfqzjG6b`) | A rank, 60 AP, one opponent: piercing damage, heals the user. Text: a water dragon encases the user like armour; every strike is mirrored by the dragon. | 6/10. "Needs more premium art." | Keep ours (ours = subject): the **blue water dragon**, head facing left, drawn in beaded water. |
| **Drowning Strike** (`eZqJ9qJ_f43VRg_HhRiyb`) | D rank, 60 AP, ground spiral: damage; they take more damage. Text: a fist of scorching water strikes and floods the target. | 6/10. "Needs more premium art." | A **fist formed of boiling water** (water, not a hand) driving forward in a burst of spray and steam. |
| **Liquid Ember Shell** (`fWb24FYrbTqYvE9GIEA49`) | B rank, 40 AP, one opponent: burning wounds, lifesteal, the user hits harder. Text: fire and water merge into a molten liquid shell that absorbs attacks. | 8/10. "May just need updating to the same art style as the others." | Keep ours (ours = subject): the **water sphere with embers churning inside**, restyled to match the family. |
| **Scorch Break** (`6v7dfraXRVo5K3NbgixzT`) | B rank, 60 AP, area: damage, reflect. Text: chakra in the palms turns to steaming liquid; a flurry of searing punches. | 6/10. "Needs more premium art." | A **flurry of steaming impact bursts** (three or four, water rings with hot orange cores) cracking a wall of water. |
| **Surfing Strike** (`M-iPxOupEp35-KptpG4DV`) | A rank, 60 AP, area: the user moves, deals damage, takes less damage. Text: a torrent floods the battlefield; the user glides over the steaming surface. | 6/10. "Needs more premium art. Resembles the Azure dragon a bit too much at thumbnail size." | A **low, horizontal wave rolling left to right** with a long steaming trail; wide and flat where the dragon is tall and coiled (D3). |

### 5.7 Blue Blade Eyes (8)

All eight scored 8/10 with one shared flaw: "The background is too noisy and makes the skill icon too difficult to make out"
(Aven: "very bright and very busy"). Keep each concept (ours = subject) and fix the treatment: **a dark, calm navy
background**, the ice subject brightest, fewer stray shards. Palette: icy white and blue on deep navy.

| Jutsu | Does | Proposed subject |
|---|---|---|
| **Arctic Frost** (`0tPhVC7G21Ej99YSICtJO`) | A rank, 40 AP: the blade is encased in ice; lifesteal. | The sword trailing a sweeping arc of frost, on a dark background. |
| **Blade Resonance** (`TFRsEeV-VacukUUop-dtN`) | A rank, 60 AP: a blade of ice disrupts the target's defenses. | The ice blade upright at the centre of concentric resonance rings, rings fading into darkness. |
| **Blue Crimson** (`bxIPWiqiEaCmPYfAysB5a`) | C rank, 60 AP, area: the user flickers around the target. | Afterimage slashes arcing around a centre point, three or four strokes only. |
| **Glacial Volley** (`Bw2OBS92Xi-4YlfErS632`) | B rank, 60 AP: ranks of ice lances volley at the target. | Ranks of ice lances flying in one direction, the lead lances largest. |
| **Ice Shackles** (`Aff56oo9BFTcoLLeEyOja`) | B rank, 60 AP: frost locks the target in blue ice; stun. | Ice chains crossing to a frozen lock at the centre. |
| **Icebound Might** (`YGBz7eIDvLwWXSVFEcK9j`) | B rank, 60 AP, area: ice armour; a shield; enemies deal less. | **Old = subject:** "the original's looming Susano'o-like ice summon reads better than our zoomed-in ice sculpture." A towering ice guardian looming above, full figure visible, original design (not anime Susano'o armour). |
| **Quintessential Flake** (`dXOjSl1vNp5G5BsFrNPkh`) | C rank, 40 AP: the user moves; the area freezes. | One bold snowflake, clean and symmetrical, on darkness. |
| **Sapphire Command** (`gIEy7THAZdXgcak5zs5U6`) | C rank, 40 AP: a pulse of Blue Blade chakra freezes the target's flow. | Two or three diagonal ice slashes crossing the frame, the rest dark. |

## 6. How to produce them

**Art director:**

1. **One jutsu per isolated generation session** (`docs/workflows/ISOLATED_ART_GENERATION.md`). Each brief carries the jutsu
   target lock (id and name above), the proposed subject, the family palette, rules R1–R9, and the section 3 exclusions.
2. **References:** at most two per generation, each with its role stated. Typical pair: the jutsu's old or ours image
   (*subject* or *element*, as the table says) plus one kept icon from section 3 (*style* only). Pull the images from the
   review cards or `docs/design/icon_overhaul/src/NN_<slug>_original|_ours`.
3. **Fail fast before returning a raw:** unreadable at 45 px; background busier than the subject; looks like a section 3
   icon or a family sibling; text or insignia; anatomy errors.
4. **Return the raw images only,** named `raw_<slug>_<candidate>.png`. Do not process, crop, upscale, key or upload them.

**Claude Code** (everything after the raw):

5. Intake into `art/jutsu_icons/overhaul_2026_10/candidates/<slug>/`; previews in context (mobile bar, desktop bar, 112 px
   tile with badge, 32 px, silhouette test) next to the old icon; old / new sheets for the staff thread.
6. After the director picks: processing, export (256 px lossless WebP), `artpreflight --type JUTSU_ICON`.
7. Text: drafts for any jutsu whose name, description or battle text no longer matches its approved art (Abyss of Shadows
   and Ethereal Rebirth at least), for the director's approval.
8. The batch manifest once all 36 are approved: the 36 new icons, the 15 kept icons, any approved text, and the AI
   unequip/re-equip cycle where an equipped jutsu changes (`docs/design/icon_overhaul/BATCH_PLAN.md`).

**Suggested order:** Replacement Technique (briefed), then the families with the clearest direction and the most to gain:
Aerathiel, Forbidden, then Event, Normal, Bakuhatsu, Vaporia, and Blue Blade Eyes last (a treatment fix on approved
concepts).
