#!/usr/bin/env python3
"""Tests for scripts/player_allowlist.py. Socket-free; reads repository files and temporary copies only.

    python3 -m unittest scripts/test_player_allowlist.py -v

One test per rule of state/prompt_ai_player_overhaul.md section 2 that an endpoint list can carry, then the
surface capture, the code scan, and the committed list against its own gates.
"""
import contextlib
import copy
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import player_allowlist as pa  # noqa: E402

ALLOW = pa._load(pa.ALLOWLIST)


def entry(kind="action", **more):
    e = {"kind": kind, "activity": ["world"], "phase": "AP1", "status": "proposed", "prerequisites": "none",
         "cooldown": "none known"}
    e.update(more)
    return e


def with_entry(name, e):
    """The committed rules with one endpoint entry and nothing else."""
    allow = copy.deepcopy(ALLOW)
    allow["endpoints"] = {name: e}
    return allow


def errors(name, e, surface=None):
    return pa.check(with_entry(name, e), surface)[0]


SCHEMA = {"type": "object", "properties": {}, "additionalProperties": False}


def surface(rows, schema=SCHEMA):
    """{"router.endpoint": type} -> a live surface capture, every endpoint with the given input schema."""
    routers = {}
    for name, kind in rows.items():
        r, ep = name.split(".", 1)
        routers.setdefault(r, {"endpointCount": None, "endpoints": {}})["endpoints"][ep] = {
            "type": kind, "type_source": "test", "description": "", "schema": schema}
    return {"_meta": {"live": True, "origin": "test", "captured": {"last": "now"},
                      "counts": {"routers": len(routers), "endpoints": len(rows), "schemas": 0}}, "routers": routers}


class NeverRules(unittest.TestCase):
    def refused(self, name, rule, kind="action"):
        errs = errors(name, entry(kind))
        self.assertTrue(any(f"NEVER ({rule}:" in x for x in errs), (name, errs))

    def test_payments(self):
        for name in ("paypal.createStoreOrder", "stripe.createCheckout", "merch.checkout"):
            self.refused(name, "payments")
        self.refused("purchases.catalogue", "payments", kind="read")      # the whole router, reads too

    def test_account_deletion_and_control(self):
        for name in ("accountDeletion.request", "profile.confirmDeletion", "profile.toggleDeletionTimer",
                     "nativeAuth.approve", "register.createCharacter", "parentalControls.save"):
            self.refused(name, "account_control")

    def test_moderation_and_reports(self):
        for name in ("reports.create", "reports.ban", "forum.moderatePost", "forum.lockThread"):
            self.refused(name, "moderation")
        self.refused("reports.getAll", "moderation", kind="read")

    def test_staff_powers_and_staff_data(self):
        for name in ("staff.forceAwake", "misc.awardReputation", "profile.updateUser", "item.adjustUserItem",
                     "jutsu.adjustUserJutsu", "contentReview.approve"):
            self.refused(name, "staff")
        for name in ("data.getJutsuBalanceStatistics", "staff.getUserHistoricalIps", "logs.getContentChanges",
                     "bloodline.getUserHistoricBloodlinesForStaff"):
            self.refused(name, "staff", kind="read")

    def test_content_editing(self):
        for name in ("jutsu.create", "item.update", "quests.clone", "bloodline.createReskin", "gameAsset.create",
                     "conceptart.toggleEmotion", "pvpRank.createSeason", "worldMap.publishSectorMap",
                     "spriteStudio.generate", "generativeAi.createImg", "gameAsset.prepareLpcSheet"):
            self.refused(name, "content_editing")

    def test_chat_messages_and_posts(self):
        for name in ("comments.createConversation", "comments.createConversationComment", "forum.createThread",
                     "forum.editPost", "clan.upsertNotice"):
            self.refused(name, "communication")

    def test_trade_requests(self):
        for name in ("auction.createAuctionOffer", "auction.acceptAuctionOffer"):
            self.refused(name, "communication")
        self.assertEqual(errors("auction.getAuctionOffers", entry("read")), [])

    def test_deletes(self):
        for name in ("quests.deleteUserQuest", "sensei.removeStudent", "avatar.deleteAvatar",
                     "bounty.removeAllTrackers", "hunting.delete", "jutsu.forget", "pets.releasePet"):
            self.refused(name, "deletes")

    def test_a_read_is_not_caught_by_an_actions_only_rule(self):
        self.assertEqual(errors("forum.getThreads", entry("read")), [])

    def test_an_exception_must_be_written_into_the_rule(self):
        allow = with_entry("bounty.create", entry())
        self.assertTrue(pa.check(allow)[0])
        next(r for r in allow["never"] if r["id"] == "content_editing")["except"] = ["bounty.create"]
        self.assertEqual(pa.check(allow)[0], [])


class AskFirstRules(unittest.TestCase):
    def test_premium_currency_must_be_marked(self):
        for name in ("blackmarket.buyItemSlot", "bloodline.roll", "item.purchaseVariant", "home.upgradeHome",
                     "occupation.finishCraftingImmediately", "bloodright.purchase"):
            errs = errors(name, entry())
            self.assertTrue(any("ASK FIRST (premium_currency" in x for x in errs), (name, errs))
            self.assertEqual(errors(name, entry(ask_first="premium_currency")), [])

    def test_ryo_only_waiver_needs_its_statement_and_both_gates(self):
        ok = entry(currency="the shop record has a ryo cost only", gates=["ryo_only", "spend_cap"])
        self.assertEqual(errors("farming.buyShopItem", ok), [])
        self.assertTrue(errors("farming.buyShopItem", entry(currency="ryo", gates=["ryo_only"])))
        self.assertTrue(errors("farming.buyShopItem", entry(currency="  ", gates=["ryo_only", "spend_cap"])))

    def test_leaving_the_clan(self):
        for name in ("clan.leaveClan", "village.leaveVillage"):
            self.assertTrue(any("ASK FIRST (leave_clan" in x for x in errors(name, entry())), name)
            self.assertEqual(errors(name, entry(ask_first="leave_clan")), [])

    def test_selling_items(self):
        for name in ("item.sellUserItem", "auction.createAuctionListing"):
            self.assertTrue(any("ASK FIRST (sell_rare_items" in x for x in errors(name, entry())), name)

    def test_marriage(self):
        self.assertTrue(any("ASK FIRST (marriage" in x for x in errors("marriage.createRequest", entry())))
        self.assertEqual(errors("marriage.getRequests", entry("read")), [])

    def test_an_unknown_ask_first_rule_is_an_error(self):
        self.assertTrue(errors("bank.toBank", entry(ask_first="whenever")))


class CallGates(unittest.TestCase):
    def test_no_flee_is_required_on_perform_action(self):
        self.assertTrue(any("'no_flee' is required" in x for x in errors("combat.performAction", entry())))
        self.assertEqual(errors("combat.performAction", entry(gates=["no_flee"])), [])

    def test_do_not_attack_and_no_snipe_are_required_on_attack(self):
        errs = errors("combat.attackUser", entry(gates=["fair_target"]))
        self.assertTrue(any("'do_not_attack' is required" in x for x in errs), errs)
        self.assertTrue(any("'no_snipe' is required" in x for x in errs), errs)

    def test_do_not_attack_is_required_on_robbing(self):
        self.assertTrue(any("'do_not_attack' is required" in x for x in errors("travel.robPlayer", entry())))

    def test_one_level_transfer_a_day(self):
        self.assertTrue(any("'one_transfer_a_day' is required" in x for x in errors("jutsu.transferLevel", entry())))
        self.assertEqual(errors("jutsu.transferLevel", entry(gates=["one_transfer_a_day"])), [])
        self.assertIn("one_transfer_a_day", ALLOW["endpoints"]["jutsu.transferLevel"]["gates"])

    def test_captchas_are_answered(self):
        # RUL-2026-11-11-149 item 2: the three captcha endpoints are on the list and no rule stops them
        for name in ("misc.getCaptcha", "misc.refreshCaptcha", "misc.verifyCaptcha"):
            self.assertIn(name, ALLOW["endpoints"])
            self.assertNotIn("ask_first", ALLOW["endpoints"][name])
        self.assertNotIn("no_captcha_answer", ALLOW["call_gates"])

    def test_spend_cap_is_required_on_ryo_spends(self):
        self.assertTrue(any("'spend_cap' is required" in x for x in errors("jutsu.startTraining", entry())))

    def test_an_undefined_gate_is_an_error(self):
        self.assertTrue(any("not defined" in x for x in errors("bank.toBank", entry(gates=["made_up"]))))


class Shape(unittest.TestCase):
    def test_every_field_is_needed(self):
        for drop in ("kind", "activity", "phase", "status", "prerequisites", "cooldown"):
            e = entry()
            del e[drop]
            self.assertTrue(errors("bank.toBank", e), drop)
        self.assertTrue(errors("bank.toBank", entry(activity=["shopping"])))
        self.assertTrue(errors("bank.toBank", entry(kind="write")))
        self.assertTrue(errors("toBank", entry()))
        self.assertEqual(errors("coop.quest.overview", entry("read")), [])     # a nested router name is a name


class Surface(unittest.TestCase):
    def test_an_entry_must_be_on_the_surface_with_the_same_kind(self):
        s = surface({"bank.toBank": "mutation", "bank.getGraph": "query", "bank.odd": None})
        self.assertEqual(errors("bank.toBank", entry("action"), s), [])
        self.assertTrue(any("surface says action" in x for x in errors("bank.toBank", entry("read"), s)))
        self.assertTrue(any("not on the captured surface" in x for x in errors("bank.toPocket", entry(), s)))
        errs, notes = pa.check(with_entry("bank.odd", entry()), s)
        self.assertEqual(errs, [])
        self.assertTrue(any("kind unchecked" in n for n in notes))

    def test_disposition_of_a_surface_endpoint(self):
        allow = with_entry("bank.toBank", entry())
        self.assertEqual(pa.disposition(allow, "bank.toBank", "action"), "allowed")
        self.assertEqual(pa.disposition(allow, "bank.transfer", "action"), "not listed")
        self.assertEqual(pa.disposition(allow, "stripe.createCheckout", "action"), "never: payments")
        allow["endpoints"]["clan.leaveClan"] = entry(ask_first="leave_clan")
        self.assertEqual(pa.disposition(allow, "clan.leaveClan", "action"), "ask first: leave_clan")

    def test_capture_from_a_transcript(self):
        def use(i, tool, inp):
            return {"timestamp": f"2026-11-11T19:50:{i:02d}Z", "message": {"content": [
                {"type": "tool_use", "id": f"u{i}", "name": f"mcp__Tnr__{tool}", "input": inp}]}}

        def res(i, text, err=False):
            return {"timestamp": f"2026-11-11T19:50:{i:02d}Z", "message": {"content": [
                {"type": "tool_result", "tool_use_id": f"u{i}", "is_error": err,
                 "content": [{"type": "text", "text": text}]}]}}

        rows = [
            use(1, "listGameRouters", {}),
            res(1, json.dumps([{"name": "bank", "endpointCount": 2}, {"name": "coop", "endpointCount": 2},
                               {"name": "train", "endpointCount": 1}])),
            use(2, "listRouterEndpoints", {"routerName": "bank"}),
            res(2, "Error POSTing to endpoint: Too Many Requests", err=True),
            use(3, "listRouterEndpoints", {"routerName": "bank"}),
            res(3, json.dumps([{"name": "bank.toBank", "description": "Deposit ryo"},
                               {"name": "bank.getGraph", "description": "query bank.getGraph"}])),
            use(4, "listRouterEndpoints", {"routerName": "coop"}),
            res(4, json.dumps([{"name": "coop.create", "description": "Start a party"},
                               {"name": "coop.quest.join", "description": "mutation coop.quest.join"}])),
            use(5, "getEndpointSchema", {"endpointName": "bank.toBank"}),
            res(5, json.dumps({"endpointName": "bank.toBank", "description": "Deposit ryo",
                               "inputSchema": {"type": "object", "properties": {"amount": {"type": "number"}},
                                               "required": ["amount"]}})),
            use(6, "callEndpoint", {"endpointName": "profile.getUser"}),        # a game call: never part of the surface
            res(6, json.dumps({"userData": {"username": "x"}})),
        ]
        with tempfile.TemporaryDirectory() as d:
            t = os.path.join(d, "t.jsonl")
            with open(t, "w") as f:
                f.write("\n".join(json.dumps(r) for r in rows) + "\n")
            src = os.path.join(d, "45f.json")
            with open(src, "w") as f:
                json.dump({"_provenance": {"source_drop": "test@abc"}, "routers": {
                    "bank": {"toBank": {"kind": "mutation"}}, "questParty": {"create": {"kind": "mutation"}}}}, f)
            s = pa.build_surface(pa.read_transcripts([t]), src)
        m = s["_meta"]
        self.assertTrue(m["live"])
        self.assertEqual(m["counts"], {"routers": 3, "endpoints": 4, "schemas": 1, "typed": 4, "untyped": 0})
        self.assertEqual(m["endpoint_count_mismatch"], [])
        self.assertEqual(m["routers_without_endpoint_list"], ["train"])
        self.assertEqual(m["failed_calls_never_answered"], [])               # the refused bank read was answered later
        self.assertEqual(m["replies_that_did_not_parse"], [])
        self.assertEqual(m["answered_calls"], {"listGameRouters": 1, "listRouterEndpoints": 2, "getEndpointSchema": 1})
        bank = s["routers"]["bank"]["endpoints"]
        self.assertEqual(bank["toBank"]["type"], "mutation")
        self.assertIn("source extract", bank["toBank"]["type_source"])
        self.assertEqual(bank["toBank"]["schema"]["required"], ["amount"])
        self.assertEqual((bank["getGraph"]["type"], bank["getGraph"]["type_source"]),
                         ("query", "the server's stand-in description"))
        self.assertIn("another router", s["routers"]["coop"]["endpoints"]["create"]["type_source"])
        self.assertEqual(s["routers"]["coop"]["endpoints"]["quest.join"]["type"], "mutation")
        self.assertIsNone(s["routers"]["train"]["endpoints"])
        self.assertNotIn("profile", s["routers"])


class CaptureCompleteness(unittest.TestCase):
    """Review of a95dfd1e, finding 1: a capture with missing schemas or failed calls passed the check, and a
    failed call followed by a reply cut short was counted as answered."""

    GOOD = json.dumps({"endpointName": "bank.toBank", "inputSchema": SCHEMA})
    CUT = '{"endpointName": "bank.toBank", "inputSchema": {"type": "obj'

    def build(self, *schema_replies):
        calls = [("listGameRouters", {}, json.dumps([{"name": "bank", "endpointCount": 1}]), "t1"),
                 ("listRouterEndpoints", {"routerName": "bank"},
                  json.dumps([{"name": "bank.toBank", "description": "Deposit ryo"}]), "t2")]
        calls += [("getEndpointSchema", {"endpointName": "bank.toBank"}, text, f"t{3 + i}")
                  for i, text in enumerate(schema_replies)]
        return pa.build_surface(calls)

    def test_a_listed_endpoint_needs_a_valid_schema_in_the_capture(self):
        allow = with_entry("bank.toBank", entry())
        self.assertEqual(pa.check(allow, surface({"bank.toBank": "mutation"}))[0], [])
        for bad in (None, "cut short", ["type", "object"], 5):
            errs = pa.check(allow, surface({"bank.toBank": "mutation"}, schema=bad))[0]
            self.assertTrue(any("no valid input schema" in x for x in errs), bad)

    def test_a_schema_that_says_nothing_is_kept_and_pointed_out(self):
        """The server answers {"$schema": ...} and no more for travel.startGlobalMove: a real answer, not a fault."""
        nothing = {"$schema": "https://json-schema.org/draft/2020-12/schema"}
        errs, notes = pa.check(with_entry("bank.toBank", entry()), surface({"bank.toBank": "mutation"}, schema=nothing))
        self.assertEqual(errs, [])
        self.assertTrue(any("publishes no input shape" in n for n in notes))
        reply = json.dumps({"endpointName": "bank.toBank", "inputSchema": nothing})
        m = self.build(reply)["_meta"]
        self.assertEqual((m["schemas_that_say_nothing"], m["answered_calls"]["getEndpointSchema"]), (["bank.toBank"], 1))

    def test_removing_every_schema_from_the_committed_capture_fails_every_entry(self):
        if not os.path.exists(pa.SURFACE):
            self.skipTest("no surface capture yet")
        s = pa._load(pa.SURFACE)
        for row in s["routers"].values():
            for e in (row["endpoints"] or {}).values():
                e["schema"] = None
        errs = [x for x in pa.check(ALLOW, s)[0] if "no valid input schema" in x]
        self.assertEqual(len(errs), len(ALLOW["endpoints"]))

    def test_a_failed_call_followed_by_a_reply_cut_short_stays_unanswered(self):
        m = self.build(None, self.CUT)["_meta"]
        self.assertEqual(m["failed_calls_never_answered"], ["getEndpointSchema bank.toBank"])
        self.assertEqual(m["replies_that_did_not_parse"], ["getEndpointSchema bank.toBank"])
        self.assertEqual(m["answered_calls"]["getEndpointSchema"], 0)
        self.assertEqual(m["counts"]["schemas"], 0)

    def test_only_a_reply_that_parsed_is_an_answer_whatever_the_order(self):
        for replies in ((None, self.GOOD), (self.CUT, self.GOOD), (self.GOOD, self.CUT), (self.GOOD, None)):
            s = self.build(*replies)
            m = s["_meta"]
            self.assertEqual((m["failed_calls_never_answered"], m["replies_that_did_not_parse"]), ([], []), replies)
            self.assertEqual(m["answered_calls"]["getEndpointSchema"], 1)
            self.assertEqual(s["routers"]["bank"]["endpoints"]["toBank"]["schema"], SCHEMA)   # the good one is kept
        wrong = json.dumps({"endpointName": "bank.toPocket", "inputSchema": SCHEMA})        # another endpoint's reply
        self.assertEqual(self.build(wrong)["_meta"]["replies_that_did_not_parse"], ["getEndpointSchema bank.toBank"])

    def test_a_capture_with_a_fault_fails_the_check(self):
        allow = with_entry("bank.toBank", entry())
        for key in ("routers_without_endpoint_list", "endpoint_count_mismatch", "replies_that_did_not_parse",
                    "failed_calls_never_answered", "schemas_for_endpoints_not_listed"):
            s = surface({"bank.toBank": "mutation"})
            s["_meta"][key] = ["x"]
            errs = pa.check(allow, s)[0]
            self.assertEqual(len([x for x in errs if x.startswith("capture: ")]), 1, key)
        m = self.build(None, self.CUT)
        self.assertGreaterEqual(len(pa.capture_errors(m)), 2)

    def test_a_router_list_that_did_not_parse_leaves_the_router_without_endpoints(self):
        calls = [("listGameRouters", {}, json.dumps([{"name": "bank", "endpointCount": 1}]), "t1"),
                 ("listRouterEndpoints", {"routerName": "bank"}, '[{"name": "bank.toBa', "t2")]
        m = pa.build_surface(calls)["_meta"]
        self.assertEqual(m["routers_without_endpoint_list"], ["bank"])
        self.assertEqual(m["replies_that_did_not_parse"], ["listRouterEndpoints bank"])
        with self.assertRaises(SystemExit):
            pa.build_surface([("listGameRouters", {}, '[{"name": "ba', "t1")])


class CodeScan(unittest.TestCase):
    def test_an_endpoint_the_code_sends_must_be_listed(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "tests"))
            for rel, text in (("a.py", 'call("bank.toBank", {})\ncall("bank.transfer", {})\n'
                                       'x = res.get("data.travelFinishAt")\n'),
                              (os.path.join("tests", "t.py"), 'call("stripe.createCheckout", {})\n'),
                              ("pilot_good.py", 'call("clan.leaveClan", {})\n')):
                with open(os.path.join(d, rel), "w") as f:
                    f.write(text)
            allow = with_entry("bank.toBank", entry())
            s = surface({"bank.toBank": "mutation", "bank.transfer": "mutation", "data.x": "query",
                         "stripe.createCheckout": "mutation", "clan.leaveClan": "mutation"})
            errs = pa.check(allow, s, [d])[0]
        self.assertEqual(len(errs), 1, errs)
        self.assertIn("bank.transfer: sent by the player code", errs[0])


class CommittedList(unittest.TestCase):
    def test_the_list_passes_its_own_gates(self):
        s = pa._load(pa.SURFACE) if os.path.exists(pa.SURFACE) else None
        errs, _ = pa.check(ALLOW, s, [d for d in pa.CODE_DIRS if os.path.isdir(d)])
        self.assertEqual(errs, [])

    def test_the_brief_never_list_is_all_there(self):
        ids = {r["id"] for r in ALLOW["never"]}
        self.assertLessEqual({"payments", "account_control", "moderation", "staff", "communication", "deletes"}, ids)
        self.assertLessEqual({"premium_currency", "leave_clan", "sell_rare_items", "marriage"},
                             {r["id"] for r in ALLOW["ask_first"]})
        self.assertLessEqual({"no_flee", "do_not_attack", "no_snipe", "spend_cap"}, set(ALLOW["call_gates"]))
        for r in ALLOW["never"] + ALLOW["ask_first"]:
            self.assertTrue(r.get("why") and r.get("source"), r["id"])

    def test_the_surface_in_the_repository_is_a_complete_live_capture(self):
        if not os.path.exists(pa.SURFACE):
            self.skipTest("no surface capture yet")
        s = pa._load(pa.SURFACE)
        self.assertTrue(s["_meta"]["live"])
        self.assertEqual(pa.capture_errors(s), [])
        for key, _ in pa.CAPTURE_FAULTS:
            self.assertEqual(s["_meta"][key], [], key)                     # the builder's own fault lists are there
        have = sum(1 for r in s["routers"].values() for e in r["endpoints"].values() if pa.valid_schema(e["schema"]))
        self.assertEqual(have, s["_meta"]["answered_calls"]["getEndpointSchema"])
        self.assertEqual(have, len(ALLOW["endpoints"]))

    def test_the_committed_review_is_a_fresh_render(self):
        if not os.path.exists(pa.SURFACE):
            self.skipTest("no surface capture yet")
        self.assertEqual(pa._read(pa.REVIEW), pa.render_report(ALLOW, pa._load(pa.SURFACE)))

    def test_check_command_exit_code(self):
        with tempfile.TemporaryDirectory() as d:
            bad = os.path.join(d, "bad.json")
            with open(bad, "w") as f:
                json.dump(with_entry("stripe.createCheckout", entry()), f)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = pa.main(["check", "--allowlist", bad, "--surface", os.path.join(d, "none.json"), "--code"])
            self.assertEqual(code, 1)
            self.assertIn("never-list check: FAILED", out.getvalue())


if __name__ == "__main__":
    unittest.main()
