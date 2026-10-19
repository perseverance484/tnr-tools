// push/122 (2026-10-19): the game's moderation step deleted uploads it could not check, the PUT
// still answered 200 with a ufsUrl, and Forge saved those dead links on whole trees. These pin
// the repair: the verdict decides, a "could not validate" refusal is retried after a pause, a
// recorded link is reused only while it loads, and a preview offers dead images as changes.
import test from "node:test";
import assert from "node:assert/strict";
import { Uploader, UploadError, RETRY_DELAYS_MS, MIN_GAP_MS } from "../src/transport/upload.mjs";
import { browserImageProbe } from "../src/transport/imageprobe.mjs";
import { recordAssetUpload, readAssetUploads, liveAssetUploads } from "../src/storage/assets.mjs";
import { MemoryStorage } from "./shim.mjs";

const file = (name = "icon.webp") => new File([new Uint8Array([82, 73, 70, 70, 1, 2])], name, { type: "image/webp" });

/** A fake game + ingest host. `verdicts` is consumed one per PUT. */
function fakeUpload(verdicts) {
  const calls = [];
  let n = 0;
  const session = { fetch: async (url) => { calls.push(["presign", url]); n++; return new Response(JSON.stringify([{ url: `https://ingest.test/${n}`, key: `k${n}` }]), { status: 200 }); } };
  const fetchImpl = async (url, init) => {
    calls.push([init.method, url]);
    if (init.method === "HEAD") return new Response(null, { status: 200, headers: { "x-ut-range-start": "0" } });
    const serverData = verdicts.shift();
    return new Response(JSON.stringify({ ufsUrl: `https://x.ufs.sh/f/raw${n}`, fileHash: "h", serverData }), { status: 200 });
  };
  const slept = [];
  let now = 0;
  const up = new Uploader({ session, fetchImpl, sleep: async (ms) => { slept.push(ms); now += ms; }, clock: () => now });
  return { up, calls, slept };
}

test("a removed upload is never returned as a URL, and a flagged image is not retried", async () => {
  const { up, calls } = fakeUpload([{ fileUrl: "", error: "Image contains disallowed content" }]);
  await assert.rejects(up.upload(file()), (e) => e instanceof UploadError && e.removed && /disallowed/.test(e.message));
  assert.equal(calls.filter(([m]) => m === "PUT").length, 1);
});

test("a verdict with no fileUrl and no error falls back to ufsUrl", async () => {
  const { up } = fakeUpload([{}]);
  assert.match((await up.upload(file())).url, /raw1$/);
});

test("long waits call onWait at least every 10 s, so the caller's job lease stays fresh", async () => {
  const fail = { fileUrl: "", error: "Unable to validate uploaded image." };
  const { up, slept } = fakeUpload([fail, fail, { fileUrl: "https://x.ufs.sh/f/ok.webp" }]);
  let beats = 0;
  await up.upload(file(), { onWait: () => beats++ });
  assert.ok(slept.every((ms) => ms <= 10_000), JSON.stringify(slept));
  assert.ok(beats >= slept.length);
});

test("a 'could not validate' removal is retried after a pause, and the served URL is kept", async () => {
  const { up, slept } = fakeUpload([
    { fileUrl: "", error: "Unable to validate uploaded image. Please try another image." },
    { fileUrl: "https://x.ufs.sh/f/abc.webp" },
  ]);
  const r = await up.upload(file());
  assert.equal(r.url, "https://x.ufs.sh/f/abc.webp", "the game's served URL, not the bare ufsUrl");
  assert.ok(slept.includes(RETRY_DELAYS_MS[0]));
});

test("retries stop after the last pause and the refusal is reported", async () => {
  const fail = { fileUrl: "", error: "Unable to validate uploaded image." };
  const { up } = fakeUpload(Array(RETRY_DELAYS_MS.length + 1).fill(fail));
  await assert.rejects(up.upload(file()), /Unable to validate/);
});

test("uploads back to back are spaced out", async () => {
  const { up, slept } = fakeUpload([{ fileUrl: "https://x.ufs.sh/f/a.webp" }, { fileUrl: "https://x.ufs.sh/f/b.webp" }]);
  await up.upload(file("a.webp")); await up.upload(file("b.webp"));
  assert.deepEqual(slept, [MIN_GAP_MS], "the second upload waited the full gap (the fake clock does not advance on its own)");
});

test("a response without a verdict still works (older ingest), using ufsUrl", async () => {
  const { up } = fakeUpload([undefined]);
  assert.match((await up.upload(file())).url, /raw1$/);
});

test("recorded uploads whose links no longer load are forgotten; undecided ones are kept", async () => {
  const storage = new MemoryStorage();
  recordAssetUpload(storage, "a".repeat(64), "https://x/dead.webp");
  recordAssetUpload(storage, "b".repeat(64), "https://x/live.webp");
  recordAssetUpload(storage, "c".repeat(64), "https://x/slow.webp");
  const probe = async (url) => (url.includes("dead") ? false : url.includes("slow") ? null : true);
  const preview = await liveAssetUploads(storage, probe);
  assert.deepEqual(Object.keys(preview).sort(), ["b".repeat(64), "c".repeat(64)]);
  assert.ok("a".repeat(64) in readAssetUploads(storage), "a preview leaves storage alone");
  await liveAssetUploads(storage, probe, null, { forget: true });
  assert.ok(!("a".repeat(64) in readAssetUploads(storage)), "forget removes the dead record");
  assert.equal(Object.keys(await liveAssetUploads(new MemoryStorage(), null)).length, 0);
});

/** A fake window whose images load or fail per URL, with an instant timer. */
function fakeWin(behaviour, { onLine = true } = {}) {
  const loads = [];
  class Image {
    set src(v) { loads.push(v); const r = behaviour(v); queueMicrotask(() => r === "load" ? (this.naturalWidth = 1, this.onload?.()) : r === "error" ? this.onerror?.() : null); }
  }
  return { Image, loads, navigator: { onLine }, setTimeout: (fn, ms) => (ms >= 15000 ? 0 : (queueMicrotask(fn), 0)), clearTimeout: () => {} };
}

test("the browser probe confirms a failure with a second, cache-busted load", async () => {
  const win = fakeWin((src) => (src.includes("forge-probe") ? "load" : "error"));
  assert.equal(await browserImageProbe(win)("https://x/a.webp"), true, "a blip that recovers is not dead");
  const dead = fakeWin(() => "error");
  assert.equal(await browserImageProbe(dead)("https://x/b.webp"), false);
  assert.equal(dead.loads.length, 2);
});

test("the browser probe answers null when offline, and refuses non-https input", async () => {
  const win = fakeWin(() => "error", { onLine: false });
  const probe = browserImageProbe(win);
  assert.equal(await probe("https://x/a.webp"), null);
  assert.equal(win.loads.length, 0);
  assert.equal(await probe("http://x/a.webp"), false);
});
