# Skyglass event: player-facing text

**Status:** DRAFT for the director (Lane B design text, 2026-10-29). Every line is written to `SKYGLASS_STORY_BIBLE.md`
(canon, voice, "relieved" rule) and to the design of record: `SKYGLASS_LOOT_TABLES.md` (§0 "every item explains
itself", chest HTML format), `SKYGLASS_THE_HAUL.md`, `SKYGLASS_BOSS_FIGHTS.md`, `SKYGLASS_PETS.md` (only the Little
Horror ships) and RUL-2026-10-28-009 … RUL-2026-10-29-056 (latest wins). This file owns no rule: where it disagrees
with those, they win and this text is rewritten.

Generators copy from here; they do not paraphrase. Chest rate lines are the expected output of the cache tables
(loot tables §0: "descriptions are generated from the same tables"), so a generator that renders them must match these
lines exactly, and `scripts/skyglass_check.py` compares the two.

## How to read this file

**Targets.** Every entry is headed with its target:

| Notation | Meaning |
|---|---|
| `item:<Name>.description` | item record field |
| `quest:<Name>.description` / `.successDescription` | quest record field |
| `obj:<quest>/<node>.description` | objective (node) field; node ids follow the generator's naming |
| `obj:<quest>/<node>.choice[<n>]` | a dialog choice's `text` |
| `obj:<quest>/<node>.failDescription` | battle objective field (also `drawDescription`, `fleeDescription`) |
| `jutsu:<Name>.description` / `.battleDescription` | jutsu record field |
| `variant:<Base>/<Variant>.name` / `.description` | item variant row (`ItemVariant`) |

**Formats.**
- Item descriptions and objective descriptions render basic HTML (theninjarpg `utils/parse.ts` parseHtml): `<br>`,
  `<b>`, `<i>`, `<span style>`. Quest-record descriptions follow the live Skyglass quests and use plain paragraphs
  (a blank line between them).
- No em dashes anywhere in player text (`skills/building-tnr-content/references/quest.md`, dialog rule; applied to all
  Skyglass text for consistency).
- `%user` and `%target` are the battle-log placeholders. Battle text is action first: what the user is doing
  (RUL-2026-10-28-028 item 5).

**Field limits** (theninjarpg@2af4b320 `drizzle/schema.ts`, `validators/objectives.ts`; skill
`data/45d_DATA_entity_schemas.json`):

| Field | Limit | Longest entry here |
|---|---|---|
| item / variant / jutsu / quest `name` | 191 | 39 (`Ledger Page: The Snare Room`-class names) |
| quest `description`, `successDescription` | 5,000 | about 900 |
| item, variant, jutsu `description`, `battleDescription` | `text` (no hard limit) | about 1,500 (Crown's Hoard) |
| objective `description`, choice `text` | no schema limit | about 700 |
| badge `description` (not used here) | 500 | — |

No entry needed trimming. House targets kept for the phone screen: choice text at most about 80 characters; item
stories one line.

**Banned words** (story bible, Voice, parsed by `scripts/skyglass_check.py`): system, network, lattice, interface,
protocol, terminal, personnel, maintenance, conduit, lift, reactor, data, scan, unit; plus the phrase "seven-bladed".
None appears below in player text. **"Relieved"** appears only in the refrain ("No one is relieved." / "None is
relieved."). The Haul's ledger uses the crossed-out due date without the word (see open question 3).

**Naming.** Boss skins are **variants**, never "trophies", in every player-facing string (RUL-2026-10-29-053). "Trophy"
survives only in the approved place names The Trophy Hold and the Trophy Warden, which are not skins.

## 0. What already exists, and what this file adds

| Surface | Status | Where |
|---|---|---|
| Quarantined Archive, Drowned Foundry, Captain's Watch run text | **exists** (only a stakes header and closing lines added, §6) | `state/skyglass_hunts/hunts.py` → push/319 |
| Buried Cache run text | **exists** (stakes header and one flag, §8) | push/319 (`The Buried Cache`) |
| Crownhold run text, aftermath, the Crowned Captain's lines | **exists** (stakes header only, §2.9) | `push/crownhold.gen.py` → push/319 |
| The Wreck's description | **exists**, needs the §0 chart line and a "relieved" fix (§8) | `push/skyglass_update.gen.py` `WRECK_DESCRIPTION` |
| Live item stories: Skyglass Coffer, Sealed Treasury, Archive Chart Case, Lastlight Lantern, Unmarked Cargo, Elemental Tool Pouch, the hunt charts | **exist** as one-line stories; the story lines are kept, the §0 rules are new (§4) | push/260, 270, 274, 319 |
| Library jutsu (harness `library_spec.json` b973ff28) | **exist** with placeholder names and neutral battle text; themed names and action-first lines are new (§6.4) | harness `fable/skyglass-wreck-sim` |
| Haul hazard effect lines (`applyDebuffs` descriptions) | **exist** in `haul_spec.json`; one split proposed (§3.8) | harness `fable/skyglass-haul-sim` |
| Wreck Sighted; Low Tide Run; Night Watch; Sealed Reliquary; The Fall; Rotted Reliquary; Burning Heading; both steeping quests | **new** (§1, §2) | none before |
| The Haul: 6 pages, tags, step lines, endings | **new** (§3) | none before (only two chart descriptions in the Haul doc) |
| Item descriptions per §0 for every Skyglass item | **new** (§4) | none |
| Variant names, flavour, art lines | **new** (§5) | none |
| Steady the Helm; boss closing lines; press-on stakes lines | **new** (§2, §6) | none |
| Walked Every Deck | **new** (§7) | none |

---

## 1. Intro quest: Wreck Sighted

One-time free quest; grants the first Tide Chart (RUL-2026-10-28-028 item 2). A public quest needs scene characters
(quest.md: "Public quests require scene characters"); open question 7.

**`quest:Wreck Sighted.name`**
```
Wreck Sighted
```

**`quest:Wreck Sighted.description`**
```
The black ship that hung over the coast for decades has finally come down. Go and see what it left on the shore.
```

**`quest:Wreck Sighted.successDescription`**
```
You have your first chart. Run it from the Battle Arena, then go to the Wreck for more.
```

**`obj:Wreck Sighted/d_word.description`**
```html
Word comes down the coast road: the Ghost Ship is down. It lies broken on the sand below the cliffs, and its crew are still aboard, still standing their watch.<br><br>A salvager pushes a wet, salt-stained chart into your hands. "Took it off the wreck," she says. "The ship keeps changing inside. A chart only works while it still holds that shape. Don't sit on it."
```
- `choice[0]`: `Look at the chart`

**`obj:Wreck Sighted/d_chart.description`**
```html
It is a <b>Tide Chart</b>, marking where the low tide opens the wreck's lower hull.<br><br>The crew carry charts like this one, and the <b>Skyglass Wreck</b> gives them up. Each chart opens a treasure run in the <b>Battle Arena</b>, and is spent when the run starts.<br><br>Health and chakra carry from fight to fight, with no refills, and a lost fight ends the run. On some runs, at the last landing you choose: leave with what you hold, or press on for more. Lose after pressing on and you keep only what you held.<br><br>Clear the Wreck for more charts, and better ones.
```
- `choice[0]`: `Take the chart`

**`obj:Wreck Sighted/w_done.description`** (win_quest; reward Tide Chart ×1)
```html
The chart is yours. The Wreck waits on the shore: a dungeon for three, with a lighter version for level 45 and up.
```

---

## 2. Chart runs

**Shared lines** (every chart run battle unless a node gives its own):
- `failDescription`: `You are defeated.`
- `drawDescription`: `The fight stalls, and the chart's way closes.`
- `fleeDescription`: `You break away, and the way back closes behind you.`
- **Press-on battle** `failDescription` (it routes to the ending at the current step, RUL-2026-10-28-022):
  `You fall back, and keep only what you held.`

Every run's quest description opens with the two-line stakes summary (RUL-2026-10-28-028 item 8). Node ids follow the
harness shape (`charts_spec.json` `objectiveShape`): base fights `b1…`, the last-landing dialog `d_landing` with the
leave / press-on choice, the press-on fight `b_press`, endings `w_leave` / `w_press`, and the fail ending `f_lost`.

**Press-on rooms** (RUL-2026-10-30-060 item 6): kept on the Night Watch, the Captain's Watch, The Fall and the Rotted
Reliquary. Cut from the Low Tide Run, the Quarantined Archive, the Sealed Reliquary and the Burning Heading. A run without a
room has no `d_landing`, `b_press` or `w_press`: its last fight routes to a single win ending `w_done`, and the closing line
from the old `d_landing` opens that ending.

### 2.1 The Low Tide Run (Tide Chart)

Fights: breach (Deck Warden + Seal Charge), flooded hold (Arsenal Keeper), tide line (Skyglass Sentinel). No press-on room
(cut, RUL-2026-10-30-060 item 6). Scaled to the player.

**`quest:The Low Tide Run.description`**
```
The chart is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run.

When the tide runs far enough out, it bares the wreck's lower hull. The Tide Chart marks where the planks have opened. Go in while the water is out, and be gone before it turns.
```

**`quest:The Low Tide Run.successDescription`**: `You came out of the lower hull before the tide.`

**`obj:The Low Tide Run/d_breach.description`** (scene: lower_hull)
```html
The sea has drawn back from the wreck, and the breach is right where the Wayfinder marked it, wide enough to walk through. Inside, the Core holds the deck the way it was: dry, lamplit, ready for sea.<br><br>A Deck Warden is counting seal charges along the bulkhead. He gets to eleven, looks up at you, and starts again from one.
```
- `choice[0]`: `Go in through the breach`

**`obj:The Low Tide Run/b1.description`**: `The Deck Warden sets down his count and draws.`

**`obj:The Low Tide Run/d_hold.description`** (scene: hold)
```html
The Warden falls apart into sand and seal script, and the count goes with him.<br><br>Past the breach the hold is filling again, one wave at a time. The Arsenal Keeper stands on a crate with his ledger held over the water, checking stores that floated away years ago. "Tide stores. Wet. Logged," he says, and turns a page. "You are not logged."
```
- `choice[0]`: `Wade through the hold`

**`obj:The Low Tide Run/b2.description`**: `The Arsenal Keeper closes his ledger, and steps down into the water.`

**`obj:The Low Tide Run/d_beach.description`** (scene: cache_site)
```html
"Unlisted," the Keeper says as he falls, and makes a note of it.<br><br>The far side of the hold opens onto the sand beneath the hull. The tide has turned. A Skyglass Sentinel stands at the waterline, shell and stone, and the surf runs up to its feet like a dog called to heel.
```
- `choice[0]`: `Hold the beach`

**`obj:The Low Tide Run/b3.description`**: `The Sentinel plants itself at the waterline. Behind it, the sea is gathering.`

**`obj:The Low Tide Run/w_done.description`** (win; follows `b3`)
```html
The Sentinel sinks back into the sand, and the surf goes back to being only surf.<br><br>You walk out through the breach as the first wave comes back in. Behind you, the hull is already closing.
```

**`obj:The Low Tide Run/f_lost.description`**
```html
The tide comes back in over you. You wake on the sand, soaked, with nothing but the spent chart.
```

### 2.2 The Night Watch (Watch Roster)

Fights: first watch (Deck Warden + Seal Charge), middle watch (Oathkeeper), last watch (Deck Warden + Oathkeeper);
press-on: the Second Watch (First Blade). Scaled to the player. The loot tables say the run "ends with you relieving the
Deck Warden"; the text shows it without using the word (bible, Voice).

**`quest:The Night Watch.description`**
```
The roster is spent when the watch starts. Health and chakra carry from fight to fight, and a lost fight ends the run.
After the last watch, leave with what you hold or stand the Second Watch; lose it and you keep only what you held.

The duty roster still hangs by the Deck Warden's post. At the bottom, in fresh ink, someone has added a new name: yours. Stand three watches back to back, and the post is yours.
```

**`quest:The Night Watch.successDescription`**: `You held the Deck Warden's post through the night.`

**`obj:The Night Watch/d_post.description`** (scene: deck_b)
```html
The deck is dark but for the lanterns. The Deck Warden stands his post by the roster board, exactly where he has stood for a generation. He reads your name off the board, then reads it again.<br><br>"New name," he says. "First watch. Hold the deck."
```
- `choice[0]`: `Take the first watch`

**`obj:The Night Watch/b1.description`**: `The Deck Warden draws. "Drill," he says. "Hold."`

**`obj:The Night Watch/d_middle.description`**
```html
"Held," the Warden says, picking himself up, and makes a mark beside your name.<br><br>The bell strikes the middle watch. The Oathkeeper climbs to the deck in an officer's coat faded by no weather and checks the roster against a list of his own. "A roster is a term of service," he says. "Terms are kept. I will see that you keep yours."
```
- `choice[0]`: `Stand the middle watch`

**`obj:The Night Watch/b2.description`**: `The Oathkeeper takes the deck as if he has always had it.`

**`obj:The Night Watch/d_last.description`**
```html
"The term holds," the Oathkeeper says, and steps back to the rail.<br><br>Near dawn, or what the Core remembers of dawn, they come together: the Deck Warden and the Oathkeeper, side by side. "Last watch," the Warden says. "Hold it and the post is yours. No one is relieved." The Oathkeeper says nothing, which is as close to agreement as he comes.
```
- `choice[0]`: `Hold the last watch`

**`obj:The Night Watch/b3.description`**: `The Deck Warden and the Oathkeeper close in from both ends of the deck.`

**`obj:The Night Watch/d_landing.description`** (press-on choice)
```html
The Deck Warden goes down on one knee by the roster board and looks at your name for a long time. "Post held," he says. He unhooks his lantern and hangs it on your side of the board. Then, for the first time in a generation, he sits down.<br><br>Under your name a second line has appeared, in a hand you do not know: SECOND WATCH. Down the deck, someone is whistling.<br><br><b>End your watch now and keep everything you hold. Stand the Second Watch and win, and it adds to the haul. Lose it and you keep only what you hold now.</b>
```
- `choice[0]`: `End your watch and go`
- `choice[1]`: `Stand the Second Watch`

**`obj:The Night Watch/b_press.description`**: `The First Blade drops onto the deck, twin cleavers forming from the gale. "Finally. Something new."`

**`obj:The Night Watch/w_leave.description`**
```html
You leave the Warden's lantern hanging on the board. By morning the roster has rewritten itself, and your name is gone from it.
```

**`obj:The Night Watch/w_press.description`**
```html
The First Blade lies on the deck, laughing quietly. "That was new," he says. You leave the Second Watch to the gale.
```

**`obj:The Night Watch/f_lost.description`**
```html
You fall at your post. When you wake, there is a new name at the bottom of the roster, and it is not yours.
```

### 2.3 The Sealed Reliquary (Reliquary Seal)

Fights: Foundry Warden; Sealwright + Lingering Echo; Skyglass Sentinel + Lingering Echo; the First Blade + Lingering
Echo. No press-on room (cut, RUL-2026-10-30-060 item 6). Twist: each fallen echo's set piece lingers (Boss Fights §8).
A failed run pays 1 Core Rot (RUL-2026-10-28-019).

**`quest:The Sealed Reliquary.description`**
```
The seal is spent when the run starts. Health and chakra carry through four echoes with no refills, and a lost fight ends the run.

Behind the Sealwright's archive, a black iron reliquary is chained to the wall. Inside are the echoes the Core could not hold: impressions too strong to fade and too damaged to rebuild, sealed away so the ship would stop trying. The Reliquary Seal opens it. What the reliquary remembers, it keeps.
```

**`quest:The Sealed Reliquary.successDescription`**: `Every frame in the reliquary stands empty.`

**`obj:The Sealed Reliquary/d_open.description`** (scene: quarantined_archive)
```html
The seal turns in the lock, and the chains fall slack. The reliquary does not open so much as unfold: a long room that could never fit inside an iron box, lined with sealed recall frames.<br><br>One by one, the seals on the frames begin to crack.
```
- `choice[0]`: `Step into the reliquary`

**`obj:The Sealed Reliquary/b1.description`**: `The first frame breaks. The Foundry Warden steps out of it, forge maul still glowing.`

**`obj:The Sealed Reliquary/d_after1.description`**
```html
The Warden cools into skyglass mid-swing. "The last pour," he says, and does not finish.<br><br>Where he fell, the floor still glows along his pour lines. The reliquary has not forgotten him.
```
- `choice[0]`: `On to the next frame`

**`obj:The Sealed Reliquary/b2.description`**: `The Sealwright steps out of the second frame and looks at the glowing floor. "I sealed him in here for a reason," he says. "Then I sealed myself in after him."`

**`obj:The Sealed Reliquary/d_after2.description`**
```html
The Sealwright kneels. "Thank you," he says, very quietly, and comes apart into seal script that does not quite fade.<br><br>Two echoes' worth of lines now cross the floor.
```
- `choice[0]`: `On to the next frame`

**`obj:The Sealed Reliquary/b3.description`**: `The third frame holds the Skyglass Sentinel, and the sound of surf in a room with no sea.`

**`obj:The Sealed Reliquary/d_after3.description`**
```html
The Sentinel crumbles to sand, but the tide it carried keeps coming, in the lines on the floor.<br><br>One frame is left. Something inside it is drumming its fingers.
```
- `choice[0]`: `Open the last frame`

**`obj:The Sealed Reliquary/b4.description`**: `The last frame bursts outward. The First Blade looks at the ruin on the floor and grins. "Finally. Something new."`

**`obj:The Sealed Reliquary/w_done.description`** (win; follows `b4`)
```html
"That was new," the First Blade says, and lies back on the floor to savour it.<br><br>You step out, and the chains draw tight behind you. Inside, the frames stand empty, for now.
```

**`obj:The Sealed Reliquary/f_lost.description`** (pays 1 Core Rot)
```html
The reliquary closes around you. You wake outside the iron box with the seal spent, and dark rot drying on your sleeve.
```

### 2.4 The Fall (The Last Heading)

Fights: burning deck (Deck Warden + Seal Charge); gun deck, at the powder magazine (Arsenal Keeper + Deck Warden); the
break (Core Horror); press-on: the Captain at the helm (kept, RUL-2026-10-30-060 item 6). The Arsenal Keeper is the only
fire source: his ember bands in the powder-magazine fight. The "Burning Deck" hazard is removed (RUL-2026-10-29-057
item 5, RUL-2026-10-30-060 item 7; Boss Fights §8). A failed run pays 1 Core Rot.

**`quest:The Fall.description`**
```
The heading is spent when the run starts. Health and chakra carry from fight to fight with no refills, and a lost fight ends the run.
After the break, leave with what you hold or climb to the helm; lose there and you keep only what you held.

The Wayfinder's last heading is not a route through the ship. It is the night the ship came down, as the Core still replays it: fire on every deck, the hull breaking, and the Core cracking open at the heart of it all. Follow the heading, and you are aboard for the fall.
```

**`quest:The Fall.successDescription`**: `You were aboard for the fall, and walked away from it.`

**`obj:The Fall/d_aboard.description`** (scene: deck_b)
```html
The heading drops you onto the open deck at night. The sky is wrong: too low, too fast, the coast rushing up out of the dark. Somewhere below, a powder store has caught, and the fire is walking up through the planks.<br><br>A Deck Warden is still counting buckets.
```
- `choice[0]`: `Get below before it spreads`

**`obj:The Fall/b1.description`**: `The Deck Warden turns from his buckets. Behind him, the planks begin to glow.`

**`obj:The Fall/d_gundeck.description`** (scene: lower_hull)
```html
The Warden goes down in the smoke, still counting.<br><br>The gun deck is full of it. At the powder magazine the Arsenal Keeper stands in the fire with his ledger open, logging every keg as it goes up. "Powder. Spent," he writes. "Spent. Spent." The fire is coming from him.
```
- `choice[0]`: `Stop the Arsenal Keeper`

**`obj:The Fall/b2.description`**: `The Arsenal Keeper does not look up from his ledger. The fire around him does not go out.`

**`obj:The Fall/d_break.description`** (scene: hold)
```html
The Keeper falls across his ledger. The last line reads: <i>Ship. Spent.</i><br><br>Below you the keel splits with a sound like a bell, and through the break you can see the Core, cracking open.
```
- `choice[0]`: `Go down to the Core`

**`obj:The Fall/b3.description`**: `The Core cracks open, and the Core Horror pulls itself out of the break.`

**`obj:The Fall/d_landing.description`** (press-on choice)
```html
The Core Horror sags into the burning water and goes still. For one moment, the fall stops.<br><br>Above you, through the smoke, the helm is still lit. The Captain is at the wheel, holding the heading straight into the shore, as he did that night. He has not let go yet.<br><br><b>Get off now and keep everything you hold. Climb to the helm and win, and the haul grows. Lose and you keep only what you hold now.</b>
```
- `choice[0]`: `Get off the ship`
- `choice[1]`: `Climb to the helm`

**`obj:The Fall/b_press.description`**: `The Captain does not turn from the helm. "I held her steady to the last," he says. "I will hold her now."`

**`obj:The Fall/w_leave.description`**
```html
You run the gangway as the hull breaks behind you. When you look back, the ship is a wreck on the sand again, cold and still, and the fire was never there.
```

**`obj:The Fall/w_press.description`**
```html
The Captain lets go of the wheel for the first time. "Then it is done," he says, as the deck tips. "It was done a long time ago." When the smoke clears you are on the sand, and the wreck is only a wreck again.
```

**`obj:The Fall/f_lost.description`** (pays 1 Core Rot)
```html
The fire takes the deck out from under you. You wake on the sand below the wreck with the heading spent and the taste of rot in your mouth.
```

### 2.5 The Rotted Reliquary (tainted Reliquary Seal)

Entry at 70% pools (first fight only); `elementalseal` for the first 2 rounds of every fight; pairs: Foundry Warden +
Sealwright, then Skyglass Sentinel + First Blade (+ Lingering Echo); press-on: Replicant Zero (RUL-2026-10-28-013).
Pick 2.

**`quest:The Rotted Reliquary.description`**
```
The seal is spent when the run starts, and you enter already worn: 70% health and chakra. They carry from fight to fight with no refills, and a lost fight ends the run.
After the last pair, leave with what you hold or open the door the rot has added; lose there and you keep only what you held.

This seal has soaked in the Core's rot, and the reliquary it opens is the one the rot remembers. The same frames, the same echoes. They come out two at a time now, and the air in there clogs the seal channels.
```

**`quest:The Rotted Reliquary.successDescription`**: `You walked out of the reliquary the rot remembers. Choose two.`

**`obj:The Rotted Reliquary/d_open.description`** (scene: quarantined_archive)
```html
The seal goes into the lock soft and wet. The chains do not fall; they rot through.<br><br>Inside, the frames weep black water, and the air is thick enough to taste. You feel your seal channels clog before you take a step.
```
- `choice[0]`: `Step into the rot`

**`obj:The Rotted Reliquary/b1.description`**: `Two frames split at once. The Foundry Warden and the Sealwright step out together, and neither looks quite like himself.`

**`obj:The Rotted Reliquary/d_pair2.description`**
```html
They fall together. The Sealwright's last words come out in the Warden's voice: "The last pour is not finished." The rot has mixed them up.
```
- `choice[0]`: `On to the last frames`

**`obj:The Rotted Reliquary/b2.description`**: `The Sentinel and the First Blade come out of one frame. The First Blade is not grinning. Nothing in here is new.`

**`obj:The Rotted Reliquary/d_landing.description`** (press-on choice)
```html
The First Blade falls without a word, and that is the wrongest thing in the room.<br><br>Past the last frame stands a door the reliquary never had: a sliding door, a plaque that reads REPLICANT ZERO, and violet light underneath. The rot has remembered him too.<br><br><b>Leave now and keep everything you hold. Open the door and win, and the haul grows. Lose and you keep only what you hold now.</b>
```
- `choice[0]`: `Leave the rot behind`
- `choice[1]`: `Open the sliding door`

**`obj:The Rotted Reliquary/b_press.description`**: `Replicant Zero turns his left hand in the violet light. "They kept trying to copy me," he says. "The rot does it better."`

**`obj:The Rotted Reliquary/w_leave.description`**
```html
You step out of the reliquary and the rot does not follow. The seal in the lock has crumbled to nothing.
```

**`obj:The Rotted Reliquary/w_press.description`**
```html
"The first to return," Replicant Zero says, as the rot takes him back. "Not the last." The sliding door closes on an empty room, and you take everything the reliquary held.
```

**`obj:The Rotted Reliquary/f_lost.description`**
```html
The rot closes over you. You wake outside with the seal gone and black water drying on your hands.
```

### 2.6 The Burning Heading (tainted Last Heading)

Runs backwards: entry at 70% pools at the break (Core Horror, embers); `afterburn` at the start of every fight; the
Captain joins as an ally (`allyAIs`) after the Core Horror; gun deck (Arsenal Keeper + Deck Warden, embers); the
gangway duel (Wayfinder). No press-on room (cut, RUL-2026-10-30-060 item 6). Pick 2.

**`quest:The Burning Heading.description`**
```
The heading is spent when the run starts, and you start in the worst of it: 70% health and chakra, carried from fight to fight with no refills. A lost fight ends the run.

Steeped in rot, the last heading runs the wrong way. It starts at the end: the Core breaking open, the ship already in pieces, fire in every breath. Fight your way out through the decks, the way no one did that night. You will not be alone for all of it.
```

**`quest:The Burning Heading.successDescription`**: `Someone walked off the ship this time. Choose two.`

**`obj:The Burning Heading/d_break.description`** (scene: hold)
```html
You open your eyes in the break. The keel has split, the Core is a burning hole in the world, and you are already hurt. The fire clings to you and will not go out.
```
- `choice[0]`: `Get up and fight`

**`obj:The Burning Heading/b1.description`**: `The Core Horror rises out of the break, burning, and you are already in its reach.`

**`obj:The Burning Heading/d_captain.description`** (scene: lower_hull)
```html
The Core Horror sinks into the fire.<br><br>Boots ring on the stair above. The Captain comes down through the smoke with his blade drawn and looks at you for a long moment. "Not this time," he says. "This time someone walks off." He takes your side.
```
- `choice[0]`: `Climb to the gun deck`

**`obj:The Burning Heading/b2.description`**: `The Arsenal Keeper and a Deck Warden bar the burning gun deck. The Captain steps in beside you.`

**`obj:The Burning Heading/d_gangway.description`** (scene: deck_b)
```html
The Keeper falls across his ledger. The Captain closes it for him. "He kept the stores for decades," he says. "Someone should have let him stop."<br><br>Ahead, the gangway, and the shore so close you can smell it.
```
- `choice[0]`: `Make for the gangway`

**`obj:The Burning Heading/b3.description`**: `The Wayfinder blocks the gangway, charts in hand. "This is not the heading," he says. "There is no heading off this ship."`

**`obj:The Burning Heading/w_done.description`** (win; follows `b3`)
```html
The Wayfinder looks at the shore. "Still no home port," he says, and lets his charts go into the wind.<br><br>You walk off the ship with the Captain beside you. At the foot of the gangway he stops. "I cannot come further," he says. "Go on." When you look back, he is gone, and the wreck is cold.
```

**`obj:The Burning Heading/f_lost.description`**
```html
The fire wins. You wake on the sand below the wreck with smoke in your lungs and rot on your hands.
```

### 2.7 Steeping: two special quests, started by using an Epic chart

RUL-2026-10-29-055: using the chart consumes it and starts its quest; the quest takes 3 Core Rot; the opening dialog is
"Steep" / "Take it back"; a loss returns the chart and spends the Rot. The fight is the steeping Core Horror (no Rot
drop). Text is identical for both quests except the names in angle brackets:

| | Reliquary Seal quest | Last Heading quest |
|---|---|---|
| `<quest>` | Steep the Reliquary Seal | Steep the Last Heading |
| `<chart>` | the Reliquary Seal | the Last Heading |
| `<tainted>` | the Rotted Reliquary Seal | the Rotted Heading (name: open question 2) |
| `<run>` | The Rotted Reliquary | The Burning Heading |

**`quest:<quest>.description`**
```
Steeping costs <chart> and 3 Core Rot. Win the fight and the rot gives you <tainted>, which opens <run>. Lose and the rot spits <chart> back out; the Core Rot is spent.
If you carry fewer than 3 Core Rot, choose Take it back: <chart> returns and nothing is spent.

You lower <chart> into the Core's rot. It drinks.
```

**`quest:<quest>.successDescription`**: `The rot took <chart>, and gave back <tainted>.`

**`obj:<quest>/d_steep.description`**
```html
You lower <chart> into a pool of the Core's rot. Black water climbs it at once, and something under the surface turns toward it, the way a sleeper turns toward a sound.<br><br><b>Steeping takes 3 Core Rot.</b> Without them, take it back now: <chart> comes back and nothing is spent.
```
- `choice[0]`: `Steep`
- `choice[1]`: `Take it back`

**`obj:<quest>/b_horror.description`**: `The rot stands up out of the pool and becomes the Core Horror.`

**`obj:<quest>/w_taken.description`** (win; reward the tainted chart)
```html
The Core Horror sinks back into the pool. When you draw <chart> out, it is dark, soft and heavy with rot: <tainted>.
```

**`obj:<quest>/f_spat.description`** (loss step, `failObjectiveId`; returns the chart)
```html
The rot spits <chart> back onto the planks beside you, untouched. The Core Rot you poured in is gone.
```

**`obj:<quest>/w_back.description`** (Take it back; refunds the chart and any Rot paid)
```html
You draw <chart> out of the rot before it takes hold. Nothing is spent.
```

### 2.8 Stakes headers for the existing hunts (prepend to the live descriptions)

The live descriptions keep their story; RUL-2026-10-28-028 item 8 asks for the two stakes lines first. The Archive's
press-on room is cut (RUL-2026-10-30-060 item 6); the Watch's is kept and its text is in §2.8a below. The second line
names each run's own choice.

- **`quest:The Buried Cache.description`** (prepend):
  `The chart is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run.`
- **`quest:The Drowned Foundry.description`** (prepend):
  `The chart is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run.`
  `There is no turning back: the only way out is through the crucible.`
- **`quest:The Quarantined Archive.description`** (prepend):
  `The chart is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run.`
  `A wrong answer at a seal costs you an extra fight and a smaller haul.`
- **`quest:The Captain's Watch.description`** (prepend):
  `The chart is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run.`
  `Every term you accept makes a fight harder and the haul bigger.`

### 2.8a The Captain's Watch press-on room (new; RUL-2026-10-30-062 item 2)

Fight: the dawn watch, the Wayfinder + Deck Warden (harness probe, 87% won from about 22% HP). It follows the Captain.
Each `d_gallery_IV / _V / _VI` gains the press-on choice; one `b_press` per step routes to `w_press_IV / _V / _VI`, and
a lost `b_press` routes to that step's `w_*` (the press-on `failDescription`, §2). No word "relieve" (bible, Voice).

**`obj:The Captain's Watch/d_gallery_*.description`** (append after the live text)
```html
<br><br>Below, a lantern moves along the deck: the Deck Warden, with the Wayfinder beside him and a chart under his arm. "Dawn watch," the Captain says. "They will want to see who held mine."<br><br><b>Claim the watch's stores now and keep everything you hold. Stand the dawn watch and win, and it adds to the haul. Lose it and you keep only what you hold now.</b>
```
- `choice[0]`: `Claim the watch's stores` (live, unchanged)
- `choice[1]`: `Stand the dawn watch`

**`obj:The Captain's Watch/b_press_*.description`**: `The Deck Warden plants himself at the head of the stairs. The Wayfinder unrolls his chart, and the deck shifts to match it.`

**`obj:The Captain's Watch/w_press_*.description`**
```html
The Deck Warden sits down hard against the rail. The Wayfinder rolls up his chart and, for once, does not correct it. "The watch is yours," the Captain says from the gallery, and the words sound new in his mouth.
```

### 2.9 Crownhold (exists; stakes header only)

**`quest:Crownhold.description`** (prepend; the live text already says the Lantern is spent and not refunded):
```
The Lantern is spent when the expedition starts. Health carries from fight to fight, and a lost fight ends the expedition.
The shrines offer shortcuts, rites and riddles; every choice changes how you meet the Crowned Captain.
```

---

## 3. The Haul

Six generated quests (RUL-2026-10-29-038, -044 … -046, -052, -053, -056). Open to every player: no rank text
anywhere (RUL-2026-10-29-052). No steeping (RUL-2026-10-29-056). Graph per `haul_spec.json` (b973ff28): choice nodes
keyed by step (1-5), alertness band (0 / 1-2 / 3+) and a pending cut-through hazard; battles per choice; endings by
haul rung (0-9) plus `fail`.

**How a choice node's text is composed** (generator):
1. the page's **step line** for that step (§3.3 … §3.7);
2. plus the page's **alertness line** when alertness is 1-2 or 3+;
3. plus the profession's **pending line** when a cut-through hazard is waiting;
4. then the options: the step's **crate tag**, **locker tag** (only on the page's locker steps), **cut tag** (only on
   its cut steps) and the fixed leave option.

### 3.1 Shared Haul text

- **Leave option** (exists in the harness, kept): `Take what you have and go`
- **Pending line, hunters:** `Your leg still burns where the last snare caught you.`
- **Pending line, gatherers:** `Skyglass dust from the cut is still in your seal channels.`
- **`fail.description`, hunters:** `You go down among the racks. When you wake, the page is ash and the hold is sealed again, every locker logged as full.`
- **`fail.description`, gatherers:** `You go down in the growth. When you wake, the manifest is ash and the crystal has closed over the stores again.`
- Battle `failDescription` / `drawDescription` / `fleeDescription`: the shared chart-run lines (§2).

**Ending text by rung** (`win_r<n>.description`). The rung's chests come from the ladder in `haul_spec.json`; the text
does not count them, because locker bonus chests vary.

| Rungs | Hunters | Gatherers |
|---|---|---|
| 0-1 | `You climb out with one chest under your arm. The Arsenal Keeper's ledger will show it gone, and he will check it every day for the rest of time.` | `You climb out with one crate on your shoulder. The manifest marks it drawn, then marks it again, as if to be sure.` |
| 2-4 | `You haul a fair take out of the stores. Behind you, the Keeper's ledger rewrites itself around the empty racks.` | `You haul a fair take out of the stores. Behind you, the skyglass is already growing into the gaps.` |
| 5-7 | `You come out loaded down with the hunters' best. Somewhere below, a ledger line is crossed out for the first time in decades.` | `You come out loaded down with the quartermaster's best. The manifest's last line reads, in a hand like a sigh: Drawn.` |
| 8-9 | `You empty the sealed racks of everything the hunters ever took. Every due date in the ledger is finally, honestly, crossed out.` | `You carry out the quartermaster's reserve itself. For the first time since it was sealed, the store-room is empty, and the growth has nothing left to hold.` |

**`quest:<page>.successDescription`** (all six): `You took your haul out of the ship's stores.`

### 3.2 Page items (`item:<chart>.description`)

All six share the rules block; only the story line and the run name change. Rarity Legendary, tradeable.

**Rules block** (after the story line; `<page>` is the run name, `<chests>` is Hunter's or Gatherer's):
```html
<br><br>Bring it to the Battle Arena to run <b><page></b>. The page is spent when the run starts.<br>Up to 5 steps. At each one, take a <b>crate</b> (a chest and a crew fight), a sealed <b>locker</b> (a better chest, a chance at a bonus chest, a harder fight and a hazard on you), or <b>cut through</b> where the way allows (no fight now, but the next fight opens with a hazard). Or leave with your haul.<br>Every locker you open puts the stores on alert for the rest of the run.<br>Health and chakra carry between fights, with no refills. Lose any fight and the run ends with nothing.<br>Pays in <chests> Chests.
```

| Item name | Story line (`<i>…</i>`) |
|---|---|
| Ledger Page: The Trophy Hold | `<i>A page torn from the Arsenal Keeper's ledger. Hides, horn and the hunters' trophies, sealed below the gun deck. Every due date is crossed out and written again.</i>` |
| Ledger Page: The Bone Store | `<i>A page from the Keeper's ledger for the bone store: horn, tusk and antler, the best of it sealed nearest the door.</i>` |
| Ledger Page: The Snare Room | `<i>The trapper's page of the ledger, stained with old bait. Every snare he ever set is listed, and none is marked as taken down.</i>` |
| Stores Manifest: The Overgrown Stores | `<i>The quartermaster's manifest for the lower stores. Ore, root and bloom, cut from the hull and sealed. Skyglass has grown through every line since.</i>` |
| Stores Manifest: The Ore Vault | `<i>The manifest for the ore vault, weighed twice and signed three times. The ship's metal was always the best guarded thing below decks.</i>` |
| Stores Manifest: The Bloom Cellar | `<i>The manifest for the drying cellar, its ink faded to the colour of old petals. The last line is a warning about the dust.</i>` |

(The two approved stories in `SKYGLASS_THE_HAUL.md` are kept, except the Trophy Hold's "Draw on relief. Relief is
crossed out", which is reworded to keep "relieved" to the refrain; open question 3. The Haul doc's "S-rank hunting
required" rule line is dropped by RUL-2026-10-29-052.)

### 3.3 The Trophy Hold (hunters; the classic balance)

Lockers at steps 1-5; cut-throughs at 3-4. Guards: the hunting party, the Trophy Warden, the Arsenal Keeper at
alertness 3+.

**`quest:The Trophy Hold.description`**
```
The page is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run with nothing. Leave after any step and take exactly what you have won.

Below the gun deck runs a long, cold hold, racked with sealed lockers. The ship's hunters stored everything they took from the high air and the coastlines here, and the Arsenal Keeper logged every piece. None of it was ever drawn. The old hunting party still walks the racks, and the Trophy Warden still guards the lockers.
```

| Step | Step line | Crate tag | Locker tag | Cut tag |
|---|---|---|---|---|
| 1 | `The ladder drops you into the Trophy Hold. Racks of lockers run off into the cold, each tagged in the Arsenal Keeper's hand, and mounted heads watch from the bulkheads. Down the racks, boots: the hunting party is on its rounds.` | `Crate: "Pelts, cured, twelve bales. Logged."` | `Locker: "Trophy, mounted. First hunter's seal."` | — |
| 2 | `Deeper in, the racks close overhead. Frost has crept over the tags, and lanterns move between the rows.` | `Crate: "Horn, sawn. Second hunter's seal."` | `Locker: "Antler, whole. Under the Warden's mark."` | — |
| 3 | `The hold narrows at the keel beam. Through a gap in the racks, a shorter way on runs past a line of old snares.` | `Crate: "Sinew, dried. Count checked. Count checked."` | `Locker: "Pelt of the great cat. Sealed, sealed again."` | `Cut through: the gap past the old snares` |
| 4 | `Here the lockers are bigger, their seals heavier, their tags older. The Trophy Warden's post is close.` | `Crate: "Hides, salted. Draw on landing."` | `Locker: "The hunt-master's own take."` | `Cut through: under the keel beam, quickly` |
| 5 | `The last rack. Beyond it stand the Keeper's own lockers in black wax, their due dates rewritten until the tags are more ink than paper.` | `Crate: "Feathers, sky-caught. Not to be opened on deck."` | `Locker: "Black wax. The best of decades."` | — |

- **Alertness 1-2:** `Lanterns are moving in the racks now. The hold knows someone is drawing.`
- **Alertness 3+:** `Every lantern in the hold is lit. Above you, the Arsenal Keeper closes his ledger and reaches for the ladder.`
- **Crate battle:** `The hunting party turns from its rounds. "Stores are not drawn," one says.`
- **Locker battle:** `The Trophy Warden steps between you and the locker. Above his cloth mask, his eyes do not blink.`
- **Locker battle, alertness 3+:** `The Trophy Warden steps between you and the locker, and the Arsenal Keeper comes down the ladder to see who is drawing from his stores.`

### 3.4 The Bone Store (hunters; lockers early, a cheap but dangerous start)

Lockers at steps 1-3 only; cut-throughs at 3-4.

**`quest:The Bone Store.description`**
```
The page is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run with nothing. Leave after any step and take exactly what you have won.

The bone store is where the hunters kept what lasts: horn, tusk, antler and bone, stacked to the deckhead. They sealed the best of it first, right by the door, in red wax. The deeper racks hold only what was left over, and the hunting party guards both the same.
```

| Step | Step line | Crate tag | Locker tag | Cut tag |
|---|---|---|---|---|
| 1 | `The door opens straight onto the finest lockers, sealed in red wax. Bone dust hangs in the lamplight, and the hunting party has heard the door.` | `Crate: "Bone, split. Glue stock. Logged."` | `Locker: "Tusk, whole. Red wax."` | — |
| 2 | `The red-waxed lockers go on a little further. Past them, the racks turn plain.` | `Crate: "Teeth, sorted by size. Logged twice."` | `Locker: "Antler crown, nine points. Red wax."` | — |
| 3 | `The last sealed locker stands at the turn of the racks. After this, only crates.` | `Crate: "Horn shavings, for the fletchers."` | `Locker: "The great skull. Red wax. Not alone."` | `Cut through: over the stacked bone` |
| 4 | `Plain racks now, bone stacked like firewood. The tags here are short and tired.` | `Crate: "Knucklebones. Someone's dice. Logged anyway."` | — | `Cut through: down the bone chute` |
| 5 | `The back wall. Leftovers, logged with the same care as the best.` | `Crate: "Remainder. Count attempted."` | — | — |

- **Alertness 1-2:** `Bone dust is sifting down from every rack. They know you are here.`
- **Alertness 3+:** `The ladder creaks. The Arsenal Keeper is coming down to count what is missing.`
- **Crate battle:** `The hunting party comes around the racks with bone dust on their boots.`
- **Locker battle:** `The Trophy Warden is already standing at the red-waxed locker, as if he never left it.`
- **Locker battle, alertness 3+:** `The Trophy Warden stands at the locker, and the Arsenal Keeper is right behind him, ledger open.`

### 3.5 The Snare Room (hunters; heavy hazards, safe cut-throughs)

Lockers at steps 1-5; cut-throughs at 2-4.

**`quest:The Snare Room.description`**
```
The page is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run with nothing. Leave after any step and take exactly what you have won.

The trapper kept his snares here and never took them down. Lines cross the floor at ankle and waist, bait vials hang from the deckhead, and the lockers sit among the snares like bait themselves. The trapper chalked his own paths through it all, and the chalk is still there.
```

| Step | Step line | Crate tag | Locker tag | Cut tag |
|---|---|---|---|---|
| 1 | `Lines everywhere, still taut after decades. Chalk paths wind between them, and the lockers sit where the lines are thickest.` | `Crate: "Line, waxed, forty coils. Logged."` | `Locker: "Trapper's kit. Mind the lid."` | — |
| 2 | `A chalk path runs off to the left, clear of the lines. The lockers lie the other way, in the thick of the snares.` | `Crate: "Hooks, barbed. Hold by the shank."` | `Locker: "Live catch. Sealed. Contents quiet."` | `Cut through: follow the chalk path` |
| 3 | `Bait vials hang overhead, the glass gone cloudy. One of them drips.` | `Crate: "Bait, dried. Do not eat. Do not eat."` | `Locker: "Venom stores. Trapper's seal."` | `Cut through: duck under the lines` |
| 4 | `The snares get cleverer the deeper you go. Whoever set these was proud of them.` | `Crate: "Snare wire. Trapper's seal."` | `Locker: "Best catch of the high air."` | `Cut through: the trapper's crawlway` |
| 5 | `The end of the room: one great locker in a nest of lines, and the hunting party waiting just outside them.` | `Crate: "Spare traps. Set. Logged as set."` | `Locker: "Trapper's own. Do not draw. Trapped."` | — |

- **Alertness 1-2:** `Somewhere a line has been cut. The hunting party is resetting snares behind you.`
- **Alertness 3+:** `Every snare in the room is set now, and the Arsenal Keeper's lantern is coming down the ladder.`
- **Crate battle:** `The hunting party steps between the lines toward you. They know where every snare is.`
- **Locker battle:** `The Trophy Warden waits among the snares, perfectly still, every line drawn tight around him.`
- **Locker battle, alertness 3+:** `The Trophy Warden waits among the snares, and the Arsenal Keeper stands at the room's edge, logging every line you trip.`

### 3.6 The Overgrown Stores (gatherers; the classic balance)

Lockers at steps 1-5; cut-throughs at 3-4. Guards: crew in the growth, Seal Charges and Core Canisters, the Stores Ward,
the Sealwright's echo at alertness 3+.

**`quest:The Overgrown Stores.description`**
```
The manifest is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run with nothing. Leave after any step and take exactly what you have won.

The lower stores were sealed full and never opened. Since then the Core has grown skyglass through them like roots through a cellar: pale columns from floor to deckhead, crates set into the crystal like stones in a ring. The Stores Ward still keeps the racks.
```

| Step | Step line | Crate tag | Locker tag | Cut tag |
|---|---|---|---|---|
| 1 | `The hatch opens onto pale light. Skyglass columns rise through the store-room, crates grown into them. A Deck Warden walks the rows with a count he will never finish.` | `Crate: "Root, dried, twelve crates. Growth noted."` | `Locker: "Ore, refined. Quartermaster's seal."` | — |
| 2 | `The growth thickens. Seal charges sit in the crystal where the quartermaster left them, still primed.` | `Crate: "Ore, broken. Sealed. Growth noted."` | `Locker: "Rare bloom, sealed in glass."` | — |
| 3 | `A crack in the growth runs straight through the next room, narrow and sharp-edged.` | `Crate: "Bloom, pressed. Faded. Logged as fresh."` | `Locker: "Heartwood, cut from the keel."` | `Cut through: the crack in the growth` |
| 4 | `The columns here are old and cloudy, and the crates inside them hold the best the ship ever cut.` | `Crate: "Ore, refined, twelve crates. Sealed. Growth noted."` | `Locker: "Crystal-grown ore. Do not chip."` | `Cut through: break the thin columns` |
| 5 | `The last room: the Stores Ward's post, and the quartermaster's sealed racks behind it.` | `Crate: "Seed stock. Germination unlikely. Logged."` | `Locker: "Quartermaster's reserve. Do not draw."` | — |

- **Alertness 1-2:** `The growth is ringing faintly, like struck glass. The stores know.`
- **Alertness 3+:** `Seal script crawls over the crystal. The Sealwright's echo is closing the stores.`
- **Crate battle:** `The crew in the growth turn toward you, skyglass dust rising where they step.`
- **Locker battle:** `The Stores Ward unseals the rack and steps into its place.`
- **Locker battle, alertness 3+:** `The Stores Ward steps into the rack's place, and the Sealwright's echo seals the room behind you.`

### 3.7 The Ore Vault (gatherers; dense guards, rich lockers) and The Bloom Cellar (gatherers; heavy dust, a steep curve)

Both: lockers at steps 1-5; cut-throughs at 3-4.

**`quest:The Ore Vault.description`**
```
The manifest is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run with nothing. Leave after any step and take exactly what you have won.

The ore vault held the ship's metal behind doors a hand thick: ingots, raw ore and the rarer stones. It was the best-guarded room below decks, and it still is. Every locker here is worth opening, and every one is watched.
```

| Step | Step line | Crate tag | Locker tag | Cut tag |
|---|---|---|---|---|
| 1 | `Iron doors stand open on a vault cut into the keel. Ore glints in the lamplight, and more crew than you would like stand between the racks.` | `Crate: "Iron, pig, forty bars. Logged."` | `Locker: "Ingots, stamped. Strongroom seal."` | — |
| 2 | `The vault narrows into strongrooms, each with its own guard and its own seal.` | `Crate: "Copper, drawn. Weighed twice."` | `Locker: "Silver, refined. Two keys required."` | — |
| 3 | `A collapsed strongroom leaves a gap in the wall, just wide enough.` | `Crate: "Silver ore, raw. Growth noted."` | `Locker: "Gold, cast. Not to be left alone."` | `Cut through: the collapsed strongroom` |
| 4 | `The deep vault. Skyglass has grown into the ore itself, and the guards stand two to a door.` | `Crate: "Gold dust, sealed jar. Weighed three times."` | `Locker: "Star-iron. Quartermaster only."` | `Cut through: down the ore chute` |
| 5 | `The quartermaster's strongroom. The Stores Ward stands at its door, and the lock is the size of a man's chest.` | `Crate: "Ore of the high passes. Weight disputed."` | `Locker: "The vault's heart. Crownhold's seal."` | — |

- **Alertness 1-2:** `Doors are closing deeper in the vault, one after another.`
- **Alertness 3+:** `Every strongroom is sealed, and the Sealwright's echo is walking the vault.`
- **Crate battle:** `Two of the vault's crew step out from the racks, and something in the ore begins to hum.`
- **Locker battle:** `The Stores Ward unlocks the strongroom from the inside and steps out to meet you.`
- **Locker battle, alertness 3+:** `The Stores Ward steps out of the strongroom, and the Sealwright's echo seals the door behind you.`

**`quest:The Bloom Cellar.description`**
```
The manifest is spent when the run starts. Health and chakra carry from fight to fight, and a lost fight ends the run with nothing. Leave after any step and take exactly what you have won.

The gatherers dried their flowers and roots in this cellar. Then the skyglass got in, and the blooms grew into it, and now the air is thick with crystal pollen that gets into the lungs and the seal channels alike. The first racks hold common roots. The inner cellar holds the rarest blooms the ship ever carried.
```

| Step | Step line | Crate tag | Locker tag | Cut tag |
|---|---|---|---|---|
| 1 | `The cellar door lets out a breath of pale dust that glitters in the lamplight. The first racks hold common roots, dry as paper.` | `Crate: "Root, common. Dried. Logged."` | `Locker: "Root stock, sealed against dust."` | — |
| 2 | `Dust hangs in the air like mist. Your chakra feels heavy.` | `Crate: "Moss, packed. Growth noted."` | `Locker: "Medicinal bloom. Do not breathe."` | — |
| 3 | `Past the drying racks the crystal has cracked open, and the air beyond is thicker still.` | `Crate: "Petals, pressed. Colour lost. Logged."` | `Locker: "Crystal-grown flower, sealed in glass."` | `Cut through: the cracked crystal` |
| 4 | `Rare blooms now, grown into the skyglass and glowing faintly. Every breath tastes of glass.` | `Crate: "Bloom of the high air. Gloves."` | `Locker: "Rare bloom. Draw on landing."` | `Cut through: hold your breath and run` |
| 5 | `The inner cellar: the rarest bloom the ship ever carried, sealed in a crystal case, and the Stores Ward beside it.` | `Crate: "Night bloom. Keep dark. Kept."` | `Locker: "The last flower. Crownhold's seal."` | — |

- **Alertness 1-2:** `The dust is stirring by itself now.`
- **Alertness 3+:** `Seal script glows through the dust. The Sealwright's echo is sealing the cellar.`
- **Crate battle:** `Shapes move in the dust: the cellar's crew, glittering.`
- **Locker battle:** `The Stores Ward steps out of the dust beside the sealed case.`
- **Locker battle, alertness 3+:** `The Stores Ward steps out of the dust, and the Sealwright's echo seals the cellar door behind you.`

### 3.8 Hazard effect lines (`applyDebuffs[].description`)

The harness lines are kept, with one split: `decreasemaxpools` carries "Cold eyes / crystal in the lungs" for both
professions. Proposed:
- hunters: `A trophy's cold eyes: your maximum health is lowered`
- gatherers: `Crystal in the lungs: your maximum health is lowered`

---

## 4. Item descriptions (loot tables §0)

Story line first, in italics; then the rules in plain words. Rates are the loot-table weights (RUL-2026-10-28-030
format). Colours: grey `#9ca3af`, blue `#3b82f6`, purple `#a855f7`, gold `#f59e0b`. A fixed roll count is not
repeated (the card shows it).

### 4.1 Charts and the Lantern

**`item:Tide Chart.description`** (Common)
```html
<i>The Wayfinder's tide table, marked where the low tide opens the wreck's lower hull.</i><br><br>Bring it to the Battle Arena to run <b>The Low Tide Run</b>: three fights, scaled to you. The chart is spent when the run starts.<br>Health and chakra carry between fights, with no refills. A lost fight ends the run.
```

**`item:Watch Roster.description`** (Common)
```html
<i>The Deck Warden's duty roster, with a new name at the bottom in fresh ink: yours.</i><br><br>Bring it to the Battle Arena to run <b>The Night Watch</b>: three watches back to back, scaled to you. The roster is spent when the run starts.<br>Health and chakra carry between fights, with no refills. A lost fight ends the run.<br>After the last watch, leave with what you hold or stand the Second Watch for more. Lose it and you keep only what you held.
```

**`item:Chart of the Buried Cache.description`** (Rare, RUL-2026-10-29-058; live story kept)
```html
<i>A salt-stained chart from the Skyglass wreck, marking a field cache its crew buried on the shore before the ship vanished.</i><br><br>Bring it to the Battle Arena to run <b>The Buried Cache</b>, scaled to you. The chart is spent when the run starts.<br>Health and chakra carry between fights, with no refills. A lost fight ends the run.
```

**`item:Chart of the Drowned Foundry.description`** (live story kept)
```html
<i>A waterlogged chart of the wreck's keel and lower decks, where the drowned foundry lies.</i><br><br>Bring it to the Battle Arena to run <b>The Drowned Foundry</b>. The chart is spent when the run starts.<br>Health and chakra carry between fights, with no refills. A lost fight ends the run. There is no way out but through the crucible.
```

**`item:Chart of the Quarantined Archive.description`** (live story kept)
```html
<i>A chart of the wreck that shows a sealed chamber missing from every other plan.</i><br><br>Bring it to the Battle Arena to run <b>The Quarantined Archive</b>. The chart is spent when the run starts.<br>Health and chakra carry between fights, with no refills. A lost fight ends the run.<br>Three seals bar the way. A wrong answer brings the archive's guard and a smaller haul.
```

**`item:Chart of the Captain's Watch.description`** (live story kept)
```html
<i>The Captain's own chart of the wreck's command decks.</i><br><br>Bring it to the Battle Arena to run <b>The Captain's Watch</b>. The chart is spent when the run starts.<br>Health and chakra carry between fights, with no refills. A lost fight ends the run.<br>Before each fight the Oathkeeper offers a term. Every term you take and survive raises the haul.
```

**`item:Reliquary Seal.description`** (Epic)
```html
<i>The seal of the iron reliquary chained behind the Sealwright, where the echoes the Core could not hold were sealed away.</i><br><br><b>Two uses.</b><br><b>Run it:</b> bring it to the Battle Arena to run <b>The Sealed Reliquary</b>: four echoes back to back, and the reliquary remembers each one that falls. The seal is spent when the run starts. Health and chakra carry, with no refills. A lost fight ends the run and leaves you 1 Core Rot.<br><b>Steep it:</b> use it from your inventory to soak it in the Core's rot. It costs 3 Core Rot. Win the fight and it becomes the Rotted Reliquary Seal. Lose and the seal comes back, but the Rot is spent. Short of 3 Core Rot? Take it back, and nothing is spent.
```

**`item:The Last Heading.description`** (Epic)
```html
<i>The Wayfinder's final course: the night the ship came down, as the Core still replays it.</i><br><br><b>Two uses.</b><br><b>Run it:</b> bring it to the Battle Arena to run <b>The Fall</b>: the burning decks, then the Core as it breaks, while the fire spreads. The heading is spent when the run starts. Health and chakra carry, with no refills. A lost fight ends the run and leaves you 1 Core Rot. After the break, leave with what you hold or climb to the helm; lose there and you keep only what you held.<br><b>Steep it:</b> use it from your inventory to soak it in the Core's rot. It costs 3 Core Rot. Win the fight and it becomes the Rotted Heading. Lose and the heading comes back, but the Rot is spent. Short of 3 Core Rot? Take it back, and nothing is spent.
```

**`item:Rotted Reliquary Seal.description`** (Legendary)
```html
<i>The Reliquary Seal, soaked in the Core's rot. It opens the reliquary as the rot remembers it.</i><br><br>Bring it to the Battle Arena to run <b>The Rotted Reliquary</b>. The seal is spent when the run starts.<br><b>The twists:</b> you enter at 70% health and chakra; the echoes come out in pairs; the rot seals your elemental jutsu for the first 2 rounds of every fight.<br>Health and chakra carry between fights, with no refills. A lost fight ends the run.<br>After the last pair, leave with what you hold or open one more door; lose there and you keep only what you held.<br>The run's reward lets you <b>pick 2</b>.
```

**`item:The Rotted Heading.description`** (Legendary; name: open question 2)
```html
<i>The Last Heading, soaked in the Core's rot. It runs the night of the fall backwards.</i><br><br>Bring it to the Battle Arena to run <b>The Burning Heading</b>. The heading is spent when the run starts.<br><b>The twists:</b> it starts at the end, in the break, at 70% health and chakra; fire catches you at the start of every fight, so the damage you take burns again; you fight your way out through the decks, and you will not fight all of it alone.<br>Health and chakra carry between fights, with no refills. A lost fight ends the run.<br>The run's reward lets you <b>pick 2</b>.
```

**`item:Lastlight Lantern.description`** (live story kept)
```html
<i>Crownhold's final signal, caught in a skyglass lantern. It still burns with the last order the wreck's crew obey, and its light points home.</i><br><br>Bring it to the Battle Arena to follow the light to <b>Crownhold</b>, the mountain fortress at the end of the story. The Lantern is spent when the expedition starts.<br>Health carries between fights, and a lost fight ends the expedition.<br>Claim any reward choice still waiting from an earlier run before you set out.
```

The six Haul pages: §3.2.

### 4.2 Core Rot and the pet items

**`item:Core Rot.description`**
```html
<i>What the Core leaves behind when it rebuilds an impression badly: dark, wet timber and rope, and skyglass gone cloudy.</i><br><br>Used for <b>steeping</b>. Use an Epic chart (the Reliquary Seal or The Last Heading) from your inventory to soak it in the Core's rot. Steeping costs the chart and <b>3 Core Rot</b>, and you fight what the rot builds.<br><b>Win:</b> you get the tainted chart (the Rotted Reliquary Seal or the Rotted Heading).<br><b>Lose:</b> the chart comes back to you, and the 3 Core Rot are spent.<br>Short of 3 Core Rot? Take the chart back at the start, and nothing is spent.
```

**`item:The Little Horror's Jar.description`**
```html
<i>One of the Skyglass Project's first recalls was the ship's mascot, sealed in a jar. The Core tried to remember it. This is what came back.</i><br><br>Open the jar to bind the <b>Little Horror</b> to you as a pet. It answers to you, not to the crown.<br>The jar will not open while your pet collection is full. It stays in your inventory until you make room.
```

**`item:Galley Stores.description`**
```html
<i>The galley still stocks a larder for a crew that does not eat. A companion that does eat grows strong on it.</i><br><br>Gives <b>20,000 pet experience</b> to your active pet. The pet must be ready for battle and not away on a task. If no pet can take it, the experience is lost.
```

### 4.3 Tokens

**`item:Skyglass Token.description`**
```html
<i>A token pressed from clouded skyglass and stamped with the four-point star.</i><br><br>Use it to unlock <b>one Skyglass variant</b> of your choice: a new look and name for one of your crafted weapons, with the same stats. You must own the weapon. Each variant unlocks once per player, and the token is used up.<br>Skyglass variants exist for Aetherion, Thornsilver, Night's Testament, Stormrender, Oathbinder, Ink of the Void, The Unwritten, Gaea's Embrace, Warden's Bracers, Eclipsed Dawnblade, Zephyr's Whisper and Yuki's Frostbite.
```

**Boss variant tokens.** Item name: the variant's name alone, `<Variant>` (RUL-2026-10-29-057 item 1). Description template:
```html
<i><story line></i><br><br>Use it to unlock the <b><Variant></b> variant of <b><Base></b>: a new look and name, with the same stats. You must own <Base>. Each variant unlocks once per player, and the token is used up.
```

| Token item | `<Base>` | Story line |
|---|---|---|
| Captain's Command Fan | The Unwritten | `Taken from the Captain on his own deck. He gave every order with it, and every order was his master's.` |
| Rot-Bloom Reaper | Oathbinder | `Cut from what the Core Horror left behind when it finally lay still.` |
| Warden's Forge-Fists | Warden's Bracers | `The Foundry Warden never set down his work. Now someone else can carry it.` |
| Wayfinder's Heading | Stormrender | `The Wayfinder's last correction, still pointing at a port that is not there.` |
| The First Blade | Aetherion | `Something new, at last. He would have liked you.` |
| Sealwright's Seal | Whispering Dawnblade | `The Sealwright's own seal, from the hand that buried every report.` |
| Crownbreaker | Thornsilver | `For walking every deck of the war-ship, and breaking the crown that held them.` |

### 4.4 Caches

**`item:Skyglass Coffer.description`**
```html
<i>A seal-locked coffer from the Skyglass Project's stores, the only place its salvage is still kept.</i><br><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 69%</b></span> · Skyglass Filament ×2<br><span style="color:#3b82f6"><b>Rare 24%</b></span> · Skyglass Serum ×3<br><span style="color:#a855f7"><b>Epic 5%</b></span> · Fragment of the Skyglass Crown<br><span style="color:#f59e0b"><b>Legendary 2%</b></span> · Skyglass Katana
```

**`item:Sealed Treasury.description`**
```html
<i>The war-ship's payroll vault, still locked under the ship's seals. No one aboard was ever paid off.</i><br><br><b>Always:</b> 150,000 ryo<br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 45%</b></span> · Imperial Gold ×5<br><span style="color:#3b82f6"><b>Rare 35%</b></span> · Rare Jewels ×10<br><span style="color:#a855f7"><b>Epic 15%</b></span> · Imperial Gold ×15<br><span style="color:#f59e0b"><b>Legendary 5%</b></span> · Unobtanium ×5
```

**`item:Archive Chart Case.description`** (Legendary 7% an Epic chart, Forbidden 3% the Lantern; RUL-2026-10-29-058)
```html
<i>A sealed chart case from the Quarantined Archive, holding one chart of the wreck's shifting decks.</i><br><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 45%</b></span> · Chart of the Drowned Foundry<br><span style="color:#3b82f6"><b>Rare 25%</b></span> · Chart of the Quarantined Archive<br><span style="color:#a855f7"><b>Epic 20%</b></span> · Chart of the Captain's Watch<br><span style="color:#f59e0b"><b>Legendary 7%</b></span> · Reliquary Seal <i>or</i> The Last Heading<br><span style="color:#ef4444"><b>Forbidden 3%</b></span> · Lastlight Lantern
```

**`item:Medicine Inro.description`**
```html
<i>A lacquered medicine case from the ship's infirmary, still stocked for a crew that cannot fall ill.</i><br><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 70%</b></span> · Field Tonic ×10 <i>or</i> Chakra Pill ×10 <i>or</i> Stamina Pill ×10<br><span style="color:#3b82f6"><b>Rare 22%</b></span> · Small Health Pill ×10 <i>or</i> Dr. Kim's Miracle Potion ×10 <i>or</i> Panacea ×10<br><span style="color:#a855f7"><b>Epic 7%</b></span> · Chakra Pill II ×10 <i>or</i> Stamina Pill II ×10<br><span style="color:#f59e0b"><b>Legendary 1%</b></span> · Pill Pack ×5
```

**`item:Sage's Strongbox.description`** (the Forbidden tier colour: open question 8)
```html
<i>The Sealwright's strongbox of remedies meant for enemies, not allies.</i><br><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 65%</b></span> · Dr. Kim Disaster Potion ×20 <i>or</i> Chakra Disrupting Needles ×20<br><span style="color:#a855f7"><b>Epic 26%</b></span> · Infernum ×10 <i>or</i> Bashōsen ×10 <i>or</i> Dr. Kim's Poison Potion ×10<br><span style="color:#f59e0b"><b>Legendary 8%</b></span> · Solider Pill ×2 <i>or</i> Enemy Pill ×2 <i>or</i> Mona's Mermaid Song ×2<br><span style="color:#ef4444"><b>Forbidden 1%</b></span> · Forbidden Jutsu Scroll: Nexus <i>or</i> Rebirth
```

**`item:Elemental Tool Pouch.description`** (live story kept)
```html
<i>A buckled armory pouch: elemental kunai and the tools that go with them.</i><br><br><b>Always:</b> Elemental Kunai ×10<br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 70%</b></span> · Elemental Kunai ×10 <i>or</i> Venom Cask ×10<br><span style="color:#3b82f6"><b>Rare 25%</b></span> · Elemental Kunai ×20 <i>or</i> Elite Smoke Bomb ×10 <i>or</i> Paper Bombs ×10<br><span style="color:#a855f7"><b>Epic 5%</b></span> · Elemental Kunai ×30 <i>or</i> Senbon Needles ×10 <i>or</i> Saki ×10
```

**`item:Unmarked Cargo.description`** (live story kept)
```html
<i>Unmarked cargo hauled out of the Skyglass wreck. Something from the ship's stores is sealed inside.</i><br><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 40%</b></span> · Medicine Inro <i>or</i> Elemental Tool Pouch<br><span style="color:#3b82f6"><b>Rare 35%</b></span> · Sage's Strongbox <i>or</i> Galley Stores<br><span style="color:#a855f7"><b>Epic 18%</b></span> · Skyglass Coffer <i>or</i> Archive Chart Case<br><span style="color:#f59e0b"><b>Legendary 7%</b></span> · Sealed Treasury <i>or</i> Skyglass Token
```

**`item:Crown's Hoard.description`** (three effects on one item: a Coffer roll, a Treasury roll, a Skyglass Token)
```html
<i>What the crown kept for itself: Crownhold's own coffer and treasury, gathered beneath the throne.</i><br><br><b>Always:</b> 150,000 ryo · Skyglass Token<br><b>Coffer, 1 roll:</b><br><span style="color:#9ca3af"><b>Common 69%</b></span> · Skyglass Filament ×2<br><span style="color:#3b82f6"><b>Rare 24%</b></span> · Skyglass Serum ×3<br><span style="color:#a855f7"><b>Epic 5%</b></span> · Fragment of the Skyglass Crown<br><span style="color:#f59e0b"><b>Legendary 2%</b></span> · Skyglass Katana<br><b>Treasury, 3–6 rolls:</b><br><span style="color:#9ca3af"><b>Common 45%</b></span> · Imperial Gold ×5<br><span style="color:#3b82f6"><b>Rare 35%</b></span> · Rare Jewels ×10<br><span style="color:#a855f7"><b>Epic 15%</b></span> · Imperial Gold ×15<br><span style="color:#f59e0b"><b>Legendary 5%</b></span> · Unobtanium ×5
```

### 4.5 The eight profession chests

Weights from `state/skyglass_design/chests.json` (generator `push/skyglass_profession_chests.gen.py`): 3 rolls 60% /
4 rolls 30% / 6 rolls 10%, so every chest shows "3–6 rolls". These chests' tiers are named Common, Rare, Epic and Legendary (RUL-2026-10-29-058; formerly Staples, Recipe kit, Bulk and
Windfall/Heirloom), coloured grey, blue, purple and gold in that order. Options
are listed most frequent first, three at most, then "and more".

Each description is `<i><story></i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br>` followed by the four tier lines.

**`item:Common Hunter's Chest.description`**
```html
<i>A hunter's sea-chest from the ship's stores: the everyday take, cured and logged.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · Owlcat's Fur ×26 <i>or</i> Glimmer Dust ×26 <i>or</i> Moonlight Antlers ×26, and more<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · Owlcat's Fur ×12 + Rust Ferret Pelt ×12 <i>or</i> Glimmer Dust ×12 + Moonlight Antlers ×12 <i>or</i> Badger Shell ×12 + Glimmer Dust ×12 + Moonlight Antlers ×12 + Owlcat's Fur ×12, and more<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Owlcat's Fur ×78 <i>or</i> Glimmer Dust ×78 <i>or</i> Moonlight Antlers ×78<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Ashrend Wing ×12 <i>or</i> Brasel Spine ×12 <i>or</i> Glimmerchitin ×12, and more
```

**`item:Rare Hunter's Chest.description`**
```html
<i>A hunter's chest of the rarer game the ship took along the coastlines.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · Ashrend Wing ×27 <i>or</i> Brasel Spine ×27 <i>or</i> Glimmerchitin ×27, and more<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · Ashrend Wing ×12 + Brasel Spine ×12 <i>or</i> Ashrend Wing ×12 + Frostscale ×12 + Glimmerchitin ×12 <i>or</i> Brasel Spine ×12 + Voltleaf Plume ×12, and more<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Ashrend Wing ×81 <i>or</i> Brasel Spine ×81 <i>or</i> Glimmerchitin ×81<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Moonpetal Weave ×12 <i>or</i> Ofuda Moss ×12 <i>or</i> Urami Drop ×12, and more
```

**`item:Epic Hunter's Chest.description`**
```html
<i>A hunter's chest of strange catches from the high air, sealed under the Warden's mark.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · Moonpetal Weave ×25 <i>or</i> Ofuda Moss ×25 <i>or</i> Urami Drop ×25, and more<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · Moonpetal Weave ×10 + Yamidangan ×10 <i>or</i> Ofuda Moss ×10 + Yamidangan ×10 <i>or</i> Ofuda Moss ×10 + Tsukinari Bell ×10, and more<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Moonpetal Weave ×75 <i>or</i> Ofuda Moss ×75 <i>or</i> Urami Drop ×75<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Parchment Core ×25 <i>or</i> Cracked Auditory Core ×25 <i>or</i> Mask Core ×25, and more
```

**`item:Legendary Hunter's Chest.description`**
```html
<i>The hunt-master's own chest: the best of decades, sealed and never drawn.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 55%</b></span> · Parchment Core ×20 <i>or</i> Cracked Auditory Core ×20 <i>or</i> Mask Core ×20, and more<br><span style="color:#3b82f6"><b>Rare 25%</b></span> · Cracked Auditory Core ×10 + Mask Core ×10 <i>or</i> Mask Core ×10 + Parchment Core ×10 <i>or</i> Mask Core ×10 + Parchment Core ×10 + Shard of Willful Steel ×10, and more<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Parchment Core ×60 <i>or</i> Cracked Auditory Core ×60 <i>or</i> Mask Core ×60<br><span style="color:#f59e0b"><b>Legendary 8%</b></span> · Mask Core ×20 + Parchment Core ×20 + Shard of Willful Steel ×20 <i>or</i> Parchment Core ×20 + Shard of Willful Steel ×20 + Thread Core ×20
```

**`item:Common Gatherer's Chest.description`**
```html
<i>The quartermaster's crate of everyday ore and root, cut from the hull and logged.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · Murkshade ×34 <i>or</i> Sunroot ×34 <i>or</i> Copper Ore ×34, and more<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · Murkshade ×16 + Whistlegrass ×16 <i>or</i> Iron Ore ×16 + Murkshade ×16<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Murkshade ×100 <i>or</i> Sunroot ×100 <i>or</i> Copper Ore ×100<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Galecrest Sage ×16 <i>or</i> Gold Ore ×16 <i>or</i> Silver Ore ×16, and more
```

**`item:Rare Gatherer's Chest.description`**
```html
<i>A gatherer's crate of the rarer ore and bloom, sealed against the damp.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · Galecrest Sage ×27 <i>or</i> Gold Ore ×27 <i>or</i> Silver Ore ×27, and more<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · Gold Ore ×12 + Shiverthorn ×12 + Starfire Petal ×12 + Wraithbloom ×12 <i>or</i> Galecrest Sage ×12 + Solar Petal ×12 <i>or</i> Gold Ore ×12 + Silver Ore ×12 + Starfire Petal ×12, and more<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Galecrest Sage ×81 <i>or</i> Gold Ore ×81 <i>or</i> Silver Ore ×81<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Rainbow Cabochon ×12 <i>or</i> Adamantine Ore ×12 <i>or</i> Celestial Thristle ×12, and more
```

**`item:Epic Gatherer's Chest.description`**
```html
<i>A gatherer's crate of crystal-grown ore and blooms the skyglass got into.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · Rainbow Cabochon ×25 <i>or</i> Adamantine Ore ×25 <i>or</i> Celestial Thristle ×25, and more<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · Celestial Thristle ×10 + Shadeleaf ×10 <i>or</i> Adamantine Ore ×10 + Icewarden Root ×10 + Rainbow Cabochon ×10 <i>or</i> Celestial Thristle ×10 + Susanoo's Tear ×10, and more<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Rainbow Cabochon ×75 <i>or</i> Adamantine Ore ×75 <i>or</i> Celestial Thristle ×75<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Mithril Ore ×25 <i>or</i> Phoenix Ash Bloom ×25 <i>or</i> Heart of Kuraokami ×25, and more
```

**`item:Legendary Gatherer's Chest.description`**
```html
<i>The quartermaster's reserve, sealed by his own hand and marked never to be drawn.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 55%</b></span> · Mithril Ore ×20 <i>or</i> Phoenix Ash Bloom ×20 <i>or</i> Heart of Kuraokami ×20, and more<br><span style="color:#3b82f6"><b>Rare 25%</b></span> · Fujin's Breath ×10 + Heart of Kuraokami ×10 <i>or</i> Fujin's Breath ×10 + Mithril Ore ×10 <i>or</i> Heart of Kuraokami ×10 + Mithril Ore ×10, and more<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Mithril Ore ×60 <i>or</i> Phoenix Ash Bloom ×60 <i>or</i> Heart of Kuraokami ×60<br><span style="color:#f59e0b"><b>Legendary 8%</b></span> · Orichalcum Ore ×20 + Tempest Heart ×20 + Voidshade Petal ×20 <i>or</i> Lunaris Bloom ×20 + Phoenix Ash Bloom ×20 + Voidshade Petal ×20 <i>or</i> Fujin's Breath ×20 + Lunaris Bloom ×20 + Phoenix Ash Bloom ×20, and more
```

---

## 5. Variants

Art rule (loot tables §5d, RUL-2026-10-29-049): each variant keeps its base weapon's silhouette, with skyglass as inlay
and accents. The Skyglass Katana stays the only all-crystal blade; no variant reads as a crystal sword. Base weapon
types are from the item captures (harvests/inbox). The art line is the subject only; the item-icon scaffold
(`skills/producing-tnr-art/references/prompts.md` §3) supplies house style, framing and chroma.

### 5.1 The 12 Skyglass variants (Skyglass Token)

`variant:<Base>/<Name>`: `name`, `description` (the flavour line), and an art line.

| Base (type) | Variant name | Description | Art line |
|---|---|---|---|
| Aetherion (sword) | Gale-Watch Aetherion | `Aetherion with a thread of skyglass down the fuller and a grip wrapped in old sailcloth. It burns like a deck lantern on a long watch.` | Aetherion's steel sword silhouette; a thin pale-cyan skyglass vein inlaid along the fuller; grip wrapped in weathered sailcloth; a small four-point star at the pommel. |
| Thornsilver (sword) | Tidewater Thornsilver | `Thornsilver cooled in the Foundry's flood, with a row of skyglass beads set down its spine.` | Thornsilver's sword silhouette, steel blade wet-dark; a row of small round skyglass beads inlaid along the spine; faint salt crust at the guard. |
| Night's Testament (sword) | Night Watch Testament | `The blackened blade of judgment, with one skyglass star at the guard, like the last lamp left lit on deck.` | Night's Testament's blackened sword silhouette unchanged; a single small cyan four-point star set into the crossguard; no crystal on the blade. |
| Stormrender (sword) | Mast-Lightning Stormrender | `Stormrender with a skyglass storm-rod set into the crossguard, the kind the war-ship carried at its mastheads.` | Stormrender's sword silhouette; a short skyglass rod set upright in the crossguard; thin cyan crackle lines along the ricasso only. |
| Oathbinder (sickle and chain) | Roll-Call Oathbinder | `Every white prayer knot on the chain is a skyglass bead now: one for each name on the duty roster.` | Oathbinder's sickle-and-chain silhouette; the chain's white prayer knots replaced by small pale-cyan skyglass beads; black chain otherwise unchanged. |
| Ink of the Void (bow) | Chartline Ink of the Void | `The bow's vow script is overwritten with the Wayfinder's chart lines in skyglass, corrected and corrected again.` | Ink of the Void's bow silhouette; fine cyan skyglass chart lines and a small compass mark inlaid along both limbs. |
| The Unwritten (fan) | The Unwritten Order | `A fan of orders with the mission line left blank, its edge sealed in cyan wax.` | The Unwritten's fan silhouette; ribs of pale paper written with faint orders, one blank line; edge sealed with drops of cyan skyglass wax. |
| Gaea's Embrace (spear) | Keelstone Embrace | `The spear's earth crystal is a shard of skyglass cut from the wreck's keel, and the shaft is banded in ship's iron.` | Gaea's Embrace's spear silhouette, plated shaft kept; the orange tip crystal recoloured pale cyan; two dark iron bands on the shaft. |
| Warden's Bracers (gauntlets) | Drill-Count Bracers | `Deck Warden's gauntlets, the knuckles notched with a count he never finished, a skyglass stud in every notch.` | Warden's Bracers' gauntlet pair silhouette; a row of tally notches across the knuckles, each set with a tiny cyan skyglass stud. |
| Eclipsed Dawnblade (silver blade) | Lastlight Dawnblade | `Pure silver around a heart of skyglass that glows like the Lastlight Lantern, faint and pointing home.` | Eclipsed Dawnblade's silver silhouette; a small lantern-shaped skyglass core set at the base of the blade, soft cyan light contained inside it. |
| Zephyr's Whisper (fan) | Skysail Whisper | `The green crystal is skyglass now, and the ribs are strung like the war-ship's sails.` | Zephyr's Whisper's fan silhouette; the embedded green crystal recoloured pale cyan; thin rigging cords strung between the ribs. |
| Yuki's Frostbite (axe) | Hullbreaker Frostbite | `Yuki's axe on a haft of ship's timber, skyglass set into the cheek of the head. It has opened a few hulls.` | Yuki's Frostbite's axe silhouette; haft of dark ship's timber with iron rings; a skyglass inlay set into the cheek of the axe head, not the edge. |

### 5.2 The 7 boss variants (one token each)

| Base (type) | Variant name | Description | Art line |
|---|---|---|---|
| The Unwritten (fan) | Captain's Command Fan | `The Captain's war fan, black lacquer with the four-point star in skyglass at its heart. He gave his orders with it for decades.` | A gunbai war fan in The Unwritten's fan footprint: rounded black-lacquered paddle with an iron rim on a short haft, a four-point star inlaid in pale cyan skyglass at the centre, faint cyan cracks along the rim. |
| Oathbinder (sickle and chain) | Rot-Bloom Reaper | `A sickle on a chain of rotten rope, cloudy skyglass blooming along the blade where the Core remembered it wrong.` | Oathbinder's sickle-and-chain silhouette; the chain is wet dark rope; clusters of cloudy, milky skyglass growing like barnacles along the back of the blade; dark rot-stained haft. |
| Warden's Bracers (gauntlets) | Warden's Forge-Fists | `Forge-blackened gauntlets with maul-head knuckles, seamed with cooled skyglass. The Foundry Warden never set his work down.` | Warden's Bracers' gauntlet pair silhouette; soot-black forged iron with blunt maul-head knuckle plates; thin seams of cooled pale-cyan skyglass between the plates. |
| Stormrender (sword) | Wayfinder's Heading | `A compass rose of skyglass in the guard, and the Wayfinder's last heading etched down the fuller. It still points at a port that is not there.` | Stormrender's sword silhouette; a small round compass rose inlaid in cyan skyglass at the crossguard; a fine etched route line running down the fuller. |
| Aetherion (sword) | The First Blade | `Aetherion in the First Blade's colours, his gale cord bound round the grip. Bored for decades. Not any more.` | Aetherion's sword silhouette; grip bound in a long grey-blue cord with trailing ends as if in wind; a short skyglass inlay at the base of the blade; old-uniform brass fittings. |
| Whispering Dawnblade (sword) | Sealwright's Seal | `The sword of sealing, written end to end in the Sealwright's script, a skyglass seal at the pommel. It remembers every report he buried.` | Whispering Dawnblade's sword silhouette; fine dark seal script engraved along the whole blade; a round skyglass seal disc at the pommel. |
| Thornsilver (sword) | Crownbreaker | `Thornsilver with the broken frost points of the Command Crown set into its guard. Proof you walked every deck.` | Thornsilver's steel sword silhouette; the crossguard set with three short broken frost-point shards of pale skyglass; plain steel blade, no crystal along the edge. |

Variant `battleDescription`: none proposed; the base weapon's battle line stands unless the director wants one
(open question 9).

---

## 6. Boss lines, Steady the Helm and library battle text

### 6.1 Intro screens (one line on the boss's scene, hinting without naming the mechanic; RUL-2026-10-28-029 item 3)

The battle objective's `description` is the line shown on the scene. New runs: written in §2. Existing hunts: their
battle lines already serve (e.g. "The Foundry Warden tips the crucible."). Subtler replacements are proposed only where
the live line is flat:

| Target | Live | Proposed |
|---|---|---|
| `obj:The Quarantined Archive/b_sealwright.description` and `b_sealwright_a` | `Break the Sealwright's seals.` | `The Sealwright steps back into the reliquary's light, and does not leave it.` |
| `obj:The Captain's Watch/b3*.description` | `The Captain steps down from the command dais.` | `The Captain steps down from the dais. Behind him, the deck rails seem closer than they were.` |
| `obj:The Captain's Watch/b1*.description` | `The Wayfinder redraws the room around you.` | kept |
| `obj:The Buried Cache` Sentinel battle | `The Sentinel rises between you and the cache.` | `The Sentinel rises between you and the cache. The tide is coming in behind it.` |

The Skyglass Wreck is a dungeon: it has no per-floor scenes or dialogs (`SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md`,
"custom scene art cannot be set per floor"), so the Captain's and the Core Horror's Wreck intros live only in their
battle-log lines (Hold the Line: "Hold the line."). See open question 4.

### 6.2 Closing lines (one per boss, when it falls; RUL-2026-10-28-029 item 2)

Target: the first sentence of the objective that follows the boss's battle (or its win ending).

| Boss | Where | Line | Status |
|---|---|---|---|
| The Captain (Watch) | `d_gallery_*` | `"The ship died once. The crown disagreed."` | exists |
| The Captain (The Fall press-on) | `w_press` | `"Then it is done. It was done a long time ago."` | new, §2.4 |
| Core Horror (Archive) | `d_conduit` | `The Core Horror comes apart, and the frame around it is already sketching it back together.` | exists |
| Core Horror (Fall, Burning Heading, steeping) | §2.4, §2.6, §2.7 | it does not speak; the line is narration | new |
| Foundry Warden (Foundry) | `d_pour`, prepend | `"Finished," the Warden says, as if he does not believe it, and cools into a shell of skyglass.` (replaces "The Warden cools into a shell of skyglass.") | new |
| Foundry Warden (Reliquary) | §2.3 | `"The last pour," he says, and does not finish.` | new |
| Sealwright (Archive) | `w_clean`, `w_alarm`, prepend | `The Sealwright lowers his seals for the last time. "Read them," he says. "Someone should, who can still leave."` | new |
| Sealwright (Reliquary) | §2.3 | `"Thank you," he says, very quietly.` | new |
| Skyglass Sentinel (Buried Cache) | live closing narration | `The Sentinel breaks apart into sand and fading script.` | exists (it says little) |
| Wayfinder (Watch) | `d_term2_*`, prepend | `"Mark it on the chart," the Wayfinder says from the floor. "You were here."` | new |
| Wayfinder (Burning Heading) | §2.6 `w_done` | `"Still no home port."` | new |
| First Blade (Watch) | `d_term3_*`, prepend | `"That was new," the First Blade says, and lowers his cleavers to savour it.` | new |
| First Blade (Night Watch, Reliquary) | §2 | `"That was new."` (Rotted: he falls silent, by design) | new |
| Arsenal Keeper (Foundry) | `d_gate`, prepend | `"Unlisted," the Keeper says as he falls, and makes a note of it.` | new |
| Deck Warden (Foundry) | `d_racks`, prepend | `The Deck Warden sinks into the water, still counting.` | new |
| Oathkeeper (Night Watch) | §2.2 | `"The term holds."` | new |
| Replicant Zero (Rotted press-on) | §2.5 | `"The first to return. Not the last."` | new |
| The Crowned Captain | Crownhold aftermath | (the crown breaks; he settles like ash) | exists |
| Crownhold commanders | Crownhold | their after-fight dialogs | exist |

### 6.3 Steady the Helm (the Captain's phase-2 transition jutsu; RUL-2026-10-28-032, -045)

Effects: cleanse (instant), 40% decreasedamagetaken, 40% absorb, clearprevent, for 2 rounds; cast on himself on the
turn he marks the deck and raises the Gunwale.

**`jutsu:Steady the Helm.name`**: `Steady the Helm`

**`jutsu:Steady the Helm.description`**
```
The Captain falls back to his helm and takes command of the deck. He shakes off whatever holds him, and for 2 rounds he takes far less damage, turns part of it aside, and cannot be stripped of his guard.
```

**`jutsu:Steady the Helm.battleDescription`**
```
%user falls back to the helm and sets both hands on the rail. "Steady. Steady."
```

### 6.4 Library jutsu: themed names and action-first battle text (RUL-2026-10-28-028 item 5, -029 item 4)

Shared marks and blasts are used by every boss, so their names stay neutral but in the story's voice, and keep the
shape word so the battle log still teaches the pattern (Boss Fights §5a). Marks and their blasts share one name.
`description` for every mark: `A warning mark. Whatever it marks is struck on the caster's next turn.` For every shared
blast: `Strikes the ground its omen marked.`

| Harness name | Themed name | `battleDescription` |
|---|---|---|
| Omen: Ring | Omen: Cracking Ring | `%user presses a palm to the floor, and a ring of red cracks opens around them.` |
| Omen: Binding Ring | Omen: Chain Ring | `%user draws a violet seal in the air, and a ring of script binds the floor around them.` |
| Omen: Rows (A and B) | Omen: Twin Rows | `%user sweeps an arm across the field, and two rows of floor glow red.` |
| Omen: Scatter (A and B) | Omen: Swelling Ground | `%user stamps once, and the floor swells red in patches.` |
| Omen: Lines | Omen: Fanned Lines | `%user points across the field, and three red lines fan out from their feet.` |
| Omen: Seal Lines | Omen: Seal Cross | `%user flicks seal script from their fingers, and it runs out across the floor in a violet cross.` |
| Omen: Last Light | Omen: Last Light (kept) | `%user raises both hands, and the whole field darkens red. Three points of skyglass light remain.` |
| Omen: Last Light, Binding | Omen: Last Light, Binding (kept) | `%user spreads violet script over the whole field. Three points of skyglass light remain.` |
| Omen: Splash | Omen: Marked Plank | `%user marks the planks under %target with a red seal.` |
| Omen: Short Line | Omen: Sighted Line | `%user sights down a short red line toward %target.` |
| Eruption: Ring | Eruption: Cracking Ring | `%user closes a fist, and the cracked ring bursts upward.` |
| Eruption: Rows (A and B) | Eruption: Twin Rows | `%user brings the arm down, and the marked rows erupt.` |
| Eruption: Scatter (A and B) | Eruption: Swelling Ground | `%user stamps again, and the swollen ground bursts.` |
| Eruption: Lines | Eruption: Fanned Lines | `%user snaps their fingers, and the marked lines split open.` |
| Binding: Seal Lines | Binding: Seal Cross | `%user closes the cross, and the marked lines bind whoever stands on them.` |
| Eruption: Splash | Eruption: Marked Plank | `%user strikes the marked planks, and they burst.` |
| Eruption: Short Line | Eruption: Sighted Line | `%user lunges down the marked line.` |
| Lowered Guard | Lowered Guard (kept) | `%user lowers their guard for one breath.` (kept; already action first) |

Bespoke signatures (their battle lines become action first; the voice lines stay):

| Jutsu | Live harness line | Proposed |
|---|---|---|
| Maw of the Deep | `Black water and teeth rise from every plank. The mass splits open along a glowing seam.` | `%user sinks into the deck, and black water and teeth rise from every plank. The mass splits open along a glowing seam.` |
| Command Absolute | `"Kneel."` | `%user lifts one hand. "Kneel."` |
| Crownfall | `Shards of the crown fall like blades.` | `%user tilts his head, and shards of the crown fall like blades.` |
| Broadside | `"Fire."` | `%user drops his raised hand. "Fire."` |
| Ship's Bell | `"All hands." The great bell answers.` | `%user strikes the deck with his blade. "All hands." The great bell answers.` |
| Quench | `%user tips seawater onto the melt. The room explodes in steam.` | kept |

Fixes to crew additions (otherwise kept): **Ward of Command** `description` says "while she stands"; the Sealwright is
"he" throughout. Proposed: `The Sealwright's ward on the Captain: the Captain takes heavily reduced damage while the Sealwright stands.`

The Fall's twist (**Spreading Fire I/II/III**, harness `chart-embers-*`, cast by the fire-source hazard):
- `description` (all three): `The fire spreads: embers on these planks burn whoever acts on them.`
- `battleDescription`: I `%user tips a burning keg across the deck, and the far planks catch.` · II `%user kicks the fire on, and it spreads toward the middle of the deck.` · III `%user throws the last of the powder, and only the gangway is left unburnt.`

---

## 7. Walked Every Deck (achievement; reward: Crownbreaker variant token, untradeable)

`questType: achievement`, one-time; `complete_specific_quest` objectives (RUL-2026-10-29-051).

**`quest:Walked Every Deck.name`**: `Walked Every Deck`

**`quest:Walked Every Deck.description`**
```
Clear every run the wreck's charts lead to, both of the runs the rot remembers, and Crownhold at the end of them all.

Reward: the Crownbreaker variant of Thornsilver.
```

**`quest:Walked Every Deck.successDescription`**
```
You have walked every deck of the Skyglass war-ship, and climbed the mountain it answered to. The Crownbreaker is yours.
```

**Objective descriptions** (`obj:Walked Every Deck/<n>.description`), one per quest, in this order:
1. `Clear the Low Tide Run.`
2. `Clear the Night Watch.`
3. `Clear the Buried Cache.`
4. `Clear the Drowned Foundry.`
5. `Clear the Quarantined Archive.`
6. `Clear the Captain's Watch.`
7. `Clear the Sealed Reliquary.`
8. `Clear the Fall.`
9. `Clear the Rotted Reliquary.`
10. `Clear the Burning Heading.`
11. `Clear Crownhold.`

---

## 8. Corrections to existing live text (flagged, not applied)

| Target | Issue | Proposed |
|---|---|---|
| `push/skyglass_update.gen.py` `WRECK_DESCRIPTION` | Says "No one has relieved them." (the bible keeps "relieved" to the refrain) and does not mention charts (loot tables §0, last bullet) | `The Ghost Ship has finally come down. The war-ship that hung over this coast for decades lies broken on the sand, its Skyglass Core cracked and still burning. Inside, the Core holds every deck the way it was, and the crew stand their watch as if nothing has changed. No one is relieved.<br><br>Enter as three. The crew carry the Wayfinder's charts, and each chart leads to a treasure run in the Battle Arena.` (The easy version adds: `For level 45 and up.`) |
| `The Buried Cache` win objectives | The cache note reads "For when we are relieved." | `Tucked under the lid is a note in a careful hand: 'For when we come home.'` |
| `item:Chart of the Quarantined Archive`, `item:Chart of the Captain's Watch` rarity | Live EPIC; hunt charts are Rare by RUL-2026-10-28-028 item 4 | rarity only; not text (noted for the consistency check) |

The Foundry ledger's "crew not relieved" stays: the bible's "carried forward" table places it there.

---

## 9. Open questions for the director

1. **Variant token names.** Settled: the bare variant name (RUL-2026-10-29-057 item 1).
2. **The tainted Last Heading's item name.** Proposed **The Rotted Heading**, to sit beside the Rotted Reliquary Seal
   and not repeat its run's name (The Burning Heading). Or "The Burning Heading" for both.
3. **"Relief" in the Haul's ledger.** The approved Haul story "Draw on relief. Relief is crossed out" uses the
   refrain's word. This file rewords it ("every due date is crossed out and written again"; tags say "Draw on landing").
   Keep the original instead?
4. **The Wreck's boss lines.** A dungeon has no dialogs, so the Captain and the Core Horror have no intro screen or
   closing line there. Options: leave them to the battle log (as now), or add a one-line defeat cue to a jutsu that
   fires on their last phase.
5. **Settled** (RUL-2026-10-29-057 item 5, RUL-2026-10-30-060 item 7): the Keeper is the only fire source and the hazard is removed. **The Fall's fire source.** RUL-2026-10-28-027 makes it the Arsenal Keeper's echo at the powder magazine; the charts
   harness still has a separate hazard record named "Burning Deck" beside a gun-deck Arsenal Keeper. The text assumes the
   Keeper is the source and the hazard is never named to the player. Confirm, and rename the hazard record (e.g. "Powder
   Fire") if it stays separate.
6. **Settled** (RUL-2026-10-30-060 item 6): the Archive's room is cut and the Watch's is kept. The Watch's press-on text is written (§2.8a, RUL-2026-10-30-062). **Archive and Watch press-on rooms.** Loot tables §5 ladder gives them "+20% from its press-on room", but the live
   hunt text has none. No press-on text is written for them until that is settled.
7. **Wreck Sighted's scene character.** A public quest needs one. The salvager is unnamed and has no portrait; use an
   existing crew portrait (the Deck Warden) or commission one?
8. **Tier colours outside the four rarities.** The Strongbox's Forbidden tier uses red `#ef4444`; the profession chests'
   Staples / Recipe kit / Bulk / Windfall map to grey / blue / purple / gold. Both need the §0 hidden-item phone check.
9. **Variant battle lines.** Should boss variants carry their own `battleDescription` (e.g. Crownbreaker: "%user swings a blade set with the crown's broken points.")? None written yet.
10. **Settled** (RUL-2026-10-30-060 item 6): Low Tide's, the Reliquary's and the Burning Heading's rooms are cut and their text is removed; the Fall's is kept. **Press-on rooms marked "proposed" in the harness** (Low Tide's Wayfinder, the Reliquary's Oathkeeper, the Fall's
    Captain, the Burning Heading's First Blade) are written; RUL-2026-10-28-026 item 10 may still cut any that add
    nothing.
