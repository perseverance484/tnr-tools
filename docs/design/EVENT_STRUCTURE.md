# TNR event structure: the framework

**Status:** ACTIVE framework (RUL-2026-11-05-116). The principles are the director's; the checks, templates and
anti-patterns are Claude's drafting of them, open to the director's revision. Open questions are listed in §8 and are
**not** settled by this file.
**Date:** 2026-11-05. **Repository baseline:** `perseverance484/tnr-tools` main at `6289a3e1`. Zero live requests.
**Reference implementation:** the Skyglass event, mapped in `docs/design/SKYGLASS_EVENT_MAP.md`.

**What this file owns:** how a TNR event is *structured*: its content nodes, its economy, its gates, its progression
ladder and how the player reads it. **What it does not own:**
- engine facts (what a dungeon, a battlepyramid, a `special` quest, an entry item, a weighted cache or a variant can do):
  `docs/ENGINE_LAWS.md`, the skill references (`references/quest.md`, `item.md`, `balance.md`), the generated contracts,
  and the game-source pin of the task. Where this file names an engine behaviour it cites the owner and does not restate it;
- cross-surface doctrine (hidden-first, the director's reserved decisions, validation): `docs/DOCTRINE.md`
  ([[D-hidden-true]], [[D-reserved-dauntless]], [[D-validate-always]]);
- precedence: `docs/00_INDEX.md`;
- any specific event's numbers: that event's own design docs and generators.

## 0. Sources

The framework is drawn from two statements by the director, recorded in `docs/RULINGS.md` RUL-2026-11-05-116.

**Statement 1 (2026-11-05), verbatim:**

> "I kind of see this event as the holy grail of content development for tnr. Not because it is perfect, but because it is the flagship that features how I think content should be structured. It should feed into each other and create an economy of sorts where doing this part of an event feeds into that one, unlocks this or that, makes this possible. It creates a sense of progression and depth for the player, allowing them to engage with content with agency. Being free to choose their approach and pursue their desired outcome and being able to adjust that approach at will is what defines a good game to me. Knowing they can do X thing to get Y outcome or Y to get X and so on. Being able to explore a game and know what you did, what's in front and behind you, trace your progress, it's important. We should look into recording a cohesive event structure future development can draw on."

**Statement 2 (2026-11-05), verbatim:**

> "It used to be that games just labeled things Level 1, Level 2 and it was obvious what your progression was and what the prerequisites were. Now a good game to me tells you that kind of information by weaving it into the story rather than telling it to the players face. You are at Level 1 of the Skyglass Wreck because you've just got a chart that leads to some buried chest in the sand, and Level 100 because you've got 4 fragments that unlock a hidden area that leads to the Final Boss Sayo who blows up the floor and shoots death everywhere and has an immunity phase from her shadow and yadda yadda. We tell a story, paint a picture, but the underlying framework is there. We can say where we start and end and then fill in the gaps with the story and worldbuilding."

## 1. Principles

Each principle has a meaning, a concrete requirement, and a check a reviewer can run against the event sheet (§2).

### P1. Interlocking content

*"It should feed into each other … doing this part of an event feeds into that one, unlocks this or that, makes this possible."*

- **Requirement:** every content node produces at least one thing another node consumes, and every node except the entry
  node is opened by something another node produces.
- **Check:** in the flow graph (§2 item 4), every node has an outgoing edge to another node, and every node but the entry
  has an incoming edge. A node whose only outputs are exports (ryo, exp, game-wide materials) is a leaf and must be named
  as one.

### P2. An economy of sources and sinks

*"Create an economy of sorts."*

- **Requirement:** every event currency (any item the event mints to be spent inside the event) has a written source list
  and a written sink list, with rates.
- **Check:** the source → sink table (§2 item 3) has no currency with zero sinks, and any currency with one source or one
  sink is marked as deliberate and says why (Skyglass: Core Rot has one job by design).

### P3. Progression and depth

*"It creates a sense of progression and depth for the player."*

- **Requirement:** the event has an explicit progression ladder (§3): ordered rungs from entry to finale, each with a
  prerequisite, a place, and a reward that makes the next rung reachable. Depth comes from optional branches off the ladder
  (gambles, side runs, cosmetic layers) that pay into it.
- **Check:** the ladder is written down; each rung's prerequisite is produced by an earlier rung or the entry; the finale
  consumes something from more than one pillar.

### P4. Player agency

*"Free to choose their approach and pursue their desired outcome and being able to adjust that approach at will … X thing to get Y outcome or Y to get X."*

- **Requirement:** every **key outcome** (each ladder prerequisite, each finale input, each headline reward) has at least
  **two routes**, and at least one of them is not trade. Choices are offered at completion (picks), mid-run (press on or
  leave; route choices), and between runs (which chart to run, steep or run). No choice locks the player out of changing
  approach next run.
- **Check:** the alternative-routes table (§2 item 6) lists two or more routes per key outcome. A single-route outcome is
  allowed only when listed as deliberate, with the director's ruling, and with trade as the second route.

### P5. Legibility

*"Know what you did, what's in front and behind you, trace your progress."*

- **Requirement:** the player can answer, from inside the game, four questions: what have I done; what can I do now; what
  is ahead; what does this item do. The event names the in-game surface that answers each.
- **Check:** the legibility table (§2 item 9) names a surface for each question, and none of them depends on a deferred
  feature. (Engine limits on those surfaces are owned elsewhere: e.g. the Logbook objective badge is static, ENGINE_LAWS
  law 53; item descriptions render basic HTML, `SKYGLASS_LOOT_TABLES.md` §0.)

### P6. Diegetic progression

*"Weaving it into the story rather than telling it to the players face … We can say where we start and end and then fill in the gaps with the story and worldbuilding."*

- **Requirement:** designers write the ladder with explicit tiers, prerequisites and gates; players never see those tiers
  as numbers. Each rung is expressed in the world instead:
  - **the prerequisite is an object in the fiction** (a chart, a lantern, a key, four shards), not a level or a flag;
  - **places read as deeper or more dangerous** as the rungs climb (the shore → the lower hull → the sealed archive →
    the fortress → the hall beneath it);
  - **enemies, dialog and descriptions signal the tier** (who guards it, what they say, what the item's story line implies);
  - **the finale is foreshadowed from the first rung**, so the end the designer fixed first is visible in the fiction long
    before the player reaches it.
- **Method:** fix the start rung and the finale first; then fill the rungs between with story and worldbuilding (§3).
- **Check:** every gate has an in-world object or story beat; the ladder table (§2 item 8) gives each rung's diegetic
  signal; no rung relies only on a stated number. Plain rules text (costs, fail conditions, drop rates) is still required
  by P5 and is not a violation: the rule is that the *tier* is told by the fiction, while the *mechanics* are told plainly.

## 2. The event sheet: what a new event must define

A new event's design doc carries these sections, in this order. Skyglass's version of each is in
`SKYGLASS_EVENT_MAP.md` (section noted).

1. **Start and end** (P6). One paragraph each: the entry rung (what the player first finds, and where) and the finale
   (what it is, what it consumes, what it pays). Written first.
2. **Pillars and content nodes** (P1). Each node: kind (dungeon, battlepyramid run, special quest, side run, finale), entry
   cost, party size, limits (repeatability, attempt caps, once-per-player drops), and what it pays. *(Map §1.)*
3. **Currencies and the source → sink table** (P2). Every event item: sources with rates, sinks, tradeability, and whether
   it is an event currency or an export. *(Map §4.)*
4. **Flow graph** (P1). A Mermaid graph: nodes, drop edges, spend edges. *(Map §3.)*
5. **Gates and unlocks** (P3). Every gate: what opens it, which engine mechanism carries it (cite the owner: entry items,
   item-started quests, picks), and its in-world object.
6. **Alternative routes per key outcome** (P4). A table: outcome → routes (with rates) → whether trade is a route.
7. **Tradeability rules.** Per item: tradeable or not, and why. Default stance: progression inputs trade (trade is the
   pity for unlucky or time-poor players, RUL-2026-11-02-104 item 2); proof-of-achievement and once-per-player rewards
   do not.
8. **The progression ladder** (P3, P6). The rung table of §3, with each rung's diegetic signal.
9. **Legibility surfaces** (P5). Which surface answers each of the four questions: item descriptions; quest and run
   descriptions; NPC dialog and closing lines; the Logbook (quest log); titles, badges and achievements; variants listed on
   their base weapon. Mark any surface that is deferred or blocked upstream. Each event also writes a **journal**: a
   weekly roadmap quest whose entries count as the player plays, one page per weekend (pattern, engine limits and
   template: `docs/design/EVENT_JOURNAL.md`, RUL-2026-11-05-120).
10. **Pacing targets.** Expected hours and clears per player type, rates per weekend for each headline reward, clear-rate
    targets per node, and the pacing of the finale's inputs. Values are the director's ([[D-reserved-dauntless]]); see §8 Q1.
11. **The finale.** It consumes the event's currencies (at least one from each pillar), it pays back into the event's shared
    containers, and a loss is stated plainly.
12. **Story bible.** Canon, voice, and a "what each surface reveals" table in play order that ends at the finale.
13. **Gaps.** The §5 anti-pattern scan, run against the sheet, with each finding either fixed or ruled.

## 3. The progression ladder

### 3.1 How to build it

1. **Fix the start.** The first rung is reachable with nothing: no item, no rank, no prior event. Name the place and the
   first object the player is handed.
2. **Fix the end.** Name the finale, its entry object, and the pillars that feed that object.
3. **Write the rungs between.** Each rung is one row:

| Field | Meaning |
|---|---|
| Rung | the designer's tier number. Never shown to players |
| Prerequisite object | the in-world item or story beat that is the gate |
| Produced by | the earlier rung(s) or node(s) that pay it, with rates |
| Place | where it happens; it must read as further or deeper than the rung below |
| Threat | who and what the player faces; it must read as stronger than the rung below |
| Diegetic signal | the story line, dialog or description that tells the tier without a number |
| Foreshadows | what this rung shows of the finale |

4. **Branches** (gambles, side runs, cosmetic layers) are listed after the rungs, each with the rung it hangs off and the
   rung it pays into.

### 3.2 Signals, strongest first

1. **The object is the prerequisite.** A chart to a buried chest; a lantern that "points home"; four shards that are "her
   invitation". The player knows what they can do by what they hold.
2. **The place deepens.** Shore, lower hull, sealed decks, the fortress, beneath the fortress.
3. **The threat escalates and is named.** The crew, then the officers, then the commander, then what was behind him.
4. **Dialog places the player.** "I defeated you once!"; "There is room in the glass for one more."
5. **Description voice.** One line of story on every item, then what it does (`SKYGLASS_LOOT_TABLES.md` §0).
6. **Weakest: stated labels.** Rarity frames, difficulty stars, level ranges. Allowed only as a back-up to a stronger
   signal on the same rung, never as the only one (see §8 Q6 for the stars Skyglass already ships).

## 4. Design checklist

Run it on the event sheet before any manifest is built. Each line is yes/no; a "no" is fixed or ruled.

**Structure**
- [ ] The start and the finale were written first (sheet item 1).
- [ ] Every node has an outgoing edge to another node, or is named as a leaf.
- [ ] Every node but the entry has an incoming edge.
- [ ] The flow graph and the node table agree.

**Economy**
- [ ] Every event currency has at least one sink inside the event.
- [ ] Every one-source or one-sink currency is marked deliberate, with the reason.
- [ ] Every container states its contents and rates in its description (generated from the same table).
- [ ] Exports (ryo, exp, game-wide materials, cosmetics) are named as exports.
- [ ] Every sink is reachable by every player it is offered to (no hidden rank, profession or crafting gate), or the gate is stated and trade is the route around it.

**Agency**
- [ ] Every key outcome has two or more routes, at least one not trade.
- [ ] Every completion pick offers options with different jobs (no option strictly dominates another; RUL-2026-11-04-114 is the worked example).
- [ ] Risk choices (press on, steep, lockers) state what is lost on a fall.
- [ ] No choice locks the player out of another approach next time.

**Progression and diegesis**
- [ ] The ladder table exists, with every rung's prerequisite object, place, threat and signal.
- [ ] Every gate has an in-world object or story beat.
- [ ] The tier is legible from the fiction on every rung, not only from a number, frame or star.
- [ ] The finale is foreshadowed from the first rung, and the story bible's "what each surface reveals" table ends at it.
- [ ] The finale consumes at least one input from each pillar and pays back into shared containers.

**Legibility**
- [ ] Each of the four questions (done / now / ahead / what is this) has a named in-game surface.
- [ ] No legibility surface depends on a deferred or upstream-blocked feature, or a fallback is named.
- [ ] Rewards visible before they are obtainable (variants on a weapon, locked picks) have a live source or say "later".

**Pacing and limits**
- [ ] Pacing targets per player type are written and were set by the director.
- [ ] Engine limits on repeatability are checked against the event's cadence (owner: the skill references and the task's source pin).

## 5. Anti-patterns

| Anti-pattern | What it looks like | Fix |
|---|---|---|
| **Dead-end drop** | an item with no sink, or a reward visible with no source | give it a sink, cut it, or label it "coming later" |
| **Leaf posing as a pillar** | a run whose only outputs are exports | add an event output (a ladder chart, a finale input) or name it as a leaf |
| **Single-route outcome** | one place makes a gate item | add a second non-trade route, or rule it deliberate and make it tradeable |
| **Opaque gate** | a prerequisite stated as a number or a hidden flag; a rank or crafting gate the item never mentions | make the gate an object; say any hard gate in the item text |
| **Reward that matters to nobody** | an untradeable item that needs something the player may lack; strictly dominated pick options | make it tradeable, change its condition, or reweight the pick |
| **Starved node** | a sink so attractive that the node it competes with is never run | accept it by ruling, or rebalance so both are worth doing |
| **Label instead of story** | "Level 1 / Level 2", tier numbers in names | signal the tier through object, place, threat and dialog |
| **Unforeshadowed finale** | the final villain first appears at the final gate | seed them in early surfaces: item story lines, dialog, scenes |
| **Untraceable progress** | no surface tells the player what they have cleared | titles, achievements, a completion quest, or a ledger item |
| **Restated owner** | design docs copying engine facts or another doc's numbers | cite the owner; derived maps say they are derived |

## 6. Skyglass as the reference

The full map is `docs/design/SKYGLASS_EVENT_MAP.md`: nodes and costs (§1), containers (§2), the flow graph (§3), the
source → sink table (§4), the ladder (§5) and gaps (§6).

### 6.1 Skyglass on the ladder

| Rung | Prerequisite object | Place / threat | Diegetic signal |
|---|---|---|---|
| 0 (start) | none | the Wreck on the shore; the crew still at its posts | Wreck Sighted: "The Ghost Ship has finally come down" |
| 1 | Tide Chart, Watch Roster | the lower hull at low tide; the Deck Warden's post | the tide opens a breach; the roster has your name on it |
| 2 | Chart of the Buried Cache | a chest buried in the sand | the crew were people; they buried things before the fall |
| 3 | Foundry, Archive, Watch charts | the works, the sealed archive, the helm; Warden, Sealwright, the Captain | sealed reports name Crownhold; "I wear his mask" |
| 4 | Reliquary Seal, The Last Heading | the reliquary behind the Sealwright; the night of the crash | the echoes the Core could not hold |
| 5 | Lastlight Lantern | Crownhold; the Crowned Captain | the last signal, still burning; "its light points home" |
| 6 (end) | four shards | the hall of glass beneath Crownhold; Sayo and the Silence | "The four shards are her invitation"; every pane holds a face you cut down |

Branches: steeping (rung 4 → tainted rung 4, paying Rot and a better Lantern chance), the Haul (off rungs 3 and the
Wreck, paying the Ledger shard), the Archive Chart Case (the sustain loop from rung 3 back into rungs 3-5), the cosmetic
layer (tokens).

### 6.2 What worked

- **One spine, many feeders.** The chart ladder is a single readable spine from the shore to Crownhold, and the finale
  draws one shard from each pillar (Wreck, Crownhold, Epic runs, the Haul).
- **Objects are the gates.** Every rung's prerequisite is a held item with a story line; the director's "Level 1 … a chart
  that leads to some buried chest" and "Level 100 … 4 fragments that unlock a hidden area" are both literal in the build.
- **Picks give agency at every completion,** with each option given its own job (Hoard all-rounder, Coffers for gear,
  Tokens for skins: RUL-2026-11-04-114). Common runs offer the other common chart, so the commons feed each other.
- **Risk is a choice:** press-on rooms, steeping (with a refund on a mis-tap), Haul lockers, the Archive's break-the-seal
  fight, Crownhold's protocol routes.
- **Multiple routes for most key outcomes:** the Lantern has four sources; tainted charts three plus steeping; Core Rot
  five; Skyglass Tokens six. Progression inputs trade, so trade is the pity (RUL-2026-11-02-104).
- **Every item explains itself** (`SKYGLASS_LOOT_TABLES.md` §0): rates, rolls and the rules footer are generated from the
  same tables as the caches and checked by `scripts/skyglass_check.py`.
- **"One home per item"** (loot tables header) keeps the source → sink table small and traceable.
- **Tuned against player types.** Casual, Dedicated and Hardcore weekends (RUL-2026-11-01-096 item 4) and per-node clear
  targets measured in the offline harness before build.

### 6.3 What to improve

Each item is a gap from the map (`SKYGLASS_EVENT_MAP.md` §6). They are recorded for future events; none is a change to
Skyglass unless the director rules it.

- **Foreshadow the finale (G1).** Sayo, the Mother Glass and the Silence appear nowhere before the shards. The story
  bible's final chapter (RUL-2026-11-01-094's destination) is unwritten, and the bible still ends on the crown breaking.
  Future events seed the finale in rung-1 and rung-3 surfaces. The Skyglass fix is proposed, not applied, in
  `docs/design/SKYGLASS_STORY_AUDIT.md` (review only, awaiting the director).
- **Give players a trace (G2, G3).** Titles and Walked Every Deck are deferred; the Crownbreaker variant shows with no
  source. Future events need a progress surface that works today.
- **Do not starve a node (G4).** Steeping consumes almost every Epic chart, so the Epic runs are rarely played.
- **Second routes for gate items (G5).** Keel (party Wreck only), Crown (Crownhold only) and the very first chart
  (party Wreck only, since the solo pyramids were not added) have trade as their only second route.
- **No hidden crafting gate on sinks (G6).** Filament → Crystal and Fragment → Crown need a crafting rank.
- **Check engine limits against cadence (G7).** The 100-attempt lifetime cap meets a weekly event.
- **Keep owners current (G10).** Loot tables §2 and §1 lag the editor and the uber; the uber has no repository design doc.

## 7. Using this framework

- **Event design** is routed here from `docs/00_INDEX.md` task routing. Build-time rules still route as before (validate,
  `skyglass_check.py` for Skyglass manifests, the skill references for each entity).
- A multi-session event uses a content workstream (`docs/workflows/CONTENT_WORKSTREAM.md`); the event sheet is its design
  input, not a replacement for its roadmap or brief.
- A new event's rulings name this file only for structural decisions; numbers and canon go to the event's own docs.

## 8. Open questions for the director

None of these is decided here; each is a placeholder until ruled.

- **Q1. Standard pacing targets.** Should every event use Skyglass's player types (Casual ~3 h, Dedicated ~10 h, Hardcore
  ~25 h a weekend, RUL-2026-11-01-096) and its finale pacing (Casual ~4 weekends, Dedicated 1-2, Hardcore under 1)?
  Standard clear-rate bands (base ~80%, hard variant ~55%, finale 10-20% skilled)?
- **Q2. Minimum routes.** Is "two routes, one not trade" the rule for every key outcome, or may trade alone be the
  second route (as for the Keel and Crown shards)?
- **Q3. Progress surface.** Which in-game surface should carry "what have I done" for events while titles and
  achievements are deferred or blocked upstream (a completion quest, a ledger item, titles once the fix lands)?
  *(Proposed answer: the event journal, `docs/design/EVENT_JOURNAL.md`; its Logbook bars carry "what can I do now"
  and "what have I done" for the weekend. Not ruled.)*
- **Q4. Crafting gates on sinks.** Does RUL-2026-11-01-096's "no crafter intermediaries" apply to every event sink, or
  only to finale inputs?
- **Q5. Starved nodes.** When a gamble consumes the input of a node (steeping vs the Epic runs), is that acceptable by
  default, or must both stay worth doing?
- **Q6. Stated tier labels.** Skyglass prints difficulty stars on every chart (RUL-2026-10-31-074 item 3). Under P6, do
  stars stay as a back-up signal, or should future events drop them?
- **Q7. Skyglass follow-ups.** Should the G1 foreshadowing (story bible final chapter; seeding Sayo in earlier surfaces)
  and the G10 doc drift be scheduled as Skyglass work?
