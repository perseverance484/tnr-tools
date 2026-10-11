/**
 * Processor adversarial controls, adapted from upstream consume.test.ts at
 * 585534d7eb21d6f0dd678d5c3eb92662f611d39b. These execute the real applyEffects
 * pipeline with upstream battleScenario fixtures, not item assembly. Powers
 * 15/10 are the revised item powers; 3/3 timing is an unapproved test carrier.
 * Explicit 80+75 ratio and oversized-hit controls test engine ceilings only.
 */
import { describe, expect, it } from "bun:test";
import { SHIELD_MAX_HEALTH } from "@/drizzle/constants";
import { insertAction } from "@/libs/combat/actions";
import { applyEffects } from "@/libs/combat/process";
import { getBattleGrid } from "@/libs/combat/util";
import { SAGE_MODE_ACTIVATION_JUTSU } from "@/libs/sageMode";
import { DamageTag, JutsuValidatorRawSchema } from "@/validators/combat";
import type { CombatAction, CompleteBattle, UserEffect } from "@/libs/combat/types";
import {
  makeBattleUser,
  makeCompleteBattle,
  makeDamageEffect,
  makeEffect,
} from "../../libs/combat/helpers/battleScenario";
import type { Evidence } from "./report";

const ROUND = 3;
const action = (): CombatAction => ({ chakraCost: 0, staminaCost: 0 }) as CombatAction;
const attacker = () => makeBattleUser("attacker", { curHealth: 1000, maxHealth: 1000 });
const defender = (id = "defender", overrides: Record<string, unknown> = {}) =>
  makeBattleUser(id, { curHealth: 100_000_000, maxHealth: 100_000_000, ...overrides });
const battle = (users: ReturnType<typeof makeBattleUser>[], effects: UserEffect[]) =>
  makeCompleteBattle({ round: ROUND, usersState: users, usersEffects: effects });
const user = (b: CompleteBattle, id: string) => b.usersState.find((u) => u.userId === id)!;
const shields = (b: CompleteBattle, id = "attacker") =>
  b.usersEffects.filter((e) => e.type === "shield" && e.targetId === id && e.power > 0);
const shieldHp = (b: CompleteBattle, id = "attacker") =>
  shields(b, id).reduce((sum, e) => sum + e.power, 0);

const hit = (id = "hit-1", creatorId = "attacker", targetId = "defender") =>
  makeDamageEffect({
    id, creatorId, targetId, actionId: id, targetType: "user",
    power: 100, powerPerLevel: 0, calculation: "static", statTypes: ["None"],
    isNew: true, castThisRound: true, createdRound: ROUND, rounds: 0,
  } as Partial<UserEffect>);

const consume = (power: number, overrides: Partial<UserEffect> = {}): UserEffect =>
  ({
    ...makeEffect("consume", {
      power, calculation: "percentage", target: "SELF", rounds: 3, shieldRounds: 3,
    }, {
      id: "active-consume", actionId: "consume-previous-action", fromType: "item",
      creatorId: "attacker", targetId: "attacker", targetType: "user",
      createdRound: ROUND - 1, isNew: false, castThisRound: false,
    }),
    ...overrides,
  }) as UserEffect;

const ongoing = (id: string, creatorId = "attacker", targetId = "defender") => ({
  id, actionId: id, creatorId, targetId, targetType: "user" as const,
  createdRound: ROUND - 1, isNew: false, castThisRound: false,
});

export function registerProcessorProbes(evidence: Evidence): void {
  const check = (name: string, pass: boolean, detail?: unknown) => {
    expect(evidence.check(`processor: ${name}`, pass, detail)).toBe(true);
  };

  describe("Consume processor adversarial probes (upstream fixtures)", () => {
    it.each([15, 10])("converts later residual and poison damage at %i%%", (power) => {
      const residual = {
        ...hit(), isNew: false, castThisRound: false, createdRound: ROUND - 1, rounds: 2,
      };
      const initial = defender();
      const tick = applyEffects(battle([attacker(), initial], [residual, consume(power)]), "defender", action());
      const lost = initial.curHealth - user(tick.newBattle, "defender").curHealth;
      const poison = makeEffect("poison", { power: 50, calculation: "percentage", rounds: 2 }, ongoing("poison"));
      const poisoned = defender();
      const spend = applyEffects(
        battle([attacker(), poisoned], [poison, consume(power)]), "defender",
        { chakraCost: 100, staminaCost: 100 } as CombatAction,
      );
      const poisonLost = poisoned.curHealth - user(spend.newBattle, "defender").curHealth;
      const measured = {
        power, residualHealthLost: lost, residualShield: shieldHp(tick.newBattle),
        poisonHealthLost: poisonLost, poisonShield: shieldHp(spend.newBattle),
      };
      evidence.put(`processor_delayed_${power}`, measured);
      check(`residual tick is nonvacuous at ${power}`, lost > 0 && tick.actionEffects.some((e) => e.txt.includes("residual damage")), measured);
      check(`residual shield uses caster ratio at ${power}`, shieldHp(tick.newBattle) === Math.floor(lost * power / 100), measured);
      check(`poison spending causes damage at ${power}`, poisonLost > 0, measured);
      check(`poison shield uses health damage at ${power}`, shieldHp(spend.newBattle) === Math.floor(poisonLost * power / 100), measured);
    });

    it.each([15, 10])("converts only the Health component of delayed drain at %i%%", (power) => {
      const variants = [
        { name: "health", pools: ["Health"] as ("Health" | "Chakra" | "Stamina")[] },
        { name: "chakra_stamina", pools: ["Chakra", "Stamina"] as ("Health" | "Chakra" | "Stamina")[] },
        { name: "all_pools", pools: ["Health", "Chakra", "Stamina"] as ("Health" | "Chakra" | "Stamina")[] },
      ].map(({ name, pools }) => {
        const victim = defender();
        const drain = makeEffect("drain", { power: 100, calculation: "static", poolsAffected: pools, rounds: 2 }, ongoing(`drain-${name}`));
        const result = applyEffects(battle([attacker(), victim], [drain, consume(power)]), "defender", action()).newBattle;
        const after = user(result, "defender");
        return {
          name, healthLost: victim.curHealth - after.curHealth,
          chakraLost: victim.curChakra - after.curChakra,
          staminaLost: victim.curStamina - after.curStamina,
          shield: shieldHp(result), count: shields(result).length,
        };
      });
      evidence.put(`processor_drain_${power}`, variants);
      for (const row of variants) {
        const hasHealth = row.name !== "chakra_stamina";
        const hasOther = row.name !== "health";
        check(`${row.name} drains exact eligible pools at ${power}`,
          row.healthLost === (hasHealth ? 100 : 0) && row.chakraLost === (hasOther ? 100 : 0) && row.staminaLost === (hasOther ? 100 : 0), row);
        check(`${row.name} converts Health only at ${power}`,
          row.shield === Math.floor(row.healthLost * power / 100) && row.count === (hasHealth ? 1 : 0), row);
      }
    });

    it("attributes simultaneous delayed drain and wound ticks to each original caster", () => {
      const rows = (["drain", "wound"] as const).map((type) => {
        const ticks = [
          { id: "attacker", power: type === "drain" ? 100 : 20 },
          { id: "other", power: type === "drain" ? 200 : 40 },
        ].map(({ id, power }) => type === "drain"
          ? makeEffect("drain", { power, calculation: "static", poolsAffected: ["Health"], rounds: 2 }, ongoing(`${type}-${id}`, id))
          : makeEffect("wound", { power, rounds: 2 }, { ...ongoing(`${type}-${id}`, id), timeTracker: { originalDamage: 1000 } }));
        const victim = defender();
        const result = applyEffects(battle([attacker(), victim, defender("other")], [
          ...ticks,
          consume(15),
          consume(10, { id: "other-consume", actionId: "other-consume", creatorId: "other", targetId: "other" }),
        ]), "defender", action()).newBattle;
        return { type, healthLost: victim.curHealth - user(result, "defender").curHealth,
          attackerShield: shieldHp(result), otherShield: shieldHp(result, "other"),
          victimShield: shieldHp(result, "defender"), expectedDamage: type === "drain" ? [100, 200] : [200, 400],
        };
      });
      evidence.put("processor_per_caster_ticks", rows);
      for (const row of rows) {
        check(`${row.type} both caster ticks apply`, row.healthLost === row.expectedDamage.reduce((a, b) => a + b, 0), row);
        check(`${row.type} attributes shields independently`,
          row.attackerShield === Math.floor(row.expectedDamage[0]! * .15) &&
          row.otherShield === Math.floor(row.expectedDamage[1]! * .10) && row.victimShield === 0, row);
      }
    });

    it("keeps another caster's direct damage out of the owner's conversion", () => {
      const reference = applyEffects(battle([attacker(), defender()], [hit(), consume(15)]), "attacker", action()).newBattle;
      const victim = defender();
      const mixed = applyEffects(battle([attacker(), victim, defender("other")], [
        hit("other-hit", "other"), hit(), consume(15),
      ]), "attacker", action()).newBattle;
      const ownLost = 100_000_000 - user(reference, "defender").curHealth;
      const mixedLost = victim.curHealth - user(mixed, "defender").curHealth;
      const measured = { ownLost, mixedLost, ownShield: shieldHp(reference), mixedShield: shieldHp(mixed) };
      evidence.put("processor_direct_attribution", measured);
      check("mixed direct damage includes both casters", ownLost > 0 && mixedLost === ownLost * 2, measured);
      check("mixed direct damage converts owner's portion only", shieldHp(mixed) === shieldHp(reference) && shieldHp(mixed, "other") === 0, measured);
    });

    it("credits capped reflection to the defender while direct damage belongs to its attacker", () => {
      const reflect = makeEffect("reflect", { power: 100, calculation: "percentage", rounds: 2 }, ongoing("reflect", "defender", "defender"));
      const initialAttacker = attacker();
      const initialDefender = defender();
      const result = applyEffects(battle([initialAttacker, initialDefender], [
        hit(), reflect, consume(15),
        consume(10, { id: "defender-consume", creatorId: "defender", targetId: "defender" }),
      ]), "attacker", action()).newBattle;
      const direct = initialDefender.curHealth - user(result, "defender").curHealth;
      const reflected = initialAttacker.curHealth - user(result, "attacker").curHealth;
      const measured = { direct, reflected, attackerShield: shieldHp(result), defenderShield: shieldHp(result, "defender") };
      evidence.put("processor_reflect_ownership", measured);
      check("reflection respects its 60 percent ceiling", direct > 0 && reflected > 0 && Math.abs(reflected - direct * .6) < 1e-8, measured);
      check("reflection does not inflate attacker's conversion", shieldHp(result) === Math.floor(direct * .15), measured);
      check("reflection converts using defender's 10 percent", shieldHp(result, "defender") === Math.floor(reflected * .10), measured);
    });

    it.each([15, 10])("excludes direct self-damage and reflected self-casts at %i%%", (power) => {
      const self = applyEffects(battle([attacker()], [hit("self-hit", "attacker", "attacker"), consume(power)]), "attacker", action());
      const selfLost = 1000 - user(self.newBattle, "attacker").curHealth;
      const jutsu = JutsuValidatorRawSchema.parse({
        ...SAGE_MODE_ACTIVATION_JUTSU,
        effects: [DamageTag.parse({ power: 100, calculation: "static", rounds: 0,
          target: "SELF", friendlyFire: "FRIENDLY", statTypes: ["None"] })],
      });
      const selfAction = { ...jutsu, id: "reflected-self-cast", type: "jutsu", updatedAt: 0, originalCooldown: 0, level: 0 } as CombatAction;
      const state = makeCompleteBattle({
        createdAt: new Date(0), round: ROUND, width: 5, height: 5,
        usersState: [attacker(), defender()],
        usersEffects: [consume(power), makeEffect("reflect", { power: 50, calculation: "percentage", rounds: 2 }, ongoing("self-reflect", "attacker", "attacker"))],
      });
      const inserted = insertAction({ battle: state, grid: getBattleGrid(20, state), action: selfAction, actorId: "attacker", longitude: 0, latitude: 0 });
      check(`self-cast inserts at ${power}`, inserted);
      const reflected = applyEffects(state, "attacker", selfAction);
      const reflectedLost = 1000 - user(reflected.newBattle, "attacker").curHealth;
      const reflectedLog = reflected.actionEffects.some((e) => e.txt.includes("reflect damage"));
      const measured = { power, selfLost, selfShield: shieldHp(self.newBattle), reflectedLost, reflectedLog, reflectedShield: shieldHp(reflected.newBattle) };
      evidence.put(`processor_self_exclusion_${power}`, measured);
      check(`self-damage actually resolves at ${power}`, selfLost > 0, measured);
      check(`self-reflection actually resolves at ${power}`, reflectedLog && reflectedLost > selfLost, measured);
      check(`neither self-damage path converts at ${power}`,
        shieldHp(self.newBattle) === 0 && shieldHp(reflected.newBattle) === 0 &&
        !reflected.actionEffects.some((e) => e.txt.includes("consumes")), measured);
    });

    it("excludes both immediate recoil and its deferred repayment", () => {
      const recoil = makeEffect("recoil", { power: 50, calculation: "percentage", rounds: 2 }, ongoing("recoil", "defender", "attacker"));
      const diffuse = makeEffect("diffuse", { power: 50, delayRounds: 2, rounds: 3 }, ongoing("diffuse", "attacker", "attacker"));
      const first = applyEffects(battle([attacker(), defender()], [
        hit(), recoil, diffuse, consume(10, { creatorId: "defender", targetId: "defender" }),
      ]), "attacker", action());
      const firstHealth = user(first.newBattle, "attacker").curHealth;
      const debt = user(first.newBattle, "attacker").diffuseDamage ?? [];
      const second = applyEffects({ ...first.newBattle, round: ROUND + 1 }, "attacker", action());
      const secondHealth = user(second.newBattle, "attacker").curHealth;
      const measured = { firstHealth, secondHealth, deferredEntries: debt.length,
        firstOpponentShield: shieldHp(first.newBattle, "defender"), secondOpponentShield: shieldHp(second.newBattle, "defender") };
      evidence.put("processor_recoil_exclusion", measured);
      check("immediate recoil is nonvacuous", firstHealth < 1000 && first.actionEffects.some((e) => e.txt.includes("recoil damage")), measured);
      check("deferred recoil is nonvacuous", debt.length > 0 && secondHealth < firstHealth, measured);
      check("neither recoil installment feeds opponent Consume", measured.firstOpponentShield === 0 && measured.secondOpponentShield === 0, measured);
    });

    it("aggregates active sources, caps their ratio at 100 percent and chooses the longest shield duration", () => {
      const rows = [
        { label: "revised_power_overlap_control", powers: [15, 10], expectedRatio: .25 },
        { label: "ceiling_stress_control_not_item_values", powers: [80, 75], expectedRatio: 1 },
      ].map(({ label, powers, expectedRatio }) => {
        const victim = defender();
        const result = applyEffects(battle([attacker(), victim], [
          hit(), consume(powers[0]!),
          consume(powers[1]!, { id: "separate-bloodline-consume", fromType: "bloodline", shieldRounds: 6 }),
        ]), "attacker", action());
        return { label, powers, expectedRatio,
          healthLost: victim.curHealth - user(result.newBattle, "defender").curHealth,
          shield: shieldHp(result.newBattle), count: shields(result.newBattle).length,
          shieldRounds: shields(result.newBattle)[0]?.rounds,
          logs: result.actionEffects.filter((e) => e.txt.includes("consumes")).length,
        };
      });
      evidence.put("processor_active_source_ratio", rows);
      for (const row of rows) {
        check(`${row.label} converts at expected capped ratio`, row.healthLost > 0 && row.shield === Math.floor(row.healthLost * row.expectedRatio), row);
        check(`${row.label} aggregates to one shield with longest lifetime`, row.count === 1 && row.logs === 1 && row.shieldRounds === 6, row);
      }
    });

    it.each([15, 10])("caps each generated shield at 100000 HP while allowing multiple stacks at %i%%", (power) => {
      // The oversized raw damage is a processor stress carrier, not legal item EP.
      const hugeHit = (id: string) => ({ ...hit(id), power: 2_000_000 });
      const victim = defender();
      const first = applyEffects(battle([attacker(), victim], [hugeHit("huge-1"), consume(power)]), "attacker", action());
      const firstDamage = victim.curHealth - user(first.newBattle, "defender").curHealth;
      const second = applyEffects({
        ...first.newBattle,
        usersEffects: [...first.newBattle.usersEffects, hugeHit("huge-2")],
      }, "attacker", action());
      const secondDamage = user(first.newBattle, "defender").curHealth - user(second.newBattle, "defender").curHealth;
      const measured = { power, stressHitPower: 2_000_000, cap: SHIELD_MAX_HEALTH,
        firstDamage, secondDamage, firstShields: shields(first.newBattle).map((e) => e.power),
        secondShields: shields(second.newBattle).map((e) => e.power),
        aggregateHp: shieldHp(second.newBattle),
      };
      evidence.put(`processor_individual_cap_${power}`, measured);
      check(`shield cap source constant remains 100000 at ${power}`, SHIELD_MAX_HEALTH === 100_000, measured);
      check(`both hits independently exceed shield ceiling at ${power}`, firstDamage * power / 100 > SHIELD_MAX_HEALTH && secondDamage * power / 100 > SHIELD_MAX_HEALTH, measured);
      check(`first generated shield is individually capped at ${power}`, measured.firstShields.length === 1 && measured.firstShields[0] === SHIELD_MAX_HEALTH, measured);
      check(`two generated shields coexist beyond aggregate cap at ${power}`,
        measured.secondShields.length === 2 && measured.secondShields.every((hp) => hp === SHIELD_MAX_HEALTH) && measured.aggregateHp === SHIELD_MAX_HEALTH * 2, measured);
    });

    it.each([15, 10])("aggregates multiple hits and targets into one per-caster shield at %i%%", (power) => {
      const a = defender("victim-a");
      const b = defender("victim-b");
      const result = applyEffects(battle([attacker(), a, b], [
        hit("hit-a1", "attacker", "victim-a"), hit("hit-a2", "attacker", "victim-a"),
        hit("hit-b", "attacker", "victim-b"), consume(power),
      ]), "attacker", action());
      const losses = [a, b].map((victim) => victim.curHealth - user(result.newBattle, victim.userId).curHealth);
      const total = losses.reduce((sum, lost) => sum + lost, 0);
      const measured = { power, losses, total, shield: shieldHp(result.newBattle),
        shieldCount: shields(result.newBattle).length,
        consumeLogs: result.actionEffects.filter((e) => e.txt.includes("consumes")).length };
      evidence.put(`processor_multihit_multitarget_${power}`, measured);
      check(`all three hits apply across both targets at ${power}`, losses.every((lost) => lost > 0) && losses[0] === losses[1]! * 2, measured);
      check(`all hits aggregate before flooring at ${power}`,
        measured.shield === Math.floor(total * power / 100) && measured.shieldCount === 1 && measured.consumeLogs === 1, measured);
    });
  });
}
