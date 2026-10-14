#!/usr/bin/env python3
"""Focused regression tests for schema_extract.py source fidelity (QW-0A slice A).

Socket-free and static: every case runs the extractor CLI over a minimal source
tree under data/fixtures/qw0a/ and asserts expected contract facts and refusals.
Nothing is compared against the extractor's own fresh output.

    python3 test_schema_extract.py
    SCHEMA_EXTRACT=/path/to/other/schema_extract.py python3 test_schema_extract.py

The second form runs the same assertions against another extractor (for example
the pre-QW-0A baseline) to show which known-bug cases it fails.
"""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRACTOR = os.environ.get("SCHEMA_EXTRACT") or os.path.join(HERE, "schema_extract.py")
FIXTURES = os.path.join(HERE, "..", "data", "fixtures", "qw0a")


def run(case, mode):
    proc = subprocess.run([sys.executable, EXTRACTOR, os.path.join(FIXTURES, case), mode],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


_CACHE = {}


def emit(mode, case="positive"):
    if (case, mode) not in _CACHE:
        code, out, err = run(case, mode)
        if code != 0:
            raise AssertionError("%s %s exited %d: %s" % (case, mode, code, err.strip()[:300]))
        _CACHE[(case, mode)] = json.loads(out)
    return _CACHE[(case, mode)]


def tag(variant):
    return emit("--ctors")["unions"]["AllTags"][variant]["fields"]


def item():
    return emit("--entities")["entities"]["item"]["fields"]


def const(name):
    return emit("--constants")["constants"][name]


class ArraySpreads(unittest.TestCase):
    def test_constant_spread_resolves_in_source_order(self):
        self.assertEqual(const("ElementNames")["value"], ["Fire", "Water", "Ice", "None"])

    def test_transitive_spread(self):
        self.assertEqual(const("NestedNames")["value"], ["Fire", "Water", "Ice", "None", "Extra"])

    def test_two_spreads_in_one_list(self):
        self.assertEqual(const("UserStatNames")["value"],
                         ["None", "Ninjutsu", "Genjutsu", "ninjutsuMastery", "sageMastery"])

    def test_combat_constants_module(self):
        self.assertEqual(const("allState")["value"], ["avatar", "level", "items"])

    def test_enum_by_reference_has_real_members(self):
        f = tag("damage")["elements"]
        self.assertEqual(f["enum_ref"], "ElementNames")
        self.assertIn("Fire", f["enum"])
        self.assertNotIn("...BasicElementName", f["enum"])

    def test_validator_local_spread_list(self):
        f = tag("damage")["target"]
        self.assertEqual(f["enum_ref"], "ActionTargets@validators/combat.ts")
        self.assertEqual(sorted(f["enum"]), ["COORDINATES", "INHERIT", "SELF"])

    def test_non_leading_inline_spread(self):
        self.assertEqual(tag("damage")["reward_mastery_stat"]["enum"],
                         ["None", "ninjutsuMastery", "sageMastery"])


class MultilineAndDelimiters(unittest.TestCase):
    def test_multiline_field_is_not_dropped(self):
        f = tag("damage")["statTypes"]
        self.assertEqual(f["type"], "array")
        self.assertTrue(f["optional"])
        # z.enum([...StatTypes, "Highest"]): the legacy input stays accepted
        self.assertEqual(sorted(f["enum"]), ["Genjutsu", "Highest", "Ninjutsu", "None"])

    def test_multiline_chain_keeps_type_and_bounds(self):
        self.assertEqual(tag("damage")["rounds"],
                         {"type": "number", "default": 3, "min": 0, "max": 3, "int": True})

    def test_nested_item_fields_do_not_leak(self):
        fields = tag("damage")
        self.assertNotIn("text", fields)
        self.assertNotIn("leaked", fields)
        self.assertEqual(fields["options"], {"type": "array", "default": []})

    def test_string_with_braces_and_commas(self):
        self.assertEqual(tag("damage")["description"]["default"], "Deals damage, {braces} and, commas")

    def test_multiline_schema_head(self):
        self.assertIn("item", emit("--entities")["entities"])


class SpreadPrecedence(unittest.TestCase):
    def test_later_spread_wins(self):
        # PowerAttributes.power (min 0, no max) is spread after BaseAttributes.power
        self.assertEqual(tag("damage")["power"], {"type": "number", "default": 1, "min": 0})

    def test_spread_after_own_field_wins(self):
        # OverrideTag declares calculation, then spreads BaseAttributes over it
        self.assertEqual(tag("override")["calculation"]["enum"], ["static"])

    def test_cross_module_object_spread(self):
        fields = tag("damage")
        self.assertEqual(fields["reward_money"], {"type": "number", "default": 0, "min": 0})
        self.assertEqual(fields["reward_flag"], {"type": "boolean", "default": False})


class Helpers(unittest.TestCase):
    def test_type_helper(self):
        self.assertEqual(tag("override")["direction"],
                         {"type": "literal", "default": "offence", "literal": "offence"})

    def test_discriminant_is_type_not_inherited_literal(self):
        spec = emit("--ctors")["unions"]["AllTags"]
        self.assertEqual(sorted(spec), ["damage", "override"])
        self.assertEqual(spec["damage"]["discriminant"], {"field": "type", "value": "damage"})

    def test_cross_file_helper_bounds_and_omission(self):
        f = item()["requiredStrength"]
        self.assertEqual((f["type"], f["max"], f["max_ref"], f["min"]), ("number", 400000, "MAX_CAP", 0))
        self.assertTrue(f["nullable"])
        self.assertTrue(f["optional"])
        self.assertIn("undefined to null", f["_omission"])
        self.assertNotIn("MAX_CAP(", f["raw"])

    def test_cross_file_helper_on_single_line_head(self):
        f = emit("--entities")["entities"]["jutsu"]["fields"]["requiredStrength"]
        self.assertEqual((f["type"], f["max"], f["optional"], f["nullable"]), ("number", 400000, True, True))

    def test_nullable_is_not_omissible(self):
        f = item()["strictCapped"]
        self.assertTrue(f["nullable"])
        self.assertFalse(f["optional"])
        self.assertNotIn("_omission", f)

    def test_constant_default(self):
        f = item()["maxDelay"]
        self.assertEqual((f["default"], f["default_ref"], f["optional"]), (3, "DEFAULT_DELAY", False))


class OmissionInference(unittest.TestCase):
    """QW0A-A-R1: optional:true only from a proven callback form and an outer
    nullable/optional inner schema; never from a substring."""

    def required(self):
        return emit("--checks")["required_on_create"]["fields"]["item"]

    def gaps(self):
        code, out, err = run("positive", "--gaps")
        self.assertEqual(code, 0, err)
        return {d["where"].rsplit(" field ", 1)[-1]: d for d in json.loads(out)["diagnostics"]}

    def assert_not_omissible(self, name):
        f = item()[name]
        self.assertFalse(f["optional"], name)
        self.assertNotIn("_omission", f)
        self.assertIn(name, self.required())

    def test_negated_predicate(self):
        # (v !== undefined ? null : v) returns undefined for undefined
        self.assert_not_omissible("negatedInput")
        self.assertEqual(self.gaps()["negatedInput"]["code"], "G_PREPROCESS_UNCLASSIFIED")

    def test_constrained_conjunction(self):
        # (v === undefined && false ? null : v) is false for undefined
        self.assert_not_omissible("constrainedInput")
        self.assertEqual(self.gaps()["constrainedInput"]["code"], "G_PREPROCESS_UNCLASSIFIED")

    def test_nested_nullable_is_not_outer_nullable(self):
        # null is produced, but only the array's elements accept it
        self.assert_not_omissible("nestedNullableInput")
        self.assertFalse(item()["nestedNullableInput"]["nullable"])

    def test_positive_strict_undefined(self):
        f = item()["validInput"]
        self.assertTrue(f["optional"] and f["nullable"])
        self.assertNotIn("validInput", self.required())

    def test_positive_loose_null_pinned_form(self):
        # nullableInteger at 585534d7: value === "" || value == null ? null : value
        f = item()["looseInput"]
        self.assertTrue(f["optional"] and f["nullable"])
        self.assertIn("undefined to null", f["_omission"])

    def test_positive_pass_through_pinned_form(self):
        # requiredSageRank at both pins: v === "" ? null : v, inner .nullish()
        f = item()["passThroughInput"]
        self.assertTrue(f["optional"])
        self.assertIn("passes undefined through", f["_omission"])

    def test_pinned_capped_helper_still_omissible(self):
        self.assertNotIn("requiredStrength", self.required())

    # re-review: undefined -> null reaches a non-nullable inner schema, so an
    # inner optional/default never applies; omission is rejected, not unknown
    def assert_rejected(self, name, inner_default=None):
        f = item()[name]
        self.assertFalse(f["optional"], name)
        self.assertNotIn("default", f)
        self.assertNotIn("_omission", f)
        self.assertEqual(f.get("_inner_default"), inner_default)
        self.assertIn(name, self.required())
        self.assertNotIn(name, self.gaps(), "a proven rejection is classified, not a gap")

    def test_rejected_inner_optional(self):
        self.assert_rejected("rejectedOptionalInput")

    def test_rejected_inner_default(self):
        self.assert_rejected("rejectedDefaultInput", inner_default=7)

    def test_rejected_inner_prefault(self):
        self.assert_rejected("rejectedPrefaultInput", inner_default=7)

    def assert_default_fallback(self, name):
        f = item()[name]
        self.assertEqual(f["default"], 7)
        self.assertIn("inner schema's default", f["_omission"])
        self.assertNotIn(name, self.required())

    def test_pass_through_to_inner_default(self):
        self.assert_default_fallback("acceptedDefaultInput")

    def test_pass_through_to_inner_prefault(self):
        self.assert_default_fallback("acceptedPrefaultInput")

    def test_unclassified_callback_is_conservatively_required(self):
        # the inner .optional() must not leak through an unrecognised callback
        self.assert_not_omissible("negatedOptionalInput")
        self.assertEqual(self.gaps()["negatedOptionalInput"]["code"], "G_PREPROCESS_UNCLASSIFIED")


class NestedFacts(unittest.TestCase):
    """QW0A-A-R2: a nested schema's bounds and coercion are not the field's."""

    def test_entity_nested_bound_not_outer(self):
        f = item()["nestedBoundInput"]
        self.assertNotIn("max", f)
        self.assertNotIn("max_ref", f)
        self.assertFalse(f["coerce"])

    def test_entity_outer_bound_kept(self):
        f = item()["outerBoundInput"]
        self.assertEqual((f["max"], f["max_ref"]), (400000, "MAX_CAP"))

    def test_entity_crafting_requirements_shape(self):
        # mirrors 585534d7 ItemValidatorRawSchema.craftingRequirements
        f = item()["craftingRequirements"]
        self.assertEqual((f["type"], f["default"], f["optional"], f["nullable"], f["coerce"]),
                         ("array", [], True, True, False))
        for key in ("max", "max_ref", "min", "int"):
            self.assertNotIn(key, f)

    def test_entity_outer_coercion_kept(self):
        self.assertTrue(item()["maxDelay"]["coerce"])

    def test_constructor_nested_bound_not_outer(self):
        self.assertEqual(tag("damage")["boundProbe"], {"type": "array", "optional": True})

    def test_constructor_outer_bound_kept(self):
        self.assertEqual(tag("damage")["outerBound"], {"type": "array", "max": 400000, "optional": True})


class FalsyMetadata(unittest.TestCase):
    def test_zero_default_and_bound_are_kept(self):
        self.assertEqual(tag("damage")["powerPerLevel"],
                         {"type": "number", "default": 0, "min": -1, "max": 1})

    def test_false_default_is_kept(self):
        self.assertEqual(tag("override")["allowFlag"], {"type": "boolean", "default": False})

    def test_null_default_is_kept(self):
        self.assertEqual(tag("override")["nullDefault"], {"type": "string", "default": None, "nullable": True})


class Refusals(unittest.TestCase):
    def assert_refused(self, case, mode, code_name):
        code, out, err = run(case, mode)
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "", "a refused extraction must not emit a partial contract")
        self.assertIn(code_name, err)

    def test_unresolved_array_spread(self):
        self.assert_refused("unresolved_array", "--constants", "E_UNRESOLVED_SPREAD")

    def test_cyclic_array_spread(self):
        self.assert_refused("cycle_array", "--constants", "E_CYCLE")

    def test_unresolved_object_spread(self):
        self.assert_refused("unresolved_object", "--ctors", "E_UNRESOLVED_SPREAD")

    def test_cyclic_object_spread(self):
        self.assert_refused("cycle_object", "--ctors", "E_CYCLE")

    def test_gaps_are_reported_not_fatal(self):
        code, out, err = run("positive", "--gaps")
        self.assertEqual(code, 0, err)
        codes = {d["code"] for d in json.loads(out)["diagnostics"]}
        self.assertIn("G_INLINE_REFINE", codes)
        self.assertIn("G_PREPROCESS_UNCLASSIFIED", codes)


class Determinism(unittest.TestCase):
    def test_repeat_runs_are_identical(self):
        for mode in ("--ctors", "--constants"):
            self.assertEqual(run("positive", mode)[1], run("positive", mode)[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
