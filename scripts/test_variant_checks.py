#!/usr/bin/env python3
"""validate.py's item-variant, variant-token and new-tag checks (variant_checks.py), and the
extractor corrections made for the 3314d122 re-pin (schema_extract.py).

    python3 -m unittest scripts/test_variant_checks.py -v

Synthetic manifests in a temp dir and synthetic source text; no game checkout, no network.
Forge's side is forge/test/variants.test.mjs.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "skills" / "building-tnr-content" / "data"
sys.path.insert(0, str(ROOT / "skills" / "building-tnr-content" / "scripts"))
import schema_extract as se  # noqa: E402

BASE = "trophyBaseItem0000001"
VARIANT = {"itemId": BASE, "name": "Fixture Trophy", "image": "https://utfs.io/f/t.webp", "costType": "VARIANT_TOKEN",
           "cost": 0, "order": 2, "requiredItemId": "trophyTokenItem000001", "hidden": True}
FX = {"power": 1, "powerPerLevel": 0, "calculation": "static", "direction": "offence", "target": "SELF",
      "description": "Unlocks a token-locked item variant when used on an item", "staticAssetPath": "", "staticAnimation": "",
      "appearAnimation": "", "disappearAnimation": "", "appearSfx": "", "disappearSfx": ""}
TOKEN = {"name": "Fixture Token", "description": "d", "itemType": "CONSUMABLE", "rarity": "RARE", "slot": "NONE",
         "target": "SELF", "method": "SINGLE", "destroyOnUse": True, "preventBattleUsage": True, "hidden": True,
         "effects": [{"type": "unlockitemvariant", "variantId": None, **FX}]}


def item(entity, data, slot="create", src="fx_one", target=None):
    it = {"entity": entity, "slot": slot, "name": data.get("name", "Fixture"), "data": data}
    if slot == "create":
        it["srcId"] = src
    else:
        it["targetId"] = target
    return it


class VariantChecks(unittest.TestCase):
    def validate(self, *items):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write(json.dumps({"items": list(items)}))
        try:
            r = subprocess.run([sys.executable, "../scripts/validate.py", "--strict", f.name], cwd=DATA, capture_output=True, text=True)
        finally:
            Path(f.name).unlink()
        return r.returncode, r.stdout + r.stderr

    def test_baselines_pass(self):
        code, out = self.validate(item("itemVariant", VARIANT))
        self.assertEqual(code, 0, out)
        code, out = self.validate(item("item", TOKEN, src="fx_tok"), item("itemVariant", {**VARIANT, "requiredItemId": "@item:fx_tok"}, src="fx_v"))
        self.assertEqual(code, 0, out)
        code, out = self.validate(item("itemVariant", {"itemId": BASE, "name": "Renamed"}, slot="edit", target="trophyVariant00000001"))
        self.assertEqual(code, 0, out)

    def test_bounds_and_keys(self):
        for patch, want in ((dict(name=" Pad"), "no leading or trailing"), (dict(name="x" * 192), "1-191"),
                            (dict(order=8), "order: an integer 1..7"), (dict(cost=-1), "cost: an integer"),
                            (dict(costType="GOLD"), "costType='GOLD' not in"), (dict(description=None), "null is refused"),
                            (dict(id="x"), "targetId"), (dict(colour="red"), "unknown key 'colour'"),
                            (dict(costType="MONEY"), "only a VARIANT_TOKEN variant can require"),
                            (dict(image="https://utfs.io/f/" + "a" * 500), "512"), (dict(itemId=None), "itemId: every variant")):
            code, out = self.validate(item("itemVariant", {**VARIANT, **patch}))
            self.assertNotEqual(code, 0, patch)
            self.assertIn(want, out, patch)

    def test_token_rules(self):
        bad = {**TOKEN, "destroyOnUse": False, "effects": [{"type": "unlockitemvariant", "variantId": "short", **FX}]}
        code, out = self.validate(item("item", bad))
        self.assertIn("destroyOnUse True", out)
        self.assertIn("variantId: null", out)
        bound = {**TOKEN, "effects": [{"type": "unlockitemvariant", "variantId": "trophyVariant00000001", **FX}]}
        code, out = self.validate(item("item", bound, src="fx_tok"), item("itemVariant", {**VARIANT, "requiredItemId": "@item:fx_tok"}, src="fx_v"))
        self.assertIn("needs an unlockitemvariant with variantId null", out)

    def test_twins_and_visibility_warnings(self):
        code, out = self.validate(item("itemVariant", VARIANT, src="a"), item("itemVariant", {**VARIANT, "name": "B"}, src="b"))
        self.assertIn("(itemId, order) is unique", out)
        _, out = self.validate(item("itemVariant", {k: v for k, v in VARIANT.items() if k != "requiredItemId"}))
        self.assertIn("every older Variant Token", out)
        _, out = self.validate(item("itemVariant", {**{k: v for k, v in VARIANT.items() if k != "requiredItemId"}, "costType": "MONEY", "cost": 5}))
        self.assertIn("no hidden switch", out)

    def test_new_tag_placement(self):
        jutsu_fx = {"type": "increasehuntingyield", "power": 1, "calculation": "static", "target": "SELF"}
        _, out = self.validate(item("jutsu", {"name": "J", "hidden": True, "effects": [jutsu_fx]}))
        self.assertIn("activity bonuses require", out)
        slots = {**TOKEN, "effects": [{"type": "increasejutsuslots", **{k: v for k, v in FX.items() if k != "description"}, "power": 2},
                                      {"type": "increasejutsuslots", **{k: v for k, v in FX.items() if k != "description"}, "power": 1}]}
        _, out = self.validate(item("item", slots))
        self.assertIn("at most 2 extra jutsu slots", out)

    def test_species_effect_skill_target(self):
        fx = {"type": "heal", "power": 2, "calculation": "percentage", "rounds": 100, "target": "SELF"}
        species = {"name": "S", "description": "d", "rarity": "RARE", "role": "HEALER", "isActive": False, "hidden": True}
        code, out = self.validate(item("petSpecies", {**species, "effects": [{**fx, "skillTarget": "ENEMIES"}]}))
        self.assertNotIn("skillTarget", out)
        _, out = self.validate(item("petSpecies", {**species, "effects": [{**fx, "skillTarget": "ALLIES"}]}))
        self.assertIn("skillTarget='ALLIES' not in", out)
        _, out = self.validate(item("petSpecies", {**species, "skillTarget": "SELF", "effects": [fx]}))
        self.assertIn("unknown key 'skillTarget'", out)


    # ---- review round 1 ---------------------------------------------------------------------

    def test_r1_f1_token_create_states_target(self):
        for k in ("target", "destroyOnUse", "preventBattleUsage"):
            code, out = self.validate(item("item", {kk: v for kk, v in TOKEN.items() if kk != k}))
            self.assertNotEqual(code, 0, k)
            self.assertIn(f"unlockitemvariant requires {k}", out, k)
        code, out = self.validate(item("item", {k: v for k, v in TOKEN.items() if k not in ("method", "itemType")}))
        self.assertEqual(code, 0, out)

    def test_r1_f2_omitted_item_type_is_consumable_on_create(self):
        bonus = {"type": "increasehuntingyield", **FX}
        code, out = self.validate(item("item", {**{k: v for k, v in TOKEN.items() if k != "itemType"}, "effects": [bonus]}))
        self.assertIn("activity bonuses require", out)

    def test_r1_f3_slot_power_defaults_before_summing(self):
        slot = {"type": "increasejutsuslots", **{k: v for k, v in FX.items() if k not in ("description", "power")}}
        code, out = self.validate(item("item", {**TOKEN, "effects": [slot, slot, slot]}))
        self.assertNotEqual(code, 0)
        self.assertIn("at most 2 extra jutsu slots", out)
        code, out = self.validate(item("item", {**TOKEN, "effects": [slot, slot]}))
        self.assertEqual(code, 0, out)


class ExtractorCorrections(unittest.TestCase):
    def test_comments_are_not_list_members(self):
        self.assertEqual(se.strip_comments('[\n  ["a"], // note\n  "http://x/y", /* c */ "b"\n]'), '[\n  ["a"], \n  "http://x/y",  "b"\n]')

    def test_named_schema_default_is_recorded(self):
        ctx = {"all_helpers": {}, "helpers": {}, "decls": {"furnitureVariantDataSchema": [("v.ts", ("obj", "{}"))]}}
        spec = se._entity_spec("furnitureVariantDataSchema.nullable().prefault(null)", "", ctx, "v.ts", {})
        self.assertEqual((spec.get("nullable"), "default" in spec, spec["default"]), (True, True, None))


if __name__ == "__main__":
    unittest.main()
