# Medical missions (dauntless)

Director (2026-11-10): "Medical missions also pay very well. You'll need to figure out the answers by using inference
and logic, they can be failed but answers dont change."

## Flow
- **Daily cap: 9 medical missions** ("daily medical mission limit of 9"). Do them first each day.
- `quests.startRandom {type:"medical", rank:"D", userLevel:100, userSector:177, userVillageId}` (rank A: "Setting not
  found"; D shows "missions up to Master rank"). Wakes the character.
- Read only each step's question and option texts (`quests.getAll {name, limit:1}` select
  `content.objectives.*.description` and `nextObjectiveId.*.text`), choose by reasoning, then look up just the chosen
  option's target id. Advance dialogs with `quests.checkRewards {questId, nextObjectiveId}`.
- move_to_location goals are re-targeted to sector 177: read coords from `profile.getUser`
  `userData.questData[i].goals[*].{longitude, latitude}`, then `travel.moveInSector` (with villageId + dest) and
  `quests.checkLocationQuest`. A defeat_opponents goal starts a fight at its spot (PvE loadouts).
- After the win_quest step: `quests.checkRewards {questId}` claims. Pays ~170,000 ryo + 1,000 tokens + 1,000 prestige
  + 2,000-3,000 medical exp. ~20 calls each.
- **Goal coordinates can change between runs of the same quest** (Zombie Outbreak run 2 moved every spot). Always
  re-read the goals right after starting; dialog choices sent before a move goal is done are silently ignored.

## Solved (answers don't change)
| Quest (id) | Path |
|---|---|
| The Crimson Bloom (90Yas_3N6eAfhUxSbvarz) | Hyper-Stimulation -> Test Water -> Find Suppressant -> Sturdy Root |
| The Ashen Lung (b6DKJZB3_6v54RDcBXYWi) | Foreign Inhalant -> Search the Eastern Shaft -> Draw It Out With a Poultice -> A Cooling Mint |
| Zombie Outbreak (QczZtQGOuODzNVA-_rnHs, pays 150k) | Check villagers -> Examine the bites -> lab -> Frostbite Leaf -> (Zombie Villager fight, 5,050 HP) -> lab -> Yes Ma'am -> tent |
| The Silent Bloom (9NCb8FSTTvJUPq__MqwFa) | Systemic Stasis -> Follow Wind -> (Wild Boar fight, 5,050 HP) -> Counteract Effect -> Aqueous Suspension |

Objective ids: Crimson omwNE, slbmR, NPt8F(11,19), AXcqm, -Z0yk(7,19), psp80, kTKP1, 9Tf3H(9,23), v28Hb.
Ashen al_diag, al_vector, al_move1(11,17), al_strategy, al_move2(17,7), al_bind, al_synth, al_move3(10,5), al_win.
Zombie qTwaY(24,12), vRQMl, rIIMe(12,7), PjMg4, m_sW9 fight(17,19), 7O9vU(12,7), 4KjRV, JuyL-(7,3), 7Vr9z.
Silent IYWsa, DQi1l, pThDl(20,10), boar(7,12), wAp8m, bhQvg(3,19), UXACt, OpyTj(19,13), yIwbX(3,14), X_Yq4.

## Log (2026-11-10 UTC)
| # | Quest | Result |
|---|---|---|
| 1 | Crimson Bloom | won, +170k |
| 2 | Ashen Lung | won, +170k |
| 3 | Silent Bloom | won, +170k |
| 4 | Silent Bloom | won, +170k |
| 5 | Crimson Bloom | won, +170k |
| 6 | Silent Bloom | won, +170k |
| 7 | Zombie Outbreak | won, +255k |
| 8 | Zombie Outbreak | won, +255k |
| 9 | Ashen Lung | won, +170k (cap reached; 9/day total ~1.70M ryo) |
