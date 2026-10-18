import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, mkdtempSync, writeFileSync, rmSync, mkdirSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { packageProblems, packBlobProblems } from "../tools/validate_bloodright_package.mjs";
const root = fileURLToPath(new URL("../../", import.meta.url));
const committed = g => JSON.parse(readFileSync(join(root, `forge/bloodright/naming_pass_collection_${g}.json`), "utf8"));
// Bind every icon to a synthetic pack for the structural checks (blob checks are separate).
function bound(g) {
  const pkg = committed(g); pkg.imagePack = { ref: "1".repeat(40), files: {} }; pkg.imgSizes = {};
  for (const t of pkg.bloodrightCollection.trees) for (const ref of Object.values(t.icons)) {
    const name = ref.slice(5); pkg.imagePack.files[name] = { path: `art/x/${name}`, sha256: "a".repeat(64), bytes: 1000 }; pkg.imgSizes[name] = 1000;
  }
  return pkg;
}
const git = (cwd, ...args) => execFileSync("git", ["-C", cwd, ...args], { encoding: "utf8" }).trim();

test("offline package check: committed templates are blocked on icons; structurally bound packages are clean", async () => {
  for (const g of ["a", "b"]) {
    const blocked = await packageProblems(committed(g), root);
    assert.ok(blocked.length && blocked.every(p => /imgSizes|imagePack/.test(p)), JSON.stringify(blocked.slice(0, 2)));
    assert.deepEqual(await packageProblems(bound(g), root, { blobs: false }), []);
  }
});

test("offline package check refuses duplicate trees, bad designs, byte mismatches, stray operations and option refs", async () => {
  for (const mutate of [
    p => { p.bloodrightCollection.trees.push(structuredClone(p.bloodrightCollection.trees[0])); },
    p => { p.bloodrightCollection.trees[0].source.ref = "f".repeat(40); },
    p => { p.bloodrightCollection.trees[0].nodes.p1_t1.rounds = null; },
    p => { const n = Object.keys(p.imgSizes)[0]; p.imgSizes[n]++; },
    p => { p.jutsu = [{ name: "x" }]; },
  ]) { const p = bound("a"); mutate(p); assert.ok((await packageProblems(p, root, { blobs: false })).length); }
  // Review F1: a ref shaped like a git option must never reach git.
  const dir = mkdtempSync(join(tmpdir(), "br-opt-")), target = join(dir, "pwned");
  try {
    const p = bound("a"); p.bloodrightCollection.trees[0].source = { path: "x", ref: `--output=${target}` };
    assert.ok((await packageProblems(p, root, { blobs: false })).length);
    p.imagePack.ref = `--output=${target}`;
    assert.ok(packBlobProblems(p.imagePack, root).length);
    assert.equal(existsSync(`${target}:x`) || existsSync(target), false);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test("review F2: pack blobs are verified offline - digest, size, upload ceiling and pushed ref", () => {
  const repo = mkdtempSync(join(tmpdir(), "br-blobs-"));
  try {
    git(repo, "init", "-q"); mkdirSync(join(repo, "art"));
    const small = new Uint8Array([82, 73, 70, 70, 1, 2, 3]), big = new Uint8Array(524289);
    writeFileSync(join(repo, "art/a.webp"), small); writeFileSync(join(repo, "art/big.webp"), big);
    git(repo, "add", "."); git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "icons");
    const ref = git(repo, "rev-parse", "HEAD"), sha = b => createHash("sha256").update(b).digest("hex");
    const good = { ref, files: { "a.webp": { path: "art/a.webp", sha256: sha(small), bytes: small.length } } };
    assert.ok(packBlobProblems(good, repo).some(p => /not on any pushed branch/.test(p)));
    git(repo, "update-ref", "refs/remotes/origin/main", ref);
    assert.deepEqual(packBlobProblems(good, repo), []);
    const bad = structuredClone(good); bad.files["a.webp"].sha256 = "0".repeat(64);
    assert.ok(packBlobProblems(bad, repo).some(p => /sha256/.test(p)));
    const size = structuredClone(good); size.files["a.webp"].bytes = 99;
    assert.ok(packBlobProblems(size, repo).some(p => /pack says 99/.test(p)));
    const missing = structuredClone(good); missing.files["a.webp"].path = "art/none.webp";
    assert.ok(packBlobProblems(missing, repo).some(p => /not readable/.test(p)));
    const over = { ref, files: { "big.webp": { path: "art/big.webp", sha256: sha(big), bytes: big.length } } };
    assert.ok(packBlobProblems(over, repo).some(p => /upload ceiling/.test(p)));
  } finally { rmSync(repo, { recursive: true, force: true }); }
});

test("validate.py --strict routes collections to the offline check: no 'no items', fabricated icons refused", () => {
  const dir = mkdtempSync(join(tmpdir(), "br-pkg-"));
  const run = file => { try { return { code: 0, out: execFileSync("python3", [join(root, "skills/building-tnr-content/scripts/validate.py"), file, "--strict"], { cwd: join(root, "skills/building-tnr-content/data"), encoding: "utf8" }) }; } catch (e) { return { code: e.status, out: String(e.stdout) }; } };
  try {
    const fake = join(dir, "bound.json"); writeFileSync(fake, JSON.stringify(bound("b")));
    const r = run(fake); assert.notEqual(r.code, 0);
    assert.doesNotMatch(r.out, /no items|capture-only/); assert.match(r.out, /checked offline/);
    const lines = r.out.split("\n").filter(l => l.startsWith("ERROR"));
    assert.ok(lines.length && lines.every(l => /icon |imagePack ref/.test(l)), lines.slice(0, 3).join("\n"));
    const blocked = run(join(root, "forge/bloodright/naming_pass_collection_b.json")); assert.notEqual(blocked.code, 0);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
