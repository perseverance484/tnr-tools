#!/usr/bin/env python3
"""validate.py check_pool_kit: the engine basic-attack exception (director 2026-10-31,
"Do an exception for basic attack for now"; RUL-2026-10-31-066 item 2).

    python3 -m unittest scripts/test_pool_kit.py -v

An AI rule `use_specific_jutsu` with `jutsuId: "basicAttack"` is live without being in the AI's
`jutsus` array: theninjarpg@3314d122 libs/combat/ai_v2.ts ~494 resolves jutsuId against the
available actions, and libs/combat/actions.ts ~513 / ~146 always offers the basic attack. Every
other check is unchanged: an unequipped real jutsu is still refused (law 18) and a pool jutsu's
gate must still be range+1 (law 40). Uses the committed 32b_DATA_pool.json; no game checkout,
no network. Forge's side is forge/test/adversarial.test.mjs K3b.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "building-tnr-content"
sys.path.insert(0, str(SKILL / "scripts"))
import validate as v  # noqa: E402

v.load_pool(str(SKILL / "data" / "32b_DATA_pool.json"))
B01 = v.POOL["B01"]
B07 = v.POOL["B07"]


def kit(rules, jutsus=None):
    rep = v.Report()
    v.check_pool_kit({"jutsus": jutsus if jutsus is not None else [B01["id"]], "rules": rules}, "ai:X", rep)
    return rep


def rule(jid, conditions=(), atype="use_specific_jutsu"):
    return {"conditions": list(conditions),
            "action": {"type": atype, "jutsuId": jid, "target": "CLOSEST_OPPONENT"}}


class EngineBasicAttack(unittest.TestCase):
    def test_basic_attack_rule_is_accepted_unequipped(self):
        rep = kit([rule(B01["id"], [{"type": "distance_lower_than", "value": B01["gate"]}]),
                   rule("basicAttack"),
                   rule("basicAttack", [{"type": "distance_lower_than", "value": 2}])])
        self.assertEqual(rep.errors, [])

    def test_unequipped_real_jutsu_is_still_refused(self):
        rep = kit([rule(B07["id"], [{"type": "distance_lower_than", "value": B07["gate"]}])])
        self.assertEqual(len(rep.errors), 1)
        self.assertIn("NOT in the AI's jutsus array", rep.errors[0])
        self.assertIn(B07["name"], rep.errors[0])

    def test_exception_is_only_the_exact_id_on_use_specific_jutsu(self):
        for jid in ("basicattack", "BasicAttack", "basicHeal", "move"):
            rep = kit([rule(jid)])
            self.assertEqual(len(rep.errors), 1, jid)
            self.assertIn("NOT in the AI's jutsus array", rep.errors[0])
        rep = kit([rule("basicAttack", atype="use_highest_power_jutsu")])
        self.assertEqual(len(rep.errors), 1)
        self.assertIn("NOT in the AI's jutsus array", rep.errors[0])

    def test_range_plus_one_gate_is_unchanged(self):
        rep = kit([rule(B01["id"], [{"type": "distance_lower_than", "value": B01["range"]}]),
                   rule("basicAttack")])
        self.assertEqual(len(rep.errors), 1)
        self.assertIn(f"the gate must be {B01['gate']} (range+1, law 40)", rep.errors[0])


if __name__ == "__main__":
    unittest.main()
