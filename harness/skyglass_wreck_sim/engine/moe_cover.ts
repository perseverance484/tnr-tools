/** Pass 6 coverage audit: which hexes each act's telegraphed eruptions can ever reach (fixed patterns; Shatterfall's fan
 *  is caster-anchored, so it is reported at the Saint's start post). Zero live requests. */
import { ALL, dist, key } from "./cclib";
import { CYCLES, FAN_OFFSETS, PAT, STARS } from "./moe_lib";
const k = (c: number[]) => `${c[0]},${c[1]}`;
const show = (name: string, sets: [string, number[][]][]) => {
  const covered = new Set<string>(); const count = new Map<string, number>();
  for (const [, cells] of sets) for (const c of cells) { covered.add(k(c)); count.set(k(c), (count.get(k(c)) ?? 0) + 1); }
  const never = ALL.filter((c) => !covered.has(k(c)));
  console.log(`${name}: ${ALL.length} hexes, ${covered.size} ever marked, ${never.length} never marked: ${never.map((c) => k(c)).join(" ")}`);
  const rows: string[] = [];
  for (let r = 0; r < 10; r++) { let s = ""; for (let c = 0; c < 12; c++) s += covered.has(`${c},${r}`) ? String(Math.min(9, count.get(`${c},${r}`)!)) : "."; rows.push(s); }
  console.log(rows.join("\n"));
};
show("Act I (Refraction A/B, Facet = A+B, Stillness)", [["A", PAT.refractA], ["B", PAT.refractB], ["still", PAT.stillReach]]);
const etchCounts: Record<string, number> = {}; for (const cy of CYCLES) for (const e of cy) etchCounts[e] = (etchCounts[e] ?? 0) + 1;
console.log("Act II etchings per full act:", JSON.stringify(etchCounts));
show("Act II (Recasts A-E)", Object.entries(PAT.etch));
for (const [i, cy] of CYCLES.entries()) show(`Act II cycle ${i + 1} (${cy.join("")})`, cy.map((e) => [e, PAT.etch[e]!]));
const saint: number[] = [8, 5];
const fan = FAN_OFFSETS.map((o: any) => [saint[0]! + o.longitude, saint[1]! + o.latitude]);
show("Act III (Glassfall thirds, flood, Shatterfall at the Saint's post 8,5)", [["g0", PAT.glass[0]!], ["g1", PAT.glass[1]!], ["g2", PAT.glass[2]!], ["flood", PAT.flood], ["fan", fan]]);
show("Act III before the Long Hush (flood + Shatterfall only)", [["flood", PAT.flood], ["fan", fan]]);
console.log("stars (dry during the flood):", STARS.map((c) => k(c)).join(" "));
