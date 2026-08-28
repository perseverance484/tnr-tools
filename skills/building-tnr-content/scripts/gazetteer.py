"""Village sector gazetteer. longitude = x (west->east), latitude = y (south->north).
Sector is 26x26; law 54 wants stops two or more tiles off every edge, so everything
here sits inside 3..22. Named places exist so that a location visited more than once
gets the same tile, and so the village is laid out the same way in every mission."""
PLACES = {
    # village core
    "north_gate":        (12, 21), "wall_walk":      (12, 22),
    "market_row":        (11, 14), "market_stalls":  (10, 15),
    "back_alleys":       ( 8, 12), "unlit_lanes":    ( 9, 13),
    "records_hall":      (10, 18), "cold_room":      (11, 19),
    "reading_room":      (10, 19), "hall_approach":  (10, 17),
    "bureau":            (13, 17), "customs_office": (14, 16),
    "principal_street":  (12, 18), "victim_houses":  ( 9, 16),
    "coach_yard":        (14,  4), "grain_yard":     ( 7, 16),
    "back_room":         ( 9, 11),
    # tannery row, south-west
    "tannery_row":       ( 6,  8), "corner_stones":  ( 7, 10),
    "third_stone":       ( 8, 10), "dyers_wall":     ( 5,  9),
    "dyers_door":        ( 6,  9), "dyers_stair":    ( 5, 10),
    # canal and warehouse, east
    "canal_rooftop":     (18, 11), "canal_drain":    (19, 10),
    "warehouse_floor":   (19, 11), "warehouse_roof": (19, 12),
    "canal_door":        (18, 10), "towpath":        (17, 13),
    "canal_frontage":    (20,  9), "frontage_third": (20,  8),
    "frontage_chase":    (21,  9), "frontage_chain": (19,  8),
    # slums, east
    "slums":             (21,  6), "slums_circle":   (20,  5),
    "slums_slope":       (22,  5), "slums_drainage": (21,  4),
    "dye_works":         (19,  6),
    # north cut
    "drying_yard":       (15, 22),
    # east road, outside the walls
    "east_road_site":    (21, 19), "rock_line":      (20, 20),
    "relay_post":        (22, 16), "old_cut":        (22, 12),
    "north_trail":       (18, 22), "bait_stone":     (20, 14),
    "cut_south":         (22, 11), "shed_approach":  (22, 10),
    "ditch_line":        (22,  9),
    # pass road, north-west, outside the walls
    "toll_shed":         ( 6, 20), "pass_low":       ( 5, 21),
    "pass_high":         ( 4, 22), "stair_cut":      ( 3, 22),
    # battle ground added 2026-08-28: places a fight happens that no Action visits
    "chalk_alley":       ( 8, 11), "drying_sheds":   ( 4, 10),
    "dyers_roof":        ( 5,  8), "street_door":    (17, 10),
    "lane_ambush":       ( 9, 12), "hall_steps":     (10, 16),
    "waystation_door":   ( 3, 21), "pass_neck":      ( 4, 21),
    "field_line":        (18, 21), "drying_shed":    (22,  8),
    "east_verge":        (22,  7), "false_warehouse":(18,  7),
    "slums_lane":        (21,  5), "wall_foot":      (22,  4),
    "annexe_door":       (19,  9), "frontage_lane":  (20,  7),
}
BATTLES = {
 "sheet_chalk":       {"c12":"chalk_alley"},
 "sheet_contract":    {"e12":"dyers_roof","e14":"drying_sheds"},
 "sheet_thinice":     {"w6":"pass_low","w10":"pass_neck","w12":"waystation_door"},
 "sheet_protection":  {"p11":"grain_yard"},
 "sheet_loud":        {"l8":"canal_rooftop","l9":"street_door",
                       "l21":"warehouse_floor","l22":"warehouse_roof"},
 "sheet_report":      {"n12":"lane_ambush","n21":"hall_steps"},
 "sheet_threerounds": {"r27":"field_line","r30":"bait_stone",
                       "r40":"drying_shed","r41":"drying_shed"},
 "sheet_longwinter":  {"w11":"coach_yard","w20":"drying_yard","w24":"drying_yard"},
 "sheet_oldghost":    {"g16":"east_verge","g20":"false_warehouse","g24":"dye_works",
                       "g28":"slums_lane","g31":"wall_foot"},
 "sheet_tenthname":   {"x12":"frontage_lane","x16":"annexe_door","x19":"canal_frontage"},
}
ASSIGN = {
 "sheet_chalk":       {"c8":"tannery_row","c5":"corner_stones","c10":"third_stone"},
 "sheet_contract":    {"e6":"dyers_wall","e10":"dyers_door","e13":"dyers_stair"},
 "sheet_thinice":     {"w4":"toll_shed","w5":"pass_low","w9":"pass_high","w11":"stair_cut"},
 "sheet_protection":  {"p3":"grain_yard","p6":"grain_yard","p8":"grain_yard","p9":"grain_yard"},
 "sheet_loud":        {"l5":"customs_office","l7":"canal_rooftop","l11":"canal_drain",
                       "l14":"warehouse_floor","l17":"canal_door","l19":"warehouse_roof"},
 "sheet_report":      {"n5":"north_gate","n8":"market_row","n10":"unlit_lanes",
                       "n13":"towpath","n17":"hall_approach"},
 "sheet_threerounds": {"r5":"east_road_site","r12":"rock_line","r21":"relay_post","r22":"old_cut",
                       "r25":"north_trail","r28":"bait_stone","r31":"cut_south",
                       "r36":"shed_approach","r38":"ditch_line"},
 "sheet_longwinter":  {"w5":"victim_houses","w6":"bureau","w7":"principal_street","w9":"coach_yard",
                       "w15":"drying_yard","w18":"drying_yard","w21":"drying_yard"},
 "sheet_oldghost":    {"g5":"wall_walk","g7":"market_stalls","g9":"back_alleys","g11":"slums",
                       "g14":"slums_circle","g22":"dye_works","g26":"slums_slope","g29":"slums_drainage"},
 "sheet_tenthname":   {"x5":"canal_frontage","x6":"north_gate","x8":"cold_room","x11":"frontage_third",
                       "x14":"frontage_chase","x15":"frontage_chain","x17":"back_room","x21":"reading_room"},
}
