# The Mender: Skyglass legendary boss pitch (Nov 9)

Status: PITCH. Nothing built. Builds only on dauntless's okay, hidden first.

## 1. Who he is

**Okabe, the Mender.** The war-ship's master carpenter. The Core rebuilds the crew and the hull every time they break, and
someone had to be its hands. Okabe was recalled to mend the hull forever. Now the Core is cracked and the wreck's halls
close and move on their own (canon: "halls close, stairs move, rooms come and go"). In the lower hold, Okabe is the one
closing them. He mends the hold shut around anything that does not belong in it. You.

- Look: a broad, stooped shipwright echo in tarred work-wraps and a leather apron, a huge carpenter's mallet with a
  skyglass head, skyglass rivets in a belt pouch, a chalk-line reel at his hip. Skyglass cyan accent.
- Opening line: "Mind your feet. The hull's coming in."
- Defeat line: "...Leave it open. Just this once."
- Ties to the story: "Nothing ever finishes, so nothing ever stops." He is the reason a chart is only good while the ship
  holds its shape. He never appears anywhere else.

## 2. The chart run

**Chart of the Closing Hold** (Legendary). Entry: the chart. Rank S, isolated, carried HP and chakra, no refills, the
first loss ends the run, no flee route. Requires level 40+ (see feasibility: quest arenas under 40 are smaller).

| Step | What happens | Teaches |
|---|---|---|
| Dialog | The lower hatch. The hold is being rebuilt around you; you can hear a mallet. | |
| Fight 1: **Okabe's Apprentice** | Short fight (5-6 rounds, about 4,000 HP). Lays Fresh Planks and swings one weak Hammerfall; the outer ring closes once at round 3. | the ring, and "stand on the warm plank" |
| Dialog | The hold is narrower than it was a minute ago. | |
| Fight 2: **Bilge Crew** (hidden copies of two existing crew AIs) | 6-8 rounds. Each copy carries a weak Keel Splitter. | read port or starboard and cross |
| Dialog | The keel room. Okabe turns around. | |
| Boss: **Okabe, the Mender** | All three mechanics together, the hold closing by quarters. | |
| Ending | Rewards (section 7). | |

Every chart-run rule holds: lose = run over, no fleeing. The two warm-up fights reuse existing art; only the boss needs a
new avatar.

## 3. The arena: the hold closes in

The battlefield is 12 x 10. Each tier is an outer band of tiles that becomes **glass-grown hull**. Standing on it gives,
for as long as you stand there:

- **Seal:** your bloodline's passive bonuses switch off.
- **Heal Prevent:** no healing.
- **Buff Prevent:** no new buffs (buffs you already had keep running).
- **+40% damage taken** from his normal hits.

Step off and all four end at once. Nothing carries over.

| Tier | Trigger (whichever comes first) | Band | Safe floor left |
|---|---|---|---|
| 1 | boss below 75% HP, or his round 4 | outer edge (40 tiles) | 10 x 8 |
| 2 | below 50%, or round 7 | next band (32) | 8 x 6 |
| 3 | below 25%, or round 10 | next band (24) | 6 x 4 |
| 4 (enrage) | round 15 | next band (16) | 4 x 2 |
| Sealed | round 18 | everything | none: the hold seals and the fight ends you |

How a tier lands: on his turn he **marks** the band (seams of cyan light run through the planks, "the timbers groan").
You get your whole next turn to step in. On his next turn the band **closes** and stays for the rest of the fight.

## 4. Abilities

| Ability | Telegraph | Lands | Damage (endgame player, about 6,250 HP) | How you answer |
|---|---|---|---|---|
| **Rivet Volley** | none (his steady attack) | the turn he uses it | about 5% (310) normal damage, 7% if you stand on the hull | nothing to dodge: it is the clock |
| **Keel Splitter** | he snaps a chalk line down the keel and calls a side: **Port** (left 6 columns) or **Starboard** (right 6). Always alternates, Port first. | next turn | 40% (2,500) pierce to anyone on that side | cross the keel. Plan your path around the closed hull. |
| **Fresh Planks**, then **Hammerfall** | 3 warm amber planks appear inside the safe floor (2 in tier 3+). The only warm colour in the fight: warm = safe. | next turn he slams the deck | 50% (3,125) normal damage; 12% on a fresh plank (75% less); 70% if you are on the hull | go stand on a plank |
| **The hold closes** (section 3) | seams of light through the band | next turn | none directly; the hull makes every normal hit worse and cuts your heals and buffs | stay inside |

Turn budget (100 AP): a mark costs 40, a payoff or Rivet Volley 60, so he does one mark and one payoff per turn, never two
payoffs. A normal cycle runs: Rivet + Splitter mark, then Splitter breaks + Planks, then Hammerfall + Rivet. A tier mark
or close takes the 40-AP slot that turn and pushes the other mark back a turn ("the hold takes his full attention").

He carries **stun immunity** for the whole fight, so stuns can never skip a tier or a payoff (the Mother of Echoes issue
where half the marks never broke came from stuns draining her turn).

## 5. Targets

- Boss HP about 16,000 (the Glasswright is 20,000), target 12-14 rounds. Tier 4 at round 15 is the soft enrage; round 18
  is the hard enrage.
- Apprentice about 4,000 HP, 5-6 rounds. Bilge Crew 6-8 rounds.
- Clean play (every Splitter crossed, every Hammerfall on a plank, never on the hull) ends the boss near 25-35% HP
  without heals. One mistake is survivable if you heal; two in a row kill.
- Numbers are tuned in the sim to these targets before anything goes live, as with the Mother of Echoes.

## 6. How it differs from what is live

- Not the Herald's oaths: no terms or handicaps chosen before the fight.
- Not the Mother of Echoes: no line marks you step off, no rings under you or around the boss, HP carries only as every
  chart run does. The arena itself changes and stays changed.
- Not Crownhold's rites, puzzles or alarms.
- New answers: cross the whole room, run to a safe spot (the reverse of every live telegraph), and manage shrinking space.

## 7. Rewards (proposal, legendary-run level)

Pick 2 of Skyglass Coffer x2 / Sealed Treasury / Skyglass Token x2 / Galley Stores x3. Lastlight Lantern 30%, Core Rot
40%, Shard of the Keel 50%, an Okabe variant token 4%, exp ladder VI (5,000), Sealed Treasury 6%.
Chart sources: Skyglass Wreck (endgame) 2%, The Spoiled Hold endings 5%.
Ships in a Friday release only on dauntless's go (it will not be ready for Nov 13).

## 8. Feasibility (what the game already does)

Seen working live:
- Tile-exact casts anywhere on the board (the Refraction lines).
- A lingering no-healing floor (The Hush, 8 rounds).
- Floor tiles that add damage taken and cut healing (Refraction Breaks).
- AI rules that fire by round or by HP.

Read in the game's current code (studie-tech/TheNinjaRPG, Nov 9):
- Anyone standing on an effect tile gets that effect on every action while they stay; it is dropped the moment they step
  off ("User effects from Ground effects are not forwarded to the next round", process.ts applyGroundEffects).
- A tile effect lands with no one-round delay (it is written one round old).
- Seal on a tile switches off bloodline passive tags while standing there; it does not lock bloodline jutsu.
- Buff Prevent stops buffs created after it; buffs cast earlier keep running (preventCheck compares creation rounds).
- +X% damage taken does not raise pierce, so the hull punishes Rivet Volley and Hammerfall, not the Splitter.
- Planks: a tile that cuts damage taken by 75% works the same way, and does reduce normal damage (not pierce).
- A tile effect can last up to 100 rounds, and one tag can list up to 400 tiles.
- Quest arenas scale with level: under 20 is 9 x 8, under 30 is 10 x 9, under 40 is 11 x 10, 40+ is 12 x 10. Hence
  the level 40 gate.

Still to test on a hidden copy, as the first build step:
1. All four effects on a hull tile and gone on stepping off (seal and buff prevent are the two not yet seen live).
2. Each tier casts once, on time, with stun immunity.
3. The fight stays responsive at the tightest tier: about 112 hull tiles x 4 effects = about 450 tile effects.
   Fallback if it drags: drop tier 4 (about 384).
4. Planks reduce Hammerfall as planned.

Not done yet: the offline engine test was refused in this session (it needs a package install); a live test fight
means fighting on an account, which needs dauntless's call.

## 9. Animations (approved soft-light style, 2.5 hex clips, per-hex pieces)

All art sits on the damage and telegraph effects themselves: telegraph art on the standard non-visual carrier, lasting
art on the lasting effect, payoff art on the payoff. No extra positioned visual effects.

| # | Clip | Sits on | Painted piece |
|---|---|---|---|
| A1 | Hull omen: cyan seams open between the planks, frost-glass creeping in from the wall side | tier mark carrier, loop, 1 round | P1 |
| A2 | Hull closes: faceted skyglass plates punch up through the deck and lock; fades to a faint glass-grown floor (about 18%) | tier close (Heal Prevent tag) appear + static | P2 |
| A3 | Splitter omen: a chalk line snaps down the keel, cyan chalk dust lifts along it | Splitter mark carrier, per hex on the called side | P3 |
| A4 | Splitter breaks: the deck splits, splinters and glass shards spray up | Splitter pierce, per hex | P4 |
| A5 | Fresh Plank: one warm amber new-cut plank with a soft gold glow, gently breathing | plank carrier, loop, 2 rounds | P5 |
| A6 | Hammerfall: the mallet's shockwave, a ring of glass dust and splinters | Hammerfall, on the player | P6 |
| A7 | Rivet Volley: three skyglass rivets punch in | Rivet Volley, on the player | P7 |
| A8 | Last tier aura: cyan sawdust and light rising off Okabe | self-buff carrier at tier 3 | P2 reused |
| AV | Okabe avatar | AI avatar | avatar prompt |

Paint prompts are in section 10.

## 10. Paint prompts (one image each, generate one at a time)

Shared notes: every effect piece is light painted on pure black, so the code can lift the black away and animate it.

### P1 Hull omen
Target: one light effect piece for The Ninja RPG, the Skyglass boss Okabe the Mender: frost-glass seams creeping across a ship's deck plank.
Style: Edo-era Japanese fantasy ninja art, soft painterly light with crisp edges, pale skyglass cyan (#98c1cc brightening to near-white) and faint white frost; no other colours.
Canvas: 1254 x 1254, one element centred with a clear margin, nothing else.
Subject: three or four thin seams of pale cyan light running across the canvas like cracks between planks, with feathery frost-glass crystals growing out from the seams toward one side, brightest where the seams meet, fading to nothing at their ends.
Background: pure flat black (#000000) covering the whole canvas. Only the light is painted; no wood, no floor, no texture in the black.
Avoid: no text, runes, glyphs or symbols; no character, hands or tools; no scenery; no frame; no glow disc or halo; no second element.
Generate ONE image. Do not crop, key or resize it.

### P2 Hull closes
Target: one light effect piece for The Ninja RPG, the Skyglass boss Okabe the Mender: skyglass hull plates bursting up through a deck.
Style: Edo-era Japanese fantasy ninja art, soft painterly light with crisp faceted edges, pale skyglass cyan (#98c1cc brightening to near-white) with a few deep teal shadows inside the crystal; no other colours.
Canvas: 1254 x 1254, one element centred with a clear margin, nothing else.
Subject: a tight cluster of five to seven flat, faceted skyglass plates thrust upward at slight angles like new hull planks made of crystal, edges lit bright, a burst of fine glass dust and a few small shards thrown out around their base.
Background: pure flat black (#000000) covering the whole canvas. Only the crystal and its light are painted.
Avoid: no text, runes, glyphs or symbols; no character; no wood floor or scenery; no frame; no glow disc or halo; no second element.
Generate ONE image. Do not crop, key or resize it.

### P3 Chalk line snap
Target: one light effect piece for The Ninja RPG, the Skyglass boss Okabe the Mender: a carpenter's chalk line snapping down a deck.
Style: Edo-era Japanese fantasy ninja art, soft painterly light with crisp edges, pale skyglass cyan (#98c1cc brightening to near-white) chalk dust; no other colours.
Canvas: 1254 x 1254, one element centred with a clear margin, nothing else.
Subject: one perfectly straight thin line of bright cyan light running vertically through the centre of the canvas, with a soft puff of fine cyan chalk dust lifting off it along its whole length, densest in the middle.
Background: pure flat black (#000000) covering the whole canvas. Only the line and dust are painted.
Avoid: no text, runes, glyphs or symbols; no string reel, hands or character; no wood or scenery; no frame; no glow disc or halo; no second element.
Generate ONE image. Do not crop, key or resize it.

### P4 Deck splits
Target: one light effect piece for The Ninja RPG, the Skyglass boss Okabe the Mender: a deck splitting open in a spray of splinters and glass.
Style: Edo-era Japanese fantasy ninja art, soft painterly light with crisp edges, pale skyglass cyan (#98c1cc brightening to near-white) light with dark blue-black wood splinters lit along their edges; no other colours.
Canvas: 1254 x 1254, one element centred with a clear margin, nothing else.
Subject: an upward burst from the bottom centre: long jagged wood splinters and sharp skyglass shards flung up and outward in a fan, a bright cyan crack-light at the burst's root, fine dust trailing the pieces.
Background: pure flat black (#000000) covering the whole canvas. Only the burst is painted.
Avoid: no text, runes, glyphs or symbols; no character; no floor or scenery; no frame; no glow disc or halo; no fire; no second element.
Generate ONE image. Do not crop, key or resize it.

### P5 Fresh plank
Target: one light effect piece for The Ninja RPG, the Skyglass boss Okabe the Mender: a single fresh-cut plank that marks a safe spot.
Style: Edo-era Japanese fantasy ninja art, soft painterly light with crisp edges, warm amber and soft gold (#e8b45a brightening to pale cream); no cyan, no other colours.
Canvas: 1254 x 1254, one element centred with a clear margin, nothing else.
Subject: one short new-cut wooden plank seen from slightly above, pale honey wood with a clean grain, glowing warmly from within, a soft gold light lifting off its top edge and a few slow motes of sawdust above it.
Background: pure flat black (#000000) covering the whole canvas. Only the plank and its light are painted.
Avoid: no text, runes, glyphs or symbols; no character or tools; no floor or scenery; no frame; no glow disc or halo; no second element.
Generate ONE image. Do not crop, key or resize it.

### P6 Hammerfall
Target: one light effect piece for The Ninja RPG, the Skyglass boss Okabe the Mender: the shockwave of a giant mallet striking a deck.
Style: Edo-era Japanese fantasy ninja art, soft painterly light with crisp edges, pale skyglass cyan (#98c1cc brightening to near-white) with a white-hot centre; no other colours.
Canvas: 1254 x 1254, one element centred with a clear margin, nothing else.
Subject: a flat, wide shockwave ring seen at a low three-quarter angle, a bright impact flash at its centre, a ring of glass dust and small splinters thrown outward along the ring, a few cracks of light radiating from the centre.
Background: pure flat black (#000000) covering the whole canvas. Only the shockwave is painted.
Avoid: no text, runes, glyphs or symbols; no mallet, character or hands; no floor or scenery; no frame; no fire; no second element.
Generate ONE image. Do not crop, key or resize it.

### P7 Skyglass rivet
Target: one light effect piece for The Ninja RPG, the Skyglass boss Okabe the Mender: a skyglass rivet in flight.
Style: Edo-era Japanese fantasy ninja art, soft painterly light with crisp faceted edges, pale skyglass cyan (#98c1cc brightening to near-white); no other colours.
Canvas: 1254 x 1254, one element centred with a clear margin, nothing else.
Subject: one short, thick faceted skyglass rivet with a domed head, flying diagonally from upper left to lower right, a long tapering streak of cyan light behind it, a few fine glass flecks shed along the streak.
Background: pure flat black (#000000) covering the whole canvas. Only the rivet and its streak are painted.
Avoid: no text, runes, glyphs or symbols; no character or hands; no target or scenery; no frame; no glow disc or halo; no second rivet.
Generate ONE image. Do not crop, key or resize it.

### AV Okabe avatar
Target: Okabe, the Mender, one AI battle avatar for The Ninja RPG's Skyglass legendary chart, the Chart of the Closing Hold.
References attached: 1. avatar_ghost_ship_crowned_captain_b.webp: STYLE-ONLY: the Skyglass crew's rendering, palette, outline weight and how skyglass crystal sits on dark cloth; this is a different person, described by the text. Follow each reference only for its stated role.
single ninja character, full body, dynamic combat stance, crisp pixel lineart, flat cel shading, limited palette, soft even lighting, camera at eye level, flat 3/4 view, no low angle and no foreshortening, both arms held within the subject's own silhouette and touching nothing, at most one restrained elemental glow accent, as rim light on edges only, centered, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard, no shadow cast onto the green
SUBJECT: Okabe, the Mender, the war-ship's master carpenter recalled to mend the hull forever: a broad, stooped, heavy-shouldered man in tarred dark indigo work-wraps and a scarred leather apron, a cloth mask over his lower face so only tired, steady eyes show, forearms bound in rope; both hands on the haft of a huge carpenter's mallet with a faceted pale-cyan skyglass head resting on his shoulder; a pouch of skyglass rivets and a chalk-line reel at his belt; thin skyglass splinters growing from his apron's hem as if the ship is mending him too. Accent: skyglass cyan.
Costume grammar: dark layered wrap robe, neck cowl or scarf, one accent colour as piping, wrapped forearms, plain buckled belt
Negative: no text, no UI, no watermark, no chibi, no blur, no soft pastel, no muddy dither, no background scenery, no aura, no halo, no light field, no glow disc, no lime spill on the character, no multiple characters, no checkerboard background, no transparent-preview background, no white or grey background, no gradient green, no asset sheet, no grid, no labels, no franchise insignia, no desk, no table, no furniture, nothing resting on a surface; no headband, no forehead protector, no clan symbol, no village mark, no real-world logo, ever. Generic masks, wraps, hoods and blank plates only.
Generate ONE image. Do not crop, key, resize or otherwise process it.
