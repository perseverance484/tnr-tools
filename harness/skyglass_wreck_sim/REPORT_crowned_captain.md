# The Crowned Captain: solo boss fight, offline tuning (2026-10-28)

The Crowned Captain is Crownhold's last fight (D5.BOSS, live id `7QofodAiUwIoM-voiA2p6`). This report tunes him for one
average endgame player and exports a build spec.

- **Engine:** the game's combat engine at `c86f43f4`, in memory, with the live damage settings.
- **Requests:** zero live requests and no credentials.
- **Specs:** `crowned_captain_spec.json` and `crownhold_spec.json` (the three division commanders).
- **Raw results:** `results/crowned_captain_tuned.json` (60 seeds with dodging, 60 without),
  `results/crownhold_commanders_solo.json` and `results/crownhold_chain.json`.
- **Sample traces:** `results/crowned_captain_trace_seed3.txt` and `..._seed5.txt` (regenerated on the library version).
- **Scripts:** `engine/crowned_captain.ts`, `engine/crownhold.ts`, shared code in `engine/cclib.ts`.
- **Inputs:** `data/crownhold_inputs.json`, built by `tools/build_crownhold_inputs.py`.

Nothing here is pushed or authorised for the live game. Report 4 (below) is current. Reports 3, 2 and 1 follow it and are
superseded where report 3 differs; their `cc-*` placeholder set pieces are replaced by library records.

## Report 4 (current): Crownhold tuned for the chain (RUL-2026-10-28-013)

The director's ruling sets three rules:
- Crownhold carries HP between fights with no refill.
- The Crowned Captain and the three commanders are never fought alone.
- They are tuned for the whole run.

The targets:
- Every route clears.
- Healing Rite is highest (about 55-60%).
- War Rite and clean are in between (about 40-50%), each with its own trade-off.
- The alarm route is lowest (about 30-35%).
- The Crowned Captain stays the hardest fight, and his fight lasts 20 rounds or less.

**Headline: the Healing Rite route clears (60-80%) and the Crowned Captain targets are met: hardest fight, at most 19
rounds. Clean (12.5%), alarm (0%) and War Rite (0%) miss their targets and cannot reach them by tuning the four bosses
alone.**
- The regular fights are fixed input. They cost about 45% of the player's HP before the Crowned Captain on the clean
  route, and nearly all of it on the War Rite route.
- With the bosses at any setting, those routes reach the Crowned Captain with 1-15% HP.
- The quest and regular changes that would meet the targets are below, as proposals for the director. They are not
  built into the specs.

### What changed before tuning

- **Shared library.**
  - Merged `5f6c3edb`: Lines as a fan, Scatter covering both halves, blast cooldown 2, enemies-only rows, a lock that is
    not shared.
  - Replicant Zero's Seal Lines blast gets cooldown 2 from the library, so he needs no change of his own.
- **Virtual clock** (`seedClock`/`tickClock`) from the Wreck agent's `sim.ts`, plus seeded id entropy in every fight.
  Same-seed fights are identical on a busy machine.
- **Pet support** (`assembleFloor({ pets })`, `model.ts` `petFor`) from the same source, plus the Wreck agent's pet
  placement fix from `c301632b` (only its `sim.ts` part: every pet is cleared to -1 before being placed again).
  - Checked: the same seed run twice gives the same trace, pet positions included.
  - With one pet per fight the fix changes no result: the trace matches the run from before the fix.
- **Fixed input: Crown Archivist** (D3.REG1, `LZiunyinw9ScK3mh9HiR2`).
  - It runs at the hunts harness tuning: pools 2, 2 damage rows (`params.regs`). Crownhold does not retune it.
  - It now costs a median 13.6% HP. At live stats it cost 1.2%.
  - If Crownhold should not carry the hunts tuning, it needs its own copy of the record.
- **Ward of Command** (`lib-ward-of-command`) is not used by any Crownhold fight, so the hunts INHERIT fix does not
  apply here.

### Player model (stated assumptions)

- **The same average endgame player as before.**
- **One pet.** It is a modelled mid-rank companion (`model.ts petFor`, shared with the Wreck harness):
  - for a JONIN owner, pet rank 5 at level 30;
  - half that rank's stat caps;
  - COMMON ASSAULT species, no passives, no pet jutsu, the engine's default AI.
  - Pets join QUEST battles. Each fight's pet starts fresh.
  - What it does: it deals 0.2-0.8% of a boss's damage, but it draws the regulars' attacks. A D2 regular costs about
    1% HP with it, 3% without.
- **The player reads each new telegraph with probability 0.85** (`--read 0.85`; one roll per new marked set, from its
  own seeded stream, so the combat sequence is unchanged).
  - A player who reads every mark takes no set-piece damage, and the only way to lose is running out of HP.
  - Then the Healing Rite route (full HP at every boss) clears about 100% and every other route far less, and no
    tuning puts Healing at 55-60% with clean at 40-50%.
  - Misreads give the set pieces a risk that does not depend on HP carried, which the targets need.
- **The chain:** a loss ends the run, and nothing regenerates between fights. Chakra and stamina carry too.

### Changed stats (shipped in `crownhold_spec.json` / `crowned_captain_spec.json`)

| Boss | Pools (before → now) | Damage rows (now) | Other changes |
|---|---|---|---|
| Crown Armsmaster (D2) | push/272 2.5 → **1.25** | **−50%** (one decreasedamagegiven row) | Opening: in round 1 he casts Sovereign Fetters (stun, seal), then the Racks Fall (Scatter A) mark, so the stunned player cannot step out. The War Rite's stun immunity is the answer to this opening. |
| Replicant Zero (D3) | 3 → **1.25** | **−90%** | none; the library gives his blast cooldown 2 |
| The Second (D4) | 3 → **2** | **−15%** | none |
| The Crowned Captain (D5) | report 2: 5 → **3** | +25% (unchanged) | See the list below. |

**The Crowned Captain's other changes:**
- **The Crown's Will** (his own record):
  - It now lasts 7 rounds, not 99.
  - It now has +50% damage plus two +100% damage rows (×6 in all) and keeps its +25% stats.
  - The duel phase is now the lethal stretch: a misread Crownfall or a landed Final Command kills.
- **Phase 2:**
  - It now uses only the design's moves: Recall, Command Absolute, Stolen Form, Extermination Order, Countermand.
  - The Scorching Rend / Devouring Grasp fillers are dropped.
  - Omen: Lines (Crownfall) is laid after Recall. Extermination Order now comes about once per phase, not twice.

**Per-fight tables at full HP** (20 seeds, telegraphs read with probability 0.85):
- **The Crowned Captain:**
  - wins 60%;
  - a win costs a median 24% HP;
  - every fight ends by round 19 (median 18; losses come early, rounds 7-16), inside the Kitsune limit of 20.
  - Every loss is a caught set piece: a Crownfall in the Crown's Will window, or a Shardstorm after a Command Absolute
    lock.
- **The commanders** cost a median 4% (D2), 13% (D3) and 16% (D4) HP and never lose at full HP.
- The ramp by HP cost and risk is D2 < D3 < D4 < Crowned Captain.

### The chain, real runs (`results/crownhold_chain.json`: pet, reads 0.85, pools carried)

Each boss cell: reached / HP at entry (median) / win% of those reached / HP left after a win / rounds.

| Route | Runs | Clears | Armsmaster | Replicant Zero | The Second | The Crowned Captain | Where runs end |
|---|---:|---:|---|---|---|---|---|
| clean | 16 | **12.5%** | 100% / 95 / 100% / 90 / 5.5 | 100% / 68.5 / 100% / 53 / 8 | 100% / 42.5 / 100% / 32 / 6 | 100% / **14.5** / 12.5% / 14 / 4 | Crowned Captain 14 |
| alert | 10 | **0%** | 100% / 96 / 100% / 90 / 5 | 100% / 68 / 100% / 51 / 8 | 100% / 41.5 / 100% / 29 / 9 | 100% / **13.5** / 0% / - / 3.5 | Crowned Captain 10 |
| healing | 10 | **80%** | 100% / 100 / 100% / 96 / 5 | 100% / 100 / 100% / 86 / 8 | 100% / 100 / 100% / 98 / 6 | 100% / 100 / 80% / 52 / **18** | Crowned Captain 2 |
| war | 10 | **0%** | 100% / 93 / 100% / 88 / 5 | 100% / 57.5 / 100% / 44 / 7.5 | 90% / **15** / 78% / 15 / 6 | 10% / 1 / 0% | D5 regulars 6, The Second 2, Crown Runner 1, Crowned Captain 1 |

**Notes on the table:**
- The clean summary comes from the run log. That run was killed by the shared machine's memory limit before it saved
  its per-chain detail. The other routes save after every chain.
- Healing clears 80% over 10 runs. The 20-seed full-HP table gives 60%, so the pooled rate is about 67%, a little above
  the target. I left it there; see the decision below.
- Ten runs give a ±15-point spread.

### Why clean, alarm and War Rite cannot reach their targets with the bosses alone

HP cost per fight at full HP, median (`--table`):

| Division | Regulars 1-3 | Regular 4 (rite routes only) | Commander / Crowned Captain |
|---|---|---|---|
| D2 | 1.0 + 1.1 + 1.0 | 3.7 (Duelist) | 4.3 |
| D3 | **13.6 (Archivist, fixed)** + 1.8 + 3.2 | 8.0 (Stonebound) | 13.4 |
| D4 | 1.2 + 1.2 + 1.8 | **20.0 (Crown Runner)** | 15.5 |
| D5 | 4.3 + 2.8 + 6.2 | 3.7 (Sealbearer) | 24 when he is beaten (60% at full HP) |

**Clean:**
- The regulars take about 38% at full-HP rates, and more in the chain as chakra and stamina run down.
- The commanders' 33% leaves the player 14.5% HP at the Crowned Captain.
- He is beaten from there only on a run with no misread.

**Alarm:**
- Alarm Raised (+10% damage taken for 2 rounds, push/273) changes almost nothing for a player who is dodging.
- I tried an "expected" opening strike or guard buff for each boss while the alarm is up. It made the alarm route
  cheaper, because it delays each boss's real threat. It is not shipped (`alarmStrike` stays null).

**War Rite:**
- The fourth regulars cost a further 35% (the Crown Runner alone 20%).
- The War Rite effects last 2-3 rounds.
- The player reaches the Second with about 15% HP.

### Proposals that would meet the targets (director's decision; not in the specs)

The offline estimate (`tools/compose_chain.py`) is built from the per-fight tables. It is a tuning surrogate: it
assumes a fight's cost does not depend on the HP carried, and its clean figure (18%) ran above the real chains
(12.5%).

| Change on top of the shipped bosses | Clean | Alarm | Healing | War Rite |
|---|---:|---:|---:|---:|
| none (push/273 quest data) | 18% | 24% | 59% | 0% |
| Alarm Raised +25% damage taken for the whole fight; War Rite effects for the whole fight, plus 30% damage reduction | 24% | 14% | 59% | 0% |
| plus regulars at half damage, Archivist kept at the hunts stats | 38% | 33% | 59% | 33% |
| plus regulars at half damage, Archivist included (a Crownhold copy) | 40% | 37% | 59% | 40% |

The rite routes could also restore some HP: a War Rite restoring 15-20% HP is estimated at 39-46% clears. This cannot
be expressed today: `givePools` sets HP to a percentage, it does not add to it.

**The real chain does not confirm the estimate** (`results/crownhold_chain_proposal.json`).
- With regulars at half damage and the quest proposals, real clean chains cleared **10%** (10 runs), not 38%.
  - The player reached the Crowned Captain with 30-40% HP (median 35%).
  - Nine runs in ten were lost to him there.
  - I stopped the remaining proposal routes: they cannot beat clean.
- **Why the estimate fails:** the Crowned Captain's risk is not independent of the HP carried. His caught set pieces cost
  40-100% at full HP rather than always killing.
- **Carried HP, chakra and stamina together** (12 seeds each), the Crowned Captain wins:
  - **60%** of fights started at 100%;
  - **25%** of fights started at 60%, and also at 35%.
  - Most losses come by round 4: a Crownfall in the Crown's Will window kills from 60%.
- **The next step if the director wants these targets:**
  - make the Crown's Will window a true one-shot (×12) while a clean read stays cheap;
  - then re-validate with real chains, together with the regular and quest changes above.
  - Even then, clean can only match Healing if the Crowned Captain's risk stops depending on HP, and that removes the
    Healing Rite's advantage at the last fight.
- The targets as written pull against each other here. That needs a design decision, not more tuning.

**What the targets need beyond the four bosses** (quest or regular data, owned by the director, not settled here; the estimate above did not hold in real chains):
1. **Regulars:** Crownhold's regulars at about half damage. The Crown Runner (20%) and the Archivist (13.6%) are the
   outliers; the Archivist would need a Crownhold copy.
2. **Alarm Raised:** a stronger effect that lasts the whole fight.
3. **War Rite:** effects that last the whole fight and add damage reduction.

### Other answers

- **The Second's line.**
  - "I questioned his orders for thirty years." has no shared-library cast to ride on. Every library record is shared
    (Rows A is also the Captain's Broadside mark), and the only window cast, Lowered Guard, carries the library's neutral
    line.
  - The line already appears in push/273's alarm text for him (`d4.n.boss.alert`: "I questioned his orders for thirty
    years. I never forged one.").
- **Replicant Zero's blast cooldown 2:** it comes from the library (every blast is cooldown 2 since `5f6c3edb`).
- **Library geometry: a new finding for the library owner.**
  - `5f6c3edb` builds Lines and Seal Lines on a "POINTY, odd rows shifted" grid.
  - The engine's `getBattleGrid` uses `Orientation.FLAT` (`libs/hexgrid.ts`).
  - On the battle grid the fan's diagonals become near-vertical lines down columns 7-8, not 60° rays.
  - From the throne [9,4], Lines covers 21 hexes:
    - a row west to (4,4);
    - columns 7-8 from row -1 to row 9.
  - Crownfall now reaches players, but the shape is not the drawn fan. The harness checks hits with the engine's own
    targeting, so the numbers here hold for the record as it is.
- **The Kitsune bonus:** every Crowned Captain fight now ends by round 19, so the Kitsune set's max-HP bonus
  (20 rounds) no longer lapses mid-fight. Report 3's "fact 11" no longer applies at these settings.
- **Machine note.** Two long chain runs were killed by the shared memory cgroup (OOM, with other agents' sims
  running). Chain runs now save after every chain.
- **Stale result files:** `results/crownhold_commanders_solo.json` and `results/crowned_captain_tuned.json` are from report
  3's solo tuning. The bosses are now tuned for the chain only (the ruling: they are never fought alone).
- **Per-fight tables:** `results/crownhold_tables.json` holds the tables the estimates were built from. The D4 entries
  under `final_bosses_read085` are from an earlier D4 setting; the shipped D4 is in `final_d4_read085`.

## Report 3 (superseded by report 4): the shared library, the three commanders, the pyramid chain

This report covers three things:
- the Crowned Captain switched to the shared set-piece library;
- the three division commanders tuned as a ramp;
- the whole isolated pyramid run with pools carried between fights.

**Sources and outputs:**
- The library is `library_spec.json` / `engine/library.ts`, merged from `fable/skyglass-wreck-sim` 4bd5356a. Its records
  are used by id and never copied.
- Shared harness code: `engine/cclib.ts`.
- Scripts: `engine/crowned_captain.ts` and `engine/crownhold.ts`.
- Specs: `crowned_captain_spec.json` and `crownhold_spec.json`.
- Results: `results/crowned_captain_tuned.json`, `results/crownhold_commanders_solo.json` and
  `results/crownhold_chain.json`.
- Inputs: `data/crownhold_inputs.json`, all 20 Crownhold AIs, built by `tools/build_crownhold_inputs.py`.

### The ramp (solo, full pools, average endgame player, 60 seeds per mode)

| Boss | Pools (HP) | Damage rows | Dodging on: win / rounds / HP left (median, p10) | Dodging off: win / HP left | Phase starts (60% / 30%) |
|---|---|---|---|---|---|
| Crown Armsmaster (D2) | 2 (10,100) | none | 100% / 8 / 84%, 61% | 100% / 67% | r3 / r6 |
| Replicant Zero (D3) | 3 (15,150) | +25% | 100% / 14 / 52%, 46% | 100% / 4% | r8 / r10.5 |
| The Second (D4) | 4 (20,200) | 3 x +100% | **90%** / 12 / 48%, 48% | **32%** / 48% | r8 / r10 |
| The Crowned Captain (D5) | 5 (25,250) | +25% | **70%** / 25 [21-25] / 0% (1 HP), 0% | **33%** / 20% | r9 / r19 |

- **The ramp holds.**
  - Win rates fall: 100, 100, 90, 70.
  - HP left at a win falls: 84%, 52%, 48%, and the Captain's wins end at 1 HP (fact 11).
  - The Crowned Captain is the hardest.
- **Where the marks decide the fight:**
  - The Second and the Crowned Captain: ignoring the marks costs most fights.
  - Replicant Zero: it costs nearly all the HP (4% left).
  - The Armsmaster: it costs a sixth of the HP. He is "the straight fight that teaches the marks".
- **The Crowned Captain's phases** (dodging on) run 9 / 10 / 6 rounds. With HP doubled, the duel phase lasts 9 rounds and
  holds about 2 Crownfalls.

### The Crowned Captain on the library

| | Dodging on | Dodging off |
|---|---:|---:|
| Win rate | **70%** (42/60) | **33.3%** (20/60) |
| Rounds to win, median [p10-p90] | 25 [21-25] | 20 [18-23] |
| HP left at a win | 35 of 42 wins end at 1 HP (fact 11) | median 20% |
| Losses by phase (1 / 2 / 3) | 0 / 18 / 0 | 0 / 5 / 35 |
| Phase lengths (rounds) | 9 / 10 / 6 | 9 / 7 / - |
| Idle boss turns | 12.8% | 11.6% |
| Set pieces that landed with no mark the turn before | 0 | 0 |

**Set pieces per fight** (marks / blasts cast / hits; damage per hit):

| Set piece | Dodging on | Dodging off |
|---|---|---|
| Crownfall | 2.1 / 0.3 / 0 | 2.0 / 0.5 / 0.2, 1,487 |
| Command Absolute | 2.2 / 1.4 / 0 | 1.5 / 1.0 / 1.0, 667 plus stun and seal |
| Shardstorm | 2.1 / 0.8 / 0 | 2.1 / 1.8 / 0.6, 733 |
| Recall | 1.3 casts; the echo deals 17% of the damage taken | 1.0 |
| Extermination Order | 1.9 casts; the largest share of damage, 26.5% | - |

**What changed from report 2:**
- His set pieces are library records:
  - Omen: Lines + Crownfall;
  - Omen: Last Light, Binding + Command Absolute;
  - Omen: Scatter A/B + Eruption: Scatter.
- His own new records are The Crown's Will and Recall only.
- Marks cost 40 AP and blasts 100 AP.
- Every blast rule sits at the top. After a mark comes `has_effect <marker>` -> basic attack (adjacent) -> end turn.
- The innate sealprevent row is removed (fact L2).
- His Shardstorm battle line now rides on the Last Directive: "\"Preserve command.\" The crown blazes, and its points
  crack loose above him."
- Extermination Order is off in phase 3. With it on, the 60 AP after each Scatter mark carried it, and dodging won 80%
  at 8.7% HP.
- The rows retune: +50% became **+25%**.
  - With the library's mark-turn attacks and weaker blasts, +50% gave 0-27% wins with dodging.
  - At 0 rows, ignoring the marks won 67%.
- Pools stay **5**, as the director set.

**Tuning path on the library** (40 seeds per mode):

| Damage rows | Beat after a mark | Library change (analysis only) | On: win / rounds / HP | Off: win |
|---:|---|---|---|---:|
| 0.5 | kit attack (60 AP) | - | 0% | 0% |
| 0.25 | kit attack | - | 0% | 10% |
| 0 | kit attack | - | 2.5% | 12.5% |
| 0.5 | basic attack | - | 27.5% / 23 / 0% | 25% |
| 1 | basic attack | - | 12.5% / 21 / 0% | 22.5% |
| 0 | basic attack | - | 85% / 25 / 0% | 67.5% |
| **0.25** | **basic attack** | **-** | **85% / 25 / 0%** (60 seeds: 70%) | **37.5%** (60 seeds: 33%) |
| 0.25 | basic attack | **Lines as a five-ray fan** | 65% / 25 / 0% | **5%** |
| 0 | basic attack | fan; Command Absolute 200 | 65% / 25 / 12% | 27.5% |

**Separation needs a fixed Lines pattern.** With the library's Lines as landed (one 5-hex ray), Crownfall almost never
reaches a player, and marks barely separate dodgers from non-dodgers. Making Lines a real fan (fact L1) takes ignoring the
marks from 37.5% wins to 5%.

### The commanders

Each keeps its push/272 kit and rules, adds library records and rules, and gains no jutsu of its own. Records and rules
are in `crownhold_spec.json`.

**Crown Armsmaster** (D2, `-GKFYAZUg1eF-3VnZhDjx`)
- **Racks Fall:** Omen: Scatter A/B + Eruption: Scatter, after his set-up moves.
- **Whirlwind:** Omen: Ring + Eruption: Ring, under 50% when the player is within 2.
- After a mark: Backlash Palm or Shuriken Storm, then end turn.
- Pools 2.5 to **2**.
- Per fight: 2.0 Racks Fall and 2.0 Whirlwind marks.
  - Dodging on: none hit.
  - Dodging off: Racks Fall hits 0.6 times (510 each) and Whirlwind hits every time it is cast (1,013 each).

**Replicant Zero** (D3, `vjEFUJ9mb1zNTuQf4lfXv`)
- **Jar Seals:** Omen: Seal Lines + Binding: Seal Lines, from round 6 (fact L5).
- After a mark: Devouring Wave or Mirror Edge, then end turn.
- He keeps his live round-2 Split Image. The design's "clones stand on the lines with him" does not work with the library
  as landed (fact L5).
- Rows: **+25%**.
- Per fight:
  - Dodging on: 2.5 marks, 0.6 blasts cast, no hits.
  - Dodging off: 2.3 hits of 329, plus seal and elemental seal. 57 second blasts landed without a mark (fact L3).

**The Second** (D4, `ZsfRoyJ55Zsay5bHNLMPv`)
- **Order of Battle:** Omen: Rows A/B, then his live Sovereign Undertow (60 AP) pulls in the mark turn, then Eruption:
  Rows next turn.
- After a mark: Undertow, Piercing Judgment, Explosive Tag, then end turn.
- **Window:** Lowered Guard under 30%, once. It fired in 0.9 of fights, in round 11. Its line is the library's neutral
  one; "I questioned his orders for thirty years." has no record to ride on.
- Pools 3 to **4**; rows: **3 x +100%**.
- Per fight: 5.1 marks and 1.2 Undertows.
  - Dodging on: no hits.
  - Dodging off: 1 hit of about 4,000 (a near one-shot), and 41 of 60 fights lost in phase 1.

### The isolated pyramid, pools carried (20 seeded runs per route policy, dodging on, all regulars at their live push/272 stats)

| Policy | Clears | Where runs end | D2 boss: enter HP / win | D3 boss: enter / win | D4 boss: reached / enter / win | Crowned Captain: reached / win |
|---|---:|---|---|---|---|---|
| clean | **0%** | D3 boss 9, D4 regulars 10, D4 boss 1 | 92% / 100% | 44% / 55% | 5% / 11% / 0% | 0% |
| alert | **0%** | the same as clean | 92% / 100% | 44% / 55% | 5% / 11% / 0% | 0% |
| healing | **45%** | D4 boss 1, Crowned Captain 10 | 100% / 100% | 100% / 100% | 100% / 100% / 95% | 95% / 47% (median 21 rounds, ends at 0-1 HP) |
| war | **0%** | D3 boss 14, D4 regulars 6 | 88% / 100% | 47% / 30% | 0% | 0% |

**Reading the chain:**
- **Without regeneration between fights, only the Healing Rite route can clear.**
  - The Healing Rite resets pools before each boss, so every boss is met at full HP. Its results match the solo ramp.
  - Clean and war arrive at Replicant Zero with under half HP (44-47%) and lose there about half the time or more. The
    survivors reach the Second at about 11% HP, or die to D4's regulars first.
- **Alarm Raised changes almost nothing.** It is +10% damage taken for 2 rounds. Clean and alert end the same way on the
  same seeds; HP left after Replicant Zero is 14.2% vs 14%.
- **The War Rite does not pay for the fourth regular without a heal.**
  - Its D2 stun immunity is spent on a fight already won 100%.
  - Its D3 +25% damage for 3 rounds does not make up for entering at 47%. It wins 30% there vs clean's 55%. Seed noise
    is about 11 points at 20 chains.
- **Open decision for the director:**
  - Either the pyramid regenerates or heals between fights, or the commanders are tuned for carried pools.
  - Retuning for carried pools would mean D3 and D4 rows of about 0 and +100%, a sim re-run, and the ramp flattening
    when they are fought solo.
  - Not settled here. The solo numbers above assume full pools, as the Healing Rite route gives.


**Assumptions:**
- The run starts at full pools.
- After each won fight the player carries the end-of-fight fraction of HP, chakra and stamina into the next fight.
- There is no regeneration between pyramid fights. An isolated pyramid keeps the player in BATTLE status. Whether time
  regeneration runs between fights is not modelled. If it does, these chains are pessimistic.
- A loss ends the run.

**The four route policies** apply the same choice in every division (push/273):

| Policy | Route per division |
|---|---|
| clean | 3 regulars, the puzzle solved, then the boss |
| alert | the puzzle failed: the boss with Alarm Raised (+10% damage taken, 2 rounds) |
| healing | 4 regulars, then the Healing Rite: the boss at full pools |
| war | 4 regulars, then the War Rite: D2 stun immunity 2r, D3 +25% damage 3r, D4 seal immunity 2r, D5 debuff immunity 3r |

### Library findings (for the library owner; each from source and/or a harness run)

**L1. Omen: Lines is one 5-hex ray west, not a fan.**
- `library_spec.json` `patterns.lines` holds 5 offsets, all latitude 0. The NW and SW rays come out empty.
- Cause: `library.ts` builds its geometry on `new Grid(TerrainHex, rectangle(...))`, the default POINTY honeycomb grid.
  The battle grid is FLAT, with odd columns offset (`getBattleGrid`). That is the same mistake as `probe_telegraph.ts` in
  report 1.
- Consequence: Crownfall reaches a player 0.2 times per fight even when they ignore it.
- A five-ray fan computed on the battle grid (`--params {"libLinesFan": true}`, analysis only) makes ignoring the marks
  lose 95% of fights.

**L2. Last Light, Binding's marker (sealprevent) collides with every Crownhold boss's innate sealprevent 100.**
- `has_effect sealprevent >= 1` is always true, so Command Absolute would fire every turn.
- Fixed on the Crowned Captain by removing his innate row. The boss has no bloodline, so the row did nothing.
- Any other boss with innate sealprevent cannot use that mark.

**L3. A 1-round marker can be seen on two boss turns.**
- `has_effect` counts the boss's effects without checking that they are still active (`ai_v2.ts` has_effect branch).
- When the boss acts before the player in a round, last round's marker is still listed at rounds 0.
- The blast (cooldown 1) then fires a second time, with no mark.
- Seen on Replicant Zero: 57 such second blasts over 60 fights where the marks were ignored.
- **Fix:** blast cooldown of 2 or more. The marks' cooldown 4 already spaces them.

**L4. Stun and seal blasts share a 3-round lock (`SHARED_COOLDOWN_TAGS`, `SHARED_COOLDOWN_ROUNDS` 3).**
- A boss's own stun or seal moves lock its stun or seal blast. Then the mark fires and its blast cannot.
- Seen: the Crowned Captain's Final Command and Ruin Refrain lock Command Absolute for 3 rounds. His first Command
  Absolute at the phase-2 turn is often a mark with no blast.
- Command Absolute, Maw of the Deep, Ship's Bell and Binding: Seal Lines are all exposed.

**L5. Binding: Seal Lines applies elementalseal with no friendlyFire, and elementalseal is also the Seal Lines marker
type.**
- A Split Image clone runs Replicant Zero's rules, so it lays and fires its own Seal Lines.
- Its blast lands the marker type on him, and he then fires the blast every turn without a mark.
- Workaround: his mark only from round 6, after his live round-2 clone is gone, and no clone after a mark.
- **Fix:** friendlyFire ENEMIES on the blast's seal rows, or another marker type.

**L6. Scatter A and B (`((c >> 1) + r) % 3`) are a third of the arena each, and the third class is never hit.** A player
who ignores marks but stands on it is safe forever. Shardstorm's "safe hexes move" holds only between A and B.

**L7. Other notes:**
- The Lines marker is `disarm`. It hides the Crowned Captain's Solar Bow and Crossbow for that round; harmless.
- He never uses Omen: Last Light (red), whose summonprevent marker would block Recall.

### Engine facts added in report 3

- **Fact 11. The Kitsune set's max-HP bonus expires after 20 rounds.**
  - The increasemaxpools rows run 20 rounds.
  - When they lapse, current HP drops with the maximum, floored at 1.
  - In the 25-round Crowned Captain fight, 35 of 42 winning players finish at 1 HP. They survive because, once the Last
    Directive is up, a dodging player takes no further damage: his only actions are Shardstorm and a basic attack.
  - Any fight over 20 rounds costs the Kitsune set's bonus.
- **Fact 12. Phase 3 for a dodger is now a pure survival test.**
  - Every Shardstorm blast is a 100 AP turn, and the mark turn carries only a basic attack.
  - So the Last Directive's 5 rounds hurt only players who ignore the marks: 35 of their 40 losses happen there.

### What does not work as designed (report 3)

- **Ignoring the marks against the Crowned Captain wins a third of fights.** With the library as landed, his marks
  separate players less than in report 2 (5%). The cause is library-side (L1, L4). The fan fix alone gets back to 5%.
- **Fights are long.** The Crowned Captain's win is razor-thin: 1 HP after the Kitsune bonus lapses at round 21. HP
  doubled plus the 5-round Directive gives 25 rounds.
- **Replicant Zero's clones cannot stand on the lines** (L5). Second blasts with no mark happen whenever he acts first
  (L3).
- **The Second's window line** has no record of his to carry it. The shared Lowered Guard is neutral.
- **The pyramid cannot be cleared on carried pools except by the Healing Rite route.** That route clears 45%. Clean,
  alert and war clear 0%, and most of those runs end at Replicant Zero or D4's regulars. The commanders were tuned solo at
  full pools. Whether there is regeneration between fights is a director decision; see the chain section.


## Report 2: HP doubled (director, 2026-10-28; superseded by report 3)

The director doubled his HP (pools 2.5 to 5, 25,250 HP) so that phase 1 lasts. The Recall echo is unchanged.

**What was retuned, and why:**
- **Unavoidable damage down:** damage rows go from +100% and +75% to a single **+50%** row.
- **Set pieces more often:** Crownfall's cooldown goes from 4 to **3** and Command Absolute's from 8 to **6**. Each set
  piece is a full boss turn that a dodger takes no damage from. A player who ignores the marks gets hit more often.
- **Set-piece damage is unchanged:** Crownfall 180, Command Absolute 130 plus stun and seal, Shardstorm 180.
- The rules and the rest of the kit are unchanged.

| 60 seeds per mode | Dodging on | Dodging off (marks ignored) |
|---|---:|---:|
| Win rate | **93.3%** (56/60) | **5%** (3/60) |
| Rounds to win, median [p10-p90] | **23 [23-23]** (range 21-25) | 22 |
| Player HP left at a win, median / p10 | **22.8% / 8%** (2 wins at almost 0%) | ~0% |
| Losses by phase (1 / 2 / 3) | 0 / 3 / 1 | 2 / 47 / 8 |
| **Phase lengths**, median: phase 1 (100-60%) / phase 2 (60-30%) / phase 3 to the kill | **7 / 10 / 6 rounds** (phase 2 starts r7, phase 3 r17) | 7 / 10 / - (most die in phase 2) |
| The Last Directive cast | 95% | 18% |
| Idle turns: boss / player | 3.8% / 0% | 0% / 0% |
| Dodge moves per fight; moves refused onto a mark | 4.6; 2.0 | - |
| Set pieces that landed with no mark the turn before | 0 | 0 |

The fight now has one mode: 48 of 56 wins take exactly 23 rounds. The two-mode split of the first tuning is gone.

**Set pieces per fight** (marked / landed / hit; damage per hit is HP actually lost):

| Set piece | Dodging on | Dodging off |
|---|---|---|
| Crownfall | 2.1 / 2.1 / 0 | 2.1 / 2.1 / 1.2 (59%), 1,612 per hit |
| Command Absolute | 1.9 / 1.0 / 0 | 1.3 / 1.3 / 1.3 (100%), 1,077 per hit, plus stun and seal |
| Shardstorm | 0.9 opener / 3.0 volleys / 0 | 0.2 / 0.5 / 0.1 (few reach phase 3) |
| Recall | 1.1 casts | 1.2 casts |

**Damage to the player by source:**

| Dodging on | | Dodging off | |
|---|---:|---|---:|
| Extermination Order | 35.1% | Crownfall | 33.3% |
| echo | 19.7% | Command Absolute | 22.6% |
| Devouring Grasp | 17.6% | Extermination Order | 15.4% |
| Scorching Rend | 13.4% | echo | 9.6% |
| Cursed Thread Weave | 6.5% | Scorching Rend | 6.6% |
| Final Command | 4.5% | Devouring Grasp, Cursed Thread Weave, Final Command, Keelbind, Solar Bow, Ruin Refrain, Shardstorm | 12.5% together |
| Keelbind, Solar Bow, Ruin Refrain | 3.1% together | | |

**Retune path at pools 5** (40 seeds per mode; on = win %, rounds, HP left; off = win %):

| Damage rows | CF cd | CA cd | Set pieces CF / CA / SS | On | Off |
|---:|---:|---:|---|---|---:|
| 1.75 (old) | 4 | 8 | 180 / 130 / 180 | 0% (dies in phase 2) | 0% |
| 1 | 4 | 8 | same | 0% | 0% |
| 0.5 | 4 | 8 | same | 45%, 25, 0% | 5% |
| 0 | 4 | 8 | same | 55%, 25, 12% | 5% |
| 0 | 4 | 5 | same | 32.5%, 25, 11% | 5% |
| 0 | 3 | 5 | same | 100%, 23, 38% | 5% |
| 0.25 | 3 | 5 | same | 100%, 23, 30% | 5% |
| 0.5 | 3 | 5 | same | 90%, 23, 23% | 0% |
| **0.5** | **3** | **6** | **same** | **92.5%, 23, 23% (tuned; 60 seeds: 93.3%)** | **5%** |

**What is still not as designed:**
- **The fight is 23 rounds, not 12-15.** The director accepted a longer fight with this change.
- **Phase 2 is the longest, at 10 rounds.** In it, Extermination Order and the echo deal most of the damage a dodger
  takes, and all 3 phase-2 losses happen there.
- **Phase 1 now lasts 7 rounds.** Crownfall fires about twice, but Final Command, Keelbind and Ruin Refrain still deal
  under 7% of the damage. They sit below Crownfall and Cursed Thread Weave in the rule order, and Crownfall now holds
  every third turn.
- **His damage still sits above the ladder,** at x1.5 rows x1.6 from The Crown's Will (x2.4), plus the Directive.

Everything below this section is the first tuning (pools 2.5), kept for the record. Its engine facts, probe answers and
open decisions still stand.

---

## First tuning (pools 2.5, superseded)

### Headline (first tuning, 60 seeds per mode)

| | Dodging on | Dodging off (marks ignored) |
|---|---:|---:|
| Win rate | **93.3%** (56/60) | **1.7%** (1/60) |
| Rounds to win, median [p10-p90] | **15 [13-16]** | 16 (one win) |
| Player HP left at a win, median / p10 | **39.3% / 30.8%** | 2% |
| Where losses happen (phase 1 / 2 / 3) | 0 / 4 / 0 | 3 / 9 / 47 |
| Boss reaches phase 2 / phase 3 (median round) | r4 / r9 | r4 / r8.5 |
| The Last Directive cast | 93.3% of fights | 80% |
| Idle turns: boss / player | 0% / 0% | 0% / 0% |
| Dodge moves per fight; moves refused onto a mark | 4.9; 1.0 | - |
| Set pieces that landed with no mark the turn before | 0 | 0 |

**The win distribution has two modes.** The fight is nearly deterministic; only the spawn tile and the 10% random
barriers vary.

| Branch (dodging on) | Wins | Phase 3 starts | Rounds | Player HP left (median) | What happens |
|---|---:|---|---:|---:|---|
| Fast | 24 | round 7 | 13 | 87% | The player's single-target jutsu stay on him through phase 2. |
| Slow | 32 | round 10 | 16 | 32% | The echo stands closest, so the auto-player spends 2-3 turns on it while Extermination Order and Scorching Rend land. |

- The 4 losses are all slow-branch, in phase 2.
- The median of 39% HP sits between the two modes.
- A real player who "focuses him" plays the fast branch. One who fights every echo plays the slow branch.

### Set pieces: how often each fires and hits

Per fight, averaged. "Hit" means the player stood on a pattern hex when it landed. Damage per hit is the HP actually
lost, so it is capped by the HP left.

| Set piece | Dodging on: marked / landed / hit | Dodging off: marked / landed / hit | Damage per hit (dodging off) |
|---|---|---|---:|
| Crownfall (phase 1) | 1.0 / 1.0 / 0 | 1.0 / 1.0 / 0.6 (60% of landings) | 2,750 |
| Command Absolute (phase 2) | 1.0 / 0.9 / 0 | 0.9 / 0.9 / 0.9 (100%) | 1,787, plus a 2-round stun and seal |
| Shardstorm (phase 3; landings are volleys) | 0.9 opener / 4.6 volleys / 0 | 0.8 / 1.7 / 0.7 (42%) | 709 (most victims already low) |
| Recall | 1.0 cast; the echo deals 25% of all damage the player takes | 0.9 | - |

### Damage to the player by source (share of all damage taken)

| Dodging on | | Dodging off | |
|---|---:|---|---:|
| Extermination Order | 34.0% | Command Absolute | 27.7% |
| Scorching Rend | 27.1% | Crownfall | 27.4% |
| echo (Sanctum Vanguard) | 24.9% | Extermination Order | 13.2% |
| Final Command | 5.0% | Scorching Rend | 9.8% |
| Devouring Grasp, Ruin Refrain, Cursed Thread Weave, Solar Bow, Keelbind | 9% together | echo / Shardstorm | 9.6% / 8.6% |

## The setup

**The player** is the harness's `average` tier:
- level-100 JONIN with capped stats, so 6,250 HP with the set;
- the full Kitsune set, worn through the item path;
- the 9 level-25 PvE jutsu (Fire/Wind);
- driven by the harness rotation (`playerRules`), with full pools.

**The battle** is a plain QUEST battle, because Crownhold's `start_battle` objectives call `initiateBattle(..., "QUEST")`.
- The grid is **12 x 10** (`getDefaultBattleSizes("QUEST", 100)`).
- The isolated battlepyramid flag does not change the battle type or the grid.
- Random initial barriers are on.

**The dodge rule** is a declared test input, run through the engine's own Move, Replacement Technique and Cleanse
actions:
1. At each action step, if the player stands on a live danger mark (`tg_heavy` or `tg_control` ground visual), they
   step to the nearest unmarked free hex:
   - Replacement Technique when that hex is 2 or more steps away, within 5, and the technique is ready;
   - otherwise one Move step.
   If rooted, they use the basic Cleanse first. In 60 runs that never came up.
2. They never end a move on a marked hex. An auto-combat move onto one is replaced by ending the turn.

## The boss record (first-tuning values; the current values are in the section above and in the spec)

| Field | Value | Note |
|---|---|---|
| poolsMultiplier | **2.5** (12,625 HP) | push/272 had 3.5 |
| statsMultiplier | 5.83 (unchanged) | Inert in battle; see engine fact 1 |
| Innate damage rows | **+100% and +75%** (x3.5), plus sealprevent | |
| The Crown's Will (opener) | +60% damage given and +25% stats | Total x5.6 before the Directive's +30% |
| Throne | (9,4) | He walks there on his first turn and never moves again (reached in 100% of runs) |

**Kit (22 jutsu):**
- Arakane's kit minus Rapid Fire (live: Shuriken Storm), Braced Strike and Surging Overflow. Live names differ from the
  package names:

  | Package name | Live name |
  |---|---|
  | Hexweave | Cursed Thread Weave |
  | Zephyr Lance | Wind Spear |
  | Apex Hunger | Oni's Hunger |
  | Worldbreaker Chorus | Great Bell Toll |

- Ruin Refrain replaces Worldbreaker Chorus.
- Plus Final Command and Keelbind, from the old Crowned Captain kit (push/249 capture).
- The Last Directive, Extermination Order and the Countermand item are kept, along with Solar Bow and Crossbow.
- Oni's Hunger is replaced by **The Crown's Will**, a Crownhold-only copy with the same effects. It carries
  `cc_crown_aura` and the opening log line.
- Plus 9 new set-piece and Recall records.

**Set pieces:**

| Set piece | Telegraph | Detonation | Pattern |
|---|---|---|---|
| Crownfall | 100 AP, cd 4; `tg_heavy` | 100 AP, damage 180; `cc_crownfall` | A fan of 5 rays (36 hexes) from the throne |
| Command Absolute | 100 AP, cd 8; `tg_control` over the hall, `tg_safe` on 3 stars, `cc_phase_shift` | 100 AP, damage 130 + stun (60 AP, 2r; `dt_control`) + seal 2r, log "Kneel."; `cc_command_absolute` | Stars at (7,1) (5,4) (8,8), each 4 hexes from the throne, so the player keeps jutsu range on a star |
| Shardstorm | Opener 60 AP | Three volleys, 60 AP each, damage 180; each also marks the next pattern; `cc_shardstorm` | Rotation by marker |
| Recall | - | 60 AP, cd 8, `cc_recall`; summons Sanctum Vanguard (D5.REG1, `pshn-LkaC5vIgI6EOv68I`) beside the throne | Echo: 2,500 HP, 70% stats, 3 rounds |

- **Shardstorm patterns:** each pattern marks one colour of the hex 3-colouring, a third of the hall. A clear hex is
  always adjacent. Why a third, not two thirds: fact 5.
- **Recall:** the condition is `does_not_have_summon` plus the cooldown.

**Rules (34, in order):**

| Rules | What they do |
|---|---|
| 0 | Walk to the throne |
| 1-5 | The detonations, each keyed `has_effect` on its own 1-round marker |
| 6-11 | **Phase 3** (under 30%): The Last Directive, then Purging Stance on afterburn or poison (fact 6), then Shardstorm, then Extermination Order, then end turn |
| 12-19 | **Phase 2** (under 60%): Command Absolute, Recall, Stolen Form, Extermination Order, Scorching Rend, Devouring Grasp, Countermand, then end turn. The end turn keeps phase-1 moves out |
| 20-33 | **Phase 1**: The Crown's Will (round 1), Arakane's Veilstep/Countermand/Purging/Wind Spear rules, Crownfall, Cursed Thread Weave, Final Command, Keelbind, Ruin Refrain, Scorching Rend, Devouring Grasp, Solar Bow, end turn |

The Last Directive gets a cosmetic edit only:
- its battle log becomes the design's "\"Preserve command.\" The crown blazes.";
- the finalstand row gets `cc_last_directive` and `cc_phase_shift`.

Its effects are unchanged: finalstand, clearprevent, +30% damage given, 5 rounds (director: no clear strips it).

**Validation:** every new record and the edited Last Directive pass `JutsuValidator`. Every rule passes `AiRule`. The AI
record passes `insertAiSchema`, including `maxPoolsMultiplier`.

## Tuning path (dodging on / off; earlier rows ran on earlier code, see the engine facts)

| Step | Seeds | Pools | Damage rows | Set pieces CF / CA / SS | Echo HP / power / cd | On: win, rounds, HP | Off: win |
|---|---:|---:|---:|---|---|---|---:|
| First pass, stars far, 2-round marks | 20 | 3 | 1 | 90 / 60 / 70 | 6,000 / 100 / 2 | 0% (stalls in phase 2) | 0% |
| Stars moved into range | 20 | 3 | 1 | 90 / 60 / 70 | 6,000 / 100 / 2 | 80%, 20, 32% | 0% |
| Echo cheaper | 20 | 2.5 | 0.5 | 150 / 110 / 130 | 2,500 / 70 / 5 | 85%, 18, 61% | 65% |
| Set pieces up | 20 | 2.5 | 0.5 | 200 / 150 / 170 | 2,500 / 70 / 6 | 95%, 12*, 79% | 5% |
| Final Stand fix (Purging Stance), 60-AP volleys | 20 | 2.5 | 1 | 200 / 150 / 170 | 2,500 / 70 / 6 | 85%, 16, 68% | 5% |
| One-third Shardstorm, CA cd 8 | 20 | 2.25 | 1.5 | 200 / 150 / 200 | 1,500 / 70 / 8 | 90%, 16, 43% | 5% |
| Echo beside the throne | 20 | 2.25 | 2 | 200 / 150 / 200 | 2,500 / 70 / 8 | 90%, 15, 26% | 5% |
| | 40 | 2.25 | 2.5 | 150 / 110 / 150 | same | 52.5%, 13, 86% | 5% |
| **Tuned** | 60 | **2.5** | **1.75** | **180 / 130 / 180** | **2,500 / 70 / 8** | **93.3%, 15, 39%** | **1.7%** |

\* Rounds of 12 before the Final Stand fix were the boss dying through the Last Directive (fact 6).

## Engine facts found or re-verified (each checked in source and/or by run)

**Stats and records:**

1. **statsMultiplier does nothing above about 4.7 for a JONIN AI.**
   - `initiateBattle` caps every participant with `capUserStats(rank)`: offence/defence 1.3M, generals 400k.
   - The push/272 boss (live readback 1,622,255.8 each) fights with exactly the player's stats.
   - Only pools and damage rows tune him.
   - Rank ELITE JONIN would lift the cap. That is a director call; not used.

2. **`increasepoolcost` needs `rounds >= 2` in the live schema** (`validators/combat.ts` IncreasePoolCostTag), so the
   probe's 1-round marker cannot be stored.
   - A 2-round marker overlaps the next set piece's.
   - Each set piece therefore carries its own harmless 1-round self effect as its marker:

     | Set piece | Marker |
     |---|---|
     | Crownfall | `fleeprevent` |
     | Command Absolute | `robprevent` |
     | Shardstorm volleys | `onehitkillprevent`, `increaseaggro`, `decreaseaggro` |

   - None of these is cleansable (not in `isNegativeUserEffect`).
   - The player's basic Clear could strip a marker and cancel a set piece; the auto-player never uses Clear.

**Geometry and patterns:**

3. **The battle grid is FLAT with odd columns offset** (`getBattleGrid`).
   - `engine/probe_telegraph.ts` measured its rings on a default (POINTY) honeycomb grid. Its "row parity" rule is
     really column parity on the battle grid.
   - All patterns here are BATTLEFIELD-origin, absolute, so parity does not matter.
   - One jutsu can carry several patterns: per-tag `target: "COORDINATES"` with its own `coordinateTargeting`, plus a
     SELF tag (`util.ts` getActionAffectedTiles, `actions.ts` insertAction). This is how one telegraph lays `tg_heavy`
     on the danger hexes and `tg_safe` on the safe ones.

4. **Marks must be 1-round visuals.**
   - A 1-round ground visual stays through the next round, which covers the detonation turn.
   - A 2-round visual stays a whole round after the hit and reads as a new warning.
   - Visuals never play a `disappearAnimation`: `expireGroundEffects` drops expired visuals before that branch. So
     `dt_heavy` is unused (spec, `animations`).

5. **Turn order can put him before the player in a round.**
   - When it does, last volley's mark is still on the floor beside the new one.
   - With two-thirds patterns the two marks covered every hex, and a careful player had nowhere to stand. That caused 7
     of 9 losses in one 20-seed batch.
   - One-third patterns fix it, because a hex of the third colour is always adjacent.

**Damage and the Last Directive:**

6. **Final Stand does not stop damage-over-time.**
   - `process.ts` applies afterburn, poison and drain ticks outside `calcAdjustedDamage` and `applyFinalStandDamage`.
   - Each damage component (damage, residual, wound) is floored separately against the HP before the hit, so their sum
     can still kill.
   - The player's Tempestual Fury afterburn killed him under the Last Directive in 2 of 60 runs.
   - The fix in rules: under 30% he uses Purging Stance on afterburn or poison before Shardstorm. After that there were
     no early kills in 60 runs.
   - The engine issue itself is worth an upstream report: Final Stand is meant to be a floor.

**Targeting:**

7. **Command Absolute's detonation is an OTHER_USER cast over the pattern.**
   - That makes stun and seal real user effects. A ground stun would only stun while the player stands on the hex.
   - The engine accepts the cast only if some unit stands in the pattern. The echo counts, and friendlyFire ENEMIES spares
     it.
   - If the player is on a star and no echo is up, the cast is refused, so the "Kneel." log and animation do not play, and
     he takes his next rule. That is why landings are 0.9 per fight with dodging, not 1.0.

8. **Initial barriers punch holes in GROUND telegraphs.** A barrier hex gets no mark, while the OTHER_USER Kneel still
   covers it if the barrier is destroyed. Rare; noted.

## Probes asked for in the brief and by the coordinator

**(3) Can a ground effect grant `injectjutsus` to whoever ends a move on it? No** (`results/probe_ground_inject.json`).
- The test: a boss jutsu laid an `injectjutsus` ground effect (3 rounds), with friendlyFire ENEMIES and with ALL. The
  player moved onto it and stood there.
- Result: no persistent effect, and the jutsu never appeared in their actions.
- A ground `increasedamagetaken` tile behaves the same way.
- Why: ground effects reach a unit only transiently while each action resolves. `applyEffects` gives them rounds 1, and
  they are "not forwarded to the next round". `handleInjectedJutsus` reads the persistent effects, so the grant never
  shows.

Two related answers came out of the same probe:
- **Preloaded: yes.** `initiateBattle` loads every `injectableInBattle` jutsu into `extraState.jutsus`
  (`routers/combat.ts` ~2321). The harness does the same.
- **One-use: yes, when the inject is cast directly on the unit.** With OTHER_USER and SINGLE, the jutsu appeared at once
  and was used once. With cooldown 20 against a 3-round grant, it did not come back.

So heal or buff tiles must be ordinary ground effects, such as heal or increasedamagegiven, which the engine applies
while the unit stands there. A granted action must be cast on the unit.

**Dropped by the director:**
- (4) can a clear remove finalstand;
- (2) the Crown Shard weakness window.

The Crown Shard is cut. Shardstorm's safe hexes are plain. The Last Directive is a 5-round survival test.

The source answer to (4), found before the drop: no.
- `clear` checks `clearprevent` first (`tags.ts` clear).
- `finalstand` is not in `isPositiveUserEffect`, so a clear would never remove it anyway.

## What does not work as designed, and open decisions

- **Phase 1, the duelist, is short.**
  - The player's opening burst takes him from 100% to 60% in about 3 turns.
  - So Crownfall fires once and Final Command, Keelbind and Ruin Refrain barely act: 9% of the damage taken together.
  - Making the duel phase longer needs more HP, which pushes the fight past 15 rounds. The Directive alone adds 6. The
    alternative is a different phase threshold. **Director's call.**
- **His HP sits below the push/272 ladder.**
  - Pools are 2.5 against 3.5, because the 5-round Directive plus 12-15 rounds forces it.
  - His damage is above the ladder (x5.6), so "above the ladder" holds for damage, not health.
- **Two modes, not one average**, as shown above. The slow branch is the "hard" fight (32% HP left, all 4 losses). The
  fast branch is comfortable (87% HP left).
- **Recall, then Command Absolute.**
  - Command Absolute's cooldown is 8, so it comes once per phase 2.
  - Each pass costs him two full turns (mark, Kneel) in which he does not attack.
  - Shorter cooldowns made phase 2 a stall (the first pass: 0% wins).
- **Countermand (clear) on the player** removes the player's jutsu buffs. The Kitsune effects stay: `fromType` armor is a
  persistent source (`tags.ts` persistentEffectSourceTypes).
- **Kit cooldowns are untouched.** No `cooldowns` override is used, so the shared live records (Final Command and so on)
  need no copies.
- **Every set-piece number assumes the live damage settings** (`data/dmg_config_live.json`).

## Reproduce

```bash
python3 harness/skyglass_wreck_sim/tools/build_crownhold_inputs.py --check
H=$PWD/harness/skyglass_wreck_sim
TNR_SCRIPT=crowned_captain.ts harness/skyglass_wreck_sim/run.sh --seeds 60 \
  --out $H/results/crowned_captain_tuned.json --write-spec $H/crowned_captain_spec.json \
  --probe-inject --probe-out $H/results/probe_ground_inject.json
# one fight, action by action (both dodge modes):
TNR_SCRIPT=crowned_captain.ts harness/skyglass_wreck_sim/run.sh --trace 5 --seeds 0
# a tuning variant (absolute path; any DEFAULTS key):
TNR_SCRIPT=crowned_captain.ts harness/skyglass_wreck_sim/run.sh --params /abs/variant.json --seeds 40
# the commanders solo, and the pyramid chain per route policy:
TNR_SCRIPT=crownhold.ts harness/skyglass_wreck_sim/run.sh --solo 60 \
  --out $H/results/crownhold_commanders_solo.json --write-spec $H/crownhold_spec.json
TNR_SCRIPT=crownhold.ts harness/skyglass_wreck_sim/run.sh --chain 20 --policies clean,alert,healing,war \
  --out $H/results/crownhold_chain.json
```

- 60 seeds per mode take about 1 minute.
- `--params` and `--write-spec` paths must be absolute, because run.sh resolves only `--out`/`--override`.
