"""PvP hunting: scan, pick a fair target, attack; with nobody to fight, move on round the circuit (design 4.3).
Ported from the pilot's world() in hunt mode.

A valid target is awake, level 90 or more, not in battle, not immune, not in my village, not on the do-not-attack
list, not a player the game just refused me, and not one who beat me in the last hours. The nearest one is
attacked in one batch: walk to the tile, read his kit if it is not saved, attack. The gates check the same list
again when the call is sent.
"""
from .. import calls as K
from .. import config as C
from .. import gates
from ..registry import REGISTRY, Activity, plan
from ..world import parse_time


def refusal_kind(message):
    msg = (message or "").lower()
    return ("bracket" if "bracket" in msg else "village" if "village" in msg or "ally" in msg else
            "immune" if "immun" in msg else "move" if "move" in msg else "other")


def _immune(t, now):
    until = parse_time(t["immunityUntil"]) if t["immunityUntil"] else None
    return bool(until and until > now)


PASS_OVER = (       # why a player in the scan is not a target: the first row that holds names the reason
    ("me", lambda t, x: t["userId"] == C.ME),
    ("dna", lambda t, x: x["dna"] is None or t["userId"].lower() in x["dna"] or (t["username"] or "").lower() in x["dna"]),
    ("battle", lambda t, x: bool(t["battleId"]) or t["status"] == "BATTLE"),
    ("asleep or away", lambda t, x: t["status"] != "AWAKE"),
    ("immune", lambda t, x: _immune(t, x["now"])),
    ("ally", lambda t, x: t["villageId"] == C.HOME_VILLAGE),
    ("lowlvl", lambda t, x: (t["level"] or 0) < C.MIN_LEVEL),
    ("refused", lambda t, x: t["userId"] in x["skip"]),
    ("beat me", lambda t, x: x["lost_to"].get(t["userId"], 0) > x["now"]),
)


def pick_target(world, rows, me_pos, dna_path=None):
    """(the nearest valid target or None, {reason: how many were passed over})."""
    now, opp = world.now, world["opponents"]
    never, _ = gates.do_not_attack(dna_path, now)
    opp["skip"] = {u: t for u, t in opp["skip"].items() if t > now}
    ctx = {"now": now, "skip": opp["skip"], "lost_to": opp["lost_to"],
           "dna": None if never is None else never | {str(n).lower() for n in world["control"]["do_not_attack"]}}
    cands, why = [], {}
    for t in rows:
        reason = next((name for name, holds in PASS_OVER if holds(t, ctx)), None)
        if reason:
            why[reason] = why.get(reason, 0) + 1
        else:
            cands.append((max(abs(t["longitude"] - me_pos[0]), abs(t["latitude"] - me_pos[1])), t))
    why.pop("me", None)
    return (min(cands, key=lambda c: c[0])[1] if cands else None), why


@REGISTRY.activity
class PvpHunt(Activity):
    name = "pvp_hunt"
    priority = "goals"
    goal = "pvp"
    reads = ("travel.getSectorData", "combat.attackUser")

    def available(self, world):
        return (world.status() == "AWAKE" and world["control"]["mode"] == "hunt"
                and not world["control"]["end_session"])          # an ending session picks no new fight

    def value(self, world):
        return 10.0

    def on_result(self, world, results):
        own = world.own(self.name)
        for r in results:
            if r.error or not isinstance(r.data, dict):
                continue
            if r.endpoint == "travel.getSectorData":
                rows = K.columns(r.data, "users.*.", K.SECTOR_COLS)
                if rows is None:
                    world.event("finding", "the sector scan's columns do not line up; no target taken from it",
                                about="selects")
                own["scan"] = {"sector": r.input.get("sector"), "rows": rows or []}
            elif r.endpoint == "combat.attackUser" and not (r.data.get("success") or r.data.get("battleId")):
                # remember why an attack was refused so the same target is not tried again at once
                kind = refusal_kind(r.data.get("message"))
                world["opponents"]["skip"][r.input.get("userId", "?")] = world.now + C.SKIP_FOR[kind]
                own["refused"] = f"attack refused ({kind}): {r.data.get('message')}"

    def plan(self, world):
        own, me = world.own(self.name), world.me
        sector, me_pos = me.get("sector"), world.position()
        head = f"AWAKE hunt {me.get('curHealth', 0):.0f}/{me.get('maxHealth', 0):.0f} HP @ {sector} {me_pos}"
        scan = own.pop("scan", None)
        refused = own.pop("refused", None)
        here = scan is not None and scan["sector"] == sector
        if here:
            target, why = pick_target(world, scan["rows"], me_pos, self.gates.dna_path)
            world["map"]["last_scan"] = why
            if target:
                return self._attack(target, sector, me_pos, head)
            if sector in C.CIRCUIT or sector == C.HOME_SECTOR:
                nxt = C.CIRCUIT[(C.CIRCUIT.index(sector) + 1) % len(C.CIRCUIT)] if sector in C.CIRCUIT else C.CIRCUIT[0]
                seen = ", ".join(f"{n} {k}" for k, n in sorted(why.items())) or "empty"
                return plan(K.go(nxt), "world", head + f": nobody to fight here ({seen})"
                            f"{'; ' + refused if refused else ''}, next sector {nxt}", tag="idle")
        if sector not in C.CIRCUIT:
            return plan(K.go(C.CIRCUIT[0]), "world", head + f": heading to the circuit ({C.CIRCUIT[0]})")
        steps = [K.user(), K.sector(sector)]
        if world.now - world["map"].get("sensory_at", 0) > C.SENSORY_EVERY:
            world["map"]["sensory_at"] = world.now
            steps.append(K.sensory(sector))
        return plan(steps, "world", head + ": scanning", hold=C.HUNT_WAIT, tag="idle")

    def _attack(self, t, sector, me_pos, head):
        there = (t["longitude"], t["latitude"])
        steps = [] if there == me_pos else [K.move(me_pos, there, sector)]
        if not self.combat.kit_known(t["userId"]):
            steps.append(K.kit(t["userId"]))                      # his kit before the attack, for his dossier
        steps += [K.attack(t, sector), K.user()]
        steps[-2]["meta"]["target"].update(level=t["level"], villageId=t["villageId"])
        return plan(steps, "world", head + f": attacking {t['username']} @ {there[0]},{there[1]}")
