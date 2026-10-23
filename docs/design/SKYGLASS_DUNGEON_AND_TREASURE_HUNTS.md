# Skyglass Wreck dungeon and treasure hunts — design

**Status:** DESIGN DIRECTION APPROVED (RUL-2026-10-23-003, -004, -005). Values, names, prose and art are open. Nothing here is a manifest or a live-write authorization.
**Date:** 2026-10-23
**Repository baseline:** `perseverance484/tnr-tools@0828f52`
**Game source pin:** `studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed` (2026-10-22). Every source claim below was read at this pin.
**Supersedes:** the profession-quest shape of Ghost Ship (Gather `6Ri-W5TtUrEMWpyYlnf_F`, Hunt `HckXVOf-qk6ESU9t5rxLh`) as the delivery for Skyglass content. Item, AI and jutsu rulings from RUL-2026-10-10 to RUL-2026-10-20 stay in force.

## 1. The loop

```
Skyglass Wreck (dungeon, parties of up to 3, repeatable, no gate)
  └─ clear → every member gets one chest
        ├─ regular loot: ryo, themed items, finished consumables, reward caches
        └─ bonus: treasure maps (tradable) — sell it or run it
              └─ map = entry item of one isolated Battle Pyramid "treasure hunt"
                    ├─ endings pay automatic loot (incl. hunt-signature reward)
                    └─ completion = player choice of reward caches ("choose")
```

The dungeon is where groups farm. The chest is its only drop. Maps turn the chest into access to short, story-led solo hunts. Every chest, cache and pick is useful to every player; nothing is profession-locked.

## 2. What the source supports (pin 107d7a86)

| Need | Supported? | Where |
|---|---|---|
| Party dungeon, 1–4 tiers × 5 floors, mini-boss ends each non-final tier, boss ends the last | Yes | `validators/dungeon.ts` superRefine |
| Up to 5 waves × 10 AIs per floor; first wave immediate | Yes | same; `ENCOUNTER_MAX_WAVE_DELAY_ROUNDS` 20 |
| Party fully healed after each floor; party wipe retries the floor | Yes | `server/utils/dungeon.ts`, `libs/dungeon.ts` |
| One-hour run; 3 idle rounds ends the run | Yes | `DUNGEON_RUN_SECONDS`, `DUNGEON_INACTIVE_ROUNDS` |
| Completion drops (item, jutsu, cache, package); each member rolls each drop | Yes | `libs/dungeonRewards.ts` `rollDungeonRewards` |
| A chest dropped as a plain `item` drop may be a **standard** reward item | Yes | only `cache`-type drops must be `weightedCache` (`routers/dungeon.ts` save) |
| AI equipment drops inside a dungeon | **No** | dungeon battles settle through `settleDungeonBattle`, not the ordinary payout |
| Dungeon entry gate (item, level, rank, cooldown) | **No** | no such fields in `dungeonContentSchema` |
| Player choice ("choose") on dungeons, caches or packages | **No** | `rewardMode` exists only on quest content |
| Quest entry items, consumed once at run start; every listed item required | Yes | `questEntryItemsSchema`, `libs/questRun.ts` |
| Isolated runs | Yes, `battlepyramid` only | `validators/objectives.ts` |
| Quest completion "choose": each reward item and each package becomes a card; pick 1–5 | Yes | `libs/rewardChoice.ts` |
| Restrict a choice card by profession | **No** | only owned content, equipped sage mode and mastery rank make a card unavailable |
| Weighted caches pay ryo | **No** | only item bundles; standard reward fields are inactive in weighted mode |

**Consequences built into this design**

- Ryo and exp become pickable cards in a "choose" quest, not automatic pay. Guaranteed pay therefore sits on hunt **ending objectives**, which grant everything; the completion reward is the pick.
- The Katana and Crown fragment cannot drop from a dungeon AI. They live on the Expedition's `w_Co` ending (where the 2026-10-13 capture already has them: Katana 3%, fragment 20%).
- **Open — attempt cap (finding, needs director decision):** `battlepyramid` is in `QuestTypesWithMaxAttempts`. `quests.ts` start runs `isAvailableUserQuests` without the attempt bypass, `previousAttempts` only increments, and `maxAttempts` is at most 100. "Map cost is the only limit" therefore means **at most 100 runs per player per hunt, lifetime**. Alternatives: accept 100; use `special` quests (started by consuming the map, no caps, but not isolated); or ask the game owner for an uncapped pyramid option.

## 3. The Skyglass Wreck (dungeon)

- **Shape:** two tiers, ten floors (RUL-2026-10-23-003). About six minutes a floor inside the one-hour limit.
- **Roster:** the Ghost Ship ensemble at its current JONIN caps (RUL-2026-10-12-012). Proposed mapping (balance for parties of three is the director's):

| Tier | Floor | Kind | Encounter |
|---|---|---|---|
| 1 Hull | 1 | floor | Deck Warden + Seal Charge + Core Canister |
| | 2 | floor | Core Horror |
| | 3 | floor | Wayfinder |
| | 4 | floor | Arsenal Keeper + Seal Charge |
| | 5 | mini-boss | Skyglass Sentinel |
| 2 Command | 6 | floor | Oathkeeper |
| | 7 | floor | First Blade, then a Deck Warden wave |
| | 8 | floor | The Captain |
| | 9 | floor | Sealwright |
| | 10 | boss | Crowned Captain |

- **Placement:** in the open, between land and sea (a shoreline sector). Sector, coordinates, biome and entrance art are open.
- **Rewards:** direct ryo/exp on clear (optional), plus exactly one chest drop at 100% ×1. Each member rolls it, so each player receives one chest.
- **Known AI issue to fix before reuse:** Skyglass Sentinel rules 0, 1, 3, 4 reference jutsu it does not carry (QA 2026-10-20).

## 4. The chest

Standard-mode consumable (independent lines, like Ornate and the War Caches), dropped as a plain `item`:

- **Guaranteed:** ryo and one Skyglass themed item (for example Skyglass Serum).
- **Regular lines:** finished consumables in ×5/×10/×20 stacks (RUL-2026-10-13-002).
- **Uncommon lines:** one of the reward caches (§5), Ornate Chest, Rare Jewels.
- **Bonus lines:** one independent line per treasure map. Independent lines mean a map is **on top of** the regular loot, never instead of it.
- **Jackpot:** Lion Token, as on the War Caches.

Open: chest name and art, tradability of the chest itself, every rate.

## 5. Reward caches — finished items

Profession material chests leave the reward plan. Reward caches pay **finished items** everyone can use (RUL-2026-10-23-005). The template is the live War Cache family (Earthen, Ember, Gale, Storm, Tide): a **shared kit** plus a **signature line**.

War Cache kit (push/95 capture): Venom Cask, Chakra Pill II, Stamina Pill II, Senbon Needles, Elite Smoke Bomb, Dr. Kim's Poison Potion, Dr. Kim's Miracle Potion, Bloodcore Ore, Lion Token 1%; signature = that element's kunai ×10/×20.

| Cache (live id, hidden) | Kit | Signature |
|---|---|---|
| Medicine Inro `ixEKlJ0MmDrX7JoMNJVhi` | Chakra Pill II, Stamina Pill II, Small Health Pill | Pill Pack; rare Dr. Kim's Miracle Potion |
| Shinobi Tool Pouch `6PguSHDJikU8y35qGcBWa` | Smoke Pellet, Senbon Needles, Elite Smoke Bomb, Venom Cask | an elemental kunai stack |
| Sage's Strongbox `h-d58UCSuHN8EZKbLjT5R` | Soldier Pill, Enemy Pill | Mona's Mermaid Song; rare Forbidden Jutsu Scroll (Nexus or Rebirth) |

These three are the exemplars for every new item-reward setup. Each needs a full edit replacing its current material lines (built by push/97). Open: weighted vs standard mode per cache, lines, rates.

## 6. Treasure hunts (Battle Pyramids)

**Format:** about 15–25 nodes, 3–5 fights and one boss, about 10–15 minutes. `battlepyramid`, isolated, entry = its own map. One signature mechanic, one signature reward on the ending, a "choose" pick of reward caches at completion. New bosses, reused Ghost Ship crew (RUL-2026-10-23-004).

| Hunt | Hook | Signature mechanic | Signature reward | Map tier |
|---|---|---|---|---|
| The Silent Bastion | the deserted fortress that issued the last directive | protocol choice before the boss (Medical heals, Combat buffs); one or two divisions plus Arakane | open | uncommon |
| The Drowned Foundry | the flooded works where Skyglass was smelted | timed filament collection under rupture threat; stay for more or leave | Skyglass Filament bundles | common |
| The Quarantine Vault | sealed archive | riddle seals; a wrong answer diverts to the alarm route instead of failing | the only direct Skyglass Crystal chance | uncommon |
| The Skyglass Expedition | the original Ghost Ship adventure, preserved | the full 83-node quest with six endings and the seal puzzle | **Skyglass Katana 3% and Crown fragment 20%, Expedition only** | rare |

Later slate (not yet approved for development): Wreck of the Tender (real-coordinate dig across sea sectors), The Crownmaker's Forge (must not compete with the Expedition's Katana/fragment draw).

**Silent Bastion source:** its 99-node design (RUL-2026-10-15-001) lives on side branches, newest `claude/silent-bastion-authoring-69za5u@6271e1f`. The hunt format cuts it to one or two divisions; which divisions survive is the director's.

**Expedition source:** a new `battlepyramid` quest reproducing the newest capture of the original (push/98, `harvests/inbox/tnr_results_1791903144042.json`), minus profession gates, Gatherer/Hunter chest lines replaced by universal loot, plus `entryItems`, `isolated` and a "choose" completion. A fresh read-only capture is required before building it.

## 7. Retirement of the profession quests

Both Ghost Ship profession quests are retired (RUL-2026-10-23-003). Mechanism (hide vs delete) and timing are the director's. Players who never finished them lose nothing they had: the Expedition carries the content, and the Skyglass items stay live.

## 8. Build plan and tooling

| Piece | Forge today | Notes |
|---|---|---|
| Chest, maps, reward cache edits | yes (`item`) | suggest mode allowed for edits; creates that other records reference cannot go through suggest mode |
| Hunts | yes (`quest`) | suggest mode refuses quests; director runs them |
| Hunt bosses | yes (`ai`, `aiProfile`) | |
| Reward packages (if used) | **no** | catalog editor in game, or Lane A |
| The dungeon | **no** | in-game editor from a spec, or Lane A (contract extraction for dungeon and reward packages, a Forge recipe, tests, `fable/*` + ChatGPT review) |

Validator gaps found: `validate.py` does not check `rewardMode`, `rewardPickCount`, `reward_packages` or a `weightedCache` body; Forge checks key names only (`forge/src/runner/nested.json`).

## 9. Live-state drift to recapture before building

From committed evidence only (newest captures listed in the 2026-10-23 research):

- quests unhidden and re-dated outside any push; ended 2026-10-19; current state unknown;
- `w_Co` Katana 3% / fragment 20% lines and the Mystery Chest's 10% Reliquary line added outside any push;
- Crowned Captain Katana drop 0% and fragment line gone by 2026-10-21;
- Skyglass items unhidden outside any push; never captured with `item.get`;
- pushes 132/139/140 sent as suggestions; applied status unrecorded;
- crafting-cache step B (unhide, `w_B2` lines) never run.

## 10. Open decisions

1. Attempt cap (§2).
2. Chest name, art, tradability and all rates.
3. Weighted or standard mode per reward cache; their lines and rates.
4. Pyramid pick: pick 1 or 2; War Caches as-is or new Skyglass elemental caches; package bundles or not.
5. Dungeon sector and coordinates, biome, entrance art.
6. Silent Bastion: which divisions survive; Bastion signature reward.
7. Hunt bosses: names, kits, art.
8. Retirement mechanism and timing.
9. Build route for the dungeon: in-game editor or Lane A.
