"""Resolve the Skyglass wave-2 enemies by AI key from push/344's results bundle(s) (literal ids, L01).

Used by push/skyglass_steeping.gen.py and push/skyglass_haul.gen.py. The enemies they fight are created by the rebuilt
push/344 (the RUL-2026-10-31-066/-067 re-simulation on `fable/skyglass-rule-cap`), so neither quest can carry a real AI
id until 344 has run. Each quest names its enemies by an AI KEY; this module turns a key into the literal id 344
created.

AI keys (the contract with the 344 builder; `KEYS` below is the authoritative list):
    veteran:<crew>   the one "Veteran <Name>" record per crew member (RUL-2026-10-31-067 item 2), fixed at level 100
                     and NOT scaled (RUL-2026-10-31-073); shared by the Rare chart runs and the Haul guards
    oneoff:<name>    a record that exists for one fight only (the Steeping Horror; the Haul elites)
    copy:<name>      a hazard/fuse copy of a live record (the Haul's Seal Charge and Core Canister)

How a key resolves, first match wins:
    1. --keymap <file.json>: {"<key>": "<21-char literal id>" or "<344 srcId>"}; for a 344 whose srcIds differ from
       the convention (a srcId value is looked up in the bundle(s) as in 2; same --keymap shape as
       push/skyglass_charts.gen.py).
    2. the 344 bundle(s): the srcId `sg344_<key with ':' replaced by '-'>` (e.g. `sg344_veteran-wayfinder`,
       `sg344_oneoff-steeping-horror`, `sg344_copy-seal-charge-haul`): an `ai` create entry with state ok and an id,
       or else the bundle's retained idmap.
A key that does not resolve stops the build and names the key (never a guessed or placeholder id).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# key -> what the 344 builder must create (for the README and error messages)
KEYS = {
    "oneoff:steeping-horror": "Steeping Horror: the Core Horror steeping copy (charts_spec newAIs chart-steeping-horror; "
                              "no Core Rot drop; fought scaled to the player)",
    "veteran:wayfinder": "Veteran Wayfinder (Haul hunter crew h-wayfinder)",
    "veteran:first-blade": "Veteran First Blade (Haul hunter crew h-blade and the steps 4-5 crew h-veteran)",
    "veteran:deck-warden": "Veteran Deck Warden (Haul crew h-warden / g-warden and the alertness crew h-lookout / g-lookout)",
    "veteran:skyglass-sentinel": "Veteran Skyglass Sentinel (Haul gatherer crew g-sentinel and the steps 4-5 crew g-veteran)",
    "veteran:arsenal-keeper": "Veteran Arsenal Keeper (Haul hunter alertness 3+ boss h-keeper)",
    "veteran:sealwright": "Veteran Sealwright, the Haul's Sealwright's Echo (gatherer alertness 3+ boss g-sealwright)",
    "oneoff:trophy-warden": "Trophy Warden (Haul hunter elite: Oathkeeper copy with the ring set piece)",
    "oneoff:stores-ward": "Stores Ward (Haul gatherer elite: Crown Archivist copy with the seal-lines set piece)",
    "copy:seal-charge-haul": "Seal Charge, Haul fuse copy (stationary, fuse round 4)",
    "copy:core-canister-haul": "Core Canister, Haul fuse copy (stationary, fuse round 5)",
}

ID_RE = re.compile(r"^[A-Za-z0-9_-]{21}$")


def src_id(key):
    return "sg344_" + key.replace(":", "-")


class Resolver:
    def __init__(self, bundles, keymap=None):
        self.bundles = [os.path.basename(b) for b in bundles]
        self.entries, self.idmap = {}, {}
        for path in bundles:
            b = json.load(open(path))
            for e in b.get("entries") or []:
                if e.get("entity") == "ai" and e.get("slot") == "create" and e.get("state") == "ok" and e.get("id"):
                    self.entries[e.get("srcId")] = e["id"]
            self.idmap.update(b.get("idmap") or {})
        self.keymap = {}
        if keymap:
            self.keymap = json.load(open(keymap))
            unknown = sorted(set(self.keymap) - set(KEYS))
            if unknown:
                raise SystemExit(f"--keymap names unknown AI keys: {', '.join(unknown)}")
        self.used = {}

    def __call__(self, key):
        if key not in KEYS:
            raise SystemExit(f"unknown AI key {key!r}")
        sid = src_id(key)
        lit = self.keymap.get(key)
        if lit and (lit.startswith("sg344_") or not ID_RE.match(lit)):  # a srcId, not a literal id
            sid, lit = lit, None
        lit = lit or self.entries.get(sid) or self.idmap.get(sid)
        if not lit:
            raise SystemExit(f"AI key {key!r} ({KEYS[key]}) does not resolve: no {sid} in "
                             f"{', '.join(self.bundles) or 'any bundle'} and no --keymap entry")
        if not ID_RE.match(lit):
            raise SystemExit(f"AI key {key!r} resolved to {lit!r}, which is not a literal 21-character id")
        self.used[key] = lit
        return lit
