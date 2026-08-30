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

def check_member(obj, union, ctors, where, rep):  # law 2: per-tag strict unions
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
        check_member(r["action"], "ZodAllAiActions", ctors, f"{w}.action", rep)  # laws 39, 64: vocabulary fixed by 45c
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
        # law 54: locationType 'specific' without coordinates lands the node at tile 0,0.
        # The engine only randomises for locationType 'random', so the player never walks
        # anywhere and never sees a pin. Not previously covered by any check.
        if o.get("locationType") == "specific":
            lat, lon = o.get("latitude"), o.get("longitude")
            if lat in (None, 0) and lon in (None, 0) and not o.get("sector"):
                task = o.get("task")
                if task in ("collect_item", "move_to_location"):
                    # The pin IS the mechanic here. 34b: an Action self-resolves at the timer and
                    # requires the player to stand on the tile for the whole duration, so a node
                    # at 0,0 can never complete.
                    rep.err(f"{where}.{o['id']}",
                            f"law 54: locationType 'specific' on a {task} node with no "
                            f"latitude/longitude places it at tile 0,0, so the player can never "
                            f"stand on it. Give real coordinates or use locationType 'random'")
                else:
                    # Live Witness Detail ships defeat_opponents as specific/0,0/sector 0, so the
                    # battle appears not to need placement. Flagged, not blocked.
                    rep.warn(f"{where}.{o['id']}",
                             f"law 54: locationType 'specific' at 0,0 on a {task} node. Matches "
                             f"the live Witness Detail convention, so probably inert, but unverified")
            else:
                for nm, v in (("latitude", lat), ("longitude", lon)):
                    if isinstance(v, (int, float)) and not (2 <= v <= 23):
                        rep.warn(f"{where}.{o['id']}",
                                 f"law 54: {nm} {v} is inside the 2-tile margin of the 26x26 sector")
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
                # House standard, ratified 2026-08-28 and NEWER than the live content that
                # breaks it. 'Copies, Not Thefts' converges at a1, a2 and f1; that quest is
                # the older pattern, not a precedent. A choice that changes nothing teaches
                # the player their input is decorative, so this stays an error.
                if len(set(tgts)) == 1:
                    rep.err(w, "choice menu converges: every option leads to the same node. "
                               "A choice that changes nothing teaches the player their input "
                               "is decorative")
                elif len(set(tgts)) < len(tgts):
                    rep.err(w, "two or more options in this menu share a target, so the menu "
                               "is narrower than it looks. Give each option its own node")
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
                                               f"{want} (range+1, law 40). Found {c.get('value')}. "
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


AI_CREATE_REQUIRED = ("rank", "regeneration", "preferredStat",
                      "preferredGeneral1", "preferredGeneral2")
STAT_TYPES = ("Highest", "Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu")
GENERAL_TYPES = ("Highest", "Strength", "Intelligence", "Willpower", "Speed")


_BOOL_CACHE = []


def _boolean_fields(ctors):
    """Law 73: derive the boolean field list from the generated files rather than restating it.
    The stack's own rule is that laws cite and never restate a generated constant."""
    if _BOOL_CACHE:
        return _BOOL_CACHE[0]
    out = set()
    sources = [ctors]
    # entity-level booleans (consecutiveObjectives, hidden, canBeCrafted...) live in 45d, not
    # 45c. Walking only the constructors missed every data-level field.
    for extra in ("45d_DATA_entity_schemas.json",):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), extra)
        if os.path.exists(p):
            try:
                sources.append(json.load(open(p)))
            except Exception:
                pass

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, dict) and v.get("type") == "boolean":
                    out.add(k)
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for src in sources:
        walk(src)
    _BOOL_CACHE.append(out)
    return out


_POOL_CACHE = []


def _pool_ranges():
    """Law 40: id -> (range, ratified gate) from 32b. All 82 pool records carry both, so the
    gate is derivable rather than asserted."""
    if _POOL_CACHE:
        return _POOL_CACHE[0]
    out = {}
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "32b_DATA_pool.json")
    if os.path.exists(p):
        try:
            recs = json.load(open(p)).get("records") or {}
            for r in (recs.values() if isinstance(recs, dict) else recs):
                if isinstance(r, dict) and r.get("id") and r.get("range") is not None:
                    out[r["id"]] = (r["range"], r.get("gate"))
        except Exception:
            pass
    _POOL_CACHE.append(out)
    return out


def check_distance_gates(data, where, rep):  # law 40: gate = range + 1
    """Law 40: the distance gate is the jutsu's range + 1. A gate above that can fire out of
    range and strand a human player in combat; a gate of 1 on a melee jutsu can never fire.
    Only checkable for pool jutsu, whose ranges are generated into 32b."""
    ranges = _pool_ranges()
    if not ranges:
        return
    for i, rule in enumerate(data.get("rules") or []):
        act = rule.get("action") or {}
        jid = act.get("jutsuId") or act.get("id")
        if not isinstance(jid, str) or jid not in ranges:
            continue
        rng, ratified = ranges[jid]
        want = rng + 1
        for cond in rule.get("conditions") or []:
            if "distance" not in json.dumps(cond).lower():
                continue
            got = cond.get("value")
            if isinstance(got, (int, float)) and got != want:
                lvl = rep.err if got > want else rep.warn
                lvl(f"{where}.rules[{i}]",
                    f"law 40: distance gate {got} on a range-{rng} jutsu. Expected {want} "
                    f"(range + 1)." + (f" 32b ratifies {ratified}." if ratified else "")
                    + (" A gate above range+1 can fire out of range and strand the player."
                       if got > want else " Below range+1 forfeits the outermost band."))


def check_entry_laws(entry, ctors, where, rep):  # laws 36, 55, 73
    """Laws 36, 55 and 73. All three were classed `validate` in 12b and had no hook in this
    tool; all three were hand-tested clean against the Forsworn wave on 2026-08-28, so they were
    unenforced rather than violated. Closing them so the matrix is true."""
    data = entry.get("data") or {}

    # law 36: data.name must be set on every create and must equal the entry name. Thirty-one
    # records in one campaign were composed with the name at entry level only and would have
    # landed carrying server defaults.
    if entry.get("slot") == "create":
        dn = data.get("name") or data.get("username")
        en = entry.get("name")
        if not dn:
            rep.err(where, "law 36: create has no name inside `data`. The entry-level name is "
                           "manifest metadata the server never sees, so this lands on defaults")
        elif en and dn.strip() != en.strip():
            rep.warn(where, f"law 36: data name {dn!r} differs from entry name {en!r}. "
                            f"The server sees only the data name")

    # law 55: sectorType 'random' on a battle node teleports the player to an arbitrary sector.
    # Cloned battle templates carry it; live Night Watch Shadow still ships it today.
    for o in (data.get("content") or {}).get("objectives") or []:
        if o.get("task") == "defeat_opponents" and o.get("sectorType") == "random":
            rep.err(f"{where}.{o.get('id')}",
                    "law 55: sectorType 'random' on a battle node teleports the player to an "
                    "arbitrary sector. Use user_village for anything meant to stay local")

    # law 73: booleans are not numbers. In Python isinstance(False, int) is True, so a numeric
    # normalisation pass silently flattens these to 0 and the write is rejected.
    BOOLS = _boolean_fields(ctors) | {"reward_hunter_items", "reward_gathering_items"}

    def scan(d, path):
        for k, v in (d or {}).items():
            if k in BOOLS and not isinstance(v, bool):
                rep.err(f"{where}{path}", f"law 73: '{k}' is {type(v).__name__} {v!r}, not a "
                                          f"boolean. A numeric pass flattened it and the server "
                                          f"will reject the write")

    scan(data, "")
    for o in (data.get("content") or {}).get("objectives") or []:
        scan(o, f".{o.get('id')}")


def check_acyclic(objs, where, rep):  # law 87
    """The builder's q.fill flow validator rejects any cycle: 'Cycle detected in objective
    chain'. Loops are legal but must go through a reset_quest node, whose resetObjectiveId
    is a separate field and not a graph edge. Live Witness Detail loops this way (x1)."""
    by_id = {o.get("id"): o for o in objs}
    if not objs:
        return

    def out(o):
        nxt = o.get("nextObjectiveId")
        e = ([c.get("nextObjectiveId") for c in nxt] if isinstance(nxt, list)
             else ([nxt] if isinstance(nxt, str) and nxt else []))
        if o.get("failObjectiveId"):
            e.append(o["failObjectiveId"])
        return [t for t in e if t in by_id]

    state, back = {}, []
    stack = [(objs[0].get("id"), iter(out(objs[0])))]
    state[objs[0].get("id")] = "open"
    while stack:
        node, it = stack[-1]
        nxt = next(it, None)
        if nxt is None:
            state[node] = "done"
            stack.pop()
            continue
        if state.get(nxt) == "open":
            back.append((node, nxt))
        elif nxt not in state:
            state[nxt] = "open"
            stack.append((nxt, iter(out(by_id[nxt]))))
    for src, dst in back:
        rep.err(f"{where}.{src}",
                f"law: edge to '{dst}' closes a cycle, which the builder's q.fill flow "
                f"validator rejects. Route the loop through a reset_quest node with "
                f"resetObjectiveId '{dst}'")


def check_reset_targets(objs, where, rep):  # law 88
    """A reset_quest must not land on a defeat_opponents node. Live practice resets to the
    node BEFORE the fight (Copies, Not Thefts: l4 -> l1 dialog, c6 -> c4 collect_item), never
    onto the fight itself. The one node in the Forsworn wave that reset onto a battle is the
    one whose read-back hung on 2026-08-28."""
    by_id = {o.get("id"): o for o in objs}
    for o in objs:
        if o.get("task") != "reset_quest":
            continue
        t = by_id.get(o.get("resetObjectiveId"))
        if t is not None and t.get("task") == "defeat_opponents":
            rep.err(f"{where}.{o.get('id')}",
                    f"resetObjectiveId '{o.get('resetObjectiveId')}' is a defeat_opponents node. "
                    f"Reset to the node that leads into the fight instead; live content never "
                    f"resets onto a battle")


def check_dialog_options(objs, where, rep):  # laws 85, 86
    """The builder's q.fill flow validator rejects any dialog objective with no options
    ('Dialog objective X must have at least one option'). Live Witness Detail shows the
    pattern: every dialog carries at least one option and the quest terminates on a
    win_quest or fail_quest node, which is the only thing allowed to carry no next."""
    TERMINAL_TASKS = ("win_quest", "fail_quest", "reset_quest")
    has_terminal = any(o.get("task") in TERMINAL_TASKS for o in objs)
    for o in objs:
        if o.get("task") != "dialog":
            continue
        nxt = o.get("nextObjectiveId")
        opts = len(nxt) if isinstance(nxt, list) else (1 if isinstance(nxt, str) and nxt else 0)
        if opts == 0:
            rep.err(f"{where}.{o.get('id')}",
                    "dialog objective has no options: the builder's q.fill flow validator "
                    "rejects this. End on a win_quest node and give this dialog one option "
                    "pointing at it")
    if not has_terminal:
        rep.warn(where, "no win_quest / fail_quest / reset_quest node: nothing marks the "
                        "quest complete")


def check_ai_create(data, where, rep):  # law 14
    """law 14: rank, regeneration, preferredStat and preferredGeneral1/2 are REQUIRED on
    every AI create. The DB default is STUDENT with every stat 10, so a create missing them
    lands as a paper doll. 12b classes this law 'validate', but the check did not exist here
    and the builder's L05 lint caught it instead."""
    for f in AI_CREATE_REQUIRED:
        if data.get(f) in (None, ""):
            rep.err(where, f"law 14: AI create missing required field '{f}' "
                           f"(builder lint L05 rejects this)")
    for f, allowed in (("preferredStat", STAT_TYPES),
                       ("preferredGeneral1", GENERAL_TYPES),
                       ("preferredGeneral2", GENERAL_TYPES)):
        v = data.get(f)
        if v is not None and v not in allowed:
            rep.err(where, f"law 14: '{f}' = {v!r} is not one of {list(allowed)}")


def check_nulls(entry, rep):  # law 72: optional vs nullable split
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
        if entry.get("slot") == "create" and data.get("consecutiveObjectives") is not True:  # law 23
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

    if slot != "create" and not entry.get("targetId"):  # law 5
        rep.err(where, "non-create entry without top-level targetId")
    if slot == "create" and data.get("hidden") is not True:  # law 16b (L13)
        rep.err(where, "create without hidden:true. Everything ships hidden, every entity; "
                       "where the column does not exist the key is stripped harmlessly")

    for k in data:
        if k.startswith("_"):
            rep.warn(where, f"debug key '{k}' left in payload")

    check_entry_laws(entry, ctors, where, rep)
    if entry.get("entity") == "quest":
        check_quest(data, ctors, where, rep)
        _objs = (data.get("content") or {}).get("objectives") or []
        check_dialog_options(_objs, where, rep)
        check_acyclic(_objs, where, rep)
        check_reset_targets(_objs, where, rep)
    if entry.get("entity") in ("ai", "aiProfile") and "rules" in data:
        check_rules(data["rules"], ctors, where, rep)
        check_distance_gates(data, where, rep)
    if entry.get("entity") == "ai":
        if entry.get("slot") == "create":
            check_ai_create(data, where, rep)
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
        if os.path.exists(f) and os.path.getsize(f) > 512 * 1024:  # law 35
            rep.err("manifest", f"{f} exceeds the 512KB presign cap")

    for e in items:
        check_entry(e, ctors, rep, man)

    if man.get("skipPreflight"):
        rep.warn("manifest", "skipPreflight is set: this bypasses every check and needs an explicit go-ahead before it ships")

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
