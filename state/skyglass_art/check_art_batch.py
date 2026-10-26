#!/usr/bin/env python3
"""Acceptance checks for the Skyglass/Crownhold art batch against the Ghost Ship art bible v0.4.

usage: python3 state/skyglass_art/check_art_batch.py [--base REF]   (REF: git ref whose items.json fixes numbering;
default main). Exit 0 = every check passed. Socket-free; reads the repo and runs the builder twice."""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = os.path.join(ROOT, "docs/design/ghost_ship_art_bible/")
base = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "main"
fails = []
def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok: fails.append(msg)

# 1. reproducible generation
outs = ["docs/handoffs/SKYGLASS_CROWNHOLD_ART_BATCH.md", "state/skyglass_art/items.json"]
def run():
    subprocess.run([sys.executable, os.path.join(ROOT, "state/skyglass_art/build_art_batch.py")], check=True, capture_output=True)
    return [hashlib.sha256(open(os.path.join(ROOT, o), "rb").read()).hexdigest() for o in outs]
h1, h2 = run(), run()
check(h1 == h2, "builder output is byte-identical across two runs")

blk = json.load(open(B + "blocks.json")); ros = json.load(open(B + "roster.json"))
items = json.load(open(os.path.join(ROOT, "state/skyglass_art/items.json")))
chars = ros["characters"]

# 2. register: exactly 20 distinct identities
check(len(chars) == 20, f"register holds exactly 20 identities ({len(chars)})")
for k in ("title", "slot", "head", "weapon_or_prop", "stance", "deliver"):
    vals = [c[k] for c in chars]
    check(len(set(vals)) == len(vals), f"register {k} values are all distinct")
check(len({(c["head"], c["weapon_or_prop"]) for c in chars}) == 20, "head + weapon/prop combinations are all distinct")
slots = sorted(c["slot"] for c in chars)
want = sorted(f"D{d}.{r}" for d in range(2, 6) for r in ("BOSS", "REG1", "REG2", "REG3", "REG4"))
check(slots == want, "register covers every Crownhold slot D2-D5 x BOSS/REG1-4 once")
for c in chars:
    miss = [k for k in ("title", "division", "rank", "head", "weapon_or_prop", "stance", "constraints") if k not in c]
    check(not miss, f"register entry {c['id']} {c['title']} has every required field")
check(sum(1 for c in chars if c.get("crown")) == 1 and [c for c in chars if c.get("crown")][0]["slot"] == "D5.BOSS",
      "the Command Crown belongs to Arakane only")

# 3. routing and stable numbering/filenames against the base
try:
    before = json.loads(subprocess.check_output(["git", "-C", ROOT, "show", f"{base}:state/skyglass_art/items.json"]))
except subprocess.CalledProcessError:
    before = None
num = [it for it in items if isinstance(it["no"], int)]
check([it["no"] for it in num] == list(range(1, 80)), "the batch is numbered 1-79 with no gaps")
if before:
    bmap = {it["no"]: it["deliver"] for it in before}
    diff = [it["no"] for it in num if bmap.get(it["no"]) != it["deliver"]]
    check(not diff, f"every delivery filename matches {base} ({diff or 'none changed'})")
byno = {it["no"]: it for it in items}
for c in chars:
    if c["batch_no"]:
        it = byno[c["batch_no"]]
        check(it["deliver"] == c["deliver"] and it["prompt"].startswith(c["title"] + ":"),
              f"#{c['batch_no']} routes to {c['title']} ({c['deliver']})")
check("A" in byno and byno["A"]["prompt"].startswith("Supreme Commander Arakane:"), "Arakane is brief A, outside the numbered batch")

# 4. shared block text and generator output agree
char_style = "\n".join([blk["style_character"], blk["costume_character"], blk["impression"], blk["chakra"],
                        blk["key_avatar"], blk["negative_character"]])
for c in chars:
    it = byno[c["batch_no"] if c["batch_no"] else "A"]
    exp = char_style if c["batch_no"] else char_style.replace("no tassels, no crown, ", "no tassels, no second crown, ")
    d = c["division"]; acc = ros["divisions"][d]["material_accent"]
    ok = (it["style"] == exp and blk["division_" + d] in it["prompt"]
          and blk["material_accent"].format(**acc) in it["prompt"]
          and (blk["regular"] in it["prompt"]) == (c["rank"] == "regular")
          and c["head"] in it["prompt"] and c["weapon_or_prop"] in it["prompt"] and c["stance"] in it["prompt"]
          and all(k in it["prompt"] for k in c["constraints"]))
    check(ok, f"{c['title']}: prompt carries its register entry and the shared blocks verbatim")

# 5. no obsolete designs or sci-fi scenery in pending prompts (negated clauses are ignored)
BANNED = ["gold", "gilded", "tassel", "filigree", "translucent", "ghost hand", "thread", "string", "crystal skin",
          "terminal", "screen", "cable", "capacitor", "relay", "laboratory", "lab coat", "specimen", "tank", "vat ",
          "operating theatre", "observation glass", "conduit", "valve", "pipe", "glitch", "clone", "automaton",
          "serial plate", "clipboard", "headset", "Grand Marshal", "Master of Arms", "Proving Proctor"]
def positive(text):
    text = re.sub(r"\(Used by:[^)]*\)", "", text)  # quest node names and ids, not visuals
    keep = []
    for cl in re.split(r"[,.;:\n]", text):
        t = cl.strip()
        if re.match(r"^(no|not|never|do not|without|keep: no|crown constraints: no)\b", t, re.I): continue
        keep.append(t)
    return " ".join(keep)
done = {1, 2, 3, 4}
for it in items:
    if it["no"] in done: continue
    txt = positive(it["prompt"])
    hits = [w for w in BANNED if w.lower() in txt.lower()]
    if it["no"] != "A" and it["target"] == "AI_AVATAR" and re.search(r"\bcrown\b", txt, re.I): hits.append("crown")
    check(not hits, f"#{it['no']} {it['name']}: no obsolete or futuristic terms ({hits or 'clean'})")

# 6. reference policy
for it in items:
    if it["no"] in done: continue
    refs = [r for _, r in it["refs"]]
    bad = [r for r in refs if r in ("arakane", "captain")]
    check(not bad and len(refs) <= 2, f"#{it['no']}: at most two references, never the Captain or old Arakane ({refs})")
    if it["target"] == "AI_AVATAR":
        check(refs == ["deck_warden"], f"#{it['no']}: character attaches the Deck Warden only")
for no in (5, 46, 47, 48):
    it = byno[no]
    check(bool(it.get("note")) or "arakane_v2" in [r for _, r in it["refs"]], f"#{no}: crown-dependent and gated on Arakane v2")

# 7. practical prompt length
mx = max(len(it["prompt"]) + len(it["style"]) for it in items)
check(mx < 4200, f"longest prompt body is {mx} characters (limit 4200)")

print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
