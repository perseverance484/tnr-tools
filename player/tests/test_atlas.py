"""The move atlas (player/atlas.py, player/atlas.json): what the generator makes of a record and of the engine's
answer, and what the committed atlas holds. None of these needs the engine or the catalog."""
import json
import os
import sys
import unittest
from unittest import mock

from player import atlas, config as C

if C.TOOLS not in sys.path:
    sys.path.insert(0, C.TOOLS)

JUTSU = {"id": "j1", "name": "Ember", "jutsuType": "NORMAL", "jutsuRank": "S", "jutsuWeapon": "NONE", "battleUsageType": "BOTH",
         "actionCostPerc": 60, "cooldown": 4, "range": 2, "target": "OTHER_USER", "method": "SINGLE",
         "elementClassification": "Fire",
         "effects": [{"type": "damage", "elements": ["Fire"]}, {"type": "visual"}, {"type": "increasedamagegiven"}]}
FIRED = {"listed": True, "cost": 60, "legal": True, "now": {"caster": -27, "target": -518},
         "effects": [{"type": "increasedamagegiven", "on": "caster", "by": "caster", "power": 25, "powerPerLevel": 0.4,
                      "level": 25, "rounds": 2, "calculation": "percentage", "isNew": False, "castThisRound": True,
                      "direction": "offence", "elements": [], "statTypes": None},
                     {"type": "visual", "on": "caster", "by": "caster", "power": 1, "rounds": 0}],
         "ground": [{"type": "visual", "on": "target", "by": "target", "x": 7, "y": 4},
                    {"type": "recoil", "on": "target", "by": "caster", "power": 0, "rounds": 0, "x": 7, "y": 4}],
         "at": {"caster": [6, 4], "target": [7, 4]},
         "next": {"caster": 0, "target": -40, "left": [["increasedamagegiven", 1], ["visual", 0]]}}


def recs(*records):
    return {r["id"]: {"kind": "item" if "itemType" in r else "jutsu", "record": r} for r in records}


class WhatBecomesACard(unittest.TestCase):
    def test_players_actions_and_the_basics(self):
        some = recs(JUTSU, dict(JUTSU, id="j2", jutsuType="AI"), dict(JUTSU, id="j3", jutsuType="PETS"),
                    dict(JUTSU, id="j4", jutsuType="BLOODLINE"),
                    {"id": "i1", "itemType": "WEAPON", "slot": "HAND", "effects": [{"type": "damage"}]},
                    {"id": "i2", "itemType": "OTHER", "slot": "ITEM", "effects": [{"type": "heal"}]},     # the Jewel's kind
                    {"id": "i3", "itemType": "ARMOR", "slot": "CHEST", "effects": [{"type": "absorb"}]},  # worn, not used
                    {"id": "i4", "itemType": "CONSUMABLE", "slot": "ITEM", "effects": []})
        got = atlas.candidates(some)
        self.assertEqual(got[:4], [("i1", "item"), ("i2", "item"), ("j1", "jutsu"), ("j4", "jutsu")])
        self.assertEqual([k for _, k in got[4:]], ["basic"] * len(atlas.BASICS))

    def test_the_caster_is_given_what_the_card_asks_for(self):
        staff = {"id": "w1", "itemType": "WEAPON", "weaponType": "STAFF", "slot": "HAND", "effects": []}
        ring = {"id": "k1", "itemType": "KEYSTONE", "slot": "KEYSTONE", "effects": []}
        blade = {"id": "w2", "itemType": "WEAPON", "weaponType": "SWORD", "slot": "HAND", "effects": []}
        some = recs(staff, ring, blade)
        gear = [{"record": {"id": "g"}, "slot": "CHEST"}, {"record": {"id": "old"}, "slot": "KEYSTONE"}]
        plain = atlas._needs(JUTSU, some, gear)
        self.assertEqual(([k["record"]["id"] for k in plain["kit"]], plain["gear"], plain["elements"]),
                         (["j1"], gear, ["Fire"]))
        cast = atlas._needs(dict(JUTSU, jutsuWeapon="STAFF", requiredBloodlineItemId="k1", elementClassification="None",
                                 effects=[{"type": "damage", "elements": ["Metal", "Fire"]}]), some, gear)
        self.assertEqual([k["record"]["id"] for k in cast["kit"]], ["j1", "w1"])              # a staff to cast with
        self.assertEqual([g["record"]["id"] for g in cast["gear"]], ["g", "k1"])              # its keystone, for his
        self.assertEqual(cast["elements"], ["Metal", "Fire"])
        held = atlas._needs(dict(JUTSU, requiredBloodlineItemId="w2"), some, gear)
        self.assertEqual(([k["record"]["id"] for k in held["kit"]], held["gear"]), (["j1", "w2"], gear))


class ACard(unittest.TestCase):
    def test_the_records_fields_then_what_the_engine_read_back(self):
        c = atlas.card("j1", "jutsu", JUTSU, FIRED, dict(FIRED, cost=40, now={"caster": 0, "target": -546}))
        self.assertEqual({k: c[k] for k in ("name", "kind", "type", "rank", "ap", "cooldown", "range", "target")},
                         {"name": "Ember", "kind": "jutsu", "type": "NORMAL", "rank": "S", "ap": 60, "cooldown": 4,
                          "range": 2, "target": "OTHER_USER"})
        self.assertNotIn("weapon", c)                                              # "NONE" is not a weapon
        self.assertEqual(c["tags"], ["damage", "increasedamagegiven"])            # the picture is no effect
        self.assertEqual((c["legal"], c["cost"], c["now"]), (True, 60, {"caster": -27, "target": -518}))
        self.assertEqual(c["effects"], [{"type": "increasedamagegiven", "on": "caster", "by": "caster", "power": 25,
                                         "powerPerLevel": 0.4, "level": 25, "rounds": 2, "calculation": "percentage",
                                         "castThisRound": True, "direction": "offence"}])
        self.assertEqual(c["ground"], [{"type": "recoil", "on": "target", "by": "caster", "power": 0, "rounds": 0,
                                        "x": 7, "y": 4}])                          # a zero is a value, and is kept
        self.assertEqual(c["next"], {"caster": 0, "target": -40, "left": [["increasedamagegiven", 1]]})
        self.assertEqual((c["mine"]["cost"], c["mine"]["now"]["target"]), (40, -546))
        self.assertEqual(c["of"], atlas.mark(JUTSU))

    def test_a_card_that_was_not_fired_says_why(self):
        self.assertEqual(atlas.card("j1", "jutsu", dict(JUTSU, battleUsageType="PVE"), FIRED)["reason"], atlas.PVE_ONLY)
        self.assertEqual(atlas.card("j1", "jutsu", JUTSU, None)["reason"], "the engine gave no answer")
        self.assertEqual(atlas.card("j1", "jutsu", JUTSU, {"listed": False, "legal": False})["reason"],
                         "not an action in a fight")
        refused = atlas.card("j1", "jutsu", JUTSU, {"listed": True, "cost": 60, "legal": False, "reason": "out of range"})
        self.assertEqual((refused["legal"], refused["reason"], refused["cost"]), (False, "out of range", 60))
        for c in (refused, atlas.card("j1", "jutsu", JUTSU, None)):
            self.assertFalse({"now", "effects", "ground", "mine"} & set(c))
        self.assertEqual(atlas.card("basicAttack", "basic", None, FIRED)["name"], "basicAttack")


class TheEngineIsAsked(unittest.TestCase):
    def rig(self, answers):
        """A bridge whose engine answers each batch with the next of `answers` (None: the process was lost)."""
        asked = []

        class EB:
            HARNESS = "/nowhere"

            @staticmethod
            def _replay_request(*a):
                return {"me": {"kit": [{"record": {"id": "j1"}}]}, "him": {"gear": []}}

            @staticmethod
            def _bloodline(i):
                return {"id": i}

            @staticmethod
            def _run(req, timeout):
                asked.append([(c["id"], c.get("by")) for c in req["cards"]])
                got = answers.pop(0)
                return None if got is None else {"cards": {("me:" if c.get("by") else "") + c["id"]: got for c in req["cards"]}}
        VM = type("VM", (), {"load_cal": staticmethod(lambda: {})})
        return mock.patch.object(atlas, "_tools", lambda: (EB, VM)), asked

    def test_my_own_kit_is_fired_by_me_as_well(self):
        patch, asked = self.rig([FIRED])
        with patch:
            got = atlas.measure(["j1", "basicAttack"], recs(JUTSU))
        self.assertEqual(asked, [[("j1", None), ("basicAttack", None), ("j1", "me"), ("basicAttack", "me")]])
        self.assertEqual(sorted(got), ["basicAttack", "j1", "me:basicAttack", "me:j1"])

    def test_a_lost_batch_is_asked_again_and_nothing_is_written_when_it_is_lost_twice(self):
        patch, asked = self.rig([None, FIRED])
        with patch:
            self.assertIn("j1", atlas.measure(["j1"], recs(JUTSU)))
        self.assertEqual(len(asked), 2)
        patch, asked = self.rig([None, None])
        with patch, self.assertRaises(SystemExit):
            atlas.measure(["j1"], recs(JUTSU))


class TheEngineFails(unittest.TestCase):
    def test_nothing_is_written_when_the_engines_own_code_failed(self):
        """Seen once: two engine runs at the same moment, one loading a file the other was copying."""
        bad = {"legal": False, "reason": "I.act is not a function. (In 'I.act(b, cid, actionId)', 'I.act' is undefined)"}
        EB = type("EB", (), {"engine_app": staticmethod(lambda: "/app"), "_records": staticmethod(lambda: recs(JUTSU))})
        with mock.patch.object(atlas, "_tools", lambda: (EB, None)), \
                mock.patch.object(atlas, "measure", lambda ids, r: {"j1": bad}), self.assertRaises(SystemExit) as stop:
            atlas.build()
        self.assertIn("nothing is written", str(stop.exception))
        self.assertIsNone(atlas.FAULT.search("Action Ember no longer possible for him"))     # a card's own refusal


class WhatHasChanged(unittest.TestCase):
    def test_a_card_is_stale_when_its_record_is_no_longer_the_one_it_was_made_of(self):
        other, gone = dict(JUTSU, id="j9", name="Other"), dict(JUTSU, id="gone", name="Gone")
        kept = {"cards": {"j1": atlas.card("j1", "jutsu", JUTSU, FIRED), "gone": atlas.card("gone", "jutsu", gone, FIRED),
                          **{b: atlas.card(b, "basic", None, FIRED) for b in atlas.BASICS}}}
        self.assertEqual(atlas.stale(kept, recs(JUTSU, gone)), {"changed": [], "new": [], "gone": []})
        now = recs(dict(JUTSU, cooldown=5), other, {"id": "x", "itemType": "MATERIAL", "slot": "NONE", "effects": []})
        self.assertEqual(atlas.stale(kept, now), {"changed": ["j1"], "new": ["j9"], "gone": ["gone"]})   # x: no card's


class TheCommittedAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = atlas.load()
        cls.cards = cls.atlas["cards"]

    def test_it_is_whole(self):
        meta = self.atlas["_meta"]
        legal = [c for c in self.cards.values() if c["legal"]]
        self.assertEqual((meta["cards"], meta["legal"]), (len(self.cards), len(legal)))
        self.assertGreater(len(legal), 800)
        self.assertEqual(len(meta["engine"]), 40)                                     # the engine's commit
        for rid, c in self.cards.items():
            self.assertTrue({"name", "kind", "tags", "legal"} <= set(c), rid)
            if c["legal"]:
                self.assertTrue({"cost", "now", "effects", "ground", "at", "next"} <= set(c), rid)
                self.assertFalse([e for e in c["effects"] + c["ground"] if e["type"] in atlas.NOISE], rid)
            else:
                self.assertTrue(c["reason"], rid)
                self.assertNotEqual(c["reason"], "the engine gave no answer", rid)
        self.assertEqual(sorted({e["type"] for c in legal for e in c["effects"] + c["ground"]}), meta["effect_types"])
        self.assertTrue(all(self.cards[b]["legal"] for b in atlas.BASICS))

    def test_one_card_a_line_in_order(self):
        with open(atlas.PATH, encoding="utf8") as f:
            lines = f.read().splitlines()
        ids = [json.loads("{" + ln.rstrip(",") + "}") for ln in lines[2:-1]]
        self.assertEqual([next(iter(x)) for x in ids], sorted(self.cards))
        self.assertEqual(len(lines), len(self.cards) + 3)

    def test_every_action_of_my_pvp_kit_has_a_card_fired_by_me(self):
        import cd_plan
        import turn
        for name in cd_plan.LOADOUTS["pvp1"]:
            c = self.cards.get(turn.ACTION_ID.get(name))
            self.assertTrue(c and c["legal"], name)
            if name != "kunai":                                  # (the kunai's id is the one equipped: it changes)
                self.assertIn("mine", c, name)                   # Chakra Resistance too: the bridge's kit had not
        storm = self.cards[turn.ACTION_ID["stormblade"]]
        self.assertEqual((storm["ap"], storm["cost"]), (60, 60))
        self.assertLess(storm["mine"]["now"]["target"], -500)


if __name__ == "__main__":
    unittest.main()
