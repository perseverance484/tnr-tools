#!/usr/bin/env python3
"""Selftest for check_draft.py: the committed draft passes; each hard check fails closed.

    python3 harness/crafting_caches/selftest.py
"""
import copy
import os
import socket
import sys
import tempfile
import unittest


def _no_network(*_a, **_k):
    raise AssertionError("selftest attempted a network connection")


socket.socket = _no_network  # type: ignore[misc,assignment]
socket.create_connection = _no_network  # type: ignore[assignment]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_draft as C  # noqa: E402

DRAFT, CENSUS = C.load(C.DRAFT, C.CENSUS)


def line(d, name):
    return next(ln for c in d["caches"] for ln in c["lines"] if ln["name"] == name)


class Draft(unittest.TestCase):
    def expect(self, mutate, needle):
        d = copy.deepcopy(DRAFT)
        mutate(d)
        errs = C.check(d, CENSUS)
        self.assertTrue(any(needle in e for e in errs), (needle, errs))

    def test_committed_draft_is_clean(self):
        self.assertEqual(C.check(DRAFT, CENSUS), [])

    def test_report_is_current(self):
        self.assertEqual(C.main(["--check"]), 0)

    def test_common_factor_with_recipe(self):
        self.expect(lambda d: line(d, "Rainbow Cabochon").update(quantity=6), "shares a factor")

    def test_unknown_id(self):
        self.expect(lambda d: line(d, "Iron Ore").update(id="nope"), "not in census")

    def test_name_mismatch(self):
        self.expect(lambda d: line(d, "Iron Ore").update(name="Iron Ingot"), "census name")

    def test_excluded_item(self):
        def m(d):
            hid = next(k for k, v in d["exclusions"]["ids"].items() if v == "Heart of Kaeruun")
            d["caches"][1]["lines"].append({"id": hid, "name": "Heart of Kaeruun", "quantity": 1, "chance": 1, "band": "rare"})
        self.expect(m, "exclusion list")

    def test_event_item(self):
        def m(d):
            uid = next(i["id"] for i in CENSUS["items"] if i["name"] == "Unobtanium")
            d["exclusions"]["ids"].pop(uid)
            d["caches"][1]["lines"].append({"id": uid, "name": "Unobtanium", "quantity": 1, "chance": 1, "band": "rare"})
        self.expect(m, "event item")

    def test_hidden_item(self):
        def m(d):
            h = next(i for i in CENSUS["items"] if i["hidden"])
            d["caches"][0]["lines"].append({"id": h["id"], "name": h["name"], "quantity": 1, "chance": 1, "band": "rare"})
        self.expect(m, "hidden")

    def test_bad_chance_and_quantity(self):
        self.expect(lambda d: line(d, "Iron Ore").update(chance=0), "chance 0")
        self.expect(lambda d: line(d, "Silver Ore").update(quantity=100000), "stackSize")

    def test_wrong_census(self):
        self.expect(lambda d: d["census"].update(capture_sha256="0" * 64), "different census")

    def test_stale_report_detected(self):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "r.md")
            open(p, "w").write("old\n")
            self.assertEqual(C.main(["--check", "--report", p]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
