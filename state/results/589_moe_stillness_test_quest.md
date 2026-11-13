# 589 MoE: the practice quest goes straight to a Stillness-only test AI

Why: director 2026-11-13 ~04:40 UTC: "Lets update the mother of Echoes test quest to use only that jutsu
straight away so I can confirm" (588's Stillness at animationScale 2.5 is buried in The Silence's rules:
she casts it only with a player within 3 hexes and after other moves).

Done 04:42-04:46 UTC over the connector under the run lock (claude), all hidden:
1. New AI "Stillness Scale Test", userId FotHaXVoYS4In_wM-qczO (profile.create), level 100, The Silence's
   avatar, 5,050 HP, only Stillness (A8c_3evIw6fOfnmKIkTgb) equipped, no items/effects. The game rescaled
   its stats to 278,260 (law 71); it has no damage move. Rules profile 8gkmO9NdoUyxLy1cfHn-H
   (ai.toggleAiProfile, then ai.updateAiProfile), includeDefaultRules false:
   cast Stillness on SELF (cooldown 3: rounds 1, 4, 7...), else end_turn. Read back.
2. The Mother of Echoes (Practice) YDmKO6fp2vBRnTf7fHWQZ, full-record quests.update built from push/496's
   record (live matched it: updatedAt 2026-11-06T02:42:34, 496 verdict match) with the live-only top-level
   fields added and the icon ref resolved:
   - d_intro1 choices: "Stillness scale test" -> b_act1 (new, first) and "Go deeper" -> d_intro2 (kept; a
     first try that dropped it was refused before saving: "Multiple starting objectives found").
   - b_act1 opponentAIs: [Sayo fJLcH1mpB1XHHGtNWwvzD, The Silence IhNR-W1FElTsrWw1KfuQ9] -> [FotHaXVoYS4In_wM-qczO];
     description "Act I: The Glasswright and the Deep" -> "Stillness scale test (animationScale 2.5)".
   Server diff named only those; read back hidden, isolated, no entry items, rewards and acts 2-3 unchanged.

RESTORE before any further practice of the real fight (this quest is the 469 practice): d_intro1 choices back
to [{"text":"Go deeper","nextObjectiveId":"d_intro2"}]; b_act1 opponentAIs back to
[{"ids":["fJLcH1mpB1XHHGtNWwvzD"],"number":1,"quantity":1},{"ids":["IhNR-W1FElTsrWw1KfuQ9"],"number":1,"quantity":1}]
and description back to "Act I: The Glasswright and the Deep". The test AI can then be deleted only on the
director's per-record yes.
