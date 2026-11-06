# The Mother of Echoes: the player experience, end to end

**Status:** design writing and audit for the director (2026-11-05). Live-game requests: 0. No records, manifests or
art were changed, and nothing ships from this file. Text written here is a **draft** for the director; balance, rewards,
art direction and publishing stay his (CLAUDE.md §10).

**The brief (director, 2026-11-05):** "Now we need to define the entire player experience across the fight. What they
see and what they do from the moment they collect the shards until they defeat Sayo and everything in between. I want
it to look, play and feel like a premium endgame limited event through and through, something fun and exciting and
dangerous."

**Standing intent this file is held to:** a puzzle fight won by reading the floor and the moves; readable on screen;
mistakes punishing; a gradual clock; diegetic progression with no rulebook voice, so the fiction carries the tiers
(`docs/design/EVENT_STRUCTURE.md` P6, RUL-2026-11-05-116); Sayo's visual arc from Heartglass light to the Silence's
corruption (the Remainder) (RUL-2026-11-03-111).

**How to read it.** Sections 1–7 walk the journey beat by beat. Each beat says what the player **sees**, **does** and
**feels**, then **today** (what exists, with its source) and **missing** (with a gap id, `X1`…, ranked in section 8).
Section 8 is the premium audit and the Friday checklist.

**Sources**

| Source | Pin |
|---|---|
| Repository | `perseverance484/tnr-tools` main @ `04c5e86e` (fetched 2026-11-05) |
| Shards, tokens, variants | `push/skyglass_uber_economy.gen.py` (`RATES`, `DROPS_TABLE`, `SHARDS`, `THUMBPRINT`, `TOKENS`); live text `push/485_skyglass_story_shards.json`, icons `push/468` |
| The quest | `push/mother_of_echoes.gen.py` (`Q_DESC`, `INTRO`, `DIALOG_OVERRIDES`, `LOSS`, `F_LOST`, `SCENES`, `SCENE_CHARS`, `PICK`, `TOKEN_PCT`); spec dialog at `SPEC_REF` `780907a7`; the practice quest `push/mother_of_echoes_practice.gen.py` |
| What is live | `push/README.md` (440–466, 476, 489, 496 run logs) |
| The fight | `docs/design/MOTHER_OF_ECHOES_FIGHT_SCRIPT.md` (**[FS]**); `docs/design/MOTHER_OF_ECHOES_ACT3.md` (**[A3]**, proposal, `3df0393a`); spec `fable/mother-of-echoes-sim` @ `700a0d6b` (pushed head) and the local sim commit `0cdb0082` (unpushed; today's approvals) |
| Text | `docs/design/MOTHER_OF_ECHOES_JUTSU_TEXT.md` (**[TXT]**, approved) |
| Art | `docs/design/MOTHER_OF_ECHOES_ART.md` (**[ART]**); art4 entrances `97641d00`; `docs/design/SAYO_BIBLE.md` (**[SB]**, DRAFT, `3a6fc6fa`) |
| What the screen can show | `docs/design/COMBAT_ANIMATION_ENGINE.md` (**[AE §n]**) |
| Event wrapper | `docs/design/EVENT_STRUCTURE.md`, `docs/design/EVENT_JOURNAL.md`, `docs/design/SKYGLASS_TEXT.md` §1a (Wreck Sighted, push/497), `docs/design/SKYGLASS_EVENT_MAP.md`, `docs/design/SKYGLASS_STORY_AUDIT.md` |
| Rulings | RUL-2026-11-01-093 … RUL-2026-11-05-122 (Mother of Echoes, uber, variant, badge, title, journal) |
| Live tester | `harvests/battle_logs/moe_practice_dauntless_2026-11-05.txt`, `…_2026-11-05b_live489.txt` (**[LOG]**) |
| Engine | theninjarpg @ `3314d122`, read only with `git show` (**[eng]**, `path:line`) |

Evidence labels: **[eng]** read in engine source; **[repo]** a record, generator or doc in this repository; **[LOG]**
the director's live practice logs; **[sim]** an offline sim result reported by [FS]/[A3]; **[I]** inference, to confirm
on a staff account.

---

## 0. The journey on one page

| # | Beat | The intended feeling | Biggest thing standing between today and premium |
|---|---|---|---|
| 1 | **The pull**: an announcement, a salvager who has stood at the bottom of Crownhold's stair, a locked tower in the Battle Arena | curiosity, then want | The main quest is still the hidden placeholder build (X1); the front door (Wreck Sighted, the Week 1 page, the post) is not published (X3) |
| 2 | **The hunt**: four splinters of one glass, each from a different pillar, each with her thumbprint | a collector's itch; "she left these for me" | Nothing marks the set coming together until the fight itself (X15); no difficulty tell on the shards (X5) |
| 3 | **The threshold**: four "1 / 1 owned" lines, a confirm that takes them, a hall of faces, a woman who grew the glass, a shadow that stands up | dread, commitment | The reveal shows Sayo's portrait one scene early, and long scenes scroll in a small box on phones (X7); the shadow standing up is text only until the entrances are wired (X8) |
| 4 | **The fight**: read the floor (I), remember the floor (II), survive the room (III) | mastery under pressure, tension and release, dread then defiance | The approved fixes are not in the live spec, and Act III stalls at the climax (X2); the clock and her buffs are invisible (X8) |
| 5 | **Failure**: lose any act and the shards are gone | "I know what I did wrong" | Every loss gets the same two generic toasts (X4); a retry costs a whole shard set and there is no public rehearsal (X10) |
| 6 | **Victory**: the glass cracks root to crown; 50,000 ryo, 1,000 exp, a pick, two 1-in-4 rolls | release, pride | The killing blow is never drawn, so every act ends on a generic "You Won" (X6); nothing proves a clear (X11) |
| 7 | **After**: repeat clears for Coffers, Tokens and the two variants; the weekly pages | a reason to return | Fine as built; the clear-to-cost loop needs the rehearsal and badge decisions (X10, X11) |

**What is live today** (push/README run logs):

| Piece | State |
|---|---|
| The four shards | live and dropping (417–420), story text and thumbprint (485 via 489), icons (468) |
| Heartglass and The Remainder tokens and variants | live (417, 418, 468); both tradeable; variants show as "Need <token>" on their bases |
| Boss AIs and 55 jutsu | live through 489 at spec `780907a7`, art3 materials and the approved jutsu text (the [LOG] shows the new lines) |
| **The Mother of Echoes** (`IBPNwhAzlAJPXoeEnp8gW`) | **hidden, still the 464 build**: engine-default icon, the placeholder chamber scene, the old one-scene opening, the old `d_act3`, no portraits. Go-live **477** is not built |
| The practice quest (`YDmKO6fp2vBRnTf7fHWQZ`) | hidden for good; carries the new opening, scenes, portraits and icon (469, 481, 496) |
| Approved but not in the live spec | Sayo stun immune (RUL-2026-11-05-119 item 2); clearable Lancet ramp; Act I stagger; the Silence's absorb at 35% as Act I's Clear target; boss buffs (sim commit `0cdb0082`, local, not pushed; [A3] lists them as approved today) |
| Proposed | the Act III redesign [A3] (decisions in its §6); the Sayo bible [SB] (draft); art4 entrances (built, unwired) |

---

## 1. The pull

### 1.1 The announcement

- **Sees:** the director's post ("Starting this Friday, meet Sayo…"). It is not in the repository, so nothing below
  quotes it (the story audit also found no announcement copy, `SKYGLASS_STORY_AUDIT.md` §1).
- **Does:** reads, looks at the art, decides whether this weekend is a Skyglass weekend.
- **Feels:** "something new is at the bottom of this event, and it is dangerous."
- **Today:** the hook exists in the director's own words. The approved art can carry it: ME01 v2 (Act I Sayo, floating,
  Heartglass fan as halo) and the quest icon (ME13).
- **Missing (X3):** the copy itself. What the post should do for the journey, so the game does not have to say it:
  1. **Name the cost plainly:** one of each shard (Keel, Crown, Tide, Ledger), all four spent when the fight begins,
     solo, three battles in a row with no refills. This is the "know what you're getting into" the director wants for
     an item lost on use (RUL-2026-11-05-119 item 6).
  2. **Name the four homes, not the rates:** the Wreck, Crownhold, the deep and tainted runs, the Haul. The shards
     trade.
  3. **Show Act I only.** Keep the Glasswright and the Saint forms as the in-fight surprise; the visual arc is the
     fight's best reveal.
  4. **Headline rewards:** the Heartglass and The Remainder variants (images), plus "Coffers, Tokens or a Crown's
     Hoard on every clear".
  5. **Where:** the Battle Arena's Battle Pyramid tab; the weekend window.

### 1.2 Wreck Sighted: the front door (push/497, hidden, text awaiting the director)

- **Sees:** six salvager scenes. Two of them seed the finale without naming it (`SKYGLASS_TEXT.md` §1a):
  `d_shards` — "Four of them brought me **shards**. One off the wreck, one from the castle, one from the deep decks, one
  from the sealed stores. Different hands, same glass. Lay them side by side and they ring. Under Crownhold the stair
  stops where the rock does. I've stood at the bottom. Something beneath it listens back." `d_page` — "Every chart and
  every shard has a buyer … Lately the name at the top isn't one of theirs."
- **Does:** clicks through; takes a Tide Chart.
- **Feels:** the ladder exists, and its bottom rung listens.
- **Today:** built, hidden, a one-time quest (RUL-2026-11-05-122 item 3). It is the event's only pre-shard
  foreshadowing (`SKYGLASS_EVENT_MAP.md` G1).
- **Missing (X3):** publish it, and delete the old live Wreck Sighted in the same sitting, before Friday.

### 1.3 The locked tower in the Battle Arena

- **Sees** [eng `app/[shell]/battlearena/page.tsx:166-187`, `layout/QuestPicker.tsx:175-330`]: Battle Arena → Battle
  Pyramid tab → "Battle Pyramids / Select a tower to start" → an accordion row **"Available: The Mother of Echoes"**.
  Open it and the card shows the quest icon, its description, **Minimum Rank: S**, **Quest Type: battlepyramid**,
  **Reward: 3 items** (`ItemWithEffects.tsx:1147-1150`, `libs/objectives.ts:313-330`), then four lines **"Shard of the
  Keel: 0 / 1 owned. Consumed on entry."** (`QuestPicker.tsx:236-243`), "Isolated run: outside activities are blocked
  until completion or abandonment." (`:245-249`), and a greyed **Take Quest** button. [I] It probably also appears as a
  "Battle pyramids" card on the profile dashboard with its name, image and description, pointing to the Battle Arena
  (`libs/profileDashboard.ts:587-641`); confirm on a staff account.
- **Does:** reads the card; sees four empty slots.
- **Feels:** the locked door. This is the strongest diegetic progress surface the engine gives: four counters that fill.
- **Today:** the description (`Q_DESC`) opens well ("The four shards are her invitation…"), then turns into rules
  (three battles, pools carry, lose and the shards are gone, claim a pending reward first). That plain cost is allowed by
  RUL-2026-11-05-119 item 6.
- **Missing:** the live card is the 464 build with the engine-default icon until go-live (X1). "**Reward: 3 items**" is
  the engine's count of the three *pick options*; it undersells a 50,000 ryo finale and misstates a pick-one as three
  items (X5). There is no difficulty marker, though the director keeps stars on pyramids and Crownhold's Lantern already
  reads ★★★★★ (RUL-2026-10-31-074 item 3) (X5).

### 1.4 The weekly page

- **Sees:** Week 1, "The Watch Log: First Page" (push/490, hidden; window 2026-11-06 00:00 UTC to 2026-11-10 00:00 UTC):
  "Your name is written in at the top, in the same ink." Its entries climb to Crownhold, so the page walks a player to
  two of the four shards (the Tide entry's runs drop it at 75%, Crownhold drops the Crown at 100%) without naming them.
- **Feels:** someone is measuring me. That is canon (RUL-2026-11-01-094 item 4: Sayo used the charts, the Lantern and
  Crownhold to measure and lure strong shinobi), and it pays off "the name at the top isn't one of theirs".
- **Today:** Week 1 is built; the fourth page, **"Her Invitation"**, is a sketch (`EVENT_JOURNAL.md` §5: Tide ×2, a Haul
  run, Crownhold, the Mother of Echoes as the stretch).
- **Missing:** publish Week 1 (X3). Post-launch, write "Her Invitation" in Sayo's hand: the page where the player learns
  whose ink it was. It is the event's natural place for the set-completion beat (X15).

---

## 2. The hunt

### 2.1 The four drop moments

| Shard | Where | Rate | How the drop is shown [eng] | Its line (live, push/485) |
|---|---|---|---|---|
| Keel | full Skyglass Wreck (party dungeon, 3 players) | 15% | the dungeon receipt, "Completion rewards delivered." with the item list (`server/api/routers/dungeon.ts:452-515`) | "A splinter of the Mother Glass, shaken loose from the Core the war-ship was built around." |
| Crown | Crownhold | 100% | the quest reward toast "Finished: Crownhold", **Items:** line (`layout/Logbook.tsx:905-931`, `libs/toast.tsx:236`) | "…fallen from the broken Command Crown." |
| Tide | The Sealed Reliquary, The Fall, The Rotted Reliquary, The Burning Heading | 75% | the same quest reward toast | "…left behind by what the Core cannot let go: the reliquary's echoes, and the night of the fall." |
| Ledger | any Haul run | 35% | the same quest reward toast | "…entered in the stores ledger and never claimed." |

Every shard adds "A small thumbprint is pressed into it, made while the glass was soft.", a **Drops:** line and
"**Her invitation:** carry all four shards (Keel, Crown, Tide and Ledger) to open the way to **The Mother of Echoes**.
All four are spent when the fight begins. Shards trade." Rarity LEGENDARY; icons ME14–ME17 (468).

- **Sees:** a name in a list of items in a toast or receipt, in the legendary colour; later, the icon and card in the
  inventory.
- **Does:** opens the item; reads "her invitation"; notices the thumbprint.
- **Feels:** first shard: "what is this for?" Second: "there's a set." The thumbprint turns an item into a person.
- **Today:** the drop surface is the engine's generic reward list; there is no fanfare and none can be added in data.
  The card does the work, and it does it well.
- **Missing:** nothing launch-critical. The shard card has no difficulty marker for the item a player will lose on use
  (X5).

### 2.2 The growing set and trading

- **Sees:** the shards in the inventory; the Battle Pyramid card's four counters, the only set tracker.
- **Does:** chooses which pillar to run next; buys or sells the shard they are short of (all four trade,
  RUL-2026-11-02-104 item 2: "trading is the pity").
- **Feels:** agency (P4): four routes in, and the market as the second route for the walled Crown shard.
- **Pacing:** a first set before trade takes Casual about 6.8 weekends (5.2 with the Wreck trim), Dedicated about 2.0
  (1.5), Hardcore about 0.9 (0.8); with trade, under 2 for every type (RUL-2026-11-02-107 item 2).

### 2.3 The fourth shard

- **Intended:** "the seams vanish".
- **Today:** nothing happens when the fourth arrives. The engine has no "owns a set" trigger [I], the journal cannot
  count "obtain" (`EVENT_JOURNAL.md` §5 template item 8), and the line "The four shards fit together in your hands, and
  the seams vanish" is the first line of `d_intro1`, **after** the shards are consumed. The visible moment is the
  Battle Pyramid card going from three counters to four and the Take Quest button lighting.
- **Missing (X15, post-launch):** let the set-completion beat land where it can: the card (its first line can speak to
  a player holding all four, e.g. "Lay the four side by side and they ring."), and the "Her Invitation" page. Keep the
  `d_intro1` line: it is the payoff.

---

## 3. The threshold

### 3.1 The cost

- **Sees** [eng `QuestPicker.tsx:252-300`]: "Start The Mother of Echoes?" and "Entering costs **1 Shard of the Keel,
  1 Shard of the Crown, 1 Shard of the Tide and 1 Shard of the Ledger**. The items are consumed when you enter and are
  not refunded on abandonment. Proceed?" with "Outside activities are blocked until this run is completed or
  abandoned." (the cost list's exact join is `formatQuestEntryCost`'s).
- **Does:** confirms. The four shards leave the inventory (`:79-84`).
- **Feels:** the stake. This is the engine's own voice, and it is the right voice here: blunt and final.
- **Today:** exactly as wanted. One trap: a player with another pyramid run active, or an unpicked reward from an
  earlier choose-quest, is stopped before this point ("You can only climb one tower at a time",
  `battlearena/page.tsx:911-919`; `Q_DESC`'s last line warns about the reward).

### 3.2 Isolation

- **Sees:** the game pulls them to the combat route between battles ("Returning to your Pyramid",
  `layout/PyramidRunBoundary.tsx:12-23`); between fights their health, chakra and stamina bars stay in the menu
  (`MenuBoxProfile.tsx:177`). The run's Logbook header is the engine's generic **"Current Battlepyramid"**
  (`Logbook.tsx:734`) [uncontrollable].
- **Feels:** the door closed behind them.

### 3.3 The opening: three scenes (live on the practice quest; reaches the real quest only with go-live 477, X1)

| Node | Background | Portrait | Text (approved) | Button |
|---|---|---|---|---|
| `d_intro1` | The Heart of the Mother Glass (ME10) | **Sayo, Act I** | "The four shards fit together in your hands, and the seams vanish. They were never broken. They were an invitation. They pull you down, past where Crownhold's stair ends, into a hall of glass. Every pane holds a face. The Deck Warden. The Captain, twice: once bareheaded, once crowned. The guards you cut down. Their eyes are open, and none of them blink." | Go deeper |
| `d_intro2` | same | Sayo, Act I | "She hangs in the air before the Mother Glass, her fan open behind her like a halo. 'Lovely, aren't they? Every one of them held still for me.' … 'Sayo. I grew the glass.' 'And you have been cutting them out of my glass, one by one. How interesting.'" | You did this |
| `d_open` | same | Sayo, Act I | "She studies you the way she studied them. 'There is room in the glass for one more.' She turns to the wall, as if choosing a place for you. Her shadow does not turn with her. It stays where it was. Then it stands up off the floor." | Step into the hall |

- **Sees** [eng `Logbook.tsx:368-400`]: a 3:2 scene (512×341), the portrait anchored bottom-left at two fifths of the
  width, and the text in a box over the bottom of the scene, **at most 128 px tall, scrolling** (`max-h-32`, `:396`).
- **Does:** reads three beats, chooses "You did this", steps in.
- **Feels:** recognition (every face is someone they fought), then the turn (the villain was behind all of it), then
  dread (the shadow).
- **Missing:**
  - **(X7) The reveal is spoiled.** `SCENE_CHARS` puts Sayo's portrait on `d_intro1`, but she is first described in
    `d_intro2` ("She hangs in the air…"). The first scene should be the hall alone: blank portrait (`BLANK`), so she
    appears with her line.
  - **(X7) The box scrolls.** `d_intro1` is 353 characters and `d_intro2` 381 of plain text; at phone width the box
    shows roughly two to three lines at a time [I]. Either trim to about 220 characters per scene or split the reveal
    into four scenes (hall; faces; Sayo; her name). The button labels already carry voice.
  - **(X8) The shadow standing up is text only.** The art4 entrance for the Silence ("the shadow standing up off the
    floor", `97641d00`) plays only when its carrier is cast, and no carrier exists yet (`ENTRANCE_NOTE`). Wired to a
    round-1 cast of the Silence, it turns `d_open`'s last line into the first thing the battle shows.

### 3.4 The first frame of the battle

- **Sees:** the battle board, both bosses, their avatars (ME01 v2 and ME02), and the battle theme.
- **Uncontrollable (X12):**
  - **The board is the player's own sector biome**, not a hall of glass: quest battles start with `biome: "default"`
    (`server/api/routers/quests.ts:4095-4105`), which resolves to the global tile under the player
    (`server/api/routers/combat.ts:2365-2374`). For most players that is their village's tile.
  - **The music is the shared battle theme** for every PvE and PvP fight ("Another day, Another battlefield",
    `libs/music.ts:64-75`). There is no per-quest or per-boss music in data.
  - **First-use lag:** the first time each jutsu is used in a battle its effects lag one asset fetch, during which
    effect syncing pauses while fighters and HP bars already update [AE §0.10]. Each act is a new battle.
- **Compensation in data:** the scene backgrounds carry the place; the boss entrances and auras (X8) carry the arrival;
  one sound per cast (`SFX_BY_NAME`) carries the rhythm. Upstream asks for later: a battle background or biome per
  `start_battle` objective, and a music asset per quest (the engine already has a MUSIC asset type,
  `hooks/asset.ts:131`).
- **Today, from the tester:** "Boss intro animation was a bit underwhelming but the aura was cool" (director,
  2026-11-05, quoted in `push/mother_of_echoes.gen.py` above `FX4`).

---

## 4. The fight

The fight's mechanics, numbers and per-round script are owned by [FS] and [A3]; this section is what the player lives
through. The state assumed is **today's approved set** (stun immunity, clearable ramp, Act I stagger, Silence absorb 35,
boss buffs; `0cdb0082`), with the live build (`780907a7`) noted where it differs.

### 4.0 What the screen can and cannot say [AE §0]

- Every AI action between two clicks lands in **one snapshot**; all clips start together; nothing is sequenced.
- A one-round mark is on screen for the rest of its cast round and the whole next round, so the player always has their
  turn to read it.
- `decrease*` tags on characters are invisible; there are no floating damage numbers; HP bars show only on hover.
- **The killing blow is never animated**: the canvas is torn down when a result exists.
- The tile language is the event's: heavy (ember-rimmed ring: an eruption), control (violet links: stun or pull),
  linger (bile through glass: a pool), safe (cyan diamond with a star), etch (gold-white lattice: remember this), in
  each act's material [ART].

### 4.1 Act I: The Glasswright and the Deep. *The floor tells you everything, one turn ahead.*

| Moment | Sees | Does | Feels |
|---|---|---|---|
| **First round** | Today (live): Refraction's 27 heavy Heartglass hexes, a heavy ring under them (The Silence Turns), a Feeler rising beside them, the Cradle loop braiding round Sayo and a Lancet hit, **all in one snapshot** [FS §3.4, D4]. Approved: the Silence Turns waits until round 4 and the first Listening until round 2 (Act I stagger) | steps off the lines (10–20 AP), then fights | Approved: a clean first lesson ("lines break next turn"). Live: overload |
| **Learning the tells** | Log lines in her voice: Refraction — "Hold still. I want to see you in the light." Light runs in from the walls. [LOG]; Facet — "Every line has a reflection." [LOG] | reads the board before acting | "She paints my death a turn early" |
| **Mastery: the Feeler under Cradle** | the Cradle loop on Sayo (moved onto `clearprevent` so it renders [ART]); log "The deep closes around Sayo… Blows slide off the glass." [LOG] | switches target to the Feeler (2,500 HP), stays more than 2 hexes from it | the first real choice; the payoff is Sayo's guard back |
| **Mastery: clearing the ramp** | Approved (`0cdb0082`): the Lancet ramp is clearable. Its glow is **not wired** (X8), so the player sees only a Lancet hit and the log line "damage given is increased by up to 7%" | Clears Sayo at a few stacks (60 AP, range 4, cooldown 10) | Intended: "reset the clock". Today: invisible, so it cannot be learned from the screen |
| **Mastery: Clear the Silence** | Approved: the Silence's absorb raised to 35% for 3 rounds as Act I's Clear target, which also strips its Stillness marker (Nothing Moves never lands) [FS R2] | one Clear on the Silence | a double payoff; the act's best "aha" |
| **Kill order** | both HP bars on hover; Lucid's aura on Sayo if the Silence falls first [ART `moe_lucid`] | chooses who dies first: Lucid (Sayo +20%, no rest turns) or Unbridled (pools and a Feeler every turn) | consequence; two lines through the act |
| **Below 40%** | Your Likeness rises in a silvered ring | outlasts it (3 rounds) or bursts it | unease: "it fights like me" |
| **Act end** | the canvas closes on the last hit, unanimated; the engine's black overlay "**You Won**", "Battle rewards", "**Continue Pyramid**" (`layout/Combat.tsx:1320-1375`) | clicks Continue | Intended: the light goes out. Today: generic (X6) |

### 4.2 Interlude I → II

- **Sees:** the Stilling scene (ME11) and the Glasswright's portrait (half her body turned to glass); text (spec,
  approved): "The deep goes quiet, but the glass does not. Sayo wipes a line of light from her sleeve. 'You read patterns
  well. Let us see how well you remember them.'" Button: **Hold your ground**. The player's pools are visible: they
  carry, with no refill.
- **Feels:** a breath, a warning, and a resource check ("I'm at 30%; is that enough?").
- **Missing (X6):** the act's last blow belongs here, because the canvas never shows it. Draft opener for
  `d_act2`: *"The last of the light runs out of her lines, and the shadow lies flat on the floor again."* then the
  existing text.

### 4.3 Act II: The Stilling. *Remember what she showed you.*

| Moment | Sees | Does | Feels |
|---|---|---|---|
| **Etching (×3–5)** | the gold-white lattice over a region for its cast round and the next; the log names it ("traces the north of the hall"); approved: the Stilling shield aura on each Etching | memorises region and order; fights freely | quiet, loaded |
| **The Hush Rises** | 10 random dark pools per etching turn (15% drain, no healing) | plans a hex that is both dry and Recast-safe | pressure; the act's top killer [FS §4.3] |
| **Recast** | **no mark**; the Recast payoff (lattice replayed in white-gold, glass blades rise, black cracks race up) and a 3-round pool; the **guard-open ring** on Sayo [ART] | before her turn, stands outside the region that comes due; during guard open, bursts (best skills, the Chakra Pill) | **the fight's best moment**: dodge, dodge, punish [FS §4.4] |
| **The lull and the Worn** | dust motes beside her (The Glass Falls Quiet); the Gate Porter, Sister Hana, Cadet Tomo rise from ash; Hana's mend art and Sayo's HP climbing | kills Hana; keeps a buffer from the Porter's push and Tomo's pull | target priority; for players who read the Worn hints, pity |
| **Clock** | the cycle counter (enrage after cycle 4) has no art [FS R11] | — | invisible (X16) |
| **Act end** | "You Won" overlay, Continue Pyramid | — | generic (X6) |

### 4.4 Interlude II → III

- **Sees:** the A Good Impression scene (ME12) and the Saint's portrait (all glass, the Silence's black filling her);
  `d_act3` (override): "Every pane in the hall turns toward you. The dark at the edge of the light folds itself small and
  slides back across the floor into Sayo's shadow. Her eyes close. When she speaks again, nothing moves her lips. 'Hold
  still. You will make for a good impression.'" Button: **Do not hold still**.
- **Feels:** the floor drops out. The best single line in the quest, and the title paid off.
- **Missing (X6):** an opener for the end of Act II. Draft: *"Her etchings fade one by one, the last in the order she
  drew them."*

### 4.5 Act III: A Good Impression. *Survive the room* (as built) *→ the same verbs, turned up* (proposed)

**As built (live):** three loops of one verb each: leave Shatterfall's fan (100–60%), stand on one of three fixed stars
(60–25%), outlast a 6-round "cannot fall" while the ceiling comes down (below 25%). A perfect player needs a median 47
rounds with Acts I–II carried in; two thirds of turns end with AP unspent; the heal block at 60% (No One Is Mended, 20
rounds) has no warning; and the climax **stalls**: after The Long Hush the Saint casts at most one pane, then idles
(seed 1: 14 idle rounds) because of the engine's shared pierce cooldown [FS D2, A3 §1.3]. The player would feel a
turret phase and then a broken boss. **This is the weakest stretch of the whole journey (X2).**

**Proposed [A3]:** the moves the player learned, faster, larger, layered, lethal, in about 17 rounds:

| Phase | Sees | Mastery moment | Feels |
|---|---|---|---|
| **I. Lucid** (100–60%) | Refraction every turn in Remainder black, Facet's double set, a heavy bar under them (Hold Still), a violet ring and the Cradle loop on *her* (The Silence Holds Her) | **Dodging the follow mark** with one side step; **one Clear from exactly 4 hexes** strips her Cradle, absorb, Stillness and ramp at once; burst on Facet Breaks (guard ×4) | Act I's lesson, with no rest turns |
| **The warning** (70%) | The Names Stir: a one-round preview of the hush floor, "Soon nothing here will mend. Except where the three refused." | top up, or push on | a real heal-timing choice, and the Worn paid off |
| **II. Every Name, Remembered** (60–25%) | three cyan stars, and two turns earlier an Act II etching that covered one of them | **trust memory over the screen**: stand on the star she did not etch; burst on the flood (guard ×3) | the fight's thesis: the glass remembers |
| **III. A Good Impression** (<25%) | each turn a third of the ceiling falls with an echo of Act I's lines (in Heartglass) or Act II's etchings (in cracked glass); a lethal column through them; her guard open ×2; she walks to them | one side step that clears pane and column, then burst | the whole fight coming back at once, in the glass it was learned in |

**The climax feeling we want:** the player sees every material of the event's arc on one floor in its last three
turns, Heartglass lines and cracked etchings under black Remainder glass, and wins by doing the things the fight taught
them, fast. [A3] delivers that; the decision is the director's ([A3] §6).

### 4.6 The arc across the fight

| | Act I | Interlude | Act II | Interlude | Act III | Win |
|---|---|---|---|---|---|---|
| Sayo's body | floating, light veins, fan as halo (ME01 v2) | — | half etched glass, the fan breaking (ME03) | — | all glass, the Silence's black inside (ME04) | gone: the glass cracks |
| Scene | Heart of the Mother Glass | The Stilling | The Stilling | A Good Impression | A Good Impression | A Good Impression, no figure |
| Floor material | Heartglass (crystal, prismatic) | | the turn (black cracks creep in) | | the Remainder (thorned black, teal veins) | — |
| Sound (existing SFX, one per cast) | wind marks, lightning breaks, sword lancets, smoke summons | none | wind etchings, sword-clash Recasts | none | earth falls, wind marks | none |
| Music | the shared battle theme (uncontrollable) | village/default theme | battle theme | | battle theme | |

The visual arc is already premium in the avatars, scenes, portraits and tile materials. Its gaps are motion and sound:
entrances and auras built but unwired (X8), the act-start flourishes judged off-model by [SB] §6 ("one ring-and-teeth
template recoloured four ways"), and no signature sound ([SB] §2.3 proposes the struck-glass ring and its dead stop as
her sound; any custom SFX is a new asset, X12).

---

## 5. Failure

### 5.1 What dying looks like

| Act | Typical cause (sim, [FS]/[A3]) | What the screen shows | Readable? |
|---|---|---|---|
| I | standing in a line (3,030), the follow ring's drain, Lancet chip | the canvas closes; "**You Lost**"; Battle rewards (any battle exp); "Quest Energy is restored when you claim the completed quest's rewards." (`layout/CombatRewards.tsx:136`); "Return to Profile" [LOG, eng `Combat.tsx:1324-1375`] | mostly: every eruption had a tile the turn before; the Lancet ramp did not (X8) |
| II | a misremembered Recast (6,500, death at full HP), a pool, the Porter's push into a pattern | same | yes, as a memory test the act taught |
| III (built) | Shatterfall, the unwarned heal block, Lancet chip | same | partly: the heal block had no tell |
| III (proposed) | the etched star, off a star at the flood, a pane or the column | same | yes, every lethal hit is told the turn before except the etching, which is memory ([A3] §3.8) |

Then two toasts titled **"Quest Update"** in the engine's success style (`Combat.tsx:481-500`): the battle's
`failDescription`, "The glass goes quiet around you. The shards are spent." (`libs/quest.ts:1838-1844`), and the fail
node, "The glass keeps what it was given. Find four more shards and come back." (`libs/quest.ts:1522-1525`). The same
two lines follow every loss in every act.

- **Feels, intended:** "I know exactly what I did wrong, and I want her again."
- **Feels, today:** the canvas vanishes on the blow that killed them, and the text says the same thing whether they fell
  on round 3 of Act I or round 40 of Act III.
- **Missing (X4):** each battle has its own `failDescription` slot. Use it to name the act's lesson in her voice,
  without instructions. Drafts for the director:
  - Act I: *"The light came where she drew it, a breath after she drew it. The glass takes you where you stood."*
  - Act II: *"The glass remembered the hall. You did not."*
  - Act III: *"Every pane turns toward you, and at last you hold still."*
  - Fail node (`F_LOST`), distinct from the battle line: *"Your impression stays in the glass beside the others. Four
    more shards will carry you back to her."*
  - Flee is already distinct ("You back out of the hall. The shards stay in the glass.").

### 5.2 What they keep and lose

- **Lose:** all four shards (consumed on entry, never refunded, `QuestPicker.tsx:278-288`; abandoning says "Consumed
  entry items will not be returned.", `Logbook.tsx:714-716`); consumables used; durability; the attempt.
- **Keep:** whatever the won battles paid (battle experience on the result screen); knowledge.
- **Rewards:** none. A loss pays nothing (RUL-2026-11-01-095 item 4, RUL-2026-11-03-110).

### 5.3 How quickly they can try again

There is no retry delay (`retryDelay`/`attemptDelay` "none"). The limit is the shards: one set is about 1.5–2 weekends
for a Dedicated player and 0.8–0.9 for a Hardcore one before trade, less with trade (RUL-2026-11-02-107).

Against the clear rates that is the journey's sharpest risk. The live-calibrated sim gives **perfect play 5–6 of 20 and
real elite 0 of 20** for the whole fight ([FS] §0; `0cdb0082` loop 18), against targets of 50–70% and 0–10%
(RUL-2026-11-05-119 item 5; [A3]). The director lost Act I in round 9 of his second test [LOG live489]. A strong player
can expect many attempts per clear, each costing a set of shards and one to two weekends. "Mistakes punishing" is the
intent; a retry loop measured in weekends with no way to rehearse is frustration (X2, X10).

### 5.4 Does failure teach?

- **Act I and II:** yes, when the death has a tile. The Lancet ramp and the unwired buffs are the exceptions (X8).
- **Act III as built:** no. The heal block is unwarned and the climax stalls (X2).
- **The text:** does not help today (X4).
- **The hints:** the approved hint voice lives in the jutsu **descriptions** [TXT]. The combat screen shows the
  `battleDescription` in the action log (`CombatHistory.tsx:162`, `CombatTimeline.tsx:394`); I found no in-battle
  surface that shows an opponent's jutsu description, and the uber jutsu were created hidden [I]. If players cannot read
  the descriptions anywhere, the puzzle's clues are invisible (X9). Verify on a non-staff account.

### 5.5 The practice quest

- **Today:** "The Mother of Echoes (Practice)" is a hidden copy of the same three battles against the same AIs, with no
  entry items and the real rewards, for the director's tester; it stays hidden for good because hidden is its only gate
  on free rewards (`push/mother_of_echoes_practice.gen.py`). Players never see it.
- **Its role for players (X10, director decision):**
  - **A. No rehearsal** (today). Pure uber; learning costs shards. Matches "dangerous"; risks the frustration in 5.3.
  - **B. A public rehearsal with no rewards** (no ryo, exp, tokens or pick; win node empty), named in the fiction (for
    example *"An Echo of the Hall"*: the salvager's memory of the stair, not the hall itself). Learning becomes free;
    the shards buy the real thing. Cost: some mystery, and players may farm battle experience from it [I: check what
    `scaleGains` permits].
  - **C. Act I only, rewardless.** Teaches the grammar; keeps Acts II and III as surprises.
  - Recommended: **C** at launch or soon after, if the clear rates stay far under target.

---

## 6. Victory

### 6.1 The killing blow and the win scene

- **Sees:** the canvas closes on the last hit, unanimated [AE §0.11]; "**You Won**"; Battle rewards; "**Continue
  Pyramid**". Then the `w_clear` scene: the A Good Impression background (ME12), **no figure** (no portrait is set, so
  the quest's blank character shows), and the text (spec): "The Mother Glass cracks from the root to the crown. For the
  first time since the siege, Crownhold makes a sound. You are not stilled." and a **Collect Reward** button with a
  sparkle icon (`Logbook.tsx:854-863`).
- **Feels, intended:** release, and a silence that breaks.
- **Missing:**
  - **(X6)** The final blow lives only in the text. Draft opener (as [A3] §4.5 and [FS] R12 ask): *"The last pane does
    not fall. It cracks, and the crack keeps going."* then the existing lines.
  - **(X14, post-launch art)** The win scene reuses the Saint's hall. A victory background, the hall with the Mother
    Glass split root to crown and the faces gone dark, or a portrait of the shattered fan, would give the clear its own
    image. Optional.

### 6.2 The reward toast and the pick

- **Sees, in order:** a toast "**Finished: The Mother of Echoes**" with "**Quest Completed:** *The Mother Glass cracks
  from the root to the crown. Choose your reward.*", **Money: 50000 ryo**, **Experience: 1000**, and **Items:** listing
  any token that rolled (`Logbook.tsx:905-931`, `libs/toast.tsx:236-330`). Then the modal opens by itself:
  "**Choose Your Reward**", "The Mother of Echoes", "Select 1 reward to claim", three cards (Crown's Hoard ×1, Skyglass
  Coffer ×5, Skyglass Token ×3), "0 / 1 selected", a red **Claim Reward** button (`layout/RewardChoice.tsx:117-190`).
  A dismissed pick waits in the Logbook as "Rewards waiting" with a **Choose** button (`:197-223`).
- **Does:** picks the all-rounder (the Hoard), gear (Coffers) or skins (Tokens) (RUL-2026-11-04-114).
- **Feels:** a payout worthy of the finale. Each option has its own job.
- **Missing (X14):** the toast repeats the scene's first sentence word for word (`Q_SUCCESS` vs `w_clear`). Draft
  `successDescription`: *"Sayo is still. You are not."* The picker already says "choose".

### 6.3 The token rolls

- Each clear rolls the **Heartglass** token at 25% and **The Remainder** token at 25%, independently (`TOKEN_PCT`); a
  roll shows only as a name in the toast's Items line. About one clear in sixteen drops both; about nine in sixteen
  drop neither. Both trade (RUL-2026-11-02-105), so a duplicate sells.
- **Using one** (token text, push/468, the push/329 pattern; not re-verified in engine here): "You must own The
  Unwritten: open it, choose **Variants**, then **Use Heartglass**. Once per player." The Remainder goes on Ink of the
  Void. A player who does not own the base weapon has a tradeable item and no use for it, which the text says.
- **Feels:** the jackpot moment, for the 1-in-4.

### 6.4 Badge, title, proof

- **What exists:** no badge, title, jutsu or pet for this fight, by ruling (RUL-2026-11-01-095 "No badge or jutsu …";
  RUL-2026-11-02-105 "Forget the title"). The event's only badge is **Crownbreaker**, a take-once Crownhold pick
  (push/340). "One badge for the whole event" (RUL-2026-11-05-121 D5) was ruled for the weekly pages; it names no badge.
  Walked Every Deck covers the chart runs and Crownhold, not the finale.
- **So:** nothing in the game proves a clear. The tokens trade, so a Heartglass fan can be bought; the Logbook history's
  "Completed" row is private.
- **Missing (X11, director decision):** whether the finale gets the event's one badge (granted on the win node, not in
  the pick, so it never competes with the Hoard; [I] confirm a repeat grant to an owner is a no-op).

### 6.5 Bragging

- **The variants are visible** where the engine shows item names and images: in battle the item's name, image and
  battle text resolve to the active variant (`libs/combat/actions.ts:777-780`), so an opponent's log reads
  "Heartglass", not "The Unwritten".
- **Missing (X11):** neither variant has a `battleDescription` (push/417, 468), so in battle the log falls back to the
  base weapon's own line (`variantBattleDescription ?? item.battleDescription`). The table supports one
  (`app/drizzle/schema.ts:1736-1750`). Two lines in [TXT]'s voice would make the skin speak in every fight it appears in.
  Post-launch; nobody owns one until the first clear.

---

## 7. After

### 7.1 Repeat clears

- **Motivation:** the pick (Hoard, ×5 Coffers, ×3 Tokens), 50,000 ryo, and two 1-in-4 rolls on tradeable variant
  tokens. With about four clears per token on average, the variants are a medium-term goal, and duplicates have a
  market.
- **Loop:** four shards from four pillars per attempt, so every attempt drives the whole event (P1/P2). At the current
  clear rates the loop is attempt-bound, not reward-bound (X2, X10).
- **Pacing:** fine as designed once the clear rates reach their targets.

### 7.2 The weekly pages

Week 1 ships with the fight. "Her Invitation" (page four, sketched) is the place for the finale's diegetic pull: Sayo's
hand on the page, the four shard sources as its orders, the fight as the stretch.

### 7.3 Between weekends and if the event ends

- **Weekdays:** the quest has no `startsAt`/`endsAt`; its availability follows its hidden flag [repo]. A hidden pyramid
  **pauses** an open run without losing it ("This Pyramid is hidden. Your run is paused…", `Logbook.tsx:722-727`), so
  hiding it at the end of a weekend is safe for players inside.
- **Edits are not safe (X13):** any content edit of the quest record ends every open run ("This Pyramid was edited.
  Abandon this run and start again.", `Logbook.tsx:722-725`; `libs/questRun.ts`), and with it four shards per player.
  AI and jutsu edits do not touch the quest record. Rule for the live window: never edit the quest during play hours
  (the story-pass generator already says "run outside event hours").
- **If Skyglass ever ends:** unspent shards and tokens remain as inventory items. A closing line on the shards ("The
  glass is quiet now.") would let them become keepsakes rather than dead keys. Not needed now (the event runs
  indefinitely, RUL-2026-11-01-096 item 4).

---

## 8. Premium audit

Ranked by impact on the director's three words: **look**, **play**, **feel**. Owner: art, text, record (a manifest
edit), sim (spec and tuning), director (a decision), ops (publishing). "Friday" marks what should be in place before the
release on 2026-11-06.

| # | Gap | Why it matters | Fix | Owner | Friday? |
|---|---|---|---|---|---|
| **X1** | The real quest is still the 464 build: engine-default icon, placeholder chamber scene, the old one-scene opening and `d_act3`, no portraits, hidden | Every player-facing surface of the threshold is the placeholder; the reveal lives only on the hidden practice quest | Build and run go-live **477** at the final `SPEC_REF`: `INTRO`, `DIALOG_OVERRIDES`, the three scenes, portraits, quest icon, the text fixes X4–X7 and X14, then unhide. Readback against 481/496 | record | **Blocking** |
| **X2** | The live spec lacks today's approvals (stun immunity, clearable ramp, Act I stagger, Silence absorb 35, boss buffs; `0cdb0082` is local, unpushed). Act III stalls at the climax and its heal block is unwarned. Clear rates: perfect 5–6/20 vs 50–70% | The fight is the product; a stalled boss at the end reads as broken, and the overload in Act I's first round teaches nothing | Push the sim commit, rebuild the tuning job, run it Monday–Thursday per law 18 (so: **today**). For Act III: the director rules on [A3] §6; if not approved by Friday, at minimum fix the stall (blasts that cannot be locked by the shared pierce cooldown, [A3] §1.3) and add the No One Is Mended warning ([FS] R8) | sim, director | **Blocking** (approved fixes and the stall); redesign can follow |
| **X3** | The front door is unpublished: Wreck Sighted (497, text awaiting the director), Week 1 (490), the release post (not in the repo) | Without them the pull is the post alone, and the locked tower has no story pointing at it | Director reviews §1a text; publish 497 and delete the old Wreck Sighted in one sitting; publish 490; the post per §1.1 | director, ops | **Blocking** |
| **X4** | Every loss shows the same two generic toasts, in the engine's success style | Failure is the most common moment of the journey; today it teaches nothing and says nothing about where they fell | Act-specific `failDescription` on `b_act1`–`b_act3` and a distinct `F_LOST` (drafts §5.1). The toast style is engine-owned | text, record (rides 477) | **Yes** (cheap) |
| **X5** | The quest card says "Reward: 3 items" and has no difficulty marker; the shards have none either | The card is the locked door and the decision point for a spend; it undersells the finale and hides the danger the director wants stated | Add to `Q_DESC` a plain rewards line: *"Every clear: 50,000 ryo and 1,000 experience; a 1 in 4 chance each at the Heartglass and The Remainder tokens; and your pick of a Crown's Hoard, five Skyglass Coffers or three Skyglass Tokens. A loss pays nothing."* Director picks a marker above Crownhold's ★★★★★ for the card and the four shard cards | text, director | **Yes** |
| **X6** | The killing blow is never animated, so each act ends on the engine's generic "You Won" | The three biggest beats of the fight happen off screen | Openers on `d_act2`, `d_act3`, `w_clear` (drafts §4.2, §4.4, §6.1) | text (rides 477) | **Yes** (cheap) |
| **X7** | Sayo's portrait shows on `d_intro1` before she is revealed; 350–380-character scenes scroll in a 128 px box on phones | The reveal is the event's story payoff | `d_intro1` gets the blank portrait; trim to about 220 characters per scene or split into four scenes | text, record (rides 477) | **Yes** (cheap) |
| **X8** | Built but unwired: boss auras (art3), boss entrances (art4), the Lancet ramp glow (the fight's clock), the act-start flourishes; [SB] §6 flags several strips to redo | The director found the intro underwhelming; the clock and her buffs cannot be read; "clear me" has no look | Wire auras to the approved boss buffs and the entrances to a round-1 carrier per form in the tuning job; ramp glow on the Lancet's `increasedamagegiven` ([FS] R3). Redo the flourishes per [SB] post-launch | sim, record, art | **Recommended** (wiring); redo post-launch |
| **X9** | The hint voice is in jutsu descriptions, which players may have no way to read in or out of battle | The puzzle's clues ([TXT]) would be invisible; only log lines remain | Verify on a non-staff account. If unreadable: carry the key clue of each tell into its `battleDescription` (the log), or surface the hints elsewhere (shard cards, the quest card, a rehearsal) | text, verify | **Verify Friday** |
| **X10** | No rehearsal; each failure costs a full shard set and one to two weekends | At today's clear rates most attempts fail; learning is priced in weekends | Director decision §5.5 (recommended C: a rewardless Act I rehearsal) | director, record | Post-launch (or launch if rates stay low) |
| **X11** | Nothing proves a clear: no badge, no title, tradeable tokens; the variants have no battle line of their own | "Premium" and "exclusive" need a mark the market cannot sell | Director: give the finale the event's one badge on the win node (art + record). Text: variant `battleDescription`s | director, art, text | Post-launch (badge could be Friday if art exists) |
| **X12** | Uncontrollable presentation: the board is the player's overworld biome; one battle theme for every fight; first-use lag; generic SFX | The hall of glass never appears in combat; no musical identity | Compensate with scenes, entrances, auras and per-cast SFX (done). Later: a custom "struck glass" SFX set ([SB] §2.3); upstream asks for a per-objective battle background and per-quest music | art, upstream | Post-launch |
| **X13** | Editing the quest record during play ends every open run and its shards | One hotfix could cost every player inside four shards | Ops rule: quest edits outside play hours only; hotfix through AI and jutsu records; decide in advance how staff compensate a voided run | ops, director | **Protocol before Friday** |
| **X14** | The win: the toast repeats the scene's sentence; the win scene reuses the Saint's hall with no figure | The payoff screen is the least designed screen | `successDescription` draft *"Sayo is still. You are not."* (Friday). A victory background or shattered-fan portrait (post-launch) | text; art | Text yes; art post-launch |
| **X15** | No set-completion moment when the fourth shard arrives | "The seams vanish" lands only after the spend | A card line for the four-held state; the "Her Invitation" page | text, journal | Post-launch |
| **X16** | No countdown for the enrages; no Act II cycle counter | A clock the player cannot see is not a clock | Cycle counter loop ([FS] R11); enrage tells per act | art, sim | Post-launch |

### 8.1 The Friday checklist (in order)

1. **Today (Thursday, law 18 window):** push the approved sim spec; build and run the tuning job with the boss buffs,
   stun immunity, stagger, clearable ramp, aura/entrance/ramp wiring and the Act III stall fix (X2, X8).
2. Director decisions: [A3] §6 (or defer it and keep the stall fix), the difficulty marker (X5), the text drafts in this
   file (X4–X7, X14), the badge (X11, optional).
3. Build go-live **477** with the text fixes; gates; run; read back the scene, portrait and text on every node (X1).
4. Staff test on a non-staff account: the Battle Pyramid card, the confirm, the opening on a phone, a loss in Act I
   (the toasts), the hint visibility (X9), a clear on the practice quest (toast and pick).
5. Publish Wreck Sighted 497 (delete the old one), Week 1 490, the quest; post the announcement (X3).
6. Freeze the quest record for the weekend (X13).

### 8.2 Director decisions this file raises

1. The difficulty marker for the finale and its shards (X5).
2. The text drafts: act fail lines, `F_LOST`, act-end openers, the win line, the rewards line (X4, X5, X6, X14).
3. Whether the opening drops Sayo's portrait from the first scene and splits into four short scenes (X7).
4. A player rehearsal: none, rewardless whole fight, or rewardless Act I (X10).
5. The event's one badge on the finale (X11).
6. Act III: the redesign or the stall fix only, for Friday (X2; [A3] §6).

---

## 9. Boundaries

- Design writing and audit only. No live requests; the game was not run; no records, manifests or art were changed.
- Engine claims are read at theninjarpg `3314d122`; anything marked [I] needs a staff-account check. Not checked here:
  the exact joined wording of the entry-cost line, the profile dashboard card, whether hidden AI jutsu descriptions are
  readable anywhere, the variant "Use" button wording, and whether a repeated badge grant is a no-op.
- The fight's numbers move with the sim; this file cites [FS] and [A3] rather than restating their tables, and loses to
  them, the spec and the rulings where they disagree.
