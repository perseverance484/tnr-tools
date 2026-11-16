"""Training: a jutsu training queue that is never idle, and energy spent on a stat in the village (design 4.3).
Ported from the pilot's restock.py `training_plan` and from its world() (the trip to the village); the standing
orders are state/player/dauntless/jutsu_training.md (director 2026-11-09: "Maintain an active jutsu training
queue"; 2026-11-11: "keep training stats with energy and jutsu with ryo").

Every LOOK seconds the queue and my jutsu are read. Each free place in the queue goes to the target whose next
level is lowest: low levels take minutes and cost little, so that is the quickest and the cheapest. A target at
the training cap is done. One the game refuses is left alone: for a day, or for ten minutes when the refusal is
about where I am (travelling, in hospital, in a fight) or a full queue.

Training is paid from the pocket, and the pocket holds little on the road (activities/bank.py). So when places
are to be filled, the bank is asked first to fill the pocket to what may be drawn for training
(world["training"]["draw_until"]), and the fill waits for that: until the pocket has it, or the bank has no more
to give, or DRAW_FOR seconds have gone. A refusal for want of money is about the moment.

Energy trains a stat only in the village sector: there, ENERGY_MIN or more goes to intelligence while it trails
willpower, else to willpower. With TRIP or more saved up elsewhere, the character goes to the village for it.
A refusal stops energy training for an hour, and a trip that did not lead to training is not made again for
half an hour.

Unspent experience goes to intelligence and willpower (state/player/dauntless/ryo_plan.md; director
2026-11-09: "can spend all our exp on willpower/intelligence"; "Put it into intelligence until it matches
willpower, then split"): the one that trails is brought level first, the rest is split between the two. EXP_MIN
or more is worth the call. A refusal stops it for an hour, and it is not tried twice in ten minutes.

Not built here (the allowlist has them as proposed, or they need a decision): the training captcha, the skill
tree, a sensei, and level transfers.
"""
from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan

# the director's targets, in his order (jutsu_training.md): the 40-AP potency and stance buffs, then the scaling
# damage and set-up jutsu near the cap
TARGETS = ("P7dDcC102RhwBTTgA4HU_", "UiBR2V2AKkmh64JiYlL3w", "7rYARNUr1kXiJb3VLXqUb", "GsDJufr8bn-55VSGPe0hA",
           "CWdsrv5uM2R3hEyG6fvaX", "rCmgi5gtJb-wnPfuwruI2", "sEDO_J07YRbTqHnxuPUA5", "GlgS3FVoQ6F8k3RAo_Uht",
           "INuy-ITnPsH22eUoGQgwW", "kbrQuf3nYNHoKEvusATTO", "pqCqPemRNk3ht-SFrjq5G", "iktsCP-RjIhlYlsTg-JTN")
CAP = 20                   # the training cap for a Jonin; 21 to 25 come from use or a transfer
SLOTS = 4                  # places in the queue behind the level in training, when the game does not say
LOOK = 900.0               # s between looks at the queue
ENERGY_MIN = 200           # energy worth a training call in the village
TRIP = 2500                # energy worth the trip to the village
REFUSED_FOR = 86_400.0     # s a refused target is left alone
SOON = 600.0               # s, when the refusal is about the moment and not the jutsu
ENERGY_BLOCK = 3600.0      # s after a refused stat training
TRIP_AGAIN = 1800.0        # s before another trip when one did not lead to training
DRAW_FOR = 120.0           # s a queue fill waits for the bank to fill the pocket
EXP_MIN = 1_000            # unspent experience worth a call
PASSING = ("travel", "hospital", "battle", "full", "asleep", "money", "afford", "funds")


@REGISTRY.activity
class Training(Activity):
    name = "training"
    priority = "upkeep"
    reads = ("jutsu.getTrainingQueue", "jutsu.getUserJutsus", "jutsu.startTraining", "train.startTraining",
             "profile.useUnusedExperiencePoints")

    # ------------------------------------------------------------ what there is to do
    def _energy(self, world):
        """("train", stat) in the village with enough energy; ("trip", None) with a lot of it elsewhere; None."""
        own, me = world.own(self.name), world.me
        energy = me.get("curEnergy") or 0
        if energy < ENERGY_MIN or world.now < own.get("energy_blocked", 0):
            return None
        if me.get("sector") == C.HOME_SECTOR:
            behind = (me.get("intelligence") or 0) < (me.get("willpower") or 0)
            return "train", "intelligence" if behind else "willpower"
        if energy >= TRIP and world.now >= own.get("no_trip", 0) and not world.overfull():
            return "trip", None                # (never with more in the pocket than it may hold on the road)
        return None

    def _experience(self, world):
        """{stat: points} for the unspent experience, or None: the one of intelligence and willpower that trails
        is brought level with the other, and what is left is split between the two."""
        me, exp = world.me, world.me.get("earnedExperience")
        if not isinstance(exp, (int, float)) or isinstance(exp, bool) or exp < EXP_MIN \
                or world.now < world.own(self.name).get("exp_blocked", 0):
            return None
        exp, gap = int(exp), int((me.get("willpower") or 0) - (me.get("intelligence") or 0))
        low, high = ("intelligence", "willpower") if gap >= 0 else ("willpower", "intelligence")
        level = min(exp, abs(gap))
        return {low: level + (exp - level + 1) // 2, high: (exp - level) // 2}

    @staticmethod
    def _funded(world):
        """Whether a queue fill may go ahead: the pocket holds what may be drawn for training, or the bank has
        nothing to add to it, or the wait for the bank is over."""
        pocket, bank = float(world.me.get("money") or 0), float(world.me.get("bank") or 0)
        return (world["training"].get("draw_until", 0) <= world.now or pocket >= C.TRAINING_DRAW
                or bank - world.caps()["reserve"] < 1)

    def available(self, world):
        own = world.own(self.name)
        return (world.status() == "AWAKE" and not world.in_battle()
                and bool((own.get("fresh") and self._funded(world)) or world.now >= own.get("next", 0)
                         or self._energy(world) or self._experience(world)))

    def value(self, world):
        return 4.0

    # ------------------------------------------------------------ what the game said
    def on_result(self, world, results):
        own, seen = world.own(self.name), {}
        for r in results:
            if r.endpoint in ("jutsu.getTrainingQueue", "jutsu.getUserJutsus"):
                seen[r.endpoint] = r.data if not r.error and isinstance(r.data, dict) else None
            elif r.endpoint == "jutsu.startTraining":
                self._queued(world, own, r)
            elif r.endpoint == "train.startTraining":
                self._trained(world, own, r)
            elif r.endpoint == "profile.useUnusedExperiencePoints":
                self._assigned(world, own, r)
        if len(seen) == 2:
            self._read(world, own, seen["jutsu.getTrainingQueue"], seen["jutsu.getUserJutsus"])

    def _read(self, world, own, queue, mine):
        """The queue and my jutsu, read together. A read that cannot be used leaves the last one standing."""
        waiting = None if queue is None else K.rows(queue, "waiting.*.", ("jutsuId", "level"))
        owned = None if mine is None else K.rows(mine, "*.", K.OWNED_COLS)
        if waiting is None or owned is None:
            world.event("finding", "a read of the training queue cannot be used", about="selects")
            own["next"] = world.now + SOON
            return
        capacity = queue.get("capacity")
        world["training"].update(
            capacity=capacity if type(capacity) is int else SLOTS,
            waiting=[[x["jutsuId"], x["level"]] for x in waiting],
            levels={x["jutsuId"]: x["level"] or 0 for x in owned},
            active=[x["jutsuId"] for x in owned if x["finishTraining"]], read_at=world.now)
        own.update(fresh=True, next=world.now + LOOK)
        if self._fill(world)[0]:                                   # places to fill: the bank is asked to pay
            world["training"]["draw_until"] = world.now + DRAW_FOR

    @staticmethod
    def _said(r):
        ok = not r.error and isinstance(r.data, dict) and bool(r.data.get("success"))
        return ok, str(r.error or (r.data.get("message") if isinstance(r.data, dict) else r.data))

    def _queued(self, world, own, r):
        ok, said = self._said(r)
        jutsu = (r.input or {}).get("jutsuId")
        if ok:
            world.event("activity_done", f"training: {jutsu} queued for its next level", activity=self.name)
            return
        wait = SOON if any(w in said.lower() for w in PASSING) else REFUSED_FOR
        own.setdefault("refused", {})[jutsu] = world.now + wait
        world.event("finding", f"training: {jutsu} was refused ({said}); left alone for {wait / 3600:.1f} h"[:300],
                    about="training")

    def _trained(self, world, own, r):
        ok, said = self._said(r)
        if ok:
            world.event("activity_done", f"training: {(r.input or {}).get('energy')} energy spent on "
                                         f"{(r.input or {}).get('stat')}", activity=self.name)
        else:
            own.update(energy_blocked=world.now + ENERGY_BLOCK, no_trip=world.now + TRIP_AGAIN)
            world.event("finding", f"training: the energy was refused ({said})"[:300], about="training")

    def _assigned(self, world, own, r):
        ok, said = self._said(r)
        given = ", ".join(f"{n:,} to {s}" for s, n in (r.input or {}).items() if n)
        if ok:
            world.event("activity_done", f"training: experience assigned ({given})", activity=self.name)
        else:
            own["exp_blocked"] = world.now + ENERGY_BLOCK
            world.event("finding", f"training: the experience was refused ({said}); {given}"[:300], about="training")

    # ------------------------------------------------------------ the plan
    def plan(self, world):
        own = world.own(self.name)
        if own.get("fresh") and self._funded(world):
            own["fresh"] = False
            world["training"].pop("draw_until", None)              # what the fill leaves may go back to the bank
            steps, notes = self._fill(world)
            if steps:
                return plan(steps + [K.user()], "world", "queued: " + ", ".join(notes))
        if world.now >= own.get("next", 0):
            own["next"] = world.now + SOON                         # an answer sets the real time of the next look
            return plan([K.training_queue(), K.my_jutsu(), K.user()], "world", "reading the queue")
        energy = self._energy(world)
        if energy and energy[0] == "train":
            n = int(world.me["curEnergy"])
            return plan([K.train_stat(energy[1], n), K.user()], "world", f"{n} energy to {energy[1]}")
        if energy:
            own["no_trip"] = world.now + TRIP_AGAIN                # (a trip that ends in training is not the last)
            return plan(K.trip(C.HOME_SECTOR), "world",
                        f"{world.me['curEnergy']:.0f} energy, going to the village ({C.HOME_SECTOR})")
        points = self._experience(world)
        if points:
            own["exp_blocked"] = world.now + SOON                  # the profile read behind it shows what is left
            return plan([K.spend_experience(points), K.user()], "world",
                        ", ".join(f"{n:,} experience to {s}" for s, n in points.items() if n))
        return None

    @staticmethod
    def _reached(t):
        """{jutsu: the level it will have once everything in training and waiting is done}."""
        nxt = dict(t.get("levels") or {})
        for j in t.get("active") or []:
            nxt[j] = nxt.get(j, 0) + 1
        for j, level in t.get("waiting") or []:
            nxt[j] = max(nxt.get(j, 0), level or 0)
        return nxt

    def _fill(self, world):
        """(the calls that fill the queue's free places, a note for each): each place goes to the target whose
        next level is lowest."""
        t, own = world["training"], world.own(self.name)
        nxt = self._reached(t)
        free = t.get("capacity", SLOTS) - len(t.get("waiting") or []) + (0 if t.get("active") else 1)
        refused, steps, notes = own.get("refused") or {}, [], []
        for _ in range(max(0, free)):
            open_ = [(nxt.get(j, 0), k, j) for k, j in enumerate(TARGETS)
                     if nxt.get(j, 0) < CAP and world.now >= refused.get(j, 0)]
            if not open_:
                break
            level, _, jutsu = min(open_)
            steps.append(K.train_jutsu(jutsu))
            nxt[jutsu] = level + 1
            notes.append(f"{jutsu[:6]} to {level + 1}")
        return steps, notes
