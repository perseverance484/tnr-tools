import sys,re
p=sys.argv[1]; s=open(p).read()
old_start=s.index("export const applyActionCooldowns = (")
old_end=s.index("/**\n * Calculate how many action points the user has left")
new='''export const applyActionCooldowns = (
  battle: CompleteBattle,
  user: BattleUserState,
  action: CombatAction,
) => {
  // HARNESS PATCH (live lock): the live game reads a per-tag shared-cooldown table
  // (misc.getSharedCooldowns, captured 2026-11-18) and locks every OTHER action of the
  // actor that shares a tag with the cast action, whatever the cast action's cooldown.
  const config: Record<string, number> = {
    barrier: 3, cleanse: 3, cleanseprevent: 3, clear: 3, clearprevent: 3, consume: 3,
    increasepoolcost: 3, increasepotency: 3, moveprevent: 3, pierce: 3, poison: 3,
    seal: 3, siphon: 3, summon: 3, vamp: 3,
    buffprevent: 4, debuffprevent: 4, drain: 4, stun: 4,
  };
  const { round } = battle;
  const sharedTags = new Set<string>(action.effects.map((e) => e.type));
  const sharedRounds = (effects: { type: string }[]) =>
    effects.reduce(
      (longest, e) => (sharedTags.has(e.type) ? Math.max(longest, config[e.type] ?? 0) : longest),
      0,
    );
  const lockedFor = (lastUsedRound: number, cooldown: number) =>
    lastUsedRound ? lastUsedRound + cooldown - round : 0;
  user.jutsus.forEach((uj) => {
    const jutsu = getJutsu(battle, uj.jutsuId);
    if (!jutsu) return;
    if (uj.jutsuId === action.id && action.type === "jutsu") {
      uj.lastUsedRound = round;
      uj.originalCooldown = jutsu.cooldown;
    } else {
      const rounds = sharedRounds(jutsu.effects);
      if (rounds > 0 && lockedFor(uj.lastUsedRound, uj.originalCooldown) < rounds) {
        uj.lastUsedRound = round;
        uj.originalCooldown = rounds;
      }
    }
  });
  user.items.forEach((ui) => {
    const item = getItem(battle, ui.itemId);
    if (!item) return;
    if (ui.itemId === action.id && action.type === "item") {
      ui.lastUsedRound = round;
      ui.originalCooldown = item.cooldown;
    } else {
      const rounds = sharedRounds([...item.effects, ...(ui.imbuementEffects ?? [])]);
      if (rounds > 0 && lockedFor(ui.lastUsedRound, ui.originalCooldown) < rounds) {
        ui.lastUsedRound = round;
        ui.originalCooldown = rounds;
      }
    }
  });
  Object.values(getActiveBasicActions(battle, user)).forEach((ba) => {
    let tracking = user.basicActions.find((t) => t.id === ba.id);
    if (ba.id === action.id && action.type === "basic") {
      if (!tracking) return;
      tracking.lastUsedRound = round;
      delete tracking.cooldown;
    } else {
      const rounds = sharedRounds(ba.effects);
      const lastUsedRound = tracking?.lastUsedRound ?? ba.lastUsedRound ?? 0;
      if (rounds > 0 && lockedFor(lastUsedRound, ba.cooldown) < rounds) {
        if (!tracking) {
          tracking = { id: ba.id, lastUsedRound };
          user.basicActions.push(tracking);
        }
        tracking.lastUsedRound = round;
        tracking.cooldown = rounds;
      }
    }
  });
};

'''
s=s[:old_start]+new+s[old_end:]
open(p,'w').write(s)
print("patched")
