// Asset upload, derived from uploadthing 7.7.4 (the version the game pins) by reading the
// package's client (client/index.js uploadFilesInternal, uploadFile, uploadWithProgress) and
// its shared schemas, not from builder_bundle.js.
//
//   1. presign  POST {origin}/api/uploadthing?actionType=upload&slug=<slug>
//               headers content-type: application/json, x-uploadthing-version: 7.7.4
//               body {files: [{name, size, type, lastModified}], input: null}
//               -> [ {url, key, name, customId?} ]   (one per file)
//      Same-origin, through the Session: the game's route handler runs the slug's middleware.
//   2. HEAD presigned.url  -> x-ut-range-start (resume offset; 0 for a fresh upload)
//   3. PUT  presigned.url  FormData "file", header x-uploadthing-version
//               -> {url, appUrl, ufsUrl, fileHash, serverData}
//      Cross-origin to the ingest host; no credentials. The stored URL is ufsUrl (url and
//      appUrl are deprecated in the package).
//
// Ceilings are per slug and are enforced server-side in app/src/app/api/uploadthing/core.ts
// (R8: carried as data, never as one constant). onUploadComplete runs moderateUploadedImage,
// so an upload is not final at the moment the PUT returns.
//
// THE VERDICT. moderateUploadedImage DELETES the file when the image is flagged, and also when the
// moderation call itself fails (a rate limit, a timeout), then answers serverData
// {fileUrl: "", error}. The PUT still returns 200 with a ufsUrl, which then points at nothing:
// push/122 (2026-10-19) saved dead image links on whole trees this way. So the serverData verdict
// decides success, a "could not validate" refusal is retried after a pause, and the URL kept is
// the one the game serves (serverData.fileUrl), never the bare ufsUrl when a verdict exists.

export const UT_VERSION = "7.7.4";
export const SLUGS = Object.freeze({
  imageUploader: { mime: "image", maxBytes: 512 * 1024 },            // core.ts:89
  conceptArtFrameUploader: { mime: "image", maxBytes: 256 * 1024 },  // core.ts:95
  modelUploader: { mime: "model/gltf-binary", maxBytes: 256 * 1024 },
  tavernUploader: { mime: "image", maxBytes: 64 * 1024 },
});

export class UploadError extends Error {
  constructor(message, info = {}) { super(message); this.name = "UploadError"; Object.assign(this, info); }
}

// A moderation call that failed (as opposed to an image it flagged) is worth retrying after a pause.
const TRANSIENT = /unable to validate/i;
export const RETRY_DELAYS_MS = Object.freeze([10_000, 30_000, 60_000]);
// Uploads back to back are what tripped moderation; keep a gap between them.
export const MIN_GAP_MS = 3_000;
const realSleep = (ms) => new Promise((r) => setTimeout(r, ms));

export class Uploader {
  /**
   * @param {object} o
   * @param {import("./session.mjs").Session} o.session  same-origin, for the presign call
   * @param {(url: string, init: object) => Promise<Response>} o.fetchImpl  plain fetch for the ingest host
   * @param {string} [o.slug="imageUploader"]
   */
  constructor({ session, fetchImpl, slug = "imageUploader", sleep = realSleep, clock = () => Date.now(), retryDelays = RETRY_DELAYS_MS, minGapMs = MIN_GAP_MS }) {
    if (!SLUGS[slug]) throw new UploadError("unknown slug " + slug);
    this.session = session; this.fetchImpl = fetchImpl; this.slug = slug;
    this.sleep = sleep; this.clock = clock; this.retryDelays = retryDelays; this.minGapMs = minGapMs;
    this._last = null;
  }

  ceiling() { return SLUGS[this.slug].maxBytes; }

  /**
   * Upload, honouring the game's verdict: retried after a pause when the game could not check the
   * image, refused when it removed it. @returns {Promise<{url: string, ufsUrl: string, key: string}>}
   */
  async upload(file) {
    for (let attempt = 0; ; attempt++) {
      if (this._last != null) {
        const wait = this._last + this.minGapMs - this.clock();
        if (wait > 0) await this.sleep(wait);
      }
      try { return await this._once(file); }
      catch (e) {
        if (!(e instanceof UploadError && e.removed && TRANSIENT.test(e.reason ?? "")) || attempt >= this.retryDelays.length) throw e;
        await this.sleep(this.retryDelays[attempt]);
      }
      finally { this._last = this.clock(); }
    }
  }

  /** @param {File|Blob & {name?: string, lastModified?: number}} file */
  async _once(file) {
    const max = this.ceiling();
    if (file.size > max) throw new UploadError(`${file.name ?? "file"} is ${file.size} bytes; ${this.slug} ceiling is ${max}`, { size: file.size, max });
    const meta = { name: file.name ?? "upload", size: file.size, type: file.type || "application/octet-stream", lastModified: file.lastModified ?? 0 };
    const pres = await this.session.fetch(`/api/uploadthing?actionType=upload&slug=${encodeURIComponent(this.slug)}`, {
      method: "POST",
      headers: { "content-type": "application/json", "x-uploadthing-version": UT_VERSION },
      body: JSON.stringify({ files: [meta], input: null }),
    });
    const presText = await pres.text();
    if (!pres.ok) throw new UploadError(`presign ${pres.status}: ${presText.slice(0, 160)}`, { status: pres.status });
    let presigneds;
    try { presigneds = JSON.parse(presText); } catch { throw new UploadError("presign response is not JSON"); }
    const p = Array.isArray(presigneds) ? presigneds[0] : null;
    if (!p || !p.url || !p.key) throw new UploadError("presign response missing url/key", { body: presText.slice(0, 160) });

    let start = 0;
    try {
      const head = await this.fetchImpl(p.url, { method: "HEAD" });
      start = parseInt(head.headers.get("x-ut-range-start") ?? "0", 10) || 0;
    } catch { start = 0; }

    const fd = new FormData();
    fd.append("file", start > 0 ? file.slice(start) : file, meta.name);
    const put = await this.fetchImpl(p.url, { method: "PUT", headers: { "x-uploadthing-version": UT_VERSION }, body: fd });
    const putText = await put.text();
    if (!put.ok) throw new UploadError(`upload PUT ${put.status}: ${putText.slice(0, 160)}`, { status: put.status });
    let done;
    try { done = JSON.parse(putText); } catch { throw new UploadError("upload response is not JSON"); }
    if (!done || typeof done.ufsUrl !== "string") throw new UploadError("upload response missing ufsUrl", { body: putText.slice(0, 160) });
    const verdict = done.serverData && typeof done.serverData === "object" ? done.serverData : null;
    if (verdict && (verdict.error || verdict.fileUrl === "")) {
      const reason = String(verdict.error || "the game removed the upload");
      throw new UploadError(`the game removed ${meta.name} after upload: ${reason}`, { removed: true, reason });
    }
    const url = verdict && typeof verdict.fileUrl === "string" && /^https:\/\//.test(verdict.fileUrl) ? verdict.fileUrl : done.ufsUrl;
    return { url, ufsUrl: done.ufsUrl, key: p.key, fileHash: done.fileHash ?? null };
  }
}
