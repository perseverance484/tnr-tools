/** Pass 5 check: does any eruption's coordinate list name a hex twice (BATTLE_TAG_STACKING would double the hit)? */
import { loadJson } from "./model";
import { buildRecords, moeParams } from "./moe_lib";
const P = moeParams(loadJson(process.argv[process.argv.indexOf("--params") + 1]!));
const R = buildRecords(P);
for (const [id, r] of Object.entries<any>(R)) {
  const ct = r.coordinateTargeting;
  if (!ct?.coordinates) continue;
  const keys = ct.coordinates.map((c: any) => JSON.stringify(c));
  const dup = keys.length - new Set(keys).size;
  const hit = r.effects.find((e: any) => e.type === "pierce" || e.type === "damage");
  if (hit) console.log(`${id} target ${r.target} origin ${ct.origin} sel ${ct.selection} cells ${keys.length} dup ${dup} ${hit.type} ${hit.power} ${hit.calculation}`);
}
