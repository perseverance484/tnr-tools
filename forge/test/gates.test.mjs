// The static gates, run as tests so a local `npm test` fails for the same reason CI does.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, cpSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { checkBoundaries } from "../tools/check_boundaries.mjs";

const FORGE = join(dirname(fileURLToPath(import.meta.url)), "..");
import { measure, BUDGET } from "../tools/check_bundle_budget.mjs";

test("no layer outside transport issues a request, and no game host is hardcoded", () => {
  const { files, findings, pin } = checkBoundaries();
  assert.ok(files >= 30, `only ${files} modules scanned`);
  assert.match(pin, /^[0-9a-f]{40}$/, "generated contracts must agree on one source pin");
  assert.deepEqual(findings, [], "boundary violations:\n" + findings.join("\n"));
});

test("the checked bundle is inside its raw and gzip budget", () => {
  const { raw, gzip } = measure();
  assert.ok(raw <= BUDGET.raw, `raw bundle ${raw} exceeds budget ${BUDGET.raw}`);
  assert.ok(gzip <= BUDGET.gzip, `gzip bundle ${gzip} exceeds budget ${BUDGET.gzip}`);
  // A budget far above the measurement stops being a ratchet. Kept honest deliberately.
  assert.ok(raw > BUDGET.raw * 0.7, "raw budget has drifted far above the bundle; re-set it");
});

test("the boundary gate catches a QUALIFIED fetch, not just a bare one", () => {
  // `globalThis.fetch("/api/...")` reaches the game from a forbidden layer without naming a host.
  // The first detector used a negative lookbehind that excluded anything after a dot, so this form
  // passed cleanly. Independent review F2.
  const root = mkdtempSync(join(tmpdir(), "forge-bound-"));
  try {
    mkdirSync(join(root, "tools"), { recursive: true });
    cpSync(join(FORGE, "src"), join(root, "src"), { recursive: true });
    cpSync(join(FORGE, "tools", "check_boundaries.mjs"), join(root, "tools", "check_boundaries.mjs"));
    // The token is assembled rather than written as a literal. ui.test.mjs greps every test file
    // for a global fetch call and cannot tell a call from a fixture string; keeping that guard
    // strict is worth more than the convenience of a literal here.
    const CALL = ["fet", "ch("].join("");
    writeFileSync(join(root, "src", "runner", "_net.mjs"), `export const go = () => globalThis.${CALL}"/api/trpc/jutsu.get");\n`);
    writeFileSync(join(root, "src", "core", "_net.mjs"), `export const go = () => window.${CALL}"/api/trpc/item.get");\n`);
    writeFileSync(join(root, "src", "storage", "_net.mjs"), `export const go = () => ${CALL}"/api/trpc/ai.get");\n`);

    let failed = false, output = "";
    try {
      execFileSync(process.execPath, [join(root, "tools", "check_boundaries.mjs")], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    } catch (e) {
      failed = true;
      output = String(e.stdout || "") + String(e.stderr || "");
    }
    assert.ok(failed, "a qualified fetch outside transport must fail the gate");
    for (const layer of ["runner", "core", "storage"]) {
      assert.match(output, new RegExp(`${layer}/_net\\.mjs: issues a request`));
    }
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("the injected fetchImpl seam is not mistaken for a request", () => {
  // compose() hands win.fetch.bind(win) to the transport layer. That is the seam working, not a
  // layer reaching for the network, and flagging it would make the gate unusable.
  const root = mkdtempSync(join(tmpdir(), "forge-seam-"));
  try {
    mkdirSync(join(root, "tools"), { recursive: true });
    cpSync(join(FORGE, "src"), join(root, "src"), { recursive: true });
    cpSync(join(FORGE, "tools", "check_boundaries.mjs"), join(root, "tools", "check_boundaries.mjs"));
    const BIND = ["fet", "ch.bind"].join("");
    writeFileSync(join(root, "src", "runner", "_seam.mjs"), `export const use = (fetchImpl) => fetchImpl("/x");\nexport const hand = (win) => win.${BIND}(win);\n`);
    execFileSync(process.execPath, [join(root, "tools", "check_boundaries.mjs")], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("the view boundary gate refuses a screen that reaches raw research data or transport", () => {
  // Phase 1 objective 6: no screen constructs a transport call or reads raw capture storage. Each
  // of these is a way a screen could route a read around ForgeCore - and so around the auth gate,
  // the budget and the tier policy - while every behaviour test kept passing.
  const root = mkdtempSync(join(tmpdir(), "forge-view-"));
  try {
    mkdirSync(join(root, "tools"), { recursive: true });
    cpSync(join(FORGE, "src"), join(root, "src"), { recursive: true });
    cpSync(join(FORGE, "tools", "check_boundaries.mjs"), join(root, "tools", "check_boundaries.mjs"));
    writeFileSync(join(root, "src", "ui", "_snap.mjs"), `export const go = (app, k) => app.cache.getSnapshot(k);\n`);
    writeFileSync(join(root, "src", "ui", "_body.mjs"), `export const go = (app) => app.cache.get("jutsu.get", "j1");\n`);
    writeFileSync(join(root, "src", "ui", "_read.mjs"), `export const go = (app, i) => app.reader.query("combat.getBattleEntries", i);\n`);
    writeFileSync(join(root, "src", "hosts", "_wire.mjs"), `export const go = (d) => d.client.batch([{ path: "jutsu.get" }]);\n`);

    let failed = false, output = "";
    try {
      execFileSync(process.execPath, [join(root, "tools", "check_boundaries.mjs")], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    } catch (e) { failed = true; output = String(e.stdout || "") + String(e.stderr || ""); }
    assert.ok(failed, "a view reaching raw research data must fail the gate");
    assert.match(output, /ui\/_snap\.mjs: reads a capture snapshot body out of storage/);
    assert.match(output, /ui\/_body\.mjs: reads or writes a cached response body directly/);
    assert.match(output, /ui\/_read\.mjs: drives the budgeted reader directly/);
    assert.match(output, /hosts\/_wire\.mjs: constructs a transport call directly/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("the Captures screen's metadata listings stay allowed, and carry no bodies", async () => {
  // The gate above must not be so wide that the Captures screen cannot render. These are the calls
  // it actually makes, and they are allowed precisely because the values they return have no `data`.
  const { IDBFactory } = await import("fake-indexeddb");
  const { CaptureCache } = await import("../src/storage/captures.mjs");
  const cache = new CaptureCache(new IDBFactory(), () => 0);
  await cache.put({ path: "jutsu.get", id: "j1", input: { id: "j1" }, data: { id: "j1", secret: "BODY" } });
  await cache.putQuery({ path: "combat.getBattleEntries", queryKey: '{"battleId":"b1"}', input: { battleId: "b1" }, data: [{ secret: "BODY" }] });
  await cache.putSnapshot({ key: "j::after::0", jobId: "j", phase: "after", ordinal: 0, path: "combat.getBattleEntries", id: null, input: null, data: [{ secret: "BODY" }], tier: "local-only" });
  const seen = JSON.stringify({ list: await cache.list(), snaps: await cache.listSnapshots() });
  assert.ok(!seen.includes("BODY"), "a metadata listing must never carry a response body");
  assert.match(seen, /"tier":"local-only"/, "it does carry the tier, so a screen can say where a body is allowed to go");
  cache.close();
});
