#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace(path, old, new):
    p = ROOT / path
    text = p.read_text()
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one patch anchor, found {count}")
    p.write_text(text.replace(old, new, 1))


# Journal: empty jobs remain invalid unless Runner explicitly opens a parsed capture-only manifest.
replace(
    "forge/src/storage/journal.mjs",
    '''export function jobOutcome(job) {
  if (!job || !Array.isArray(job.items)) return "open";
  if (job.state === "RUNNING" || job.state === "PAUSED") return "open";
  if (job.items.some((it) => it.state === "FAILED")) return "failed";
  if (job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state) || it.state === "SKIPPED" || (it.verify && it.verify !== "match"))) return "unverified";
  return job.items.length ? "success" : "unverified";
}''',
    '''export function jobOutcome(job) {
  if (!job || !Array.isArray(job.items)) return "open";
  if (job.state === "RUNNING" || job.state === "PAUSED") return "open";
  if (!job.items.length) {
    const captures = [...(job.capturesBefore || []), ...(job.capturesAfter || [])];
    if (!captures.length) return "unverified";
    return captures.every((capture) => capture && capture.ok === true) ? "success" : "failed";
  }
  if (job.items.some((it) => it.state === "FAILED")) return "failed";
  if (job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state) || it.state === "SKIPPED" || (it.verify && it.verify !== "match"))) return "unverified";
  return "success";
}''')

replace(
    "forge/src/storage/journal.mjs",
    '''  open({ jobId, manifestPath, manifestNumber, manifestHash, items }) {
    if (!jobId) throw new JournalError("jobId required");
    if (!Array.isArray(items) || !items.length) throw new JournalError("a job needs at least one item");''',
    '''  open({ jobId, manifestPath, manifestNumber, manifestHash, items, allowEmpty = false }) {
    if (!jobId) throw new JournalError("jobId required");
    if (!Array.isArray(items) || (!items.length && !allowEmpty)) throw new JournalError("a job needs at least one item unless it is an explicit capture-only job");''')

# Runner: only the parser-validated capture-only shape receives the empty-job exception.
replace(
    "forge/src/runner/runner.mjs",
    '''    const order = planOrder(manifest, readIdmap(this.storage));
    const job = this.journal.open({ jobId, manifestPath, manifestNumber, manifestHash: manifest.hash, items: toJournalSpecs(order) });''',
    '''    const order = planOrder(manifest, readIdmap(this.storage));
    const captureOnly = order.length === 0 && manifest.capture.before.length + manifest.capture.after.length > 0;
    const job = this.journal.open({ jobId, manifestPath, manifestNumber, manifestHash: manifest.hash, items: toJournalSpecs(order), allowEmpty: captureOnly });''')

# UI: capture-only work must never display mutation language.
replace(
    "forge/src/ui/screens.mjs",
    '''  const s = app.state.selected;
  const card = h("div", { class: "f-card" }, h("h2", {}, s.entry.name), h("div", { class: "f-mute" }, `${s.plan.length} items · manifest hash ${s.manifest.hash}`));''',
    '''  const s = app.state.selected;
  const captureCount = s.manifest.capture.before.length + s.manifest.capture.after.length;
  const readOnly = s.plan.length === 0;
  const card = h("div", { class: "f-card" }, h("h2", {}, s.entry.name), h("div", { class: "f-mute" }, `${s.plan.length} items${captureCount ? ` · ${captureCount} capture${captureCount === 1 ? "" : "s"}` : ""} · manifest hash ${s.manifest.hash}`));
  if (readOnly) card.appendChild(h("div", { class: "f-banner info" }, "Read-only capture job. This sends queries only; zero mutations."));''')

replace(
    "forge/src/ui/screens.mjs",
    '''    h("button", { class: "f-primary", disabled: s.problems.length > 0 || missingImgs.length > 0, onClick: () => app.confirm(`Start job for ${s.entry.name}: ${s.plan.length} items (${s.plan.filter((i) => i.op === "create").length} creates)? This writes to the game.`, () => app.startJob()) }, "Start job"),''',
    '''    h("button", { class: "f-primary", disabled: s.problems.length > 0 || missingImgs.length > 0, onClick: () => app.confirm(
      readOnly
        ? `Run read-only capture job for ${s.entry.name}: ${captureCount} capture${captureCount === 1 ? "" : "s"}? No mutations will be sent.`
        : `Start job for ${s.entry.name}: ${s.plan.length} items (${s.plan.filter((i) => i.op === "create").length} creates)? This writes to the game.`,
      () => app.startJob()),
    }, readOnly ? "Run captures" : "Start job"),''')

old_run = '''  const outcome = jobOutcome(job);
  if (job.state === "DONE" || job.state === "INCOMPLETE") {
    const drift = job.items.filter((i) => i.verify === "drift").length;
    const unread = job.items.filter((i) => i.verify === "unread").length;
    const failed = job.items.filter((i) => i.state === "FAILED").length;
    const skipped = job.items.filter((i) => i.state === "SKIPPED").length;
    root.appendChild(outcome === "success"
      ? h("div", { class: "f-banner ok" }, h("b", {}, "Verified. "), "every item read back equal on its asserted keys.")
      : h("div", { class: "f-banner " + (outcome === "failed" ? "bad" : "warn") },
          h("b", {}, outcome === "failed" ? "Finished with failures. " : "Finished UNVERIFIED. "),
          [failed ? `${failed} failed` : null, drift ? `${drift} drifted` : null, unread ? `${unread} could not be read back` : null, skipped ? `${skipped} skipped` : null].filter(Boolean).join(", "),
          ". These writes are not proven. ",
          job.state === "INCOMPLETE" ? "Resume to re-read them; resuming can only read, never re-send." : ""));
  }'''
new_run = '''  const outcome = jobOutcome(job);
  if ((job.state === "DONE" || job.state === "INCOMPLETE") && job.items.length === 0) {
    const captures = [...(job.capturesBefore || []), ...(job.capturesAfter || [])];
    const failed = captures.filter((capture) => !capture.ok).length;
    root.appendChild(outcome === "success"
      ? h("div", { class: "f-banner ok" }, h("b", {}, "Read-only capture complete. "), `${captures.length}/${captures.length} reads succeeded; zero mutations were sent.`)
      : h("div", { class: "f-banner bad" }, h("b", {}, "Read-only capture failed. "), `${failed} of ${captures.length} reads failed; zero mutations were sent.`));
  } else if (job.state === "DONE" || job.state === "INCOMPLETE") {
    const drift = job.items.filter((i) => i.verify === "drift").length;
    const unread = job.items.filter((i) => i.verify === "unread").length;
    const failed = job.items.filter((i) => i.state === "FAILED").length;
    const skipped = job.items.filter((i) => i.state === "SKIPPED").length;
    root.appendChild(outcome === "success"
      ? h("div", { class: "f-banner ok" }, h("b", {}, "Verified. "), "every item read back equal on its asserted keys.")
      : h("div", { class: "f-banner " + (outcome === "failed" ? "bad" : "warn") },
          h("b", {}, outcome === "failed" ? "Finished with failures. " : "Finished UNVERIFIED. "),
          [failed ? `${failed} failed` : null, drift ? `${drift} drifted` : null, unread ? `${unread} could not be read back` : null, skipped ? `${skipped} skipped` : null].filter(Boolean).join(", "),
          ". These writes are not proven. ",
          job.state === "INCOMPLETE" ? "Resume to re-read them; resuming can only read, never re-send." : ""));
  }'''
replace("forge/src/ui/screens.mjs", old_run, new_run)

replace(
    "forge/src/ui/app.mjs",
    '''      const counts = Object.entries(s.counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ");
      const verify = s.verify ? `${s.verify.match} verified, ${s.verify.drift} drift, ${s.verify.unread} unread` : "";
      const kind = s.outcome === "success" ? "ok" : s.outcome === "failed" ? "bad" : "warn";
      this.toast(`job ${s.state} (${s.outcome}): ${counts}${verify ? " · " + verify : ""}`, kind, 8000);''',
    '''      const job = this.journal.get(jobId);
      const captures = [...(job.capturesBefore || []), ...(job.capturesAfter || [])];
      const detail = job.items.length
        ? `${Object.entries(s.counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")} · ${s.verify.match} verified, ${s.verify.drift} drift, ${s.verify.unread} unread`
        : `${captures.filter((capture) => capture.ok).length}/${captures.length} captures ok · zero mutations`;
      const kind = s.outcome === "success" ? "ok" : s.outcome === "failed" ? "bad" : "warn";
      this.toast(`job ${s.state} (${s.outcome}): ${detail}`, kind, 8000);''')

# Release version metadata.
replace("forge/package.json", '"version": "0.2.0"', '"version": "0.2.1"')
lock = ROOT / "forge/package-lock.json"
lock_text = lock.read_text()
if lock_text.count('"version": "0.1.0"') < 2:
    raise SystemExit("package-lock.json: expected stale root version anchors")
lock.write_text(lock_text.replace('"version": "0.1.0"', '"version": "0.2.1"', 2))
replace("forge/src/main.mjs", 'export const VERSION = "forge 0.2.0";', 'export const VERSION = "forge 0.2.1";')
replace("forge_loader_user.js", '// @version      0.2.0', '// @version      0.2.1')

# Journal regressions.
replace(
    "forge/test/storage.journal.test.mjs",
    'import { Journal, JournalError, KEY_PREFIX, TERMINAL_ITEM_STATES, migrate, JOURNAL_VERSION } from "../src/storage/journal.mjs";',
    'import { Journal, JournalError, KEY_PREFIX, TERMINAL_ITEM_STATES, jobOutcome, migrate, JOURNAL_VERSION } from "../src/storage/journal.mjs";')

journal_anchor = '''test("duplicate jobId refuses", () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  assert.throws(() => j.open({ jobId: "job1", items: specs() }), JournalError);
});'''
journal_test = journal_anchor + '''

test("capture-only journal open is explicit and its outcome follows the capture results", () => {
  const s = new MemoryStorage(); const j = new Journal(s, fakeClock());
  assert.throws(() => j.open({ jobId: "empty", items: [] }), /at least one item/);
  j.open({ jobId: "capture", manifestPath: "push/read.json", items: [], allowEmpty: true });
  j.annotateJob("capture", { capturesAfter: [{ phase: "after", proc: "jutsu.getAllNames", ok: true, rows: 0, error: null }] });
  j.setJobState("capture", "DONE");
  assert.equal(jobOutcome(j.get("capture")), "success");
  j.annotateJob("capture", { capturesAfter: [{ phase: "after", proc: "jutsu.getAllNames", ok: false, rows: 0, error: "NOT_FOUND" }] });
  assert.equal(jobOutcome(j.get("capture")), "failed");
});'''
replace("forge/test/storage.journal.test.mjs", journal_anchor, journal_test)

runner_anchor = '''// ---------------------------------------------------------------- happy paths
test("two-phase create: create -> placeholder -> update -> read-back VERIFIED; exactly one row", async () => {'''
runner_test = '''// ---------------------------------------------------------------- happy paths
test("capture-only manifest runs audited reads with zero mutations", async () => {
  const h = harness();
  const manifest = { items: [], capture: { after: [
    { proc: "jutsu.getAllNames", input: {} },
    { proc: "quests.getAllNames", input: {} },
  ] } };
  h.runner.plan(manifest, { jobId: "capture", manifestPath: "push/00_forge_readonly_smoke.json" });
  const s = await h.runner.run("capture");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success");
  assert.deepEqual(h.game.calls.map((call) => call.path), ["jutsu.getAllNames", "quests.getAllNames"]);
  const job = h.journal.get("capture");
  assert.equal(job.items.length, 0);
  assert.equal(job.capturesAfter.length, 2);
  assert.ok(job.capturesAfter.every((capture) => capture.ok));
});

test("two-phase create: create -> placeholder -> update -> read-back VERIFIED; exactly one row", async () => {'''
replace("forge/test/runner.test.mjs", runner_anchor, runner_test)

ui_anchor = '''test("Manifests: list, select, plan shown, Start job runs to DONE through the runner", async () => {'''
ui_test = '''test("capture-only manifest is presented and completed as read-only", async () => {
  const win = dom();
  const { app, game } = appWith();
  app.github.text = async () => JSON.stringify({ items: [], capture: { after: [{ proc: "jutsu.getAllNames", input: {} }] } });
  app.mount(win.document.body, win.document);
  app.go("manifests");
  await app.loadPicker(true);
  await app.selectManifest(app.state.picker[0]);
  const main = win.document.querySelector(".f-main");
  assert.match(main.textContent, /Read-only capture job/);
  assert.match(main.textContent, /zero mutations/);
  const start = [...main.querySelectorAll("button")].find((button) => button.textContent === "Run captures");
  assert.ok(start && !start.disabled);
  let prompt = "";
  app.confirm = (message, run) => { prompt = message; run(); };
  start.click();
  await new Promise((resolve) => setTimeout(resolve, 20));
  assert.match(prompt, /No mutations will be sent/);
  assert.doesNotMatch(prompt, /writes to the game/i);
  assert.deepEqual(game.calls.map((call) => call.path), ["jutsu.getAllNames"]);
  const job = app.journal.listJobs()[0];
  assert.equal(job.state, "DONE");
  app.go("run", { jobId: job.jobId });
  assert.match(win.document.querySelector(".f-main").textContent, /Read-only capture complete/);
  assert.match(win.document.querySelector(".f-main").textContent, /zero mutations were sent/);
});

test("Manifests: list, select, plan shown, Start job runs to DONE through the runner", async () => {'''
replace("forge/test/ui.test.mjs", ui_anchor, ui_test)

# Keep the implementation notes accurate for the released journal behavior.
notes = ROOT / "docs/BUILDER_APP_NOTES.md"
text = notes.read_text()
marker = "## The readiness pass, and what it changed\n"
if text.count(marker) != 1:
    raise SystemExit("BUILDER_APP_NOTES.md: release-note anchor missing")
text = text.replace(marker, "## 0.2.1 capture-only repair\n\nThe first real Firefox Android smoke exposed one integration seam: `parseManifest()` accepted capture-only manifests, but `Journal.open()` still rejected an empty item list. Forge 0.2.1 permits an empty journal only when `Runner.plan()` has parsed at least one capture, treats the job as successful only when every capture read succeeds, and labels the flow as read-only/zero-mutation in the UI. The smoke manifest is `push/00_forge_readonly_smoke.json`.\n\n" + marker, 1)
text = text.replace("`open()` refuses empty item lists and a\nsecond resumable job", "`open()` refuses empty item lists unless the runner explicitly opens a parsed capture-only job, and refuses a\nsecond resumable job")
notes.write_text(text)

print("capture-only Forge source/test patch applied")
