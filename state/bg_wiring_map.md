# Scene background wiring map - Forsworn backgrounds wave
Composed 2026-08-30 against capture harvests/inbox/tnr_results_1788127352899.json
(11 reads, ten missions incl. The Waystation, 445 asset rows). Node ids asserted
against live content: no duplicates, no unknown ids, no unassigned dialog nodes.

## Live generic ids (resolved from the capture, no longer truncated)
| short | id | name |
|---|---|---|
| Alley | wyMQkpiugsLs8BQpDdTf2 | Back Alley Night |
| Market | gXpaJL3VnawaQ5PGqSoAB | Market Road Pre-Dawn |
| Hall | JAh1c6Ykf_nUfM5Xk67DW | Hall Steps Before Dawn |
| Safe | XAjOr4zBngvaztvPd0Ls0 | Safehouse Room |
| Door | p76eudOzH1KfbpLzhBgrJ | Doorway After |

## Control nodes stay empty
27 nodes carry no sceneBackground: 10 win_quest + 17 reset_quest, zero dialog
nodes. Publish gate covers sceneCharacters only; control nodes render no dwelt
scene. They are NOT filled by this wave.

## Six specced clusters (unchanged from the backlog spec)
| plate | mission | nodes |
|---|---|---|
| Warehouse Loading Floor | The Loud Way | main set ~12 |
| Pass Road Dusk | The Waystation | w5-w13 |
| Waystation Door | The Waystation | w14 |
| East Road Ambush Site | Three Rounds | r5-r16 |
| Drying Shed | Three Rounds | r37-r45 |
| Drying Yard | The Long Winter | w16-w25 |

## Old Ghost - node by node (45 nodes: 42 assigned + 3 control)
| target | nodes | why |
|---|---|---|
| NEW Rooftop | g5 g6 g25 g26 g29 | the wall walk, the stakeout roofline, the watch, the run across four roofs |
| NEW Warehouse Floor | g20 g20_f_x2 g21 | the warehouse off the cut - the ambush, waking on the floor, two down in an empty building |
| NEW Drying Yard | g24 g24_f_x3 | "three of them in a yard" at the dye works |
| NEW Ambush Site | g16 g16_f_x1 | the east verge and the treeline - the plate is literally an east road with a treeline |
| Alley | g9 g10 g22 g23 g27 g28 g28_f_x5 g28_x4 g29_x6 g30 g31 g31_f_x7 | back alleys, street chase, lane fight, the drainage cut, the foot of the wall |
| Safe | g18 g19 g32 g33 g34 g35 g36 | back room off tannery row, the small room, the debrief |
| Hall | g1 g2 g3 g4 | missions hall and the board |
| Market | g7 g8 g14 | working the stalls, walking the circle |
| Door | g11 g12 g13 g15 | the Slums, the doss house, the fourth address |

CHANGED off their current generic: g5 g6 g25 g26 g29 g20 g20_f_x2 g21 g24
g24_f_x3 g16 g16_f_x1 g18 g29_x6 g30 g31 g31_f_x7.
Notable repairs: g30 sat on Safehouse Room while its text is "alone at the foot
of the wall"; g16/g16_f_x1 sat on Market Road while the text is a verge and a
treeline.

## The Tenth Name - node by node (36 nodes: 33 assigned + 3 control)
| target | nodes | why |
|---|---|---|
| NEW Canal Frontage | x5 x5b x11 x12 x12f x14 x15 x15b | the frontage, the marked stones, the lane at the chalk hour, the runner chain |
| Door | x16 x16f | the annexe doorway |
| Safe | x1 x2 x3 x4 x8 x9 x17 x18 x19 x19f x20 x21 x21b x22 x23 x24 x25 x26 x27 x28 | briefing room, cold room, the wrong sort of room, the reading room, the debrief |
| Hall | x6 x6b | the gate ledgers |
| Alley | x10 | planning the intercept |

FINDING that killed the cluster assumption: all 11 nodes sitting on Safehouse
Room are the briefing and debrief room (x1-x4, x22-x28). Swapping "the 11
Safehouse nodes" to the canal plate - the reading the backlog implied - would
have put a canal quay behind an officer reading a page across a table. The canal
nodes were on Market and Alley instead.

## Not swept
Chalk and Corner, Nothing to Report, Protection, The Empty Contract take no new
plate and were not re-examined node by node. A logic sweep of their generics is
a separate pass if wanted.
