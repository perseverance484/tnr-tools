# 592 MoE: raw %target in two Saint jutsu texts

Why: the 591 run saw "The glass either side of %target goes quiet" (battle 671wW9Pb_u9_4jZTEpSJ_, Act III R7). The game
replaces %target only with the names of fighters the action hit (libs/combat/actions.ts ~1296-1306); a ground mark that
hits no one prints the token raw. Director go 2026-11-13 ~17:13 UTC (fix list "Approved").

Changed 17:20-17:24 UTC over the connector under the run lock, law 18/60 order on Sayo, Saint of Stillness
(k0hgSrghl_KcYs9ATVDJT): unequip the two, full-record jutsu.update, re-equip all 25.
- Hold Still (0yple4t11fS5B6F2fYbad) battleDescription: "...either side of %target goes quiet..." -> "...either side of
  you goes quiet. It minds where you would go, not where you are."
- Every Line Through You (1p44ivUB8TjzaPFiqyitx): "A line of glass runs through %target." -> "A line of glass runs across
  the hall. It bears one who stays, not one who walks along it."
Server diffs named only battleDescription (plus the default animationScale 1). Read back: Saint 25/25 equipped, 20,200
HP, stats and armour unchanged. An Absence (nwjETj5gD7gD68KomTmxF) already read "settles on the floor nearby" live.

Note: push/mother_of_echoes.gen.py's spec still carries the old texts; a rebuild from spec would bring them back.
