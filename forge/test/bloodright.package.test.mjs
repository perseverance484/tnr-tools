import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { packageProblems } from "../tools/validate_bloodright_package.mjs";
const root = fileURLToPath(new URL("../../", import.meta.url));
const committed = g => JSON.parse(readFileSync(join(root, `forge/bloodright/naming_pass_collection_${g}.json`), "utf8"));
// Bind every icon to a synthetic pack. The offline check parses the pack; it never fetches bytes.
function bound(g) {
  const pkg = committed(g); pkg.imagePack = { ref: "1".repeat(40), files: {} }; pkg.imgSizes = {};
  for (const t of pkg.bloodrightCollection.trees) for (const ref of Object.values(t.icons)) {
    const name = ref.slice(5); pkg.imagePack.files[name] = { path: `art/x/${name}`, sha256: "a".repeat(64), bytes: 1000 }; pkg.imgSizes[name] = 1000;
  }
  return pkg;
}

test("offline package check: committed templates are blocked on icons; bound packages are clean", async () => {
  for (const g of ["a", "b"]) {
    const blocked = await packageProblems(committed(g), root);
    assert.ok(blocked.length && blocked.every(p => /imgSizes|imagePack/.test(p)), JSON.stringify(blocked.slice(0, 2)));
    assert.deepEqual(await packageProblems(bound(g), root), []);
  }
});

test("offline package check refuses duplicate trees, bad designs, byte mismatches and stray operations", async () => {
  for (const mutate of [
    p => { p.bloodrightCollection.trees.push(structuredClone(p.bloodrightCollection.trees[0])); },
    p => { p.bloodrightCollection.trees[0].source.ref = "f".repeat(40); },
    p => { p.bloodrightCollection.trees[0].nodes.p1_t1.rounds = null; },
    p => { const n = Object.keys(p.imgSizes)[0]; p.imgSizes[n]++; },
    p => { p.jutsu = [{ name: "x" }]; },
  ]) { const p = bound("a"); mutate(p); assert.ok((await packageProblems(p, root)).length); }
});

test("validate.py --strict passes a bound collection package and fails the blocked template", () => {
  const dir = mkdtempSync(join(tmpdir(), "br-pkg-"));
  const run = file => { try { return { code: 0, out: execFileSync("python3", [join(root, "skills/building-tnr-content/scripts/validate.py"), file, "--strict"], { cwd: join(root, "skills/building-tnr-content/data"), encoding: "utf8" }) }; } catch (e) { return { code: e.status, out: String(e.stdout) }; } };
  try {
    const ok = join(dir, "bound.json"); writeFileSync(ok, JSON.stringify(bound("b")));
    const r = run(ok); assert.equal(r.code, 0, r.out); assert.match(r.out, /0 errors/); assert.doesNotMatch(r.out, /no items|capture-only/);
    const bad = run(join(root, "forge/bloodright/naming_pass_collection_b.json")); assert.notEqual(bad.code, 0);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
