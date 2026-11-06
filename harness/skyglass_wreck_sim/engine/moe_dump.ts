import { loadJson } from "./model";
import { buildRecords, moeParams } from "./moe_lib";
const P = moeParams(loadJson(process.argv[process.argv.indexOf("--params") + 1]!));
const R = buildRecords(P);
const seen: Record<string, Set<string>> = {};
for (const [id, r] of Object.entries<any>(R)) for (const e of r.effects) (seen[`${e.type}/${e.target ?? "-"}/${e.friendlyFire ?? "-"}`] ??= new Set()).add(id);
for (const [k, v] of Object.entries(seen).sort()) console.log(k.padEnd(45), v.size, [...v].slice(0, 3).join(" "));
