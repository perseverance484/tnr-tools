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

export class Uploader {
  /**
   * @param {object} o
   * @param {import("./session.mjs").Session} o.session  same-origin, for the presign call
   * @param {(url: string, init: object) => Promise<Response>} o.fetchImpl  plain fetch for the ingest host
   * @param {string} [o.slug="imageUploader"]
   */
  constructor({ session, fetchImpl, slug = "imageUploader" }) {
    if (!SLUGS[slug]) throw new UploadError("unknown slug " + slug);
    this.session = session; this.fetchImpl = fetchImpl; this.slug = slug;
  }

  ceiling() { return SLUGS[this.slug].maxBytes; }

  /** @param {File|Blob & {name?: string, lastModified?: number}} file  @returns {Promise<{ufsUrl: string, key: string}>} */
  async upload(file) {
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
    return { ufsUrl: done.ufsUrl, key: p.key, fileHash: done.fileHash ?? null };
  }
}
