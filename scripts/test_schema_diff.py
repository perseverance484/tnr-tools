#!/usr/bin/env python3
"""Regression tests for the generated-contract adoption gate (schema_diff.py).

    python3 -m unittest scripts/test_schema_diff.py -v

Synthetic 45c/45d/45f/45g documents only; no game source, no network.
PR #76 review F2: a type-only change inside an existing 45c union-variant field produced no atom,
so `diff OLD NEW` reported nothing breaking and needed no ledger.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "building-tnr-content" / "scripts"))
import schema_diff as sd  # noqa: E402

CTORS = {
    "_contract": {},
    "unions": {
        "AllTags": {
            "damage": {"schema": "DamageTag", "discriminant": {"field": "type", "value": "damage"},
                       "fields": {"type": {"type": "literal", "literal": "damage", "default": "damage"},
                                  "power": {"type": "number", "default": 1, "min": 0},
                                  "rounds": {"type": "number", "optional": True},
                                  "statTypes": {"type": "array", "optional": True,
                                                "enum": ["None", "Ninjutsu"], "enum_ref": "StatTypes"}}},
        }
    },
}


class Gate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, doc):
        p = self.dir / name
        p.write_text(json.dumps(doc, indent=1))
        return str(p)

    def diff(self, old, new, ledger=None):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = sd.cmd_diff(old, new, ledger)
        return code, out.getvalue()

    def breaking(self, old_doc, new_doc):
        return sd.classify(sd.atoms(old_doc), sd.atoms(new_doc))[3]

    def ledger(self, old, new, atoms, cls="upstream_field_removed", evidence="source read at both pins"):
        sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
        return self.write("ledger.json", {
            "classes": {cls: {"evidence": evidence}},
            "files": [{"old_sha256": sha(old), "new_sha256": sha(new),
                       "accepted": [{"atom": list(a), "class": cls} for a in atoms]}]})

    # ---- F2: union-variant field type and required-ness -----------------------------------------

    def test_variant_field_type_change_is_breaking(self):
        new = copy.deepcopy(CTORS)
        new["unions"]["AllTags"]["damage"]["fields"]["power"]["type"] = "string"
        self.assertEqual(sd.atoms(CTORS) == sd.atoms(new), False, "a type flip must change the atom set")
        self.assertEqual(self.breaking(CTORS, new), [("type-changed", "AllTags.damage", "power", "number -> string")])
        code, out = self.diff(self.write("old.json", CTORS), self.write("new.json", new))
        self.assertEqual(code, 1)
        self.assertIn("type-changed", out)

    def test_variant_field_type_change_passes_only_with_exact_evidenced_ledger(self):
        new = copy.deepcopy(CTORS)
        new["unions"]["AllTags"]["damage"]["fields"]["power"]["type"] = "string"
        old_p, new_p = self.write("old.json", CTORS), self.write("new.json", new)
        flip = ("type-changed", "AllTags.damage", "power", "number -> string")
        self.assertEqual(self.diff(old_p, new_p, self.ledger(old_p, new_p, [flip]))[0], 0)
        # unevidenced class
        self.assertEqual(self.diff(old_p, new_p, self.ledger(old_p, new_p, [flip], evidence=""))[0], 1)
        # stale extra entry
        stale = ("variant-field", "AllTags.damage", "rounds")
        self.assertEqual(self.diff(old_p, new_p, self.ledger(old_p, new_p, [flip, stale]))[0], 1)
        # missing entry
        self.assertEqual(self.diff(old_p, new_p, self.ledger(old_p, new_p, []))[0], 1)
        # a different NEW file voids the ledger, however similar
        led = self.ledger(old_p, new_p, [flip])
        new["unions"]["AllTags"]["damage"]["fields"]["power"]["min"] = 1
        self.assertEqual(self.diff(old_p, self.write("new.json", new), led)[0], 1)

    def test_variant_field_dropping_its_type_is_breaking(self):
        new = copy.deepcopy(CTORS)
        del new["unions"]["AllTags"]["damage"]["fields"]["power"]["type"]
        self.assertEqual(self.breaking(CTORS, new), [("type-changed", "AllTags.damage", "power", "number -> (none)")])

    def test_variant_field_optional_to_required_is_breaking(self):
        new = copy.deepcopy(CTORS)
        del new["unions"]["AllTags"]["damage"]["fields"]["rounds"]["optional"]
        self.assertEqual(self.breaking(CTORS, new), [("now-required", "AllTags.damage", "rounds", "optional -> required")])

    def test_new_required_variant_field_is_additive(self):
        new = copy.deepcopy(CTORS)
        new["unions"]["AllTags"]["damage"]["fields"]["apReduction"] = {"type": "number"}
        self.assertEqual(self.breaking(CTORS, new), [])

    def test_variant_field_removal_is_breaking_once(self):
        new = copy.deepcopy(CTORS)
        del new["unions"]["AllTags"]["damage"]["fields"]["statTypes"]
        got = self.breaking(CTORS, new)
        self.assertIn(("variant-field", "AllTags.damage", "statTypes"), got)
        self.assertFalse([a for a in got if a[0] == "type-changed"], "a removed field is not also a type change")

    # ---- the other blind spots fixed on this branch -------------------------------------------------

    def test_entity_type_change_still_breaking(self):
        old = {"entities": {"item": {"fields": {"cost": {"type": "number", "optional": True}}}}}
        new = {"entities": {"item": {"fields": {"cost": {"type": "string", "optional": True}}}}}
        self.assertEqual(self.breaking(old, new), [("type-changed", "item", "cost", "number -> string")])

    def test_45g_entry_removal_is_breaking(self):
        old = {"_contract": {}, "nullable": {"_class": "derived", "fields": {"item": ["bloodlineId", "image"]}}}
        new = {"_contract": {}, "nullable": {"_class": "derived", "fields": {"item": ["bloodlineId"]}}}
        self.assertEqual(self.breaking(old, new), [("check", "nullable.fields.item", '"image"')])

    def test_45f_procedure_removal_is_breaking(self):
        old = {"routers": {"train": {"stopTraining": {"procedure": "protectedProcedure", "kind": "mutation"}}}}
        got = self.breaking(old, {"routers": {"train": {}}})
        self.assertIn(("procedure", "train", "stopTraining"), got)

    # ---- 45c intersections (PetSpeciesEffect = AllTags.and({skillTarget}), 3314d122) ------------

    def test_intersection_key_and_enum_member_removal_is_breaking(self):
        old = {"_contract": {}, "unions": {}, "intersections": {"PetSpeciesEffect": {"base": "AllTags", "fields": {
            "skillTarget": {"type": "enum", "optional": True, "enum": ["ENEMIES", "SELF"]}}}}}
        less = copy.deepcopy(old)
        less["intersections"]["PetSpeciesEffect"]["fields"]["skillTarget"]["enum"] = ["SELF"]
        self.assertEqual(self.breaking(old, less), [("enum-member", "PetSpeciesEffect.skillTarget", "ENEMIES")])
        gone = copy.deepcopy(old)
        gone["intersections"]["PetSpeciesEffect"]["fields"] = {}
        self.assertIn(("variant-field", "PetSpeciesEffect", "skillTarget"), self.breaking(old, gone))
        self.assertEqual(self.breaking({"_contract": {}, "unions": {}}, old), [], "a new intersection is additive")


if __name__ == "__main__":
    unittest.main()
