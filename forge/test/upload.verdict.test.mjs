// push/122 (2026-10-19): the game's moderation step deleted uploads it could not check, the PUT
// still answered 200 with a ufsUrl, and Forge saved those dead links on whole trees. These pin
// the repair: the verdict decides, a "could not validate" refusal is retried after a pause, a
// recorded link is reused only while it loads, and a preview offers dead images as changes.
import test from "node:test";
import assert from "node:assert/strict";
import { Uploader, UploadError, RETRY_DELAYS_MS } from "../src/transport/upload.mjs";
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

test("a removed upload is never returned as a URL", async () => {
  const { up } = fakeUpload([{ fileUrl: "", error: "Image contains disallowed content" }]);
  await assert.rejects(up.upload(file()), (e) => e instanceof UploadError && e.removed && /disallowed/.test(e.message));
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
  assert.ok(slept.length >= 1 && slept[0] > 0, "the second upload waited");
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
  const live = await liveAssetUploads(storage, probe);
  assert.deepEqual(Object.keys(live).sort(), ["b".repeat(64), "c".repeat(64)]);
  assert.ok(!("a".repeat(64) in readAssetUploads(storage)), "the dead record is gone from storage too");
  assert.equal(Object.keys(await liveAssetUploads(new MemoryStorage(), null)).length, 0);
});
