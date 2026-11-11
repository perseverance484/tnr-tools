"""The gates: one test per rule of state/prompt_ai_player_overhaul.md section 2, on the approved allowlist."""
import copy
import importlib.util
import json
import os
import unittest

from player import calls as K
from player import config as C
from player import gates as G
from player.tests.support import Rig, user


def step(endpoint, **inp):
    return {"call": endpoint, "input": inp, "select": []}


class Never(unittest.TestCase):
    def setUp(self):
        self.rig = Rig()
        self.rig.tick(user())
        self.g, self.w = self.rig.brain.gates, self.rig.world

    def refused(self, s, activity=None):
        v = self.g.check(s, self.w, activity)
        self.assertEqual(v.kind, "refuse", (s["call"], v))
        return v

    def test_only_listed_endpoints_are_sent(self):
        self.assertEqual(self.refused(step("clan.createClan")).rule, "allowlist")
        self.assertTrue(self.g.check(K.user(), self.w, "pvp_hunt").ok)

    def test_payments_and_purchases(self):
        for ep in ("paypal.createStoreOrder", "stripe.createCheckout", "purchases.catalogue", "merch.checkout"):
            self.refused(step(ep))

    def test_account_deletion(self):
        for ep in ("accountDeletion.request", "profile.confirmDeletion", "profile.toggleDeletionTimer"):
            self.refused(step(ep))

    def test_other_players_accounts_and_data(self):
        self.refused(step("bank.transfer", userId="user_other", amount=5))
        self.refused(step("quests.getUserQuests", userId="user_other"), "missions")
        self.assertTrue(self.g.check(step("quests.getUserQuests", userId=C.ME), self.w, "missions").ok)
        self.refused(step("profile.getPublicUsers", limit=5, isAi=False, orderBy="Online", ip="1.2.3.4"), "pvp_hunt")

    def test_moderation_and_reports(self):
        for ep in ("reports.create", "reports.ban", "forum.moderatePost"):
            self.refused(step(ep))

    def test_deletes(self):
        for ep in ("jutsu.forget", "pets.releasePet", "quests.deleteUserQuest", "item.sellUserItem"):
            self.assertFalse(self.g.check(step(ep), self.w).ok, ep)

    def test_chat_messages_and_posts(self):
        for ep in ("comments.createConversation", "comments.createConversationComment", "forum.createThread",
                   "auction.createAuctionOffer", "clan.upsertNotice"):
            self.refused(step(ep))

    def test_staff_powers_and_hidden_records(self):
        for ep in ("staff.forceAwake", "jutsu.adjustUserJutsu", "jutsu.update", "misc.awardReputation"):
            self.refused(step(ep))
        self.assertEqual(self.refused(step("jutsu.get", id="x", hidden=True), "battle").rule, "player_visible_only")

    def test_flee(self):
        v = self.refused(K.act("B", "flee", 1, 1, 3), "battle")
        self.assertEqual(v.rule, "no_flee")
        self.assertTrue(self.g.check(K.act("B", "defensiveStance", 1, 1, 3), self.w, "battle").ok)

    def test_do_not_attack(self):
        ok = {"userId": "user_prey", "username": "Prey", "longitude": 1, "latitude": 1}
        self.assertTrue(self.g.check(K.attack(ok, 1538), self.w, "pvp_hunt").ok)
        for who in ({"userId": "user_f", "username": "Friend"}, {"userId": "user_shisui", "username": "renamed"},
                    {"userId": "user_f", "username": "FRIEND"}):
            v = self.refused(K.attack(dict(who, longitude=1, latitude=1), 1538), "pvp_hunt")
            self.assertEqual(v.rule, "do_not_attack")

    def test_do_not_attack_holds_and_the_directors_additions(self):
        luka = K.attack({"userId": "user_l", "username": "Luka", "longitude": 1, "latitude": 1}, 1538)
        self.assertTrue(self.g.check(luka, self.w, "pvp_hunt").ok)             # the hold's window closed in 2026
        never, _ = G.do_not_attack(self.rig.dna, now=1_794_327_800)            # 2026-11-10 16:30 UTC: inside it
        self.assertIn("luka", never)
        self.assertIn("4qua", never)
        self.w["control"]["do_not_attack"] = ["Luka"]
        self.assertEqual(self.refused(luka, "pvp_hunt").rule, "do_not_attack")

    def test_no_list_means_no_attack(self):
        os.unlink(self.rig.dna)
        prey = K.attack({"userId": "user_prey", "username": "Prey", "longitude": 1, "latitude": 1}, 1538)
        self.assertEqual(self.refused(prey, "pvp_hunt").rule, "do_not_attack")

    def test_sniping_angelsaber(self):
        snipe = K.attack({"userId": "user_a", "username": "AngelSaber", "longitude": 1, "latitude": 1,
                          "third_party": True}, 1538)
        self.refused(snipe, "pvp_hunt")
        v = G.g_no_snipe(snipe, self.w, self.g)
        self.assertEqual((v.kind, v.rule), ("refuse", "no_snipe"))

    def test_no_credentials(self):
        v = self.refused(dict(K.user(), input={"token": "abc"}), "pvp_hunt")
        self.assertEqual(v.rule, "credentials")
        self.refused(dict(K.user(), input={"opts": {"Authorization": "Bearer x"}}), "pvp_hunt")

    def test_an_activity_sends_only_its_own_calls(self):
        self.assertEqual(self.refused(K.ramen(), "pvp_hunt").rule, "allowlist")
        self.assertTrue(self.g.check(K.ramen(), self.w, "recovery").ok)
        self.assertTrue(self.g.check(K.finish_trip(), self.w, "pvp_hunt").ok)   # world reads and trips are shared

    def test_other_players_fights_are_not_read_in_a_fight(self):
        s = step("combat.getBattleHistory", userId="user_other", limit=30)
        self.assertTrue(self.g.check(s, self.w, "harvest").ok)
        self.w["battle"] = {"bid": "B1", "entries": []}
        self.assertEqual(self.refused(s, "harvest").rule, "study_only")
        self.assertTrue(self.g.check(K.entries("B1", 8), self.w, "battle").ok)


class AskFirst(unittest.TestCase):
    def setUp(self):
        self.rig = Rig()
        self.rig.tick(user())
        self.g, self.w = self.rig.brain.gates, self.rig.world

    def asks(self, s, activity, rule):
        v = self.g.check(s, self.w, activity)
        self.assertEqual((v.kind, v.rule), ("ask", rule), s["call"])
        return v

    def test_premium_currency(self):
        s = step("skillTree.purchaseSkill", skillId="s1")
        self.asks(s, "training", "premium_currency")
        self.assertTrue(self.w.decide(self.g.key(s, "premium_currency"), "buy the skill?", s))
        self.w["decisions"][-1]["answer"] = "no"
        self.asks(s, "training", "premium_currency")
        self.w["decisions"][-1]["answer"] = "yes"
        self.assertTrue(self.g.check(s, self.w, "training").ok)
        self.asks(step("skillTree.purchaseSkill", skillId="s2"), "training", "premium_currency")   # a yes is per call

    def test_leaving_the_clan_and_marriage_are_never_sent_unasked(self):
        for ep in ("clan.leaveClan", "village.leaveVillage", "marriage.createRequest"):
            self.assertFalse(self.g.check(step(ep), self.w).ok, ep)
        allow = copy.deepcopy(self.g.allowlist)
        for ep in ("clan.leaveClan", "marriage.createRequest"):
            allow["endpoints"][ep] = {"kind": "action", "activity": ["world"]}
        g = G.Gates(allow, self.rig.dna)
        self.assertEqual(g.check(step("clan.leaveClan"), self.w).rule, "leave_clan")
        self.assertEqual(g.check(step("marriage.createRequest"), self.w).rule, "marriage")

    def test_selling_items(self):
        listing = step("auction.createAuctionListing", userItemId="u1", listingType="AUCTION", startingPrice=9,
                       buyoutPrice=10, durationHours=72, currencyType="MONEY", bidderMinLevel=1, bidderMaxLevel=110)
        self.asks(listing, "hunting", "sell_rare_items")
        direct = dict(listing, input=dict(listing["input"], listingType="DIRECT", targetUserId="user_x"))
        self.assertEqual(self.g.check(direct, self.w, "hunting").rule, "auction_only")
        reps = dict(listing, input=dict(listing["input"], currencyType="REPUTATION"))
        self.assertFalse(self.g.check(reps, self.w, "hunting").ok)

    def test_a_ryo_spend_above_the_caps(self):
        self.assertTrue(self.g.check(K.ramen(), self.w, "recovery").ok)
        self.w["records"]["spend"] = {"day": __import__("player.world").world.utc_day(self.rig.t), "ryo": C.DAILY_CAP + 1}
        self.asks(K.ramen(), "recovery", "spend_cap")
        self.w["control"]["spend_caps"] = {"daily": C.DAILY_CAP * 10}
        self.assertTrue(self.g.check(K.ramen(), self.w, "recovery").ok)
        self.w.me.update(money=100_000, bank=100_000)                 # under the reserve
        self.asks(K.ramen(), "recovery", "spend_cap")

    def test_one_level_transfer_a_day(self):
        s = step("jutsu.transferLevel", fromJutsuId="a", toJutsuId="b", transferLevels=24)
        self.assertTrue(self.g.check(s, self.w, "training").ok)
        self.g.sent(s, self.w)
        self.assertEqual(self.g.check(s, self.w, "training").rule, "one_transfer_a_day")
        self.rig.t += 86_400
        self.assertTrue(self.g.check(s, self.w, "training").ok)

    def test_captchas_are_answered(self):
        self.assertTrue(self.g.check(step("misc.verifyCaptcha", guess="abc"), self.w, "training").ok)
        self.assertTrue(self.g.check(step("train.startTraining", stat="intelligence", energy=100, guess="abc"),
                                     self.w, "training").ok)


class Screening(unittest.TestCase):
    def test_a_refused_call_is_a_finding_and_the_brain_does_something_else(self):
        rig = Rig()
        rig.tick(user())
        ok, v, s = rig.brain.gates.screen([K.user(), step("stripe.createCheckout")], rig.world, "pvp_hunt")
        self.assertFalse(ok)
        self.assertEqual(s["call"], "stripe.createCheckout")
        self.assertEqual([e["about"] for e in rig.events("finding")], ["gate"])

    def test_an_ask_first_call_becomes_a_pending_decision(self):
        rig = Rig()
        rig.tick(user())
        s = step("skillTree.purchaseSkill", skillId="s1")
        self.assertFalse(rig.brain.gates.screen([s], rig.world, "training")[0])
        self.assertFalse(rig.brain.gates.screen([s], rig.world, "training")[0])
        self.assertEqual(len(rig.events("decision_raised")), 1)
        self.assertEqual(len([d for d in rig.world["decisions"] if not d["answer"]]), 1)

    def test_every_gate_on_the_list_has_code_behind_it(self):
        with open(C.ALLOWLIST) as f:
            allow = json.load(f)
        self.assertLessEqual(set(allow["call_gates"]), set(G.CALL_GATES))
        allow["endpoints"]["profile.getUser"]["gates"] = ["made_up"]
        with self.assertRaises(ValueError):
            G.Gates(allow)

    def test_the_rule_test_is_the_checker_s(self):
        """player.gates.rule_hits and scripts/player_allowlist.py rule_hits agree on every captured endpoint."""
        spec = importlib.util.spec_from_file_location("pa", os.path.join(C.ROOT, "scripts", "player_allowlist.py"))
        pa = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pa)
        allow, surface = pa._load(pa.ALLOWLIST), pa._load(pa.SURFACE)
        n = 0
        for router, row in surface["routers"].items():
            for ep, e in row["endpoints"].items():
                kind = {"query": "read", "mutation": "action"}.get(e["type"])
                for r in allow["never"] + allow["ask_first"]:
                    self.assertEqual(G.rule_hits(r, f"{router}.{ep}", kind), pa.rule_hits(r, f"{router}.{ep}", kind))
                    n += 1
        self.assertGreater(n, 9000)


if __name__ == "__main__":
    unittest.main()
