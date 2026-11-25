import json, sys, glob
sys.path.insert(0, glob.glob('/root/.claude/skills/synced/*/producing-tnr-art/scripts')[0])
from shotlist import render_prompt
spec = json.load(open(glob.glob('/root/.claude/skills/synced/*/producing-tnr-art/data/25x_DATA_art_spec.json')[0]))
SUIT = "black pinstriped haori jacket cut like a mob boss's suit over dark hakama"
SHOTS = [
 ("SCENE_BACKGROUND", None, "gobblefather_bg_trade_road", "Harvest Plains Trade Road (o1-o3, o15-o16)",
  "an autumn trade road across golden harvest fields at late afternoon, an abandoned wooden merchant wagon, scattered corn cobs and a few black feathers on the dirt road, distant thatched farmhouses, Edo-era countryside"),
 ("SCENE_BACKGROUND", None, "gobblefather_bg_tollgate", "The Drumstick Tollgate (o4-o6)",
  "a makeshift road checkpoint built from stolen wooden crates, sacks of grain and timber barriers across a country road, blank wooden signboards, autumn fields behind, Edo-era"),
 ("SCENE_BACKGROUND", None, "gobblefather_bg_golden_silo", "Golden Silo Warehouse (o7-o10)",
  "interior of a towering wooden grain warehouse, stacked crates, barrels overflowing with corn, an accountant's desk with ledgers and an abacus, dim lantern light, Edo-era"),
 ("SCENE_BACKGROUND", None, "gobblefather_bg_estate", "The Feathered Estate (o11)",
  "a grand Edo-era mansion at dusk beyond tall golden cornfields, gilded fence, stone turkey statues flanking the gate path, warm lanterns"),
 ("SCENE_BACKGROUND", None, "gobblefather_bg_office", "The Gobblefather's Office (o12-o12b)",
  "a dim luxurious study, heavy red curtains, dark lacquered wood furniture, a grand desk with a high-backed leather chair, a framed portrait of an enormous turkey on the wall, single lantern"),
 ("SCENE_BACKGROUND", None, "gobblefather_bg_feast_hall", "The Grand Feast Hall (o14)",
  "a magnificent banquet hall with a long table piled with a Thanksgiving harvest feast, pumpkins, corn, pies, autumn garlands, paper chandeliers, one end of the table smashed in half"),
 ("SCENE_CHARACTER", "full", "gobblefather_sc_hachiro", "Merchant Hachiro (o3)",
  "a nervous middle-aged human traveling merchant in a plain brown kimono and straw sandals, wringing his hands, worried face, empty coin pouch at his belt, accent colour copper"),
 ("SCENE_CHARACTER", "full", "gobblefather_sc_tony", "Tony Drumstick (o4-o6)",
  f"an enormous bulky anthropomorphic turkey brute in a {SUIT}, a stone-hard giant drumstick club resting on his shoulder, cocky grin, accent colour earth brown"),
 ("SCENE_CHARACTER", "full", "gobblefather_sc_vinny", "Vinny Drumstick (o4-o6)",
  f"a tall lean anthropomorphic turkey enforcer in a {SUIT}, wings folded calmly, gold rings on his feathered fingers, polite cold smile, accent colour gold"),
 ("SCENE_CHARACTER", "full", "gobblefather_sc_don_giblet", "Don Giblet (o9-o10)",
  "a calculating anthropomorphic turkey accountant in an expensive burgundy waistcoat over a dark robe, small round spectacles, holding a closed ledger against his chest, accent colour burgundy"),
 ("SCENE_CHARACTER", "full", "gobblefather_sc_gobblefather", "The Gobblefather (o12-o14)",
  f"an enormous imposing anthropomorphic turkey crime boss, {SUIT}, crimson silk tie, a gold ring on one wing, a tiny calm chicken perched on his shoulder, heavy-lidded eyes, accent colour crimson"),
 ("AI_AVATAR", None, "gobblefather_av_tony", "Tony Drumstick (AI)",
  f"bulky anthropomorphic turkey brute in a {SUIT}, swinging a stone-hard giant drumstick club, earth-brown accent"),
 ("AI_AVATAR", None, "gobblefather_av_vinny", "Vinny Drumstick (AI)",
  f"lean anthropomorphic turkey enforcer in a {SUIT}, wings raised in a guarding counter stance, gold rings on his feathered fingers, gold accent"),
 ("AI_AVATAR", None, "gobblefather_av_don_giblet", "Don Giblet (AI)",
  "anthropomorphic turkey accountant in a burgundy waistcoat and round spectacles, hurling a burst of golden corn kernels from an open ledger, gold accent"),
 ("AI_AVATAR", None, "gobblefather_av_gobblefather", "The Gobblefather (AI)",
  f"enormous anthropomorphic turkey crime boss in a {SUIT} and crimson tie, gold ring on one wing, gathering a blazing golden corn-shaped chakra sphere, crimson accent"),
 ("AI_AVATAR", None, "gobblefather_av_enforcer", "Feathered Enforcer (AI)",
  f"large anthropomorphic turkey bodyguard in a plain black haori suit, wing slap stance, grey accent"),
 ("AI_AVATAR", None, "gobblefather_av_corn_collector", "Corn Collector (AI)",
  "small wiry anthropomorphic turkey thug carrying a sack of stolen corn over one shoulder, throwing a corn cob, amber accent"),
 ("AI_AVATAR", None, "gobblefather_av_accountant", "Feathered Accountant (AI)",
  "thin anthropomorphic turkey clerk in a dark robe with an abacus and a brush, casting a glowing debt mark sigil, teal accent"),
 ("ICON", None, "gobblefather_badge_family_business", "Badge: Family Business",
  "golden signet ring set with a black feather wrapped around a golden ear of corn"),
 ("ICON", None, "gobblefather_item_golden_feathered_ring", "Item: Golden Feathered Ring (accessory)",
  "heavy gold ring set with a single black feather curled around a golden ear of corn"),
 ("ICON", None, "gobblefather_item_cane_skin", "Item: Gobblefather's Cane (weapon reskin)",
  "ceremonial black lacquered walking cane topped with a golden turkey head, held diagonally"),
]
out = ["# The Gobblefather: art shot list", "",
       "One image per fresh session. Deliver each file under the name shown; I process (key, crop, export webp), QC and wire it.",
       "Goah Way reuses his existing asset (Goah, j4tEoLtefH12sZwZY6MF-). Jutsu icons stay default (AI-only jutsu).", ""]
for n, (t, frame, name, use, subj) in enumerate(SHOTS, 1):
    p = render_prompt(spec, t, subj, frame)
    pos = p["positive"]
    lines = [pos]
    if p.get("subject_line"): lines.append(p["subject_line"])
    if p.get("costume_grammar"): lines.append("Costume note: replace the default ninja robe with the outfit in SUBJECT.")
    neg = p["negative"] + (", " + p["hard_negatives"] if p.get("hard_negatives") else "")
    out += [f"## {n}. {use}", f"`{name}.png` · {t}" + (f" ({frame})" if frame else ""), "", "```", "\n".join(lines), "", "Negative: " + neg, "```", ""]
    if p.get("reserve_note"): out[-4:-4] = []
open('/home/claude/tnr2/state/gobblefather/art_shotlist.md','w').write("\n".join(out))
print(len(SHOTS))
