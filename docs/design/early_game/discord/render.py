"""Render the early-game review infographics (Discord thread) to PNG.

python3 -I render.py   (needs playwright + a Chrome/Chromium; writes *.png next to this file)
Content mirrors docs/design/early_game/LEVELLING_DESIGN.md (RUL-2026-11-04-116).
"""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
W = 1200

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:%dpx;background:#14131a;color:#e9e4d8;font-family:Inter,sans-serif;font-size:20px;line-height:1.35}
.card{padding:44px 48px 40px;background:
  radial-gradient(1200px 400px at 100%% 0%%,rgba(140,92,214,.16),transparent 60%%),
  radial-gradient(900px 400px at 0%% 100%%,rgba(214,92,62,.10),transparent 60%%),#14131a}
.kicker{font-size:15px;letter-spacing:.18em;text-transform:uppercase;color:#a99fd6;font-weight:600}
h1{font-family:Lora,serif;font-weight:700;font-size:46px;line-height:1.1;margin:8px 0 6px;color:#f4efe3}
.sub{color:#b9b2a3;font-size:20px;margin-bottom:28px}
.foot{margin-top:26px;color:#8d8778;font-size:14px;letter-spacing:.04em}
.violet{color:#b48cff}.ver{color:#ff8a65}.jade{color:#7fd1a8}.gold{color:#f2c46d}.mute{color:#8d8778}
""" % W

def page(body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{body[0]}</style></head><body><div class='card'>{body[1]}</div></body></html>"

# ---------- 1. Where the thread breaks ----------
def lvl(x):  # level 1..70 -> % across the bar
    return (x - 1) / 69 * 100

def seg(a, b, cls, label=""):
    return f"<div class='seg {cls}' style='left:{lvl(a)}%;width:{lvl(b)-lvl(a)}%'><span>{label}</span></div>"

TICKS = "".join(f"<div class='tick' style='left:{lvl(t)}%'><span>{t}</span></div>" for t in [1,10,20,30,40,50,57,70])
IMG1 = ("""
.row{margin:0 0 30px}.lab{font-weight:700;font-size:19px;margin-bottom:10px;display:flex;gap:12px;align-items:baseline}
.lab small{font-weight:500;color:#9a9384;font-size:16px}
.bar{position:relative;height:62px;border-radius:10px;background:#211f2a;overflow:hidden}
.seg{position:absolute;top:0;bottom:0;display:flex;align-items:center;justify-content:center;border-right:2px solid #14131a}
.seg span{font-size:15px;font-weight:700;white-space:nowrap;padding:0 6px}
.ok{background:#2f6f55}.gap{background:repeating-linear-gradient(135deg,#4a2420 0 12px,#3a1d1a 12px 24px)}
.gap span{color:#ffb4a0}.dead{background:#7a2b23}.exam{background:#c9a24a;color:#1b1710}
.c1{background:#2f6f55}.c2a{background:#5b3f9e}.c2b{background:#6c4bb8}.c2c{background:#7d58d0}.c3{background:#b4532f}
.axis{position:relative;height:30px;margin-top:6px}
.tick{position:absolute;top:0;transform:translateX(-50%);font-size:15px;color:#9a9384;font-weight:600}
.tick:before{content:'';display:block;width:2px;height:8px;background:#4a4658;margin:0 auto 3px}
.leg{display:flex;align-items:center;flex-wrap:wrap;gap:8px 10px;font-size:15px;color:#b9b2a3;margin-top:4px}
.leg i{display:inline-block;width:16px;height:16px;border-radius:4px;margin-left:10px}.leg i:first-child{margin-left:0}
.leg i.h{background:repeating-linear-gradient(135deg,#6a3028 0 4px,#3a1d1a 4px 8px)}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px}
.stat{background:#1d1b25;border:1px solid #2c2938;border-radius:12px;padding:18px 20px}
.stat b{display:block;font-family:Lora,serif;font-size:36px;color:#ff8a65;line-height:1}
.stat p{color:#cfc8b8;font-size:17px;margin-top:8px}
""", f"""
<div class='kicker'>Early game rework · levels 1-70</div>
<h1>Where the story thread breaks</h1>
<div class='sub'>Visible live content today vs. the approved spine</div>
<div class='row'><div class='lab'>Today <small>chained story content</small></div>
<div class='bar'>{seg(1,30,'ok','Genin Trials chain')}{seg(30,40,'gap','no thread')}{seg(40,50,'dead','nothing unlocks')}{seg(50,57,'gap','')}{seg(57,59,'exam','')}{seg(59,70,'gap','no thread')}</div>
<div class='axis'>{TICKS}</div>
<div class='leg'><i style='background:#2f6f55'></i>Story chain<i class='h'></i>No thread (580k XP from 30 to 57)<i style='background:#7a2b23'></i>Nothing unlocks<i style='background:#c9a24a'></i>Jonin Exam</div></div>
<div class='row'><div class='lab'>Proposed <small>one case, three chapters</small></div>
<div class='bar'>{seg(1,30,'c1','Ch.1 Academy & Genin')}{seg(30,39,'c2a','Act I')}{seg(39,48,'c2b','Act II')}{seg(48,57,'c2c','Act III')}{seg(57,70,'c3','Ch.3 The Fifth Seal')}</div>
<div class='axis'>{TICKS}</div></div>
<div class='stats'>
<div class='stat'><b>27 levels</b><p>between the Chunin Exams and the next chained quest</p></div>
<div class='stat'><b>0</b><p>visible quests unlocking anywhere in levels 40-49</p></div>
<div class='stat'><b>0</b><p>system intros (professions, pets, clans) in levels 10-30</p></div>
</div>
<div class='foot'>Source: 235 visible live quests with required level ≤ 70 (captures to 2026-11-04)</div>
""")

# ---------- 2. Chapter 2 acts ----------
def act(n, title, lv, attach, contracts, cap, caplv, why, col):
    cs = "".join(f"<li>{c}</li>" for c in contracts)
    return f"""<div class='act' style='--c:{col}'>
<div class='ah'><span class='an'>ACT {n}</span><span class='al'>Lv {lv}</span></div>
<div class='at'>{title}</div>
<div class='k'>Attaches to</div><div class='v'>{attach}</div>
<div class='k'>Unlocks contracts</div><ul>{cs}</ul>
<div class='cap'><div class='k'>Capstone · Lv {caplv}</div><div class='cn'>{cap}</div><div class='cw'>{why}</div></div></div>"""

IMG2 = ("""
.acts{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.act{background:#1d1b25;border:1px solid #2c2938;border-top:6px solid var(--c);border-radius:14px;padding:20px 20px 18px;display:flex;flex-direction:column}
.ah{display:flex;justify-content:space-between;font-size:14px;font-weight:700;letter-spacing:.12em}
.an{color:var(--c)}.al{color:#9a9384}
.at{font-family:Lora,serif;font-size:27px;font-weight:700;margin:6px 0 14px;color:#f4efe3}
.k{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#9a9384;font-weight:700;margin-top:6px}
.v{font-size:17px;color:#d9d2c2;margin:4px 0 10px}
ul{list-style:none;margin:6px 0 14px}li{font-size:17px;padding:5px 0 5px 18px;position:relative;color:#e9e4d8}
li:before{content:'';position:absolute;left:0;top:13px;width:8px;height:8px;border-radius:2px;background:var(--c)}
.cap{margin-top:auto;background:#262331;border-radius:10px;padding:14px}
.cn{font-family:Lora,serif;font-size:23px;font-weight:700;color:#f2c46d;margin:4px 0 6px}
.cw{font-size:15px;color:#cfc8b8}
.arc{display:flex;align-items:center;gap:14px;margin-top:22px;font-size:18px;color:#d9d2c2}
.pill{background:#f2c46d;color:#1b1710;font-weight:800;border-radius:999px;padding:6px 14px;font-size:15px;letter-spacing:.06em}
""", "<div class='kicker'>Chapter 2 · Chunin era · levels 30-57</div><h1>The Violet Road</h1>"
"<div class='sub'>The stronghold was only a depot. Follow the blacksteel by road, mountain and sea.</div><div class='acts'>"
+ act("I","Waystation","30-38","Kuroganekai CHUNIN pyramid; post roads and checkpoints",
      ["Checkpoint Inspection","Night Caravan Escort","Pass-Forger Bounty"],"Howling Hills","33-40",
      "The Monster of the Moon becomes an Iron Aberration; the wolves are being driven.","#8b63e6")
+ act("II","The Sealed Route","39-47","Skychain's split order and the Abbot's existing grievance",
      ["Mountain Courier","Bell-Tower Watch","Debt-Note Recovery"],"Skychain Monastery","41-48",
      "Scaled to the player, and the 10-clear lifetime cap lifted.","#a07cf0")
+ act("III","Tide at Kaiyo","48-56","Kaiyo, the canon neutral port beyond village law",
      ["Harbour Patrol","Wreck Salvage","Manifest Interdiction"],"The Drowned Fleet","49-56",
      "Unhidden and repeatable; fills the empty 40s.","#c4a6ff")
+ "</div><div class='arc'><span class='pill'>PAYOFF</span>The flagship's orders name the commander and reveal the blacksteel is for an engine → Jonin Exam (57)</div>"
"<div class='foot'>Working titles. Names, reward values and capstone scaling are open for review.</div>")

# ---------- 3. Capstone ladder ----------
STEPS = [
    ("24-30","Kuroganekai GENIN","Window fix: after the Trials, not at 10","#2f6f55","FIX"),
    ("30-36","Kuroganekai CHUNIN","Act I opener, or folded into Act I","#5b3f9e","OPEN"),
    ("33-40","Howling Hills","Re-band · re-theme the Moon · fix ranks","#6c4bb8","REWORK"),
    ("41-48","Skychain Monastery","Re-band · scale · lift 10-clear cap","#7d58d0","REWORK"),
    ("49-56","The Drowned Fleet","Unhide · repeatable · re-band","#9a74e8","REWORK"),
    ("60-64","Blacksteel Foundry","New capstone","#b4532f","NEW"),
    ("66-70","Engine Site","New · hands off to 70+ endgame","#d2683c","NEW"),
]
def steps():
    out = []
    for i, (lv, name, note, col, tag) in enumerate(STEPS):
        out.append(f"<div class='st' style='--c:{col};margin-left:{i*58}px'><div class='lv'>Lv {lv}</div>"
                   f"<div class='nm'>{name}</div><div class='nt'>{note}</div><div class='tg'>{tag}</div></div>")
    return "".join(out)
IMG3 = ("""
.ladder{display:flex;flex-direction:column-reverse;gap:10px}
.st{display:grid;grid-template-columns:110px 300px 1fr 92px;align-items:center;gap:14px;background:#1d1b25;border:1px solid #2c2938;border-left:8px solid var(--c);border-radius:12px;padding:14px 18px;width:calc(100% - 348px)}
.lv{font-weight:800;color:var(--c);font-size:18px;filter:brightness(1.35)}
.nm{font-family:Lora,serif;font-weight:700;font-size:23px;color:#f4efe3}
.nt{font-size:16px;color:#cfc8b8}
.tg{justify-self:end;font-size:12px;font-weight:800;letter-spacing:.14em;background:var(--c);color:#fff;border-radius:999px;padding:5px 10px}
.end{margin:0 0 10px 406px;font-size:16px;color:#f2c46d;font-weight:700;letter-spacing:.06em}
""", "<div class='kicker'>PvE ladder · battle pyramids</div><h1>The capstone ladder</h1>"
"<div class='sub'>One daily capstone per act. First clear advances the story; repeats pay the band.</div>"
"<div class='end'>▲ Lv 70+: Subaku · Tower of Endless Night · Ritual of Sotek</div>"
f"<div class='ladder'>{steps()}</div>"
"<div class='foot'>Open: scaled-to-player vs fixed-level capstones. Either way, the fight must hold at the bottom of its band.</div>")

# ---------- 4. Systems steering + Field Office ----------
NODES = [
    ("10","Bloodline check","Science Building, at Genin"),
    ("11","Pick a guild","Choose your one trade"),
    ("12","Craft · Gather · Hunt","A smith reads the shard · herbs for the wounded · a beast on the route"),
    ("14","Farming & cooking","The waystation cook"),
    ("16","Pets","A Bondkeeper creature tracks the aberration"),
    ("18","Medical","Raid-site wounded"),
    ("20","Clans","Contract crews"),
]
def nodes():
    return "".join(f"<div class='nd'><div class='dot'>{l}</div><div class='nn'>{n}</div><div class='nw'>{w}</div></div>" for l, n, w in NODES)
IMG4 = ("""
.tl{display:grid;grid-template-columns:repeat(7,1fr);gap:10px;position:relative;margin-bottom:30px}
.tl:before{content:'';position:absolute;left:5%;right:5%;top:31px;height:4px;background:linear-gradient(90deg,#2f6f55,#7fd1a8)}
.nd{text-align:center;position:relative}
.dot{width:66px;height:66px;margin:0 auto 10px;border-radius:50%;background:#14131a;border:4px solid #7fd1a8;display:flex;align-items:center;justify-content:center;font-family:Lora,serif;font-weight:700;font-size:24px;color:#f4efe3}
.nn{font-weight:800;font-size:17px;color:#f4efe3}
.nw{font-size:14px;color:#b9b2a3;margin-top:4px;padding:0 4px}
.board{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.b{background:#1d1b25;border:1px solid #2c2938;border-radius:14px;padding:18px}
.bt{font-size:13px;letter-spacing:.14em;font-weight:800;color:var(--c)}
.bn{font-family:Lora,serif;font-size:25px;font-weight:700;margin:4px 0 8px;color:#f4efe3}
.bd{font-size:16px;color:#cfc8b8}
h2{font-family:Lora,serif;font-size:30px;margin:4px 0 14px;color:#f4efe3}
""", "<div class='kicker'>Levels 10-20 · story reasons for every system</div><h1>Steering into systems</h1>"
"<div class='sub'>Today all 61 profession quests open at level 1 with no introduction.</div>"
f"<div class='tl'>{nodes()}</div>"
"<h2>Field Office board <span class='mute' style='font-size:20px;font-family:Inter'>· dailies, every band</span></h2><div class='board'>"
"<div class='b' style='--c:#ff8a65'><div class='bt'>DAILY</div><div class='bn'>Duty</div><div class='bd'>Missions, arena or encounters</div></div>"
"<div class='b' style='--c:#7fd1a8'><div class='bt'>DAILY</div><div class='bn'>Trade</div><div class='bd'>Gather, hunt or craft X. Your trade only.</div></div>"
"<div class='b' style='--c:#a99fd6'><div class='bt'>DAILY</div><div class='bn'>Discipline</div><div class='bd'>Minutes of training</div></div>"
"<div class='b' style='--c:#f2c46d'><div class='bt'>WEEKLY</div><div class='bn'>Capstone</div><div class='bd'>Clear your band's pyramid</div></div>"
"</div><div class='foot'>Uses objective counters no live quest uses yet: herbs gathered, creatures hunted, items crafted.</div>")

# ---------- 5. The case at a glance ----------
LEADS = [
    ("10-24","The case desk","Ledgers, conductors, a violet-veined shard","#2f6f55",""),
    ("24-30","The stronghold","Only a depot. The commander needs a name.","#2f6f55",""),
    ("30-40","Post road · Howling Hills","A tally: “high route, Skychain, paid in full”","#6c4bb8",""),
    ("39-48","Skychain Monastery","The courier ledger ends at Kaiyo","#7d58d0",""),
    ("48-56","Kaiyo · The Drowned Fleet","The commander is named. The parts are an engine.","#9a74e8",""),
    ("57-64","Jonin Exam · The Foundry","Blacksteel is iron soaked in Null Chakra","#b4532f",""),
    ("64-70","Heart of Balance","The engine at the first Kage's seal","#f2c46d","end"),
]
def leads():
    out = []
    for i, (lv, name, clue, col, end) in enumerate(LEADS):
        if i: out.append("<div class='ar'></div>")
        out.append(f"<div class='ld {end}' style='--c:{col}'><div class='lv'>Lv {lv}</div><div class='nm'>{name}</div><div class='cl'>{clue}</div></div>")
    return "".join(out)
IMG5 = ("""
.ld{display:grid;grid-template-columns:120px 380px 1fr;align-items:center;gap:16px;background:#1d1b25;border:1px solid #2c2938;border-left:8px solid var(--c);border-radius:12px;padding:16px 20px}
.ld .lv{font-weight:800;color:var(--c);font-size:18px;filter:brightness(1.3)}
.ld .nm{font-family:Lora,serif;font-weight:700;font-size:25px;color:#f4efe3}
.ld .cl{font-size:18px;color:#cfc8b8}
.ld.end{background:rgba(242,196,109,.12);border-color:#f2c46d}.ld.end .cl{color:#f4efe3}
.ar{width:2px;height:22px;background:#4a4658;margin:0 0 0 60px;position:relative}
.ar:after{content:'';position:absolute;left:-5px;bottom:-2px;border:6px solid transparent;border-top:8px solid #4a4658}
.leg2{display:flex;gap:18px;margin-top:22px;font-size:15px;color:#b9b2a3}.leg2 i{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-2px}
""", "<div class='kicker'>The Kuroganekai case · levels 10-70</div><h1>Every lead points to the Heart of Balance</h1>"
"<div class='sub'>Each place hands the player the clue that leads to the next.</div>"
f"{leads()}"
"<div class='leg2'><span><i style='background:#2f6f55'></i>Ch.1 Academy &amp; Genin (live)</span><span><i style='background:#7d58d0'></i>Ch.2 The Violet Road</span><span><i style='background:#b4532f'></i>Ch.3 The Fifth Seal</span></div>"
"<div class='foot'>Working titles. The commander's name and motive are open for review.</div>")

IMAGES = {"5_case_at_a_glance": IMG5,
"1_thread_breaks": IMG1, "2_violet_road": IMG2, "3_capstone_ladder": IMG3, "4_systems_and_dailies": IMG4}

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": W, "height": 800}, device_scale_factor=2)
        for name, img in IMAGES.items():
            pg.set_content(page(img), wait_until="load")
            pg.wait_for_timeout(150)
            pg.locator(".card").screenshot(path=os.path.join(HERE, f"{name}.png"))
            print("wrote", name)
        b.close()
