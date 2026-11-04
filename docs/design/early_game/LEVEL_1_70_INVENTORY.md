# Early game, levels 1-70: source and content inventory (pass 1)

- **Brief:** `state/prompt_early_game_sim.md` (Lane A, `fable/early-game-sim`).
- **Game source pin:** `studie-tech/TheNinjaRPG@3314d122c93e036618483d18229a793ad7ad21fd` (2026-10-29). Upstream HEAD on 2026-11-04 is `4d09bbcd`; nothing below is verified against it.
- **Live content:** committed captures in `harvests/inbox/` (451 bundles, 2026-08-30 to 2026-11-04), de-duplicated by record id, keeping the fullest copy.
- **Evidence tiers** follow `docs/00_INDEX.md`:
  - **SV** (source-verified): file:line cited, relative to `app/`, `C` = `drizzle/constants.ts`
  - **CAP** (capture: what live records hold)
  - **SEED** (`app/data/quests.sql`, old seed values; live may differ)
  - **ASSUMED** (nobody checked)
- Zero live requests were made.

## 1. The progression engine

### Experience and level
- **XP is the running total of combat-stat points gained.** It is not a per-level bar. **SV**
  - `profile.ts:62-71` sets the cumulative requirement: `calcLevelRequirements(L) = 250·L·(L+1)` for L ≤ 80. The factor rises from 500 to 950 above level 80 (C:213-215).
- **Level-up is a manual button** (`LevelUpBtn.tsx`; router `profile.ts:619-720`). **SV**
  - It is blocked at the rank's level cap.
  - Horizon players are blocked past level 9 (`profile.ts:85-88`).
  - Combat uses `calcLevel(experience)`, so holding a level down does not lower combat level (`profile.ts:113-117`).
- **Quest `reward_exp` goes to `earnedExperience`,** which the player assigns by hand. Points assigned to combat stats also add to `experience`. **SV** (`quests.ts:2137`; profile router `:1881-1990`)
- **Cumulative XP to reach a level:** **SV**

| Level | XP |
|---|---|
| 10 | 22,500 |
| 30 | 217,500 |
| 57 | 798,000 |
| 70 | 1,207,500 |

- **XP per band:**

| Band | XP |
|---|---|
| 1-10 | 22.5k |
| 10-30 | 195k |
| 30-57 | 580k |
| 57-70 | 410k |

### Ranks and caps
- **USER_CAPS** (C:1474-1505), **SV**:

| Rank | Level cap | Stat cap (offence/defence) | General cap (each) |
|---|---|---|---|
| Student | 10 | 20k | 20k |
| Genin | 30 | 60k | 60k |
| Chunin / Jonin | 100 | 1.3M | 400k |

- **Rank-ups come only from a quest's `reward_rank`** (`quest.ts:530`). **SV**
- **Live rank-granting quests**, **CAP**:
  - Road to Genin (starter, L1-20) → GENIN
  - The Chunin Exams (starter, L27-30) → CHUNIN
  - The Path of a Shinobi: The Jonin Exam (starter, L57-100) → JONIN
  - A hidden duplicate at L48-100 also grants JONIN
- **Rank gates elsewhere**, **SV**:
  - PvP: Chunin and up (C:1969)
  - Leaving a village: Chunin (C:1655)
  - War missions: Chunin (C:2089)
  - Clan: Genin (C:2287)
  - Medical: Genin (C:1709)
  - Bloodline roll: Genin, once per account (`bloodline.ts:692-760`)

### Pools and stats
- **HP, SP, CP and Energy** are each `100 + 50·(L-1)`, independent of stats (`profile.ts:227-239`). **SV**
  - Level 10: 550. Level 30: 1,550. Level 70: 3,550. Level 100: 5,050.
- **Regeneration** is 60 per 60 s, with home, bloodline, clan, structure and event modifiers (`profile.ts:460-521`). **SV**
- **New character:** **SV**
  - all stats and masteries 10
  - 2,000 unassigned XP (10,000 with an email reminder)
  - 1,000 ryo plus 1,000 in the bank
  - a D-rank bloodline
  - starts in Horizon
  - (`schema.ts:2651-2716`, `register.ts:101-300`)
- **Energy training:** `energy × 0.085 × trainingBoost` (C:1213; `train.ts` router `:210-260`). **SV**
  - Unboosted that is about 5.1 XP per minute, or about 7.3k per day if a player trained continuously. **SV formula; ASSUMED live boosts**
  - The live `trainingGainMultiplier` and other boosts are unknown.
- **Timed mastery/element training:** 15 min to 24 h sessions, 64 per day (`train.ts:714-791`; C:1943). **SV**

## 2. Activities and rewards
| Activity | Gate | Reward shape | Evidence |
|---|---|---|---|
| Mission Hall missions/crimes | Letter rank by user rank (Student D, Genin D/C, Chunin D-B, Jonin D-H); `requiredLevel ≤ L ≤ maxLevel` | One **random** quest per start. Daily cap 20 (missions + crimes); from the 10th of the day rewards are ×0.4. Seed XP: D 222, C 450, B 670, A 700-1000. | SV `quest.ts:384-650, 2106-2178, 3071-3094`; C:2043, 2070-2071; SEED |
| Errands | Any | 50 per day; seed pays ryo only | SV C:2042; SEED |
| Daily quest | Active in the last 7 days | A cron hands out one per day | SV `api/daily-quest/route.ts:60-175` |
| Tier / exam quests | Level fits | **Handed out automatically** on user fetch (`BOOTSTRAP_QUEST_TYPES`) | SV profile router `:3204-3225, 3673-3714` |
| Story / starter | Story needs the Global ANBU HQ; up to 4 story quests at once | Authored per quest; +20 energy on completion | SV `quest.ts:2917-3031`; C:1072, 1247-1253 |
| Arena vs AI | Allied village arena | **XP capped at 20 per win.** Ryo `(30-40 + L)`. AI **not** scaled to the player. | SV `util.ts:2040, 2104-2113`; `queries/combat.ts:378-389` |
| Quest / encounter battles | Per objective | ELO-style XP, no cap. AI scaled if `scaleStats`. Jutsu XP 0.5 × battle XP. | SV `combat.ts:2768-2771`; `util.ts:2005`; `train.ts:796-834` |
| Battle pyramid | Quest type | Authored rewards; **+100 energy** on completion | SV C:1247-1253 |
| Dungeon | Sector; no level gate found | Battles give 0 XP; flat reward only on a full clear | SV `dungeon.ts:93`; `dungeonRewards.ts:24-66` |
| Raids | Sector / quest level | Damage thresholds, each claimable once | SV `raids.ts:218-227` |
| PvP (COMBAT) | Chunin and up | XP = ELO × 10 × streak bonus | SV `util.ts:2022-2027` |
| Hunting / gathering / crafting | Occupation, no rank gate | Profession XP and materials | SV `occupation.ts:104-140`; C:1743-1930 |
| Pets | Owner rank caps pet rank (Genin → pet rank 2-3) | Pet XP from battle and quest XP | SV C:720-731 |

### Combat scaling
- **Hit size is set by the attacker's level:** `calcHP(attackerLevel)/10 × power/40 × advantage`. **SV**
  - advantage = `clamp(1 + 0.75·((atk/def)^1.6 - 1), 0.01, 10)`.
  - There is no level-difference term (`tags.ts:1409-1494`).
- **Scaled AI get 50% of the player's stat budget** for the level (`profile.ts:307-358`; C:1306). **SV**

### Jutsu, items, bloodlines
- **Jutsu training:** **SV** (`train.ts:105-121, 508-639`)
  - Time `1 + level·inc` minutes, capped at 60.
  - Cost `floor(base^(1 + level/20))`, base D 50 … S 250.
  - Training stops at level 20; combat XP can take a jutsu to 25.
  - Equip slots for a free player: Student 7, Genin 8, Chunin 9, Jonin 10.
  - Letter ranks available: Student D, Genin C, Chunin A, Jonin S.
- **Shop:** `requiredLevel` is not checked on purchase, only on equip. **SV** (`item.ts` router `:3094-3179`)
  - Gear effects scale with the **item's** level; item XP comes from PvP only (C:1948-1951).
- **Bloodline:** roll odds S 0.5%, A 1%, B 5%, C 25% (C:1309-1316). A bloodline can also be bought with reputation. **SV**

## 3. The narrative spine as it exists live (CAP)
**Levels 1-30 have a connected thread:**
1. Getting Started → Road to Genin → GENIN.
2. Genin Trials 1-9 (L10-24). Each trial is the `prerequisiteQuestId` of a repeatable mission: Case Contracts (Ledger Sweep, Route Watch, Courier Intercept, Site Sweep) and Blacksteel Contracts (Shard Salvage, Supply Raid, Cleanup Detail, Iron Hunt, Perimeter Breach).
3. Capstone: the Kuroganekai: The Order of Black Steel GENIN pyramid (L10-50, 5 battles).
4. Then Debrief, then The Chunin Exams (L27-30) → CHUNIN.

**Levels 30-57 have no thread.**
- Visible chained content is limited to:
  - the Kuroganekai CHUNIN pyramid (L30-50; prerequisite: the GENIN pyramid)
  - Echoes in the Gust I-V (story, all L35-100)
  - unchained pyramids
- No rank gate until the Jonin Exam at 57.
- 580k XP, which is 3.0× everything in levels 1-30.

**Levels 57-70:** the Jonin Exam, then the next story quest at 70 (The Nameless Thorn).

**Visible quests with `requiredLevel ≤ 70`:** 262. Largest types: mission 76, gathering 35, achievement 30, hunting 26, event 17, starter 13, story 10, battle pyramid 7.

## 4. PvE ladder (battle pyramids, CAP)
| Band | Visible pyramids |
|---|---|
| 1-10 | none |
| 10-30 | Kuroganekai GENIN only |
| 30-50 | Kuroganekai CHUNIN; Skychain Monastery; Howling Hills |
| 50-70 | Ritual of Sotek - Lesser (L50-84, once only) |
| 70-100 | Kaeruun's Pyramid; Subaku Demon Castle; Ritual of Sotek; Tower of Endless Night ×3 (hidden) |

### The three named for rework
| Quest | Rank / window | Repeat | Battles | Enemies | Scaled | Pays |
|---|---|---|---|---|---|---|
| Howling Hills `fzEbIURkNYwRj_dotibrc` | D, L35-50 | daily, 100 | 11 | Howler, Dark Wolf, Cave Goblin, Harpy, White Wolf, Growler, Shrieker, Death's Maw, The Banshee (L10-15); Monster of the Moon (L35). Several are STUDENT rank above that rank's L10 cap. | yes | 6,000 XP, 30,000 ryo, 158 tokens, 152 prestige, item drops |
| Skychain Monastery `M85vPxofZIVijLpspm7Uu` | C, L30-50 | daily, **10 lifetime** | 15 | Gale Step Acolyte (45) → Abbot of the Broken Sky (55), all JONIN | **no**: a L30 player meets L45-55 | 8,438 XP, 39,375 ryo, 281 tokens, 270 prestige |
| The Drowned Fleet `n39gs_bqeLgXe6tLcqsPJ` | C, L40-100 | **once** | 15 | Tide Treader (40) → Tidelord Kaisei (50), all JONIN | **no** | same as Skychain. **Hidden.** |

Enemy levels and ranks come from `harvests/seed/42_INDEX_ai.json`. The full records are in the `profile.getAi` captures, keyed by `userId`.

## 5. Rough time scale (ASSUMED: unboosted single sources, an upper bound for orientation)
- **Energy training alone:** 1→70 about 164 days of continuous regen; 30→57 about 79 days.
- **Seed-value missions alone:** about 9k XP/day (9 full plus 11 at 0.4×), so 30→57 about 65 days.
- Against those rates, **one Howling Hills daily clear (6k XP) is about 40-65% of a day's mission XP.**
- Real rates combine sources and live multipliers. These figures are an upper bound until the live boosts are known.

## 6. Evidence the sim still needs
1. **Live game settings:** `trainingGainMultiplier`, `regenGainMultiplier`, mission/battle/jutsu XP multipliers, and any running boost timers.
   - These decide the time scale. Without them every time-to-level is **ASSUMED**.
2. **Real low-level player records:** level, stats, pools, gear, jutsu and levels, at three or four points (~10, ~30, ~50, ~70).
   - No captured record of a real player exists at any level.
3. **Battle logs** of a low-level player in a quest or pyramid fight, to calibrate damage and read rates (as `loveispure` did at level 100).
4. **AI rule profiles:**
   - 179 captured low-level AIs reference 163 profiles; only 19 profiles are captured.
   - A capture manifest for the profiles used by the spine and the three pyramids is the priority.
5. **Chunin and Jonin exam contents:** the starter quests above are captured; their objective graphs need reading for the actual requirements.
6. **Real player-time evidence:** how long players actually take per band (staff analytics, or the director's knowledge), to validate the activity model.

## 7. Decisions for the director (open)
1. **Scope of "the loop":**
   - Proposed in scope: training, Mission Hall, story/starter chain, pyramids, arena.
   - Out of scope for pass 1: PvP, professions, farming, tower defense.
2. **Engagement targets in measurable terms**, for example:
   - a story step or unlock every N hours of play
   - capstone win rate 60-80% at the bottom of its band
   - no stretch longer than X days without a new choice
3. **Player types:** new casual, engaged daily, returning, alt.
4. **Spine direction:** extend a Genin-Trials-shaped chain (story step → repeatable contract → pyramid capstone → exam) through the Chunin (30-57) and Jonin (57-70) eras, with the three old pyramids as Chunin-era capstones.
   - The story frame is the director's call (proposal under discussion 2026-11-04).
