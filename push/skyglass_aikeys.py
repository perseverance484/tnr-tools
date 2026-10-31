"""Resolve the Skyglass enemies by AI key (RUL-2026-10-31-077 record structure; literal ids, L01).

    python3 push/skyglass_aikeys.py --list                 # every key, its srcId / live id, username and uses
    python3 push/skyglass_aikeys.py --stand-in <path>      # TEST ONLY: a fake 344 bundle with made-up ids for every
                                                           #   key 344 creates (named as the records table names them)

The record table is state/skyglass_build/records_spec.json (harness/skyglass_wreck_sim/tools/records.py on
fable/skyglass-rule-cap; do not hand-edit): every AI record the event fights, one per measured tuning, with the spec
entry holding its row and rules and every fight that uses it. `KEYS` below is the authoritative key list; importing
this module fails if it and the table disagree (a re-simulation that changes the records must change both).

Key prefixes (srcId of a created record = `sg344_<key with ':' replaced by '-'>`):
    base:<crew>             the LIVE crew record, edited in place to the endgame Wreck version (push/361)
    live:<name>             a live record that is not Wreck crew, fought as it is (the Foundry hunt boss, the Arsenal
                            Keeper, the Core Canister, the Crown Archivist): unchanged by RUL-077
    veteran:<crew>[-<use>]  the rare-chart tier, fixed level 100: the hunts, the Sealed Reliquary echoes (-echo), the
                            Fall (-fall), the Burning Heading's ally (-ally); one record per measured tuning (push/344)
    haul:<crew>[-<role>]    the Haul tier, fixed level 100, unscaled (push/344)
    common:<crew>           the Common charts' scaled copies (push/344)
    rot:<crew>              Rot-Touched, the tainted runs (push/344)
    faded:<crew>            Faded, the level-50 Wreck (push/344)
    oneoff:<name>           one fight only (push/344)
    copy:<name>-haul        the Haul's fuse hazards (push/344)

How a key resolves, first match wins:
    live keys (base:, live:): the record's liveId from the table; no bundle needed.
    1. --keymap <file.json>: {"<key>": "<21-char literal id>" or "<344 srcId>"}.
    2. the 344 bundle(s): srcId `sg344_<key>` as an `ai` create entry with state ok and an id whose name is the
       table's username, or else the bundle's retained idmap.
A key that does not resolve stops the build and names the key (never a guessed or placeholder id).
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDS_SPEC = os.path.join(os.environ.get("SKYGLASS_BUILD") or os.path.join(ROOT, "state/skyglass_build"),
                            "records_spec.json")
PFX = "sg344_"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{21}$")

# key -> username (RUL-2026-10-31-077; names: Veteran / Rot-Touched / Faded tier names with a leading "The" dropped,
# checked free against the captured AI usernames; Common and Haul keep their placeholder names; theninjarpg@3314d122
# forbids duplicate usernames: UserData_username_key, profile.updateAi "Username already taken").
KEYS = {
    # (a) the live records = the endgame Wreck version (push/361)
    "base:deck-warden": "Deck Warden",
    "base:seal-charge": "Seal Charge",
    "base:skyglass-sentinel": "Skyglass Sentinel",
    "base:first-blade": "First Blade",
    "base:oathkeeper": "Oathkeeper",
    "base:wayfinder": "Wayfinder",
    "base:core-horror": "Core Horror",
    "base:the-captain": "The Captain",
    "base:sealwright": "Sealwright",
    # live records outside the Wreck crew, fought as they are by their hunts
    "live:core-canister": "Core Canister",
    "live:arsenal-keeper": "Arsenal Keeper",
    "live:foundry-warden": "Foundry Warden",
    "live:crown-archivist": "Crown Archivist",
    # (c) Veteran: the hunts, the Fall's / Burning Heading's crew fights, the Sealed Reliquary echoes, the Fall's helm
    "veteran:deck-warden": "Veteran Deck Warden",
    "veteran:seal-charge": "Veteran Seal Charge",
    "veteran:core-horror": "Veteran Core Horror",
    "veteran:skyglass-sentinel": "Veteran Skyglass Sentinel",
    "veteran:sealwright": "Veteran Sealwright",
    "veteran:wayfinder": "Veteran Wayfinder",
    "veteran:first-blade": "Veteran First Blade",
    "veteran:the-captain": "Veteran Captain",
    "veteran:foundry-warden": "Veteran Foundry Warden",
    "veteran:sealwright-echo": "Veteran Sealwright (Echo)",
    "veteran:skyglass-sentinel-echo": "Veteran Skyglass Sentinel (Echo)",
    "veteran:first-blade-echo": "Veteran First Blade (Echo)",
    "veteran:the-captain-fall": "Veteran Captain (Fall)",
    "veteran:the-captain-ally": "Veteran Captain (Ally)",
    # (b) Common charts (scaled)
    "common:deck-warden": "Deck Warden (Chart)",
    "common:seal-charge": "Seal Charge (Chart)",
    "common:arsenal-keeper": "Arsenal Keeper (Chart)",
    "common:skyglass-sentinel": "Skyglass Sentinel (Chart)",
    "common:first-blade": "First Blade (Chart)",
    "common:oathkeeper": "Oathkeeper (Chart)",
    # Rot-Touched (tainted runs)
    "rot:foundry-warden": "Rot-Touched Foundry Warden",
    "rot:sealwright": "Rot-Touched Sealwright",
    "rot:skyglass-sentinel": "Rot-Touched Skyglass Sentinel",
    "rot:first-blade": "Rot-Touched First Blade",
    "rot:core-horror": "Rot-Touched Core Horror",
    # Faded (level-50 Wreck)
    "faded:deck-warden": "Faded Deck Warden",
    "faded:seal-charge": "Faded Seal Charge",
    "faded:skyglass-sentinel": "Faded Skyglass Sentinel",
    "faded:first-blade": "Faded First Blade",
    "faded:oathkeeper": "Faded Oathkeeper",
    "faded:wayfinder": "Faded Wayfinder",
    "faded:core-horror": "Faded Core Horror",
    "faded:the-captain": "Faded Captain",
    # (c) Haul tier (fixed level 100, unscaled)
    "haul:wayfinder": "Wayfinder (Hunter)",
    "haul:first-blade": "First Blade (Hunter)",
    "haul:first-blade-steps": "First Blade (Veteran)",
    "haul:deck-warden": "Deck Warden (Haul)",
    "haul:deck-warden-lookout": "Deck Warden (Lookout)",
    "haul:skyglass-sentinel": "Skyglass Sentinel (Stores)",
    "haul:skyglass-sentinel-steps": "Skyglass Sentinel (Veteran)",
    "haul:arsenal-keeper": "Arsenal Keeper (Haul)",
    "haul:sealwright": "Sealwright's Echo",
    "copy:seal-charge-haul": "Seal Charge (Haul)",
    "copy:core-canister-haul": "Core Canister (Haul)",
    # one-offs
    "oneoff:lingering-echo-i": "Lingering Echo I",
    "oneoff:lingering-echo-ii": "Lingering Echo II",
    "oneoff:lingering-echo-iii": "Lingering Echo III",
    "oneoff:fall-arsenal-keeper": "Arsenal Keeper (Magazine)",
    "oneoff:steeping-horror": "Steeping Horror",
    "oneoff:trophy-warden": "Trophy Warden",
    "oneoff:stores-ward": "Stores Ward",
    "oneoff:crown-stonebound": "Crown Stonebound (Summoned)",
}


def _load_records():
    spec = json.load(open(RECORDS_SPEC))
    recs = {r["key"]: r for r in spec["records"]}
    if set(recs) != set(KEYS):
        raise SystemExit(f"push/skyglass_aikeys.py KEYS and {os.path.relpath(RECORDS_SPEC, ROOT)} disagree: "
                         f"{sorted(set(recs) ^ set(KEYS))}")
    bad = {k: (KEYS[k], r["name"]) for k, r in recs.items() if r["name"] != KEYS[k]}
    if bad:
        raise SystemExit(f"KEYS usernames differ from the records table: {bad}")
    return recs


RECORDS = _load_records()


def src_id(key):
    return PFX + key.replace(":", "-")


def is_live(key):
    return RECORDS[key]["kind"] == "live"


def created_keys():
    """Every key push/344 creates (all but the live records), in table order."""
    return [k for k in KEYS if not is_live(k)]


def key_of_source(spec, section, entry):
    """The key whose record holds this spec entry (its source or a merged identical one), e.g.
    key_of_source("charts_spec.json", "newAIs", "chart-c-deck-warden") -> "common:deck-warden"."""
    want = {"spec": spec, "path": [section, entry]}
    for k, r in RECORDS.items():
        s = r.get("source") or {}
        if {"spec": s.get("spec"), "path": s.get("path")} == want or want in s.get("also", []):
            return k
    return None


class Resolver:
    def __init__(self, bundles, keymap=None):
        self.bundles = [os.path.basename(b) for b in bundles]
        self.entries, self.names, self.idmap = {}, {}, {}
        for path in bundles:
            b = json.load(open(path))
            for e in b.get("entries") or []:
                if e.get("entity") == "ai" and e.get("slot") == "create" and e.get("state") == "ok" and e.get("id"):
                    self.entries[e.get("srcId")] = e["id"]
                    self.names[e.get("srcId")] = e.get("name")
            self.idmap.update(b.get("idmap") or {})
        self.keymap = {}
        if keymap:
            self.keymap = json.load(open(keymap)) if isinstance(keymap, str) else dict(keymap)
            unknown = sorted(set(self.keymap) - set(KEYS))
            if unknown:
                raise SystemExit(f"--keymap names unknown AI keys: {', '.join(unknown)}")
        self.used = {}

    def __call__(self, key):
        if key not in KEYS:
            raise SystemExit(f"unknown AI key {key!r}")
        rec = RECORDS[key]
        if is_live(key):
            lit = rec["liveId"]
        else:
            sid = src_id(key)
            lit = self.keymap.get(key)
            if lit and (lit.startswith(PFX) or not ID_RE.match(lit)):  # a srcId, not a literal id
                sid, lit = lit, None
            if not lit:
                lit = self.entries.get(sid) or self.idmap.get(sid)
                name = self.names.get(sid)
                if lit and name is not None and name != rec["name"]:
                    raise SystemExit(f"AI key {key!r}: {sid} is named {name!r} in the bundle, not {rec['name']!r}")
            if not lit:
                raise SystemExit(f"AI key {key!r} ({rec['name']}) does not resolve: no {sid} in "
                                 f"{', '.join(self.bundles) or 'any bundle'} and no --keymap entry")
        if not ID_RE.match(lit):
            raise SystemExit(f"AI key {key!r} resolved to {lit!r}, which is not a literal 21-character id")
        self.used[key] = lit
        return lit


def stand_in(path):
    """TEST ONLY: a fake 344 results bundle naming every created key, with made-up ids (never commit its output)."""
    entries, idmap = [], {}
    for k in created_keys():
        src = src_id(k)
        fake = ("X" + hashlib.sha256(k.encode()).hexdigest())[:21].replace("a", "_")
        entries.append({"name": KEYS[k], "srcId": src, "entity": "ai", "slot": "create", "op": "create", "state": "ok",
                        "verdict": "match", "id": fake})
        idmap[src] = fake
    json.dump({"builder": "STAND-IN (not a real run)", "state": "DONE", "outcome": "success", "entries": entries,
               "idmap": idmap}, open(path, "w"), indent=1)
    print(f"{path}: stand-in 344 bundle, {len(entries)} AI records (fake ids)")


def main():
    a = sys.argv[1:]
    if "--stand-in" in a:
        return stand_in(a[a.index("--stand-in") + 1])
    if "--list" in a:
        for k, r in RECORDS.items():
            where = r["liveId"] + " (live)" if is_live(k) else src_id(k)
            print(f"{k:32} {where:40} {r['name']:34} {'; '.join(r['usedBy'])[:120]}")
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
