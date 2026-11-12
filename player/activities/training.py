"""Training: a jutsu training queue that is never idle, and energy spent on a stat in the village (design 4.3).
Ported from the pilot's restock.py `training_plan` and from its world() (the trip to the village); the standing
orders are state/player/dauntless/jutsu_training.md (director 2026-11-09: "Maintain an active jutsu training
queue"; 2026-11-11: "keep training stats with energy and jutsu with ryo").

Every LOOK seconds the queue and my jutsu are read. Each free place in the queue goes to the target whose next
level is lowest: low levels take minutes and cost little, so that is the quickest and the cheapest. A target at
the training cap is done. One the game refuses is left alone: for a day, or for ten minutes when the refusal is
about where I am (travelling, in hospital, in a fight) or a full queue.

Energy trains a stat only in the village sector: there, ENERGY_MIN or more goes to intelligence while it trails
willpower, else to willpower. With TRIP or more saved up elsewhere, the character goes to the village for it.
A refusal stops energy training for an hour, and a trip that did not lead to training is not made again for
half an hour.

Not built here (the allowlist has them as proposed, or they need a decision): the training captcha, the skill
tree, a sensei, spending unused experience, and level transfers.
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
PASSING = ("travel", "hospital", "battle", "full", "asleep")


@REGISTRY.activity
class Training(Activity):
    name = "training"
    priority = "upkeep"
    reads = ("jutsu.getTrainingQueue", "jutsu.getUserJutsus", "jutsu.startTraining", "train.startTraining")

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
        if energy >= TRIP and world.now >= own.get("no_trip", 0):
            return "trip", None
        return None

    def available(self, world):
        own = world.own(self.name)
        return (world.status() == "AWAKE" and not world.in_battle()
                and bool(own.get("fresh") or world.now >= own.get("next", 0) or self._energy(world)))

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
        if len(seen) == 2:
            self._read(world, own, seen["jutsu.getTrainingQueue"], seen["jutsu.getUserJutsus"])

    @staticmethod
    def _read(world, own, queue, mine):
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

    # ------------------------------------------------------------ the plan
    def plan(self, world):
        own = world.own(self.name)
        if own.pop("fresh", False):
            steps, notes = self._fill(world)
            if steps:
                return plan(steps + [K.user()], "world", "training: " + ", ".join(notes))
        if world.now >= own.get("next", 0):
            own["next"] = world.now + SOON                         # an answer sets the real time of the next look
            return plan([K.training_queue(), K.my_jutsu(), K.user()], "world", "training: reading the queue")
        energy = self._energy(world)
        if energy and energy[0] == "train":
            n = int(world.me["curEnergy"])
            return plan([K.train_stat(energy[1], n), K.user()], "world", f"training: {n} energy to {energy[1]}")
        if energy:
            own["no_trip"] = world.now + TRIP_AGAIN                # (a trip that ends in training is not the last)
            return plan(K.trip(C.HOME_SECTOR), "world",
                        f"training: {world.me['curEnergy']:.0f} energy, going to the village ({C.HOME_SECTOR})")
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
