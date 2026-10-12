// Offline: parse every AI rule in push/90 with the pinned engine's AiRule / updateAiProfileSchema.
// Usage (cwd = an exported engine app at the pin, e.g. the harness work dir; Bun with --no-install):
//   bun --no-install run <repo>/push/90_ghost_ship_skyglass_release.rules.ts "$PWD" <repo>/push/90_ghost_ship_skyglass_release.json
import { readFileSync } from "node:fs";
const app = process.argv[2], manifest = process.argv[3];
const { AiRule, updateAiProfileSchema } = await import(app + "/src/validators/ai.ts");
const m = JSON.parse(readFileSync(manifest, "utf8"));
let bad = 0, n = 0;
for (const it of m.items) {
  if (it.entity !== "ai" || !Array.isArray(it.data.rules)) continue;
  const r = updateAiProfileSchema.safeParse({ id: "x", rules: it.data.rules, includeDefaultRules: it.data.includeDefaultRules });
  n += it.data.rules.length;
  if (!r.success) { bad++; console.log("FAIL", it.name, JSON.stringify(r.error.issues).slice(0, 400)); continue; }
  const canon = (v: any): any => Array.isArray(v) ? v.map(canon) : v && typeof v === "object" ? Object.fromEntries(Object.keys(v).sort().map((k) => [k, canon(v[k])])) : v;
  const lossy = JSON.stringify(canon(r.data.rules.map((x: any) => ({ conditions: x.conditions, action: x.action })))) !== JSON.stringify(canon(it.data.rules.map((x: any) => ({ conditions: x.conditions, action: x.action }))));
  const last = it.data.rules[it.data.rules.length - 1];
  console.log(`${r.success ? "ok  " : "FAIL"} ${it.name}: ${it.data.rules.length} rules, includeDefaultRules ${it.data.includeDefaultRules}, roundTripChanged ${lossy}, lastRuleUnconditional ${last.conditions.length === 0}`);
}
console.log(`${n} rules parsed, ${bad} profile(s) failed`);
process.exit(bad ? 1 : 0);
