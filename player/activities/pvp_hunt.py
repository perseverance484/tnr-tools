"""PvP hunting: scan, pick a fair target, attack; with nobody to fight, move on round the circuit (design 4.3).
Ported from the pilot's world() in hunt mode.

A valid target is awake, level 100 (or 85-99 with a public record the rater puts at 60% or more for me), not in
battle, not immune, not in my village, not on the do-not-attack list, not a player the game just refused me, and
not one who beat me in the last hours. The nearest one is attacked in one batch: walk to the tile, read his kit if
it is not saved, attack from stealth (director: "You have to have stealth up and drop it, then attack, in quick succession"; the
attack breaks stealth, and the explicit drop is added once its schema is read). The gates check the same list again when the call is sent.

No attack goes out short of full health, chakra or stamina (director: "Never send me into battle missing hp"):
with a target in sight and pools short, the hunt holds, scans and lets regeneration (or recovery's potion or
ramen, which come first by class) fill them.

Stealth is kept up while hunting: cast whenever it is off and off cooldown (director 2026-11-14: "recast whenever
off cooldown, check each sweep"). Its state is kept here from what the game answered: on for STEALTH_FOR after a
cast that took, off after an attack, a trip or a fight, with STEALTH_COOLDOWN before the next cast.
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
    ("lowlvl", lambda t, x: not gates.level_ok(t["level"], t["userId"], x["world"], x["rated"])),
    ("refused", lambda t, x: t["userId"] in x["skip"]),
    ("beat me", lambda t, x: x["lost_to"].get(t["userId"], 0) > x["now"]),
)


def pick_target(world, rows, me_pos, dna_path=None):
    """(the nearest valid target or None, {reason: how many were passed over})."""
    now, opp = world.now, world["opponents"]
    never, _ = gates.do_not_attack(dna_path, now)
    opp["skip"] = {u: t for u, t in opp["skip"].items() if t > now}
    ctx = {"now": now, "skip": opp["skip"], "lost_to": opp["lost_to"], "world": world, "rated": gates.rated(world),
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


def circuit_of(world):
    """The hunt's sectors: the director's, when he has named them in control.json, else the default. Never 210."""
    return [x for x in (world["control"].get("circuit") or C.CIRCUIT) if x not in C.NO_SECTORS] or \
        [x for x in C.CIRCUIT if x not in C.NO_SECTORS]


def stealth(world):
    """{on, until, ready_at}: what is known of my stealth."""
    return world["map"].setdefault("stealth", {"on": False, "until": 0, "ready_at": 0})


def stealth_off(world, why):
    """Stealth is broken (an attack, a fight, a trip): off, and ready again after the cooldown."""
    st = stealth(world)
    if st["on"] or why == "attack":
        st.update(on=False, until=0, ready_at=max(st.get("ready_at", 0), world.now + C.STEALTH_COOLDOWN))
    st["why_off"] = why


def stealth_up(world):
    st = stealth(world)
    if st["on"] and st["until"] <= world.now:
        st.update(on=False, why_off="expired")
    return st["on"]


@REGISTRY.activity
class PvpHunt(Activity):
    name = "pvp_hunt"
    priority = "goals"
    goal = "pvp"
    reads = ("travel.getSectorData", "combat.attackUser", "stealth.activateStealth", "travel.startGlobalMove")

    def available(self, world):
        return (world.status() == "AWAKE" and world["control"]["mode"] == "hunt"
                and not world["control"]["end_session"]           # an ending session picks no new fight
                and not world["inventory"].get("stale"))          # nor one before a loadout's items are read

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
            elif r.endpoint == "stealth.activateStealth":
                st, said = stealth(world), str(r.data.get("message") or "").lower()
                if r.data.get("success") or "already" in said:
                    st.update(on=True, until=world.now + C.STEALTH_FOR)
                else:                                             # on cooldown, or refused: try again later
                    st.update(on=False, ready_at=world.now + C.STEALTH_COOLDOWN)
                    world.event("finding", f"stealth: the game said no ({r.data.get('message')})"[:300],
                                about="stealth")
            elif r.endpoint == "travel.startGlobalMove" and r.data.get("success"):
                stealth_off(world, "trip")                        # hunt notes: stealth found off after travel
            if r.endpoint == "combat.attackUser":
                stealth_off(world, "attack")                      # an attack breaks it whether or not it lands
            if r.endpoint == "combat.attackUser" and not (r.data.get("success") or r.data.get("battleId")):
                # remember why an attack was refused so the same target is not tried again at once
                kind = refusal_kind(r.data.get("message"))
                world["opponents"]["skip"][r.input.get("userId", "?")] = world.now + C.SKIP_FOR[kind]
                own["refused"] = f"attack refused ({kind}): {r.data.get('message')}"

    def plan(self, world):
        """The hunt's plan. With more in the pocket than it may hold on the road it starts no trip (director
        2026-11-12, RUL-2026-11-12-153; review of 988c56cc, H3): it stays where it is, fights who is there,
        and scans, until the bank has had its turn."""
        p = self._hunt(world)
        if world.overfull() and any(s.get("call") == "travel.startGlobalMove" for s in p.steps):
            return self._scan(world, ", staying here: the pocket holds more than it may on the road")
        return p

    @staticmethod
    def _head(world):
        me = world.me
        return (f"AWAKE hunt {me.get('curHealth', 0):.0f}/{me.get('maxHealth', 0):.0f} HP @ {me.get('sector')} "
                f"{world.position()}")

    def _hunt(self, world):
        own, me = world.own(self.name), world.me
        sector, me_pos = me.get("sector"), world.position()
        circuit = circuit_of(world)
        head = self._head(world)
        scan = own.pop("scan", None)
        refused = own.pop("refused", None)
        here = scan is not None and scan["sector"] == sector
        if here:
            target, why = pick_target(world, scan["rows"], me_pos, self.gates.dna_path)
            world["map"]["last_scan"] = why
            if target:
                short = gates.full_for_a_fight(world)
                if short:
                    if world.pools()["cpsp"] < C.FULL_POOLS:
                        world.own("recovery")["ramen_due"] = True     # recovery's large ramen comes first
                    return self._scan(world, f", holding the attack on {target['username']}: {short}")
                return self._attack(target, sector, me_pos, head)
            if sector in circuit or sector == C.HOME_SECTOR:
                nxt = circuit[(circuit.index(sector) + 1) % len(circuit)] if sector in circuit else circuit[0]
                seen = ", ".join(f"{n} {k}" for k, n in sorted(why.items())) or "empty"
                return plan(K.go(nxt), "world", head + f": nobody to fight here ({seen})"
                            f"{'; ' + refused if refused else ''}, next sector {nxt}", tag="idle")
        if sector not in circuit:
            return plan(K.go(circuit[0]), "world", head + f": heading to the circuit ({circuit[0]})")
        return self._scan(world)

    def _scan(self, world, why=""):
        sector = world.me.get("sector")
        steps = [K.user(), K.sector(sector)]
        if not stealth_up(world) and world.now >= stealth(world).get("ready_at", 0):
            steps.append(K.stealth_on())                          # up in the same batch as the scan
            stealth(world)["ready_at"] = world.now + C.STEALTH_COOLDOWN   # not asked twice before it answers
        if world.now - world["map"].get("sensory_at", 0) > C.SENSORY_EVERY:
            world["map"]["sensory_at"] = world.now
            steps.insert(2, K.sensory(sector))
        return plan(steps, "world", self._head(world) + ": scanning" + why, hold=C.HUNT_WAIT, tag="idle")

    def _attack(self, t, sector, me_pos, head):
        there = (t["longitude"], t["latitude"])
        steps = [] if there == me_pos else [K.move(me_pos, there, sector)]
        if not self.combat.kit_known(t["userId"]):
            steps.append(K.kit(t["userId"]))                      # his kit before the attack, for his dossier
        # The director's sequence is stealth up, drop, attack. The attack itself breaks stealth (hunt 2026-11-14),
        # so the attack goes out stealthed. The explicit drop (the stealth router's deactivate call, straight before the
        # attack) waits until its input schema has been read live and it is on the allowlist: the capture has no
        # schema for it (tnr-autopilot DESIGN.md, build notes).
        steps += [K.attack(t, sector), K.user()]
        steps[-2]["meta"]["target"].update(level=t["level"], villageId=t["villageId"])
        return plan(steps, "world", head + f": attacking {t['username']} @ {there[0]},{there[1]}")
