# A clean levelling experience, levels 1-70: design proposal (draft 1)

**Status: PROPOSAL.** Nothing here is approved content. Story frame, names, level windows, reward values and publishing are the director's decisions (CLAUDE.md section 10). Reward amounts are deliberately left as placeholders.

- **Evidence:** `LEVEL_1_70_INVENTORY.md` (engine, activities, pyramids) and `sweep/` (every captured quest with requiredLevel ≤ 70, classified; reproducible with `python3 -I sweep/build.py`).
- **Tier labels:** CAP = live record (capture), SV = source-verified at TheNinjaRPG@3314d122, PROPOSAL = new.

## Director direction so far (2026-11-04)
- Make the early game as engaging as the endgame fights. Focus on a PvE loop; the Skyglass dungeon + pyramid model is sound.
- Look at the whole 1-70 journey, not just pyramid levels. There must be a thread that pulls players along while they level.
- Rework Howling Hills, Skychain Monastery and The Drowned Fleet to fit the new structure.
- Stories must be original and fit Seichi: an Edo-era-flavoured fantasy ninja world, neither real Japan nor the franchise.
- The spine is **village-neutral**.
- Tie into the existing mission story spine. Rename and re-premise the first-pass "Five Roads / Ashen Ledger" idea.
- Ground the mundane world.
- Steer players into professions and other systems with quests, including dailies such as "do X gathering".

## 1. What the sweep found (CAP, 235 visible + 131 hidden quests with requiredLevel ≤ 70)

1. **The thread stops at 30.**
   - Getting Started → Road to Genin → Genin Trials 1-9 → the Kuroganekai GENIN pyramid → The Chunin Exams is a real chain, and each Trial unlocks a repeatable Case/Blacksteel Contract.
   - After that, nothing chains until the Jonin Exam at 57.
2. **Levels 40-49 have zero visible quests of any kind unlocking.** The only candidate is The Drowned Fleet, which is hidden.
3. **Levels 10-30 have no system content.**
   - All 61 profession quests open at level 1, gated by profession rank, with no tutorial.
   - Crafting, pets, cooking and clans have no onboarding quest anywhere. Farming has one, at level 1.
4. **No visible quest typed "daily" actually repeats** (all are `retryDelay: none`, `maxCompletes: 1`).
   - The only visible quests that reset daily are four pyramids plus one dialog quest.
   - The real daily loop (8 profession supply turn-ins, Tower of Endless Night) is hidden. There are no weekly quests.
5. **The Mission Hall pool is thin and paid on two scales.**
   - C-rank appears at 20; B-rank has 3-6 quests; A-rank appears at 50.
   - New narrative missions pay about half the XP and a tenth of the ryo of legacy peers.
   - Many C missions are village-locked: at levels 10-20 Hyorin, Akikaze and Syndicate players have none, which makes **Path To Chunin impossible to finish for them**.
6. **The objective tasks that suit steering and dailies have never been used at ≤ 70:**
   - `herbs_gathered`, `items_crafted`, `creatures_hunted`, `stats_trained`
   - `*_experience_gained`
   - the completion counters (pyramids, raids, stories)
7. **Breakage to clean up regardless of design:**
   - Genin Trials 9 and the GENIN pyramid are gated at level 10 behind level-24 content.
   - Shattered Sakura's level order is inverted.
   - Three quests have a start date after their end date.
   - Eight expired quests are still visible.
   - A staff test stub is visible (Salt Gate Phantom).
   - Path of a Shinobi exists twice.
   - Hyorin's god is named Okami in one place and Kuraokami in another.
   - Kill the Creator pays nothing.

## 2. Seichi as written (canon), and the grounded layer it needs

### Canon to build on (CAP quest text; SV seed text)
- **The case desk.** An anonymous, village-neutral case officer ("they") runs a case file, an evidence vault and a contract board. They are the player's patron from level 10 to 30.
- **Kuroganekai, the Order of Black Steel.** A syndicate, not a village. Its trademarks:
  - **Blacksteel:** dark metal with violet veins, cold as steel should not be.
  - **Violet energy residue.**
  - **Iron Aberrations and Obelisk anchors.**
  - **Stolen conductors** feeding power-hungry machinery.
  - **Rumoured altered-bloodline experiments.**
  - **Smuggling** through Wake Island's free port, "beyond village law."
  - **Theft routes** that bend around one guarded region.
  - **Its commander is promised three times and never named.**
- **Global ANBU** (HQ on Wake Island, sector 222): the cross-village authority for higher-level arcs.
- **Deep history:**
  - the Great Collapse, ended by the Five Blades of Balance
  - a Fifth Element (Void Flame / Null Chakra) sealed before Seichi's founding by the first Kage of the five villages, at a forgotten altar called the Heart of Balance
  - the Great Seichi Wars, in which large villages absorbed and in one case massacred small ones
  - the Mortal King and the Monarch Powers (Jonin Exam)
  - Divine Fragments (Echoes in the Gust)
- **Political layer:** feudal lords, a daimyo, Hoshikage province, Kaiyo (a neutral port city), and Shinobi University with the Esakanki Medical Hospital.
- **Everyday life already in the text:**
  - Ramen shop, village depot, storage house
  - Caravans and trade routes, a wandering salesman
  - Wire artisans, clay sculptors, mining, herb farming
  - D-rank chores (a broken gate, koi ponds, lost animals)
- **Tone of the newer content:** restrained procedural noir (ledgers, seals, manifests, evidence, dry humour) with moral ambiguity about villages and duty (the Skychain Abbot, the Grounded Spiral). The new spine keeps this tone.
- **Avoid in new text:** franchise-derived terms the old content uses ("Fire/Wind/Water Country", "Land of Iron", tailed beasts, Namikaze). Rank titles are game mechanics and stay.

### The grounded layer (PROPOSAL)
The rule: every mechanic the player touches has a reason to exist in the world. The mundane layer explains why ninja villages earn ryo, why there are contracts, and why professions matter to a shinobi.

| World fact (proposed) | Explains | Used by |
|---|---|---|
| **Lords own the land; villages sell protection.** Provinces are held by lords under a daimyo, and a village is a military house paid by contract. Mission Hall fees are lords' and merchants' money. | Ryo income, contracts, why missions vary by region | Mission Hall flavour, contract boards |
| **The post roads.** Highways between provinces carry waystations (inns, stables, a ramen stall), checkpoints that check **road passes**, and courier relays. | Travel, escort and courier work | Chunin-era contracts |
| **Road passes.** A sealed paper issued by a lord's office; forging one is a serious crime. | A concrete crime for the Order to commit | Act I evidence |
| **Wayside shrines** to the five patron gods mark each province border; travellers leave ryo and rice. | Shrines as war objectives; a reason for people on the roads | Dailies, flavour |
| **Guilds.** Smiths and wire-workers, clay and kiln houses, herbalists who supply Esakanki, beast-hunters paid by bounty. A shinobi may apprentice to one trade. | The single-occupation rule (one trade at a time, switch every 3 days, SV) | Profession onboarding |
| **The hospital runs on herbs.** Esakanki and every village hospital buy gathered herbs. | Gathering, medical | Gathering onboarding, medical dailies |
| **Blacksteel needs a smith to read it.** Only a guild smith can tell where a bar was smelted. | Crafting matters to the story | Crafting onboarding |
| **Beasts follow the roads.** Wolves and aberrations prey on caravans; bounties are posted at waystations. | Hunting | Hunting onboarding, Howling Hills |
| **The seasons are real** (the game follows the real month, SV `utils/time.ts:171-197`): rice planting, the rainy season, harvest, winter roads closing. | Event timing | Seasonal event hooks |

## 3. The spine, levels 1-70 (PROPOSAL)

Every chapter has the same shape as the Genin Trials:

> story step → unlocks a repeatable contract → … → **capstone pyramid** (first clear advances the story; daily repeats pay the band's reward) → **rank exam or chapter close**

The case officer remains the thread through levels 10-57. Global ANBU takes over at Jonin.

### Chapter 1, Academy and Genin (1-30): exists; fix, don't rewrite
- **Fix level windows into chain order:**
  - Genin Trials 9 and the GENIN pyramid move to the Trials' end (about 24-30).
  - Genin Trials 8 should be a starter, not an event.
- **Unhide Blacksteel Tides** (level 24-30, the case officer's Chunin recommendation). Rewrite **The Chunin Exams** opening to acknowledge that recommendation.
- **Add the system onboarding steps here** (section 4); this band has none today.
- Make **Path To Chunin** completable for every village (village-neutral C missions at 10-20).

### Chapter 2, "The Violet Road" (Chunin era, 30-57)
- **Premise:** the stronghold the Genins hit was a depot, not the heart. Blacksteel still moves.
  - It travels by caravan on the post roads under forged road passes, over a sealed mountain route, and by sea to Kaiyo.
  - The case officer, now running a field office out of a waystation, sends their new Chunin to follow the freight.
- **The question carried through:** who commands the Order, and what is the blacksteel for?
- **Patron:** the case officer. **Antagonist:** Kuroganekai's quartermaster network, and finally the commander (named at the end of Act III).
- Alternative titles: "Blacksteel Roads", "The Freight Ledger".

**Act I, Waystation (30-38)**
- **Story steps:**
  1. Report to the field office at a mountain waystation.
  2. A checkpoint clerk notices a road pass whose seal is too perfect.
  3. The forger's workshop points to a caravan line that only ever travels at night.
  4. The night caravan's drivers say their cargo is guarded by "the wolves that don't sleep."
- **Contracts unlocked:**
  - **Checkpoint Inspection** (detect forged passes)
  - **Night Caravan Escort**
  - **Pass-Forger Bounty**
- **Capstone: Howling Hills** (re-banded 33-40, scaled)
  - The wolves of the pass are being driven. The Monster of the Moon is an Iron Aberration grown from beast stock, with violet veins under its fur.
  - The three existing branch paths stay.
  - First clear recovers a quartermaster's tally that names the next leg: the high route over Skychain.

**Act II, The Sealed Route (39-47)**
- **Story steps:**
  1. The high courier route is closed by the Skychain order, which "answers to no rank and no village" (canon).
  2. The order is split: one faction wants the route open.
  3. The faction keeping it sealed is being paid to let one courier line through. That line is Kuroganekai.
  4. The Abbot's grievance, that villages send children across storms and call it duty, is real. The Order exploits it.
- **Contracts unlocked:**
  - **Mountain Courier** (the open faction's mail)
  - **Bell-Tower Watch**
  - **Debt-Note Recovery**
- **Capstone: Skychain Monastery** (re-banded 41-48, **scaled**)
  - The Challenge of the Three Bells stays, along with its existing "yields by the monastery's own law" ending.
  - The Abbot reopens the route and gives you the courier-line ledger, which ends at the sea: Kaiyo.

**Act III, Tide at Kaiyo (48-56)**
- **Story steps:**
  1. Kaiyo is a neutral port where no village has authority.
  2. The Drowned Fleet, tide-ninja raiders, are the Order's sea haulers, paid in blacksteel.
  3. Recovered manifests show the freight's destination: a site "where the old altar was."
- **Contracts unlocked:**
  - **Harbour Patrol**
  - **Wreck Salvage**
  - **Manifest Interdiction**
- **Capstone: The Drowned Fleet** (unhidden, repeatable, re-banded 49-56, scaled)
  - Tidelord Kaisei is defeated. The flagship's strongroom holds the commander's orders, which finally **name the commander**. The name is the director's choice.
  - It also names the cargo's purpose: the conductors and blacksteel are parts of an engine meant to draw on something sealed.
- **Chapter close:** the case officer takes the file to Global ANBU. Their last line hands the player up to the Jonin Exam.

### Chapter 3, "The Fifth Seal" (Jonin era, 57-70)
- **Premise:** the Jonin Exam (existing; Mortal King, Monarch Powers) now has context.
  - The Order's engine was built to draw on the Fifth Element sealed at the Heart of Balance.
  - Whether the commander serves the Mortal King, or wants the power to stand against him, is the chapter's turn.
- **Patron:** Global ANBU (canon), with the case officer as a recurring adviser.
- **Contracts unlocked:** squad contracts:
  - **Foundry Raid**
  - **Conductor Recovery**
  - **Engine Survey**
- **Capstones:**
  - New pyramid **~60-64**: the blacksteel foundry.
  - New pyramid **~66-70**: the engine site at the Heart of Balance. Its close hands into the existing 70+ endgame (Subaku, the Tower, Sotek).
- **Clean-up:** fix the duplicate Path of a Shinobi and the Hyorin deity name.
- Alternative titles: "The Heart of Balance", "Null Chakra".

### Capstone ladder after the change
| Band | Capstone | Change |
|---|---|---|
| 24-30 | Kuroganekai GENIN | Window fix |
| 30-36 | Kuroganekai CHUNIN | Keep as Act I's first fight, or fold into Act I. Director call. |
| 33-40 | Howling Hills | Re-band; re-theme the Monster of the Moon; fix the Student-rank-over-cap enemies |
| 41-48 | Skychain Monastery | Re-band; **scale**; lift the 10-lifetime cap |
| 49-56 | The Drowned Fleet | Unhide; repeatable; re-band; scale |
| 60-64 | New: blacksteel foundry | New |
| 66-70 | New: engine site | New |

Under both "scaled" and "fixed" capstones, the window and the difficulty must hold at the **bottom** of the band. That is what the sim measures first.

## 4. Steering players into systems (PROPOSAL)

**Design constraint (SV):**
- A player holds **one occupation** (gathering, hunting or crafting) and can switch every 3 days.
- So onboarding offers a **choice of trade**, not three mandatory tutorials. The non-chosen trades stay available as optional side steps.
- Medical needs Genin. Pets are rank-capped by owner rank.

| Level | Spine hook (story reason) | System | Objective (unused task today) |
|---|---|---|---|
| 10 (Genin) | The Science Building's bloodline check, mentioned in Road to Genin | Bloodline roll | Verify an objective can observe a roll; `bloodline_collection` exists, behaviour unread |
| 11 | The case officer: "Pick a guild. A shinobi who can only fight is a shinobi who waits for other people." | **Choose a trade** | Branch dialog → one of the three rows below |
| 12 | A blacksteel shard needs a smith to read where it was smelted | Crafting | `items_crafted` ≥ N |
| 12 | The escort's wounded need herbs from Esakanki's supply | Gathering | `herbs_gathered` ≥ N |
| 12 | A beast is following the transport route | Hunting | `creatures_hunted` ≥ N |
| 14 | The waystation cook pays in meals for fresh produce | Farming → cooking | `plants_harvested`, cooking |
| 16 | A Bondkeeper's creature tracked the aberration's scent | Pets | Adopt/feed (verify an objective exists) |
| 18 (Genin) | Raid-site wounded at the hospital | Medical | `medical_experience_gained` |
| 20 | Contract work goes faster with a crew | Clan | Join a clan (verify an objective exists) |
| 30 (Chunin) | Field office: Act I | Village outside the walls, PvP opt-in | Existing gates |

## 5. Grind loops per band (PROPOSAL)
For the time between story steps, each band should offer three repeatable lanes:
- **Contracts** (story-flavoured missions, unlocked by the spine)
- **The Field Office board** (dailies)
- **The band's capstone** (daily pyramid)

Training and the Mission Hall sit underneath all three.

### Field Office board (dailies)
- Each band posts three dailies. A player does any of them, and each has a separate reward:
  1. **Duty:** a combat count, e.g. `c_missions_total` / `b_missions_total`, `arena_kills` or `random_encounter_wins`.
  2. **Trade:** one per occupation (`herbs_gathered` / `creatures_hunted` / `items_crafted`). Only the player's own trade is doable, so every occupation has a daily.
  3. **Discipline:** `minutes_training` or `stats_trained`.
- **Weekly:** clear the band's capstone N times (`battle_pyramids` completion counter), plus one contract set.
- **To verify in source before building:** that `*_gained` / count tasks baseline at quest start, so a daily counts today's work and not the lifetime total.

### Mission Hall
- Village-neutral C missions at levels 10-20.
- B-rank depth at 30-50 and A-rank depth at 50-70.
- One pay scale for missions of the same rank. Which scale is the director's call.

### The hidden daily economy
The 8 profession supply turn-ins (200-300k ryo, hidden) either become the Trade dailies or are reconciled with them.

## 6. Measuring it: what the sim answers
It runs three player types (casual about 1 h/day, engaged about 3 h/day, optimal) through the proposal and through **today's** live content. For each it reports:
- Time per chapter and act. The longest stretch with no new story step, unlock or system.
- XP sources by band: training, missions, contracts, dailies, capstones. Whether each reward is meaningful when it lands (as a fraction of the band's XP need).
- Capstone win rate and fight length at the **bottom** of each band, using the real combat engine (the Skyglass harness), with player numbers calibrated from evidence.
- Rank-up timing: when the 9th and 10th jutsu slots and the C, A and S letter ranks arrive.

## 7. Decisions for the director
1. **Chapter names and the commander's name.** Proposed: "The Violet Road" (30-57) and "The Fifth Seal" (57-70). The commander is unnamed until Act III.
2. **Scaled or fixed capstones.** Scaled widens a capstone's useful window; fixed is what Skyglass uses (RUL-2026-10-31-073).
3. **Kuroganekai CHUNIN:** keep it as a separate fight or fold it into Act I.
4. **Mission pay scale:** legacy (about 450 XP / 15k ryo for C) or narrative (about 230 / 1.5k), for each rank.
5. **Engagement targets**, for example:
   - a story step at least every N hours of play
   - capstone win rate 60-80% at the band floor
   - no stretch longer than X days without a new choice
6. **The hidden daily economy** (profession supply turn-ins): make it the Trade dailies, keep it separate, or leave it hidden.
7. **Evidence:**
   - live game-setting multipliers (training, regen, mission/battle/jutsu XP)
   - real low-level player records at about levels 10/30/50/70
   - low-level battle logs
   - a capture of the AI rule profiles used by the spine and the three capstones (about 144 missing)
