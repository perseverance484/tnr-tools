import test from "node:test";
import assert from "node:assert/strict";
import { JSDOM, VirtualConsole } from "jsdom";
import { build } from "esbuild";
import { webcrypto } from "node:crypto";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { registry, origin } from "./helpers.mjs";
import { restoreDraft, saveDraft } from "../src/drafts.mjs";
const output = await build({
  entryPoints: ["src/App.jsx"],
  bundle: true,
  format: "iife",
  outfile: "test-output/editor.js",
  write: false,
  define: { "process.env.NODE_ENV": '"production"' },
});
const js = output.outputFiles.find((f) => f.path.endsWith(".js")).text,
  css = output.outputFiles.find((f) => f.path.endsWith(".css")).text;
function mount(path = "/", saved = {}, handler) {
  const errors = [],
    requests = [],
    assetRequests = [],
    virtualConsole = new VirtualConsole();
  virtualConsole.on("jsdomError", (e) => errors.push(e.message));
  const dom = new JSDOM(
    '<!doctype html><html><head></head><body><div id="root"></div></body></html>',
    {
      url: origin + path,
      runScripts: "outside-only",
      pretendToBeVisual: true,
      virtualConsole,
    },
  );
  const w = dom.window;
  w.STUDIO_CONFIG = { localHarness: true };
  w.TextEncoder = TextEncoder;
  w.TextDecoder = TextDecoder;
  Object.defineProperty(w, "crypto", { value: webcrypto });
  w.scrollTo = () => {};
  w.HTMLDialogElement.prototype.showModal = function () {
    this.open = true;
  };
  w.HTMLDialogElement.prototype.close = function () {
    this.open = false;
  };
  w.fetch = async (url, opts) => {
    if (url.startsWith("/assets/")) {
      assert.match(url, /^\/assets\/[a-f0-9]{24}\.webp$/);
      assert.equal(opts.credentials, "omit");
      assert.equal(opts.redirect, "error");
      assetRequests.push(url);
      return new Response(await readFile("public" + url));
    }
    if (handler) return handler(url, opts);
    requests.push({ url, body: JSON.parse(opts.body) });
    return Response.json(
      {
        id: "a2345678-1234-1234-1234-123456789abc",
        token: "mock-receipt",
        status: "Submitted",
      },
      { status: 201 },
    );
  };
  for (const [key, value] of Object.entries(saved))
    w.localStorage.setItem(key, value);
  w.eval(js);
  return { dom, w, errors, requests, assetRequests, doc: w.document };
}
async function flush() {
  await new Promise((resolve) => setTimeout(resolve, 10));
  for (let i = 0; i < 12; i++)
    await new Promise((resolve) => setImmediate(resolve));
}
async function click(el) {
  assert.ok(el, "control exists");
  el.click();
  await flush();
}
async function fill(el, value, w) {
  assert.ok(el);
  Object.getOwnPropertyDescriptor(
    el.tagName === "TEXTAREA"
      ? w.HTMLTextAreaElement.prototype
      : w.HTMLInputElement.prototype,
    "value",
  ).set.call(el, value);
  el.dispatchEvent(new w.Event("input", { bubbles: true }));
  await flush();
}
const button = (doc, text) =>
  [...doc.querySelectorAll("button")].find((b) => b.textContent.includes(text));
test("real editor DOM: create, select, inline notes, order, autosave/recovery, chapters, preview and submit with zero TNR calls", async () => {
  let h = mount();
  await flush();
  assert.equal(h.doc.querySelectorAll(".template-tile").length, 2);
  assert.equal(
    h.assetRequests.length,
    0,
    "no embedded-card fetch at first paint",
  );
  await click(button(h.doc, "Create guide"));
  await fill(
    h.doc.querySelector('input[placeholder="Your player name"]'),
    "Mobile fixture author",
    h.w,
  );
  await click(button(h.doc, "Shape my build"));
  await click(button(h.doc, "Add jutsu"));
  let row = [...h.doc.querySelectorAll(".picker-row")].find((r) =>
    r.textContent.includes("Atomic Shield"),
  );
  await click(button(row, "Add"));
  row = [...h.doc.querySelectorAll(".picker-row")].find((r) =>
    r.textContent.includes("Kinjutsu: Black Thorn Rose"),
  );
  await click(button(row, "Add"));
  await click(button(h.doc, "Write my notes"));
  await fill(
    h.doc.querySelectorAll(".tactical-note textarea")[0],
    "I establish reflect before the exchange. ",
    h.w,
  );
  await fill(
    h.doc.querySelectorAll(".tactical-note textarea")[0],
    "I establish reflect before the exchange. Then I watch the reply.",
    h.w,
  );
  await fill(
    h.doc.querySelectorAll(".tactical-note textarea")[1],
    "I reduce incoming damage and enemy healing.",
    h.w,
  );
  await click(
    h.doc.querySelector(
      'button[aria-label="Move Kinjutsu: Black Thorn Rose up"]',
    ),
  );
  const saved = Object.fromEntries(
    Object.keys(h.w.localStorage).map((k) => [k, h.w.localStorage.getItem(k)]),
  );
  assert.equal(h.requests.length, 0);
  h.w.close();
  h = mount("/", saved);
  await flush();
  for (let i = 0; i < 100 && !button(h.doc, "Continue my guide"); i++)
    await flush();
  await click(button(h.doc, "Continue my guide"));
  await click(button(h.doc, "Your build"));
  assert.equal(
    h.doc.querySelector(".loadout-entry h2").textContent,
    "Kinjutsu: Black Thorn Rose",
  );
  assert.equal(
    h.doc.querySelector(".tactical-note textarea").value,
    "I reduce incoming damage and enemy healing.",
  );
  await click(button(h.doc, "Write the game plan"));
  await fill(
    h.doc.querySelector("#chapter-text"),
    "My build wins through efficient exchanges.",
    h.w,
  );
  await click(button(h.doc, "Pressure, Then Cash Out"));
  await fill(
    h.doc.querySelector("#chapter-text"),
    "Set up, watch the reply, and commit when the opening is real.",
    h.w,
  );
  await click(button(h.doc, "Adaptation & Matchups"));
  await fill(
    h.doc.querySelector("#chapter-text"),
    "Against burst I preserve recovery; against sustain I pressure healing.",
    h.w,
  );
  await click(button(h.doc, "Preview guide"));
  assert.ok(h.doc.querySelector(".preview-dialog[open]"));
  for (
    let i = 0;
    i < 80 && !h.doc.querySelector(".preview-dialog iframe").srcdoc;
    i++
  )
    await flush();
  const preview = h.doc.querySelector(".preview-dialog iframe").srcdoc;
  assert.ok(preview.includes("I reduce incoming damage and enemy healing."));
  assert.ok(preview.includes("bloodline-kit"));
  assert.ok(
    h.assetRequests.length > 0,
    "preview loads same-origin verified art",
  );
  assert.equal(h.requests.length, 0);
  await click(
    h.doc.querySelector('[aria-label="Close preview and return to editor"]'),
  );
  await click(button(h.doc, "Give it a final read"));
  const send = button(h.doc, "Submit");
  assert.ok(send && !send.disabled);
  await click(send);
  for (let i = 0; i < 100 && !h.doc.querySelector(".receipt"); i++)
    await flush();
  assert.equal(h.requests.length, 1);
  assert.equal(h.requests[0].url, "/api/submissions");
  assert.equal(
    h.requests[0].body.draft.loadout[0].howIUseIt,
    "I reduce incoming damage and enemy healing.",
  );
  assert.ok(
    h.doc.body.textContent.includes("Your perspective"),
    h.doc.body.textContent.slice(-1600),
  );
  assert.deepEqual(h.errors, []);
  h.w.close();
});
test("draft quota and corrupt/stale recovery never silently destroy saved work", () => {
  const map = new Map(),
    storage = {
      getItem: (k) => map.get(k) || null,
      setItem: (k, v) => map.set(k, v),
    };
  storage.setItem("tnr-guide-studio:drafts:v2", "not JSON");
  const recovered = restoreDraft(storage, "aerathiel", registry);
  assert.ok(recovered.error);
  assert.equal(recovered.raw, "not JSON");
  assert.throws(() => saveDraft(storage, { template: { slug: "aerathiel" } }));
  assert.equal(storage.getItem("tnr-guide-studio:drafts:v2"), "not JSON");
});
test("public authoring dependency graph cannot contain importer, credential adapter, or live refresh", () => {
  assert.ok(!js.includes("/api/trpc"));
  assert.ok(!js.includes("APPROVAL_PRIVATE_JWK"));
  assert.ok(!js.includes("Cf-Access-Jwt-Assertion"));
  assert.ok(!js.includes("guide.create"));
  assert.ok(!js.includes('credentials:"include"'));
});

test("actual staff UI opens final artifact, begins review, and freezes approval", async () => {
  const { createService } = await import("../server/service.mjs"),
    { MemoryStore, MemoryBucket } = await import("../server/store.mjs"),
    { aerathiel } = await import("./helpers.mjs");
  const store = new MemoryStore(),
    bucket = new MemoryBucket(),
    service = createService({
      store,
      bucket,
      registry,
      origin,
      authenticate: async () => ({ id: "mock-reviewer" }),
      verifyTurnstile: async () => {},
      signApproval: async () => "mock-signature-never-used-for-import",
    });
  const posted = await service(
    new Request(origin + "/api/submissions", {
      method: "POST",
      headers: { Origin: origin, "Content-Type": "application/json" },
      body: JSON.stringify({ draft: aerathiel, turnstileToken: "mock" }),
    }),
  );
  assert.equal(posted.status, 201);
  const h = mount("/staff", {}, (url, opts = {}) =>
    service(
      new Request(origin + url, {
        ...opts,
        headers: { Origin: origin, ...opts.headers },
      }),
    ),
  );
  await flush();
  for (let i = 0; i < 60 && !h.doc.querySelector(".queue-row"); i++)
    await flush();
  await click(h.doc.querySelector(".queue-row"));
  for (let i = 0; i < 100 && !h.doc.querySelector(".review-render iframe"); i++)
    await flush();
  assert.ok(
    h.doc
      .querySelector(".review-render iframe")
      .srcdoc.includes("HOW I USE IT"),
  );
  await click(button(h.doc, "Begin review"));
  for (let i = 0; i < 60 && !button(h.doc, "Approve & freeze"); i++)
    await flush();
  await click(button(h.doc, "Approve & freeze"));
  for (let i = 0; i < 100 && !h.doc.querySelector(".approval-status"); i++)
    await flush();
  assert.ok(h.doc.querySelector(".approval-status"));
  assert.ok(button(h.doc, "Download game-ready package"));
  assert.deepEqual(h.errors, []);
  h.w.close();
});
