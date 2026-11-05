import { loadJson } from "./model";
import { buildPlayer, moeParams, playerJutsuCatalog, playerModel, setGearOverride } from "./moe_lib";
const P = loadJson(process.argv[process.argv.indexOf("--params") + 1]!);
setGearOverride(P.gear ?? null, P.avgGear ?? null); moeParams(P);
const m = playerModel("elite_real");
console.log("variant DR", m.variant.damageTakenReductionPct, "pools", m.variant.poolsMultiplier);
const u = buildPlayer(m, playerJutsuCatalog());
for (const it of u.items) for (const e of it.item?.effects ?? []) if (e.type === "decreasedamagetaken") console.log(it.item.id, e.type, e.power, e.calculation, JSON.stringify({statTypes: e.statTypes, generalTypes: e.generalTypes, elements: e.elements}));
