# Scene background sweep - all ten Forsworn missions
Composed 2026-08-30 against capture harvests/inbox/tnr_results_1788127352899.json.
Every dialog node in all ten missions read against its assigned background.
Node ids asserted: no duplicates, no unknown ids, no unassigned dialog nodes.

## Totals
- 299 nodes: 272 dialog + 27 control (10 win_quest, 17 reset_quest)
- 144 dialog nodes change: 112 onto one of the eight new plates, 32 generic-to-generic repairs
- 128 dialog nodes keep their current background

## OUTRIGHT MISSING
27 nodes carry no sceneBackground. All 27 are win_quest or reset_quest control nodes;
ZERO dialog nodes are bare. Control nodes render no dwelt scene and there is no publish
gate on sceneBackground, so they are deliberately left empty - filling them would be
cosmetic writes on records that never display.

## MISMATCHES THAT EXIST TODAY (generic on the wrong generic - independent of this wave)
| mission | node | now | should be | why |
|---|---|---|---|---|
| Nothing to Report | n22 | Back Alley Night | Safehouse Room | the audit table at first light - an interior room, not a lane |
| Old Ghost | g29_x6 | Market Road Pre-Dawn | Back Alley Night | the drainage cut ending at the wall, not a market road |
| Old Ghost | g30 | Safehouse Room | Back Alley Night | "alone at the foot of the wall" - sat on an interior room |
| Old Ghost | g31 | Market Road Pre-Dawn | Back Alley Night | the foot of the wall |
| Old Ghost | g31_f_x7 | Market Road Pre-Dawn | Back Alley Night | the foot of the wall |
| Old Ghost | g18 | Doorway After | Safehouse Room | a back room off the tannery row - interior |
| Old Ghost | g19 | Back Alley Night | Safehouse Room | "the room is small and he keeps his voice down" - interior |
| Old Ghost | g14 | Back Alley Night | Market Road Pre-Dawn | walking a circle through the streets by day |
| Old Ghost | g15 | Back Alley Night | Doorway After | the fourth address, a woman at her door |
| Protection | p7 | Doorway After | Back Alley Night | watching the empty lane from the gate |
| Protection | p8b | Doorway After | Back Alley Night | watching the empty lane from the gate |
| The Long Winter | w5 | Doorway After | Safehouse Room | inside three houses - cold pot on a stove, chair pushed back |
| The Long Winter | w5b | Doorway After | Safehouse Room | inside three houses |
| The Long Winter | w6 | Hall Steps Before Dawn | Safehouse Room | the bureau file under seal - an office, not hall steps |
| The Long Winter | w6b | Hall Steps Before Dawn | Safehouse Room | the requisition file - an office |
| The Long Winter | w13 | Doorway After | Safehouse Room | the principal reading six pages seated - interior |
| The Long Winter | w14 | Doorway After | Safehouse Room | the principal answering the invoice - interior |
| The Loud Way | l5 | Hall Steps Before Dawn | Safehouse Room | the customs office bond book - an office |
| The Loud Way | l6 | Hall Steps Before Dawn | Safehouse Room | an hour with the paperwork - an office |
| The Loud Way | l9 | Back Alley Night | Doorway After | "eight feet of doorway" - literally a doorway |
| The Loud Way | l9f | Back Alley Night | Doorway After | "eight feet of doorway" |
| The Tenth Name | x16 | Hall Steps Before Dawn | Doorway After | the last runner standing in the annexe doorway |
| The Tenth Name | x16f | Hall Steps Before Dawn | Doorway After | through the annexe door |
| The Tenth Name | x8 | Doorway After | Safehouse Room | the cold room - interior |
| The Tenth Name | x9 | Doorway After | Safehouse Room | going through the coat - interior |
| The Tenth Name | x17 | Doorway After | Safehouse Room | "the wrong sort of room" - interior |
| The Tenth Name | x18 | Doorway After | Safehouse Room | the man who sells it - same room |
| The Tenth Name | x19 | Doorway After | Safehouse Room | two men come through the door behind you - same room |
| The Tenth Name | x19f | Doorway After | Safehouse Room | out of the window, room empty behind you |
| The Tenth Name | x20 | Hall Steps Before Dawn | Safehouse Room | the nine entries and their fields - reading, interior |
| The Tenth Name | x21 | Hall Steps Before Dawn | Safehouse Room | the reading room itself |
| The Tenth Name | x21b | Hall Steps Before Dawn | Safehouse Room | the reading room walls |

## NEW PLATE WIRING - by mission
### The Waystation  (17 dialog + 3 control)
- **Hall Steps Before Dawn** (4): w1 w2 w15 w16
- **Market Road Pre-Dawn** (1): w3
- **NEW: Pass Road Dusk** (11): w4 w5 w6 w6f w7 w8 w9 w10 w11 w12 w13
- **NEW: Waystation Door** (1): w14

### Chalk and Corner  (14 dialog + 2 control)
- **Hall Steps Before Dawn** (5): c1 c2 c3 c13 c14
- **Market Road Pre-Dawn** (5): c4 c5 c6 c8 c9
- **Back Alley Night** (4): c10 c11 c12 c12f

### Nothing to Report  (25 dialog + 2 control)
- **Hall Steps Before Dawn** (7): n1 n17 n18 n19 n20 n21 n21f
- **Safehouse Room** (8): n2 n3 n4a n4 n22 n23 n24 n25
- **Back Alley Night** (6): n5 n6 n10 n11 n12 n12f
- **Market Road Pre-Dawn** (2): n8 n9
- **NEW: Canal Frontage** (2): n13 n14

### Old Ghost  (42 dialog + 3 control)
- **NEW: Rooftop Eastern Quarter** (5): g5 g6 g25 g26 g29
- **NEW: Warehouse Loading Floor** (3): g20 g20_f_x2 g21
- **NEW: Drying Yard** (2): g24 g24_f_x3
- **NEW: East Road Ambush Site** (2): g16 g16_f_x1
- **Back Alley Night** (12): g9 g10 g22 g23 g27 g28 g28_f_x5 g28_x4 g29_x6 g30 g31 g31_f_x7
- **Safehouse Room** (7): g18 g19 g32 g33 g34 g35 g36
- **Hall Steps Before Dawn** (4): g1 g2 g3 g4
- **Market Road Pre-Dawn** (3): g7 g8 g14
- **Doorway After** (4): g11 g12 g13 g15

### Protection  (17 dialog + 2 control)
- **Hall Steps Before Dawn** (5): p1 p2 p14 p15 p16
- **NEW: Drying Yard** (9): p3 p5 p6 p8 p9 p11 p11f p12 p13
- **Back Alley Night** (3): p7 p8b p10

### The Empty Contract  (15 dialog + 2 control)
- **Hall Steps Before Dawn** (4): e1 e2 e3 e16
- **Doorway After** (3): e5 e10 e11
- **Back Alley Night** (5): e6 e12 e12f e13 e15
- **NEW: Rooftop Eastern Quarter** (3): e7 e14 e14f

### The Long Winter  (35 dialog + 3 control)
- **Safehouse Room** (13): w1 w2 w3 w4 w5 w5b w6 w6b w13 w14 w26 w27 w28
- **Back Alley Night** (2): w7 w7b
- **Market Road Pre-Dawn** (5): w9 w10 w11 w11f w12
- **NEW: Drying Yard** (15): w14b w15 w16 w17 w17b w18 w19 w20 w20f w21 w22 w23 w24 w24f w25

### The Loud Way  (29 dialog + 3 control)
- **Hall Steps Before Dawn** (1): l1
- **Safehouse Room** (5): l2 l3 l5 l6 l24
- **Doorway After** (3): l4 l9 l9f
- **NEW: Rooftop Eastern Quarter** (3): l7 l8 l8f
- **NEW: Warehouse Loading Floor** (17): l10 l11 l12 l13 l14 l15 l16 l17 l18 l19 l20 l21 l21f l22 l22f l23 l25

### The Tenth Name  (33 dialog + 3 control)
- **NEW: Canal Frontage** (8): x5 x5b x11 x12 x12f x14 x15 x15b
- **Doorway After** (2): x16 x16f
- **Safehouse Room** (20): x1 x2 x3 x4 x8 x9 x17 x18 x19 x19f x20 x21 x21b x22 x23 x24 x25 x26 x27 x28
- **Hall Steps Before Dawn** (2): x6 x6b
- **Back Alley Night** (1): x10

### Three Rounds  (45 dialog + 4 control)
- **Hall Steps Before Dawn** (3): r1 r2 r3
- **NEW: East Road Ambush Site** (18): r5 r8 r11 r12 r13 r14 r15 r16 r22 r22b r24 r25 r26 r27 r27f r31 r32 r33
- **Doorway After** (4): r18 r20 r21 r21b
- **Market Road Pre-Dawn** (4): r28 r29 r30 r30f
- **Safehouse Room** (3): r34 r46 r47
- **NEW: Drying Shed** (13): r35 r36 r37 r38 r39 r40 r40f r41 r41f r42 r43 r44 r45

## Plate reuse worth flagging
Four plates carry nodes outside the mission they were cut for. Each is a fiction match,
not a convenience:
- Warehouse Loading Floor -> Old Ghost g20 g20_f_x2 g21 (the warehouse off the cut)
- Drying Yard -> Protection p3 p5 p6 p8 p9 p11 p11f p12 p13 (a grain yard with a weighbridge - the same kind of place) and Old Ghost g24 g24_f_x3 (the dye works yard)
- Rooftop Eastern Quarter -> Loud Way l7 l8 l8f (the roofline to the warehouse gable) and Empty Contract e7 e14 e14f (over the roof edge, the dead end above the drying sheds)
- East Road Ambush Site -> Old Ghost g16 g16_f_x1 (the east verge and the treeline)
- Canal Frontage -> Nothing to Report n13 n14 (the towpath)

## Clusters that grew past the backlog spec
- Waystation: spec said w5-w13; w4 (the toll shed on the pass road) and w8 belong too.
- Long Winter: spec said w16-w25; the yard actually starts at w14b/w15.
- Loud Way: spec said "main set ~12"; the loading floor is 17 nodes, l10-l23 plus l25.
- Three Rounds: spec said r5-r16 and r37-r45; ambush also covers r22 r22b r24-r27f r31-r33, and the shed also covers r35 r36.

## Chalk and Corner
Zero changes. The only mission that was already correct on every node.
