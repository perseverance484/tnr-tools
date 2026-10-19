import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { ForgeCore } from "../src/core/core.mjs";
import { readIdmap, writeIdmap } from "../src/storage/compat.mjs";
import { readAssetUploads } from "../src/storage/assets.mjs";
import { composeForTest } from "./compose.mjs";
import { BloodrightGame } from "./bloodright.game.mjs";
const design = JSON.parse(readFileSync(new URL("../../docs/design/bloodright/examples/blood_enchanted_eyes_structural.json", import.meta.url)));
const pilot = JSON.parse(readFileSync(new URL("../bloodright/bee.pilot.json", import.meta.url)));
const clone = structuredClone;
const sha = bytes => createHash("sha256").update(bytes).digest("hex");
const categories = ["Foundation", "Hidden Art", "Advanced Art"];
const HP = pilot.bloodright.hiddenProbeId, FOLDER = pilot.bloodright.bindings.folderId;
const mutations = d => d.game.calls.filter(c => /skillTree\.(create|update)/.test(c.path));

function setup() {
  const game = new BloodrightGame();
  game.folders.set(FOLDER, { id: FOLDER, name: "Blood-Enchanted Eyes", image: "", description: null, order: 120, hidden: false });
  game.skills.set(HP, { id: HP, name: "Hungry Pulse", image: "https://example.test/keep.webp", description: "New skill description", target: "SELF", tier: 1, requiredSkillIds: [], costSkillPoints: 1, pathType: "BLOODRIGHT", bloodlineId: design.bloodline.id, seichiSilverCost: 20, hidden: true, skillType: "DEFAULT", folderId: FOLDER, effects: [] });
  const d = composeForTest({ game });
  // Second tree is synthetic TEST DATA, never a proposal for another bloodline.
  const second = clone(design); second.bloodline.id = "collection-test-bloodline";
  second.nodes.forEach(n => n.name = `Test ${n.name}`);
  const configs = [clone(pilot.bloodright), clone(pilot.bloodright)];
  configs[1].source.path = "test/second.json";
  configs[1].bindings = {}; configs[1].folder = { name: "Test collection folder" };
  const pkg = { bloodrightCollection: { version: 1, trees: configs }, imagePack: { ref: pilot.bloodright.source.ref, files: {} }, imgSizes: {} };
  const blobs = new Map();
  for (const [i, c] of configs.entries()) {
    c.icons = {};
    for (const [tier, category] of categories.entries()) {
      const name = `test-${i}-${tier}.webp`, path = `test/${name}`;
      // Transport fixture bytes; no claim of art/pixel validation.
      const bytes = new Uint8Array([82, 73, 70, 70, i, tier]);
      blobs.set(path, bytes);
      c.icons[category] = `@img:${name}`;
      pkg.imgSizes[name] = bytes.length;
      pkg.imagePack.files[name] = { path, sha256: sha(bytes), bytes: bytes.length };
    }
  }
  d.github.text = async path => JSON.stringify(path === configs[1].source.path ? second : design);
  d.github.raw = async path => blobs.get(path);
  let uploads = 0;
  d.uploader.upload = async file => { uploads++; return { ufsUrl: `https://example.test/${sha(new Uint8Array(await file.arrayBuffer()))}.webp` }; };
  const core = new ForgeCore({ ...d, version: "test", now: d.clock });
  const events = []; core.subscribe(e => events.push(e));
  const entry = () => ({ path: "push/collection.json", name: "collection", text: JSON.stringify(pkg) });
  return { ...d, core, pkg, second, blobs, entry, events, uploadCount: () => uploads };
}

test("Core collection: all icons verified before writes, two scoped exports, repeat preview and run are no-ops", async () => {
  const d = setup();
  await d.core.selectManifest(d.entry());
  assert.deepEqual(d.core.state.selected.problems, []);
  assert.equal(d.core.state.selected.plan.length, 26);
  assert.equal(d.core.state.selected.packResult.entries.length, 6);
  assert.equal(mutations(d).length, 0); assert.equal(d.uploadCount(), 0);
  await d.core.startJob();
  const jobs = d.journal.listJobs();
  assert.equal(jobs.length, 2, JSON.stringify(d.events));
  assert.ok(jobs.every(j => j.state === "DONE" && j.items.every(i => i.verify === "match")));
  assert.equal(d.game.skills.size, 24); assert.equal(d.uploadCount(), 6);
  for (const [i, tree] of [design, d.second].entries()) for (const n of tree.nodes) {
    const row = [...d.game.skills.values()].find(r => r.bloodlineId === tree.bloodline.id && r.name === n.name);
    const digest = d.pkg.imagePack.files[d.pkg.bloodrightCollection.trees[i].icons[n.category].slice(5)].sha256;
    assert.equal(row.image, readAssetUploads(d.storage)[digest].url);
    assert.equal(row.hidden, true);
  }
  const exported = d.events.filter(e => e.type === "export").map(e => JSON.parse(e.text));
  assert.equal(exported.length, 2);
  assert.ok(exported.every(b => b.compiledManifest.imagePack && b.journal.collection.total === 2));
  assert.equal(new Set(exported.map(b => b.compiledManifest.bloodrightImport.bloodlineId)).size, 2);
  const before = mutations(d).length;
  await d.core.selectManifest(d.entry());
  assert.deepEqual(d.core.state.selected.problems, []);
  assert.ok(d.core.state.selected.bloodright.preview.every(r => r.operation === "reuse"));
  await d.core.startJob();
  assert.equal(mutations(d).length, before); assert.equal(d.uploadCount(), 6);
});

test("collection refuses every tree before Start for duplicates, unsupported designs or missing icons", async () => {
  for (const mutate of [
    d => { d.pkg.bloodrightCollection.trees[1] = clone(d.pkg.bloodrightCollection.trees[0]); },
    d => { d.second.nodes[0].name = design.nodes[0].name; },
    d => { d.pkg.bloodrightCollection.trees[1].folder.name = "Blood-Enchanted Eyes"; },
    d => { d.second.build_rules.max_bp = 4; },
    d => { delete d.pkg.bloodrightCollection.trees[1].icons; },
    d => { delete d.pkg.imagePack.files["test-1-0.webp"]; },
    d => { d.pkg.imgSizes["test-1-0.webp"]++; },
    d => { d.pkg.imagePack.ref = "main"; },
    d => { d.pkg.bloodrightCollection.trees[1].nodes.p1_t1.rounds = null; },
  ]) {
    const d = setup(); mutate(d); await d.core.selectManifest(d.entry());
    assert.ok(d.core.state.selected.problems.length);
    await d.core.startJob();
    assert.equal(d.journal.listJobs().length, 0); assert.equal(mutations(d).length, 0); assert.equal(d.uploadCount(), 0);
  }
});

test("corrupt icon in the final tree and same-size post-preview replacement both stop all writes", async () => {
  for (const mode of ["digest", "replacement"]) {
    const d = setup();
    if (mode === "digest") d.blobs.set("test/test-1-2.webp", new Uint8Array(6));
    await d.core.selectManifest(d.entry());
    if (mode === "replacement") d.runner.files.set("test-1-2.webp", new File([new Uint8Array(6)], "test-1-2.webp", { type: "image/webp" }));
    await d.core.startJob();
    assert.equal(d.journal.listJobs().length, 0); assert.equal(mutations(d).length, 0); assert.equal(d.uploadCount(), 0);
  }
});

test("collection stops after a lost update; Core reload resumes frozen text, then a fresh collection finishes", async () => {
  const d = setup(); await d.core.selectManifest(d.entry()); d.game.crashPath = "skillTree.update";
  await d.core.startJob();
  assert.equal(d.journal.listJobs().length, 1);
  const job = d.journal.listJobs()[0]; assert.equal(job.state, "PAUSED");
  assert.ok(![...d.game.skills.values()].some(s => s.bloodlineId === d.second.bloodline.id));
  const reload = composeForTest({ game: d.game, storage: d.storage, idb: d.idb });
  reload.github.raw = d.github.raw;
  reload.github.text = async () => { throw new Error("active job must not recompile"); };
  reload.uploader.upload = d.uploader.upload;
  const core = new ForgeCore({ ...reload, version: "test" });
  await core.resumeJob(job.jobId);
  assert.equal(reload.journal.get(job.jobId).state, "DONE");
  assert.equal(reload.journal.listJobs().length, 1, "reload must not automatically start the next tree");
  reload.github.text = d.github.text;
  await core.selectManifest(d.entry()); assert.deepEqual(core.state.selected.problems, []);
  await core.startJob(); assert.equal(d.game.skills.size, 24);
  assert.equal(d.game.calls.filter(c => c.path === "skillTree.create").length, 23);
});

test("explicit Pause at the final item of tree one prevents tree two, even if tree one is DONE", async () => {
  const d = setup(); await d.core.selectManifest(d.entry());
  d.core.subscribe(e => { if (e.type === "idle") d.core.requestPause(); });
  await d.core.startJob();
  assert.equal(d.journal.listJobs().length, 1); assert.equal(d.journal.listJobs()[0].state, "DONE");
  assert.equal(d.game.skills.size, 12);
});

test("a new unresolved job for the final bloodline blocks the whole collection at Start", async () => {
  const d = setup(); await d.core.selectManifest(d.entry());
  const selected = d.core.state.selected;
  d.runner.plan(selected.collection[1].text, { jobId: "other" });
  d.journal.transition("other", 0, "SENT", { phase: "create" });
  await d.core.startJob();
  assert.equal(d.journal.listJobs().length, 1);
  assert.equal(mutations(d).length, 0); assert.equal(d.uploadCount(), 0);
});

test("drift in the first tree stops the collection, and concurrent Start/selection cannot switch it", async () => {
  const d = setup(); await d.core.selectManifest(d.entry());
  const handle = d.game.handle.bind(d.game); let reentered = false;
  d.game.handle = (path, input) => {
    const result = handle(path, input);
    if (path === "skillTree.update" && input.id === HP) {
      d.game.skills.get(HP).description = "external drift";
      if (!reentered) {
        reentered = true;
        void d.core.startJob(); void d.core.selectManifest(d.entry());
      }
    }
    return result;
  };
  await d.core.startJob();
  assert.equal(d.journal.listJobs().length, 1);
  assert.ok(d.journal.listJobs()[0].items.some(i => i.verify === "drift"));
  assert.ok(![...d.game.skills.values()].some(s => s.bloodlineId === d.second.bloodline.id));
});

test("Pause during frozen-preview persistence opens no job and sends nothing", async () => {
  const d = setup(); await d.core.selectManifest(d.entry());
  const put = d.repoCache.put.bind(d.repoCache);
  d.repoCache.put = async row => { await put(row); d.core.requestPause(); };
  await d.core.startJob();
  assert.equal(d.journal.listJobs().length, 0); assert.equal(mutations(d).length, 0); assert.equal(d.uploadCount(), 0);
});

test("single-tree package forwards image packs, per-node icon wins, changed bytes never reuse filename URL", async () => {
  const d = setup(), cfg = d.pkg.bloodrightCollection.trees[0];
  cfg.nodes.p1_t1.image = "https://example.test/explicit.webp";
  const single = () => ({ ...d.entry(), text: JSON.stringify({ bloodright: cfg, imagePack: d.pkg.imagePack, imgSizes: d.pkg.imgSizes }) });
  await d.core.selectManifest(single()); assert.deepEqual(d.core.state.selected.problems, []);
  await d.core.startJob();
  assert.equal([...d.game.skills.values()].find(s => s.name === design.nodes[0].name).image, "https://example.test/explicit.webp");
  const before = d.uploadCount(), bytes = new Uint8Array([82, 73, 70, 70, 9, 9]);
  d.blobs.set("test/test-0-0.webp", bytes); d.pkg.imagePack.files["test-0-0.webp"].sha256 = sha(bytes);
  const map = readIdmap(d.storage); map["test-0-0.webp"] = "https://example.test/old-filename.webp"; writeIdmap(d.storage, map);
  await d.core.selectManifest(single());
  assert.ok(d.core.state.selected.bloodright.preview.some(r => r.changes.some(c => c.key === "image")));
  await d.core.startJob(); assert.equal(d.uploadCount(), before + 1);
  assert.equal(d.game.skills.get(HP).image, readAssetUploads(d.storage)[sha(bytes)].url);
});

test("committed starter stays blocked without the missing icon pack", async () => {
  const d = setup();
  const text = readFileSync(new URL("../bloodright/collection.template.json", import.meta.url), "utf8");
  await d.core.selectManifest({ ...d.entry(), text });
  assert.equal(d.core.state.selected.problems.length, 3);
  assert.ok(d.core.state.selected.problems.every(p => p.includes("immutable imagePack binding")));
  await d.core.startJob(); assert.equal(mutations(d).length, 0); assert.equal(d.journal.listJobs().length, 0);
});

test("collection screen labels the scope and compiled icon manifests pass Python strict validation and harvest", async () => {
  const { execFileSync } = await import("node:child_process");
  const { mkdtempSync, writeFileSync, rmSync } = await import("node:fs");
  const { tmpdir } = await import("node:os");
  const { join } = await import("node:path");
  const { fileURLToPath } = await import("node:url");
  const { JSDOM } = await import("jsdom");
  const { ManifestsScreen, RunScreen } = await import("../src/ui/screens.mjs");
  const root = fileURLToPath(new URL("../../", import.meta.url));
  const d = setup(); await d.core.selectManifest(d.entry());
  const dom = new JSDOM("<!doctype html><body></body>");
  const previous = globalThis.document; globalThis.document = dom.window.document;
  try {
    // The real screen consumes the core through the same app facade as the other UI tests.
    d.core.state.picker = [];
    const app = { state: d.core.state, journal: d.journal, runner: d.runner, storage: d.storage, now: d.clock, budget: d.budget,
      view: { pickerQuery: "" }, blockedPaths: (...args) => d.core.blockedPaths(...args) };
    const screen = ManifestsScreen(app);
    assert.match(screen.textContent, /2 Bloodright trees, all hidden/);
    assert.match(screen.textContent, /2 trees · 24 skills · 2 folders · 6 icons/);
    assert.ok([...screen.querySelectorAll("button")].some(b => b.textContent === "Start all trees" && !b.disabled));
    await d.core.startJob();
    assert.match(RunScreen(app).textContent, /tree 2\/2/);
  } finally { globalThis.document = previous; dom.window.close(); }
  const dir = mkdtempSync(join(tmpdir(), "br-collection-"));
  try {
    for (const [i, event] of d.events.filter(e => e.type === "export").entries()) {
      const bundle = JSON.parse(event.text), file = join(dir, `compiled-${i}.json`), results = join(dir, `results-${i}.json`);
      writeFileSync(file, JSON.stringify(bundle.compiledManifest)); writeFileSync(results, event.text);
      const validated = execFileSync("python3", [join(root, "skills/building-tnr-content/scripts/validate.py"), file, "--strict"], { cwd: join(root, "skills/building-tnr-content/data"), encoding: "utf8" });
      assert.match(validated, /0 errors/);
      const verified = execFileSync("python3", [join(root, "skills/building-tnr-content/scripts/harvest.py"), "verify", results], { cwd: root, encoding: "utf8" });
      assert.match(verified, /13 ok, 0 fail, 0 unverified, 0 skipped  ->  verified/);
    }
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test("D1: an explicit node image of null is refused, not replaced by the category icon", async () => {
  const d = setup();
  d.pkg.bloodrightCollection.trees[1].nodes.p1_t1.image = null;
  await d.core.selectManifest(d.entry());
  const problems = d.core.state.selected.problems;
  assert.ok(problems.some(p => /icon must be an HTTPS URL or @img filename/.test(p)), JSON.stringify(problems));
  await d.core.startJob();
  assert.equal(d.journal.listJobs().length, 0); assert.equal(mutations(d).length, 0); assert.equal(d.uploadCount(), 0);
});

test("D2: a collection beside top-level jutsu is refused before Start", async () => {
  const d = setup();
  d.pkg.jutsu = [{ name: "x" }];
  await d.core.selectManifest(d.entry());
  assert.equal(d.core.state.selected, null, "nothing selectable means nothing startable");
  assert.ok(d.events.some(e => e.type === "error" && /without other manifest operations/.test(e.text)), JSON.stringify(d.events));
  await d.core.startJob();
  assert.equal(d.journal.listJobs().length, 0); assert.equal(mutations(d).length, 0); assert.equal(d.uploadCount(), 0);
});

test("Core collection: the live inventory is read once for every tree, progress is shown, and a failed open stays on screen", async () => {
  const d = setup();
  const steps = []; d.core.subscribe(() => { if (d.core.state.opening) steps.push(d.core.state.opening.step); });
  await d.core.selectManifest(d.entry());
  assert.deepEqual(d.core.state.selected.problems, []);
  const calls = p => d.game.calls.filter(c => c.path === p).length;
  // One probe read and one folder read for the whole collection (two trees), not one per tree.
  assert.equal(calls("skillTree.getAllFolders"), 1);
  // One complete inventory: two agreeing scans over the SKILL and BLOODRIGHT paths, one page each here.
  assert.equal(calls("skillTree.getAll"), 4);
  assert.ok(steps.some(s => /live skill inventory/.test(s)) && steps.some(s => /tree 2\/2/.test(s)), steps.join(" | "));
  assert.equal(d.core.state.opening, null);

  // Mixed probes are refused before any read.
  const mixed = structuredClone(d.pkg); mixed.bloodrightCollection.trees[1].hiddenProbeId = "Zz".repeat(10) + "Z";
  const before = d.game.calls.length;
  await d.core.selectManifest({ path: "push/mixed.json", name: "mixed", text: JSON.stringify(mixed) });
  assert.equal(d.game.calls.length, before);
  assert.match(d.core.state.openError.text, /same hidden probe/);
  assert.equal(d.core.state.selected, null); assert.equal(d.core.state.opening, null);

  // Lost hidden access: the reason stays on screen until cleared.
  d.game.hiddenAccess = false;
  await d.core.selectManifest(d.entry());
  assert.match(d.core.state.openError.text, /hidden-content access not established/);
  d.core.clearSelection();
  assert.equal(d.core.state.openError, null);
});

test("a shared collection inventory is never changed by one tree's bound-skill re-reads", async () => {
  const { readBloodrightInventory, prepareBloodright } = await import("../src/bloodright/compiler.mjs");
  const d = setup();
  const inventory = await readBloodrightInventory({ reader: d.core.reader, hiddenProbeId: HP });
  const before = JSON.stringify(inventory);
  // The bound skill now reads differently from the inventory row, so tree one replaces that row.
  d.game.skills.get(HP).description = "changed after the inventory read";
  const tree = d.pkg.bloodrightCollection.trees[0];
  const r = await prepareBloodright({ ...d.core, config: tree, imagePack: d.pkg.imagePack, imgSizes: d.pkg.imgSizes, requireIcons: true, inventory });
  assert.deepEqual(r.problems, []);
  assert.equal(JSON.stringify(inventory), before);
});

test("repair: reopening a collection whose recorded icons no longer load re-uploads only those and updates only their skills", async () => {
  const d = setup();
  await d.core.selectManifest(d.entry());
  await d.core.startJob();
  const before = d.uploadCount();
  // The game deleted tree one's Foundation icon after it was saved. Fresh uploads get new URLs.
  const deadUrl = readAssetUploads(d.storage)[d.pkg.imagePack.files["test-0-0.webp"].sha256].url;
  let n = 0;
  d.uploader.upload = async () => ({ url: `https://example.test/fresh-${++n}.webp` });
  const probe = async (url) => url !== deadUrl;
  d.core.imageProbe = probe; d.runner.imageProbe = probe;
  await d.core.selectManifest(d.entry());
  const s = d.core.state.selected;
  assert.deepEqual(s.problems, []);
  const updates = s.bloodright.preview.filter((row) => row.operation === "update");
  assert.equal(updates.length, 4, "the four Foundation skills of tree one, nothing else");
  assert.ok(updates.every((row) => row.changes.length === 1 && row.changes[0].key === "image"));
  await d.core.startJob();
  assert.equal(n, 1, "the dead icon is uploaded once and shared by its four skills");
  const fresh = [...d.game.skills.values()].filter((sk) => sk.image === "https://example.test/fresh-1.webp");
  assert.equal(fresh.length, 4);
  assert.ok(d.uploadCount() === before, "the original uploader was not used again");
});

test("an upload that does not load is never saved onto a skill or recorded for reuse", async () => {
  const d = setup();
  d.runner.imageProbe = async () => false;
  await d.core.selectManifest(d.entry());
  await d.core.startJob();
  const jobs = d.journal.listJobs();
  const failed = jobs.flatMap((j) => j.items).filter((it) => it.state === "FAILED");
  assert.ok(failed.length > 0 && failed.every((it) => /does not load/.test(it.error ?? "")), JSON.stringify(failed.slice(0, 1)));
  assert.deepEqual(readAssetUploads(d.storage), {}, "nothing recorded for reuse");
  assert.ok(![...d.game.skills.values()].some((sk) => /^https:\/\/example\.test\/[0-9a-f]{64}\.webp$/.test(sk.image)), "no skill carries the dead upload");
});

test("verification resolves images from what was recorded and never uploads", async () => {
  const d = setup();
  // Probes say every link is dead DURING verification only: a verify that probed would forget the
  // records and upload again; one that only reads finishes with exactly the six original uploads.
  let verifying = false;
  d.runner.imageProbe = async () => !verifying;
  const verify = d.runner._verify.bind(d.runner);
  d.runner._verify = async (...a) => { verifying = true; try { return await verify(...a); } finally { verifying = false; } };
  await d.core.selectManifest(d.entry());
  const uploadsBefore = d.uploadCount();
  await d.core.startJob();
  assert.equal(d.uploadCount() - uploadsBefore, 6);
  assert.ok(d.journal.listJobs().every((j) => j.state === "DONE" && j.items.every((it) => it.verify === "match")));
});

test("a name clash with an existing folder names that folder's ID, so it can be bound", async () => {
  const d = setup();
  d.game.folders.set("existingF1", { id: "existingF1", name: "Test collection folder", image: "", description: null, order: 0, hidden: true });
  await d.core.selectManifest(d.entry());
  assert.ok(d.core.state.selected.problems.some((p) => /folder "Test collection folder" exists \(existingF1, hidden\)/.test(p)), d.core.state.selected.problems.join(" | "));
});
