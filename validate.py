#!/usr/bin/env python3
"""Validate a builder manifest in the container, BEFORE it reaches the browser.

Every push failure this project has had was catchable without a network round
trip: a field the validator does not have, an enum value that does not exist,
a rule shape authored from memory. This runs the same checks locally, against
45c_DATA_constructors.json (generated from the TNR source), plus the coded
invariants that keep getting linted by hand.

Usage:
  python3 tnr_validate.py manifest.json [--ctors 45c_DATA_constructors.json] [--strict]

Exit code 0 clean, 1 errors found. --strict promotes warnings to errors.

What it checks
  shapes      every AI rule condition/action, every effect tag, every quest
              objective: unknown fields, bad enums, bounds, missing discriminant
  invariants  hidden:true on creates; rule sets end unconditional; multi-choice
              dialogs fork to distinct targets; quest graph has one start and no
              dangling edges; battle nodes carry failObjectiveId + opponentAIs
  hygiene     em dashes in player-facing dialog; unresolved @refs; id length;
              imgSizes present and matching disk; debug keys left in payloads
"""
import json, os, re, sys

DASHES = ("\u2014", "\u2013")
ID_LEN = 21
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CAP_100 = ("maxLevel", "maxAttempts", "maxCompletes")
FORMULA_TAGS = ("damage", "pierce", "wound")
POOL = {}          # code -> record, loaded from 32b
POOL_BY_ID = {}
ENTITIES = {}      # entity -> field -> rule, loaded from 45d
CHECKS = {}        # the shared check config, loaded from 45g
RANK_NONE = ("huntingRank", "gatheringRank", "medicalRank")
# Fallbacks used only when 45g is absent. 45g is the source of truth and the
# builder preflight reads the same file; anything hardcoded here is a parity
# risk, which is why the list is short and the loader warns.
RUNTIME_ONLY_TAGS = ("activatesagemode",)
NEEDS_DAMAGE = ("vamp", "consume", "wound")


def load_checks(path):
    """45g_DATA_checks.json: the config the builder preflight also reads.
    Loading it is what makes parity possible - two validators reading one
    config cannot disagree about what the rules are, only about whether they
    implement them."""
    global RUNTIME_ONLY_TAGS, NEEDS_DAMAGE
    if not os.path.exists(path):
        return False
    try:
        CHECKS.update(json.load(open(path)))
    except Exception:
        return False
    RUNTIME_ONLY_TAGS = tuple(CHECKS["runtime_only_tags"]["values"])
    NEEDS_DAMAGE = tuple(CHECKS["companion_required"]["values"])
    return True


def check_ids():
    """Every check this validator implements, by the 45g block it comes from.
    The builder exposes the same inventory; `--parity <file>` diffs them."""
    return sorted([
        # nullable / null_strip_exempt are law 72 at two precisions: this side
        # has entity context and uses the full map, the builder walks a
        # context-free body and uses the name-safe subset. Both list both.
        "nullable", "null_strip_exempt", "cap_100", "required_on_create", "enums", "booleans",
        "date_fields", "tag_power_max", "runtime_only_tags", "companion_required",
        "entity_only_tags", "zero_power_per_level", "terminal_actions",
        "formula_tags", "hidden_on_create", "build_order",
    ])


def parity(path, rep):
    """Compare this validator's check inventory against the builder's.
    A check that exists in one and not the other is the failure this test
    exists to prevent: the browser accepting what the container rejects, or
    worse, the reverse."""
    mine = set(check_ids())
    theirs = set(json.load(open(path)).get("checks", []))
    for c in sorted(mine - theirs):
        rep.err("parity", f"'{c}' is checked here but NOT by the builder preflight")
    for c in sorted(theirs - mine):
        rep.err("parity", f"'{c}' is checked by the builder but NOT here")
    if mine == theirs:
        rep.note("parity", f"builder and validator implement the same {len(mine)} checks")
    declared = {k for k in CHECKS if not k.startswith("_")}
    for c in sorted(declared - mine):
        rep.warn("parity", f"45g declares '{c}' but neither side implements it")


class Report:
    def __init__(self):
        self.errors, self.warns, self.notes = [], [], []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warns.append(f"{where}: {msg}")

    def note(self, where, msg):
        """Informational only. Never counts toward the exit status, even under --strict."""
        self.notes.append(f"{where}: {msg}")

    def dump(self, strict=False):
        for e in self.errors:
            print("ERROR  " + e)
        for w in self.warns:
            print(("ERROR  " if strict else "warn   ") + w)
        for n in self.notes:
            print("note   " + n)
        n = len(self.errors) + (len(self.warns) if strict else 0)
        print(f"\n{len(self.errors)} errors, {len(self.warns)} warnings")
        return 1 if n else 0


# ------------------------------------------------------------------ shapes

def check_member(obj, union, ctors, where, rep):
    """Validate one tagged object against its generated constructor."""
    members = ctors["unions"].get(union)
    if not members:
        rep.warn(where, f"union {union} not in constructors file, shape unchecked")
        return
    disc_field = None
    for spec in members.values():
        if spec.get("discriminant"):
            disc_field = spec["discriminant"]["field"]
            break
    disc_field = disc_field or "type"
    key = obj.get(disc_field)
    if key is None:
        rep.err(where, f"missing discriminant '{disc_field}' (expected one of {sorted(members)[:6]}...)")
        return
    spec = members.get(key)
    if not spec:
        rep.err(where, f"'{key}' is not a member of {union}. Valid: {', '.join(sorted(members))}")
        return
    fields = spec["fields"]
    for f, v in obj.items():
        if f not in fields:
            rep.err(where, f"{key}: unknown field '{f}'. Valid: {', '.join(sorted(fields))}")
            continue
        r = fields[f]
        if r.get("enum"):
            vals = v if isinstance(v, list) else [v]
            for one in vals:
                if one not in r["enum"]:
                    rep.err(where, f"{key}.{f}={one!r} not in enum ({', '.join(r['enum'][:8])}...)")
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if r.get("min") is not None and v < r["min"]:
                rep.err(where, f"{key}.{f}={v} below min {r['min']}")
            if r.get("max") is not None and v > r["max"]:
                rep.err(where, f"{key}.{f}={v} above max {r['max']}")
            if r.get("int") and float(v) != int(v):
                rep.err(where, f"{key}.{f}={v} must be an integer")


def check_rules(rules, ctors, where, rep):
    if not isinstance(rules, list):
        rep.err(where, "rules must be an array")
        return
    if len(rules) > 20:
        rep.err(where, f"{len(rules)} rules exceeds the profile cap of 20")
    for i, r in enumerate(rules):
        w = f"{where}.rules[{i}]"
        if not isinstance(r, dict) or "conditions" not in r or "action" not in r:
            rep.err(w, "rule must be {conditions: [...], action: {...}} "
                       "(NOT a flat action/condition/conditionValue triple)")
            continue
        if not isinstance(r["conditions"], list):
            rep.err(w, "conditions must be an array")
        else:
            for j, c in enumerate(r["conditions"]):
                check_member(c, "ZodAllAiConditions", ctors, f"{w}.conditions[{j}]", rep)
        check_member(r["action"], "ZodAllAiActions", ctors, f"{w}.action", rep)
    uncond = {"move_towards_opponent", "end_turn", "use_random_jutsu"}

    def act_type(r):
        a = r.get("action") if isinstance(r, dict) else None
        return a.get("type") if isinstance(a, dict) else None

    if rules and isinstance(rules[-1], dict):
        last = rules[-1]
        if last.get("conditions") or act_type(last) not in uncond:
            rep.err(where, "law 41: the final rule must be unconditional "
                           "(move_towards_opponent, end_turn or use_random_jutsu) with conditions: []")
        for i, r in enumerate(rules[:-1]):
            if isinstance(r, dict) and not r.get("conditions") and act_type(r) in uncond:
                rep.err(f"{where}.rules[{i}]", "unconditional rule above the end; every rule below it is dead")


def check_effects(effects, ctors, where, rep):
    if not isinstance(effects, list):
        return
    for i, e in enumerate(effects):
        check_member(e, "AllTags", ctors, f"{where}.effects[{i}]", rep)


# -------------------------------------------------------------- invariants

def check_quest(data, ctors, where, rep):
    content = data.get("content") or {}
    objs = content.get("objectives") or []
    if not objs:
        rep.err(where, "no objectives")
        return
    ids = [o.get("id") for o in objs]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        rep.err(where, f"duplicate node ids: {sorted(dupes)}")
    edges = set()
    for o in objs:
        n = o.get("nextObjectiveId")
        if isinstance(n, list):
            edges |= {c.get("nextObjectiveId") for c in n if isinstance(c, dict)}
        elif isinstance(n, str):
            edges.add(n)
        if o.get("failObjectiveId"):
            edges.add(o["failObjectiveId"])
        if o.get("resetObjectiveId") and o["resetObjectiveId"] not in ids:
            rep.err(f"{where}.{o['id']}", f"resetObjectiveId '{o['resetObjectiveId']}' does not resolve")
    dangling = [e for e in edges if e and e not in ids]
    if dangling:
        rep.err(where, f"dangling edges: {sorted(dangling)}")
    starts = [i for i in ids if i not in edges]
    if len(starts) != 1:
        rep.err(where, f"expected exactly one start node, found {starts}")

    for o in objs:
        w = f"{where}.{o.get('id')}"
        task = o.get("task")
        if task == "defeat_opponents":
            if not o.get("failObjectiveId"):
                rep.err(w, "battle node without failObjectiveId (re-arm loop)")
            if not o.get("opponentAIs"):
                rep.err(w, "battle node without opponentAIs")
            for a in o.get("opponentAIs") or []:
                for i in a.get("ids", []):
                    if not str(i).startswith("@") and len(str(i)) != ID_LEN:
                        rep.err(w, f"opponent id {i!r} is not {ID_LEN} chars")
                if not isinstance(a.get("number"), int):
                    rep.err(w, "opponentAIs[].number must be an int COUNT (law 44)")
        if task == "dialog":
            ch = o.get("nextObjectiveId") or []
            if isinstance(ch, list) and len(ch) > 1:
                tgts = [c.get("nextObjectiveId") for c in ch]
                if len(set(tgts)) < len(tgts):
                    rep.err(w, "choice menu converges: every option leads to the same node. "
                               "A choice that changes nothing teaches the player their input is decorative")
            txt = o.get("description", "")
            if any(d in txt for d in DASHES):
                rep.err(w, "em dash in dialog text")
            for c in ch if isinstance(ch, list) else []:
                if any(d in c.get("text", "") for d in DASHES):
                    rep.err(w, "em dash in choice text")
            if "\n\n" in txt and "<br>" not in txt:
                rep.warn(w, "blank-line paragraphs but no <br>: node text renders as HTML, newlines do nothing")
        if len(o.get("sceneCharacters") or []) > 1:
            rep.err(w, "more than one scene character; the client stacks them at the same position (law 48)")

    if data.get("hidden") is False:
        main = content.get("sceneCharacters")
        every = objs and all(o.get("sceneCharacters") for o in objs)
        if not main and not every:
            rep.err(where, "public quest needs main sceneCharacters or sceneCharacters on every objective")


def check_pool_kit(data, where, rep):
    """Laws that only a machine should be trusted with: gate arithmetic, dead
    rules, and the AP economy."""
    if not POOL_BY_ID:
        return
    equipped = [str(j) for j in (data.get("jutsus") or [])]
    eq_set = set(equipped)

    ap = [POOL_BY_ID[j]["ap"] for j in equipped if j in POOL_BY_ID]
    if ap and min(ap) >= 60 and len(ap) >= 3:
        rep.warn(where, "kit is all 60 AP actions and no 40 AP stance: the AI will exhaust itself "
                        "(a round is 100 AP; laws 61 to 63)")

    for i, r in enumerate(data.get("rules") or []):
        if not isinstance(r, dict):
            continue
        a = r.get("action") or {}
        jid = a.get("jutsuId")
        if not jid:
            continue
        if equipped and jid not in eq_set:
            nm = POOL_BY_ID.get(jid, {}).get("name", jid)
            rep.err(f"{where}.rules[{i}]", f"rule fires '{nm}' but that jutsu is NOT in the AI's "
                                           "jutsus array. The rule is inert and the log signature is "
                                           "identical to a severed equip link (law 18)")
        rec = POOL_BY_ID.get(jid)
        if not rec:
            continue
        want = rec.get("gate")
        for c in r.get("conditions") or []:
            if c.get("type") == "distance_lower_than" and want and c.get("value") != want:
                rep.err(f"{where}.rules[{i}]", f"{rec['name']} is range {rec['range']}, so the gate must be "
                                               f"{want} (range+1, law 39). Found {c.get('value')}. "
                                               "A higher gate fires out of range and can strand a player in combat")
            if c.get("type") == "distance_lower_than" and rec.get("range") is None:
                rep.warn(f"{where}.rules[{i}]", f"{rec['name']} is self/ground targeted; a distance gate is "
                                                "meaningless on it")


def load_entities(path):
    """45d_DATA_entity_schemas.json: generated write validators. Absent is not
    fatal; the checks that need it just do not run."""
    if not os.path.exists(path):
        return
    try:
        d = json.load(open(path))
    except Exception:
        return
    for ent, spec in (d.get("entities") or {}).items():
        ENTITIES[ent] = spec.get("fields") or {}


def check_nulls(entry, rep):
    """Law 72, generated form. An explicit null is legal only where the zod
    chain is .nullable()/.nullish(). Everywhere else the key must be ABSENT,
    and the builder's null-optional guard must not silently strip a null the
    server would have accepted."""
    ent = entry.get("entity")
    fields = ENTITIES.get(ent)
    if not fields:
        return
    data = entry.get("data") or {}
    where = f"[{ent}:{entry.get('name') or entry.get('srcId')}]"
    for f, v in data.items():
        if v is not None:
            continue
        rule = fields.get(f)
        if rule is None:
            rep.warn(where, f"law 72: '{f}' is null but is not a field of the {ent} "
                            "write validator; it will be dropped or rejected")
        elif rule.get("nullable"):
            rep.note(where, f"'{f}': explicit null is ACCEPTED by the server "
                            "(.nullish()). The builder must not strip it")
        else:
            rep.err(where, f"law 72: '{f}' is null but the validator is not nullable. "
                           "Omit the key entirely; null is rejected")


def check_laws(entry, rep):
    """Assertable laws from 12_TECH. Each one folded in here is a law that can
    no longer be forgotten."""
    data = entry.get("data") or {}
    where = f"[{entry.get('entity')}:{entry.get('name') or entry.get('srcId')}]"
    ent = entry.get("entity")

    if "image" in data and data["image"] == "":
        rep.err(where, "law 46: image sent as empty string is nulled at the write path and 500s. Omit the key")

    check_nulls(entry, rep)

    if ent == "quest":
        for f in ("startsAt", "endsAt"):
            v = data.get(f)
            if v and not DATE_RE.match(str(v)):
                rep.err(where, f"law 7: {f} must be plain YYYY-MM-DD, got {v!r}")
        for f in CAP_100:
            v = data.get(f)
            if isinstance(v, (int, float)) and v > 100:
                rep.err(where, f"law 8: {f}={v} exceeds the cap of 100; the whole fill 400s")
        if entry.get("slot") == "create" and data.get("consecutiveObjectives") is not True:
            rep.err(where, "consecutiveObjectives must be set true explicitly on every create: the DB default "
                           "is false, which makes every objective simultaneously claimable")
        content = data.get("content") or {}
        nodes = list(content.get("objectives") or []) + [content.get("reward") or {}]
        for o in nodes:
            for f, t in (("reward_rank", str), ("reward_village_membership", str)):
                if f in o and not isinstance(o[f], t):
                    rep.err(where, f"{f} must be a string")
            for f in ("reward_gathering_items", "reward_hunter_items"):
                if f in o and not isinstance(o[f], bool):
                    rep.err(where, f"{f} must be a boolean")

    for e in data.get("effects") or []:
        if not isinstance(e, dict):
            continue
        t = e.get("type")
        if isinstance(e.get("power"), (int, float)) and e["power"] > 100:
            rep.err(where, f"law 6: effect '{t}' power {e['power']} exceeds the cap of 100 (rows are rounded down)")
        if t in FORMULA_TAGS and e.get("calculation", "formula") == "formula":
            if not e.get("statTypes") or not e.get("generalTypes"):
                rep.err(where, f"law 4: formula effect '{t}' requires BOTH statTypes AND generalTypes; "
                               "an empty one silently zeroes the damage")
        if t in RUNTIME_ONLY_TAGS:
            rep.err(where, f"law 77: '{t}' is a RUNTIME-ONLY tag. The engine injects it in battle "
                           "and SuperRefineEffects rejects it on every authored record")
        if t in NEEDS_DAMAGE:
            if not any(isinstance(x, dict) and x.get("type") in ("damage", "pierce")
                       for x in data.get("effects") or []):
                rep.err(where, f"law 78: '{t}' requires a damage or pierce effect on the SAME action")
        if t == "rollsagemode":
            if ent != "item":
                rep.err(where, "law 78: 'rollsagemode' is item-only; jutsu reject bloodline/sage roll effects")
            if e.get("powerPerLevel"):
                rep.err(where, "law 78: powerPerLevel must be 0 for rollsagemode")
        if t == "injectjutsus":
            rep.warn(where, "law 20 (CORRECTED): the injector guard fires only when a write sets "
                            "injectableInBattle FALSE. The referenced jutsu stays editable as long as "
                            "every edit keeps injectableInBattle true, and it must be unhidden")

    if ent == "jutsu" and entry.get("slot") in ("edit", "convert"):
        if "injectableInBattle" not in data:
            rep.warn(where, "law 20: injectableInBattle is absent and its schema default is FALSE. "
                            "If anything injects this jutsu, the edit is rejected. Send it explicitly")

    if ent == "quest":
        for f in RANK_NONE:
            if data.get(f) == "NONE":
                rep.warn(where, f"law 42: {f}='NONE' reads as gated but is inert. Omit the field")


def check_entry(entry, ctors, rep, manifest):
    name = entry.get("name") or entry.get("srcId") or "?"
    where = f"[{entry.get('entity')}:{name}]"
    data = entry.get("data") or {}
    slot = entry.get("slot")

    if slot != "create" and not entry.get("targetId"):
        rep.err(where, "non-create entry without top-level targetId")
    if slot == "create" and data.get("hidden") is not True:
        rep.err(where, "create without hidden:true. Everything ships hidden, every entity; "
                       "where the column does not exist the key is stripped harmlessly")

    for k in data:
        if k.startswith("_"):
            rep.warn(where, f"debug key '{k}' left in payload")

    if entry.get("entity") == "quest":
        check_quest(data, ctors, where, rep)
    if entry.get("entity") in ("ai", "aiProfile") and "rules" in data:
        check_rules(data["rules"], ctors, where, rep)
    if entry.get("entity") == "ai":
        for j in data.get("jutsus") or []:
            if str(j).startswith("@"):
                rep.err(where, f"unresolved ref {j} in AI jutsus array: refs are silently STRIPPED "
                               "server-side and the AI stands naked (law 17). Substitute literal ids")
            elif len(str(j)) != ID_LEN:
                rep.err(where, f"jutsu id {j!r} is not {ID_LEN} chars")
    if "effects" in data:
        check_effects(data["effects"], ctors, where, rep)
    if entry.get("entity") in ("ai", "aiProfile"):
        check_pool_kit(data, where, rep)
    check_laws(entry, rep)

    blob = json.dumps(data)
    for m in re.findall(r"@(?:jutsu|ai|scene|item|quest|img|bloodline):[^\"]{1,60}", blob):
        if "@@" in m or m.count(":") > 1:
            rep.err(where, f"malformed ref {m} (doubled prefix survives naive sweeps, law 45)")


def load_pool(path):
    if not path or not os.path.exists(path):
        return
    d = json.load(open(path))
    POOL.update(d.get("records") or {})
    for code, r in POOL.items():
        r["code"] = code
        POOL_BY_ID[r["id"]] = r


def check_manifest(path, ctors_path, strict=False):
    rep = Report()
    man = json.load(open(path))
    ctors = json.load(open(ctors_path))
    items = man.get("items") or []
    cap = man.get("capture") or {}
    cap_calls = (cap.get("before") or []) + (cap.get("after") or [])
    if not items and not cap_calls:
        rep.err("manifest", "no items")
    elif not items:
        rep.note("manifest", f"capture-only manifest: {len(cap_calls)} read(s), zero mutations")
    for phase in ("before", "after"):
        for c in (cap.get(phase) or []):
            if not isinstance(c, dict) or not c.get("proc"):
                rep.err("capture", f"{phase}: entry missing 'proc'")
            elif "input" in c and not isinstance(c["input"], dict):
                rep.err("capture", f"{phase}: {c['proc']} input must be an object")

    order = {"jutsu": 0, "asset": 1, "item": 2, "ai": 3, "aiProfile": 4, "quest": 5}
    seen = -1
    for e in items:
        o = order.get(e.get("entity"), 9)
        if o < seen:
            rep.warn("manifest", f"build order: {e.get('entity')} appears after a later phase")
        seen = max(seen, o)

    srcs = {e.get("srcId") for e in items if e.get("srcId")}
    blob = json.dumps(man)
    for ref in set(re.findall(r"@(?:jutsu|ai|scene|item|quest|bloodline):([A-Za-z0-9_\-]+)", blob)):
        if ref not in srcs:
            rep.warn("manifest", f"@ref '{ref}' has no srcId in this manifest; it must already be in the idmap")

    imgs = set(re.findall(r"@img:([A-Za-z0-9_.\-]+)", blob))
    sizes = man.get("imgSizes") or {}
    for f in imgs:
        if f not in sizes:
            rep.err("manifest", f"@img:{f} has no imgSizes entry (Android picker fallback)")
        elif os.path.exists(f) and sizes[f] != os.path.getsize(f):
            rep.err("manifest", f"imgSizes[{f}]={sizes[f]} but file on disk is {os.path.getsize(f)}")
        if os.path.exists(f) and os.path.getsize(f) > 512 * 1024:
            rep.err("manifest", f"{f} exceeds the 512KB presign cap")

    for e in items:
        check_entry(e, ctors, rep, man)

    if man.get("skipPreflight"):
        rep.warn("manifest", "skipPreflight is set: this needs an explicit ruling from Brandon")

    print(f"{path}: {len(items)} entries")
    return rep.dump(strict)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    ctors = "45c_DATA_constructors.json"
    if "--ctors" in sys.argv:
        ctors = sys.argv[sys.argv.index("--ctors") + 1]
    pool = "32b_DATA_pool.json"
    if "--pool" in sys.argv:
        pool = sys.argv[sys.argv.index("--pool") + 1]
    ents = "45d_DATA_entity_schemas.json"
    if "--entities" in sys.argv:
        ents = sys.argv[sys.argv.index("--entities") + 1]
    checks = "45g_DATA_checks.json"
    if "--checks" in sys.argv:
        checks = sys.argv[sys.argv.index("--checks") + 1]
    load_pool(pool)
    load_entities(ents)
    load_checks(checks)
    if "--parity" in sys.argv:
        r = Report()
        parity(sys.argv[sys.argv.index("--parity") + 1], r)
        sys.exit(r.dump(strict))
    if "--check-ids" in sys.argv:
        print(json.dumps({"checks": check_ids()}, indent=1))
        sys.exit(0)
    sys.exit(check_manifest(args[0], ctors, strict))
