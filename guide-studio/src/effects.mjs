// Display semantics are independent of the engine's offence/defence stat axis.
// Source: TheNinjaRPG 36c5873b, combat/tags.ts and validators/combat.ts.
const semantics = {
  damage: ["POWER", "deal"],
  increasedamagegiven: ["DAMAGE GIVEN", "increase"],
  decreasedamagegiven: ["DAMAGE GIVEN", "reduction"],
  increasedamagetaken: ["DAMAGE TAKEN", "increase"],
  decreasedamagetaken: ["DAMAGE TAKEN", "reduction"],
  decreaseheal: ["HEALING REDUCTION", "reduction"],
  increaseheal: ["HEALING GIVEN", "increase"],
  recoil: ["RECOIL", "apply"],
  afterburn: ["AFTERBURN", "apply"],
  wound: ["WOUND", "apply"],
  drain: ["POOL DRAIN", "drain"],
  heal: ["HEAL", "restore"],
  shield: ["SHIELD", "protect"],
  lifesteal: ["LIFESTEAL", "restore"],
  buffprevent: ["BUFF PREVENTION", "prevent"],
  debuffprevent: ["DEBUFF PREVENTION", "prevent"],
  stun: ["AP STUN", "reduce"],
  seal: ["SEAL", "prevent"],
  absorb: ["ABSORB", "protect"],
  reflect: ["REFLECT", "return"],
  increasepoolcost: ["STAMINA & CHAKRA COST", "increase"],
  decreasepoolcost: ["STAMINA & CHAKRA COST", "reduction"],
  summon: ["SUMMON", "summon"],
  onehitkill: ["INSTANT DEFEAT", "apply"],
  redirection: ["MOVEMENT", "move"],
  clear: ["CLEAR", "remove"],
  cleanse: ["CLEANSE", "remove"],
};
const targetNames = {
  SELF: "self",
  ALLY: "allies",
  OPPONENT: "enemy",
  OTHER_USER: "target",
  GROUND: "area",
  EMPTY_GROUND: "empty ground",
};
export function normalizeEffect(effect, owner, level = 25) {
  if (effect.type === "visual") return null;
  const semantic = semantics[effect.type];
  if (!semantic)
    throw new Error(`Unmapped effect ${effect.type} on ${owner.id}`);
  const rawTarget = effect.target ?? "INHERIT";
  const inherited = rawTarget === "INHERIT" ? owner.target : rawTarget;
  let target = targetNames[inherited] ?? inherited?.toLowerCase();
  if (rawTarget === "INHERIT" && inherited !== "SELF") {
    if (effect.friendlyFire === "ENEMIES") target = "enemy";
    else if (effect.friendlyFire === "FRIENDLY") target = "allies";
  }
  if (!target) throw new Error(`Unresolved target on ${owner.id}`);
  let [label, direction] = semantic;
  if (
    effect.type === "onehitkill" &&
    target === "self" &&
    owner.jutsuType === "AI"
  )
    label = "SUMMON DEPARTURE";
  if (
    effect.type.endsWith("poolcost") &&
    effect.poolsAffected?.includes("Health")
  )
    label = "POOL COST";
  if (
    effect.type === "heal" &&
    effect.poolsAffected?.some((p) => p !== "Health")
  )
    label = "POOL HEAL";
  if (effect.type === "damage" && effect.calculation !== "formula")
    label = "DAMAGE";
  const power = effect.power + level * (effect.powerPerLevel ?? 0);
  if (!Number.isFinite(power))
    throw new Error(`Invalid effect power on ${owner.id}`);
  const value =
    Math.round(
      (effect.calculation === "percentage" ? Math.min(100, power) : power) *
        100,
    ) / 100;
  return {
    type: effect.type,
    label,
    direction,
    target,
    rawTarget,
    inheritedTarget: inherited,
    statDirection: effect.direction ?? null,
    calculation: effect.calculation,
    value,
    basePower: effect.power,
    powerPerLevel: effect.powerPerLevel ?? 0,
    level,
    rounds: effect.rounds ?? 0,
    chance: [
      "onehitkill",
      "stun",
      "seal",
      "buffprevent",
      "debuffprevent",
    ].includes(effect.type)
      ? value
      : null,
    apReduction: effect.apReduction ?? null,
    shieldHealth: effect.health ?? null,
    pools: effect.poolsAffected ?? [],
    elements: effect.elements ?? [],
    statTypes: effect.statTypes ?? [],
    generalTypes: effect.generalTypes ?? [],
    damageModifier: effect.dmgModifier ?? null,
    residualModifier: effect.residualModifier ?? null,
    allowBloodlineDamageDecrease: effect.allowBloodlineDamageDecrease ?? null,
    allowBloodlineDamageIncrease: effect.allowBloodlineDamageIncrease ?? null,
    summonId: effect.aiId ?? null,
    summonHealth: effect.aiHp ?? null,
    movement: effect.type === "redirection" ? effect.direction : null,
    friendlyFire: effect.friendlyFire ?? null,
    delay: effect.delay ?? 0,
  };
}
export function effectText(e) {
  const signed =
    e.direction === "increase" ? "+" : e.direction === "reduction" ? "−" : "";
  let value = `${signed}${e.value}${e.calculation === "percentage" ? "%" : ""}`;
  if (e.chance !== null)
    value = `${e.apReduction !== null ? `${e.apReduction} AP · ` : ""}${e.chance}% chance`;
  if (e.label === "SHIELD")
    value = `${e.shieldHealth} health · ${e.value}% chance`;
  if (e.label === "SUMMON")
    value = `${e.summonHealth} health · ${e.value}% stat scaling`;
  if (e.label === "MOVEMENT") value = `${e.movement} ${e.value} spaces`;
  if (["HEAL", "POOL HEAL"].includes(e.label) && e.calculation === "static")
    value = `${e.value * 10} per application${e.rounds ? " · from next round" : ""}`;
  const qualifiers = [
    e.pools.join(" / "),
    e.elements.join(" / "),
    e.statTypes.length === 4 &&
    ["Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"].every((s) =>
      e.statTypes.includes(s),
    )
      ? "all combat stats"
      : e.statTypes.length
        ? "stats: " + e.statTypes.join(" / ")
        : "",
    e.generalTypes?.length ? "generals: " + e.generalTypes.join(" / ") : "",
    e.allowBloodlineDamageDecrease === false
      ? "bloodline damage decreases excluded"
      : "",
    e.allowBloodlineDamageIncrease === false
      ? "bloodline damage increases excluded"
      : "",
    e.damageModifier && e.damageModifier !== 1
      ? "damage multiplier " + e.damageModifier
      : "",
    e.residualModifier && e.residualModifier !== 1
      ? "residual multiplier " + e.residualModifier
      : "",
  ].filter(Boolean);
  return `${e.target.toUpperCase()} · ${e.label} · ${value}${e.rounds ? ` · ${e.rounds} rounds` : ""}${e.delay ? ` · delay ${e.delay}` : ""}${qualifiers.length ? ` · ${qualifiers.join(" · ")}` : ""}`;
}
