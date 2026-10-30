#!/usr/bin/env python3
"""Pet species builder support (RUL-2026-10-28-012): extractor fixes, the ledger's bound class and
validate.py's pet checks.

    python3 -m unittest scripts/test_pet_species.py -v

Synthetic TypeScript sources in a temp dir and the committed fixtures under forge/test/fixtures/pets/;
no game checkout, no network. Forge's side of the same fixtures is forge/test/pets.test.mjs.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "building-tnr-content"
DATA = SKILL / "data"
FIX = ROOT / "forge" / "test" / "fixtures" / "pets"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(ROOT / "scripts"))
import schema_extract as se  # noqa: E402
import schema_adoption_ledger as sal  # noqa: E402


def validate(name):
    r = subprocess.run([sys.executable, "../scripts/validate.py", "--strict", str(FIX / name)],
                       cwd=DATA, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


class Extractor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        os.makedirs(os.path.join(self.root, "app/src/validators"))

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        p = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        Path(p).write_text(text)
        return p

    def test_object_values_spread_resolves(self):
        p = self.write("app/src/validators/objectives.ts", """
export const Combat = ["pvp_participated", "ranked_wins"] as const;
export const QuestDone = { story: "stories_completed", event: "events_completed" } as const;
export const Done = [...Object.values(QuestDone), "raids_completed"] as const;
""")
        got = se.parse_const_arrays(p)
        self.assertEqual(got["Done"], ["stories_completed", "events_completed", "raids_completed"])

    def test_shape_ref_array_bounds_and_inline_refine(self):
        self.write("app/drizzle/constants.ts", "export const PET_MAX_ABILITY_SLOTS = 6;\nexport const AI_PROFILE_MAX_RULES = 20;\n")
        self.write("app/src/validators/pets.ts", """
export const petAiProfileSchema = z.object({
  rules: z.array(AiRule).max(AI_PROFILE_MAX_RULES),
  includeDefaultRules: z.boolean(),
});
""")
        rel = "app/src/validators/petSpecies.ts"
        self.write(rel, """
export const PetSpeciesValidator = z
  .object({
    rankConcepts: z.array(z.string().max(1000).nullish()).max(10).default([]),
    defaultJutsuIds: z.array(z.string().min(1).max(191)).max(PET_MAX_ABILITY_SLOTS).default([]),
    aiRules: petAiProfileSchema.shape.rules.default([]),
    includeDefaultRules: petAiProfileSchema.shape.includeDefaultRules.default(true),
  })
  .superRefine((species, ctx) => {});
""")
        consts = se.extract_constants(self.root)
        e = se.extract_entity(self.root, rel, "PetSpeciesValidator", consts)
        f = e["fields"]
        self.assertEqual(e["superRefine"], ["<inline>"])
        self.assertEqual((f["defaultJutsuIds"].get("max"), f["defaultJutsuIds"].get("min")), (6, None),
                         "the array's bound, not the element's .min(1).max(191)")
        self.assertEqual((f["rankConcepts"]["optional"], f["rankConcepts"]["nullable"], f["rankConcepts"]["max"]), (False, False, 10))
        self.assertEqual(f["aiRules"]["shape_ref"], "petAiProfileSchema.shape.rules")
        self.assertEqual((f["aiRules"]["max"], f["aiRules"]["default"]), (20, []))
        self.assertEqual((f["includeDefaultRules"]["type"], f["includeDefaultRules"]["default"]), ("boolean", True))


class LedgerBoundClass(unittest.TestCase):
    def test_upper_bound_reads_a_named_constant(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "app/drizzle"))
            os.makedirs(os.path.join(root, "app/src/validators"))
            Path(root, "app/drizzle/constants.ts").write_text("export const MAX_PLAYER_LEVEL = 110;\n")
            self.assertEqual(sal.upper_bound(root, "z.coerce.number().min(1).max(MAX_PLAYER_LEVEL)"), 110)
            self.assertEqual(sal.upper_bound(root, "z.coerce.number().min(1).max(100)"), 100)
            self.assertIsNone(sal.upper_bound(root, "z.coerce.number().max(NOT_DECLARED)"))
        self.assertIn("upstream_bound_changed", sal.CLASSES)


class Contracts(unittest.TestCase):
    def test_adopted_contracts_carry_the_pet_surface(self):
        c, d, k, g = (json.loads((DATA / f).read_text()) for f in (
            "45c_DATA_constructors.json", "45d_DATA_entity_schemas.json", "45e_DATA_constants.json", "45g_DATA_checks.json"))
        k = k["constants"]
        self.assertIn("3314d122", d["_provenance"]["source_drop"])  # re-pinned from 2af4b320 (RUL-2026-10-29-047)
        self.assertIn("reward_pet_experience", c["unions"]["AllTags"]["noncombatconsumereward"]["fields"])
        self.assertIn("reward_pets", c["unions"]["AllTags"]["noncombatconsumereward"]["fields"])
        self.assertEqual(sorted(d["entities"]["petSpecies"]["fields"]), sorted(
            ["name", "description", "artDirection", "rankConcepts", "rarity", "role", "preferredDamageElement",
             "isActive", "defaultJutsuIds", "aiRules", "includeDefaultRules", "effects"]))
        # 3314d122: skillTarget moved from the species onto each innate effect
        self.assertEqual(sorted(c["intersections"]["PetSpeciesEffect"]["fields"]), ["skillTarget"])
        self.assertIn("requiredPetSpeciesId", d["entities"]["jutsu"]["fields"])
        self.assertIn("PETS", g["enums"]["fields"]["jutsu"]["jutsuType"])
        self.assertEqual(k["PET_AI_ACTION_TYPES"]["value"], ["move_towards_opponent", "end_turn", "use_highest_power_action"])
        self.assertEqual(g["required_on_create"]["fields"]["petSpecies"], ["description", "isActive", "name", "rarity"])
        for f in ("45c_DATA_constructors.json", "45g_DATA_checks.json"):
            self.assertEqual((ROOT / f).read_bytes(), (DATA / f).read_bytes(), "root copy equals skill data/")


class Validate(unittest.TestCase):
    def test_good_fixtures_pass_strict(self):
        for f in ("species_create.json", "pet_jutsu_create.json", "species_defaults_edit.json", "pet_rewards.json"):
            code, out = validate(f)
            self.assertEqual(code, 0, f + "\n" + out)

    def test_bad_fixtures_fail_for_their_reasons(self):
        expect = {
            "species_bad.json": ["isActive must be false", "only once", "exceed the 4 slots", "empty-ground",
                                 "COORDINATES", "unknown key 'colour'", "pet AI action 'use_random_jutsu'"],
            "pet_jutsu_bad.json": ["jutsuWeapon must be NONE", "elementClassification must be None",
                                   "injectableInBattle must be false", "actionCostPerc must be 10-100",
                                   "'stun' is not a pet effect", "carries elements", "needs jutsuType PETS"],
            "species_defaults_same_manifest.json": ["created hidden in this manifest"],
            "pet_rewards_bad.json": ["at most 1 companion", "require standard rewards", "prevent battle usage",
                                     "reward_pets is not a quest reward", "reward_pet_experience must be a number >= 0"],
        }
        for f, needles in expect.items():
            code, out = validate(f)
            self.assertNotEqual(code, 0, f)
            for n in needles:
                self.assertIn(n, out, f)

    def test_build_order_is_slot_aware(self):
        m = {"items": [
            {"entity": "petSpecies", "slot": "edit", "name": "S", "targetId": "fxPetSpecies000000001",
             "data": {"rarity": "COMMON", "defaultJutsuIds": ["fxPetJutsu00000000001"]}},
            {"entity": "jutsu", "slot": "edit", "name": "J", "targetId": "fxPetJutsu00000000001",
             "data": {"description": "x", "injectableInBattle": False}},
        ]}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(m, fh)
        try:
            r = subprocess.run([sys.executable, "../scripts/validate.py", fh.name], cwd=DATA, capture_output=True, text=True)
        finally:
            os.unlink(fh.name)
        self.assertIn("build order: jutsu appears after a later phase", r.stdout)


def validate_doc(doc, strict=True):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(doc, fh)
    try:
        args = [sys.executable, "../scripts/validate.py"] + (["--strict"] if strict else []) + [fh.name]
        r = subprocess.run(args, cwd=DATA, capture_output=True, text=True)
    finally:
        os.unlink(fh.name)
    return r.returncode, r.stdout + r.stderr


def species_with(**over):
    m = json.loads((FIX / "species_create.json").read_text())
    m["items"][0]["data"].update(over)
    return m


class ReviewFixes(unittest.TestCase):
    """Independent review of 45b02007, findings 3 and 4 (Python side)."""

    def test_f3_explicitly_empty_effects_on_a_pets_edit_refused(self):
        edit = {"entity": "jutsu", "slot": "edit", "name": "Fixture Glow", "targetId": "fxPetJutsu00000000001",
                "data": {"jutsuType": "PETS", "injectableInBattle": False, "effects": []}}
        code, out = validate_doc({"items": [edit]})
        self.assertNotEqual(code, 0)
        self.assertIn("its effects are explicitly empty", out)
        del edit["data"]["effects"]  # a partial edit may leave them to the live record
        code, out = validate_doc({"items": [edit]})
        self.assertEqual(code, 0, out)
        create = json.loads((FIX / "pet_jutsu_create.json").read_text())
        del create["items"][0]["data"]["effects"]
        code, out = validate_doc(create)
        self.assertIn("it has no effects", out)

    def test_f4_sparse_and_trimmed_rank_concepts(self):
        self.assertEqual(validate_doc(species_with(rankConcepts=["first rank", None, "third rank"]))[0], 0)
        self.assertEqual(validate_doc(species_with(rankConcepts=["  " + "x" * 1000 + "  "]))[0], 0, "1000 after trimming")
        for bad, why in ((["x" * 1001], "at most 1000"), ([1, "a"], "list of strings"), ("a", "list of strings"),
                         (["r"] * 11, "there are 10 pet ranks")):
            code, out = validate_doc(species_with(rankConcepts=bad))
            self.assertNotEqual(code, 0, bad)
            self.assertIn(why, out)

    def test_f2_cap_counts_every_effect(self):
        m = json.loads((FIX / "pet_rewards.json").read_text())
        m["items"] = m["items"][:1]
        self.assertEqual(validate_doc(m)[0], 0)
        m["items"][0]["data"]["effects"].append(dict(m["items"][0]["data"]["effects"][0]))
        code, out = validate_doc(m)
        self.assertIn("at most 1 companion (2 in reward_pets)", out)


if __name__ == "__main__":
    unittest.main()
