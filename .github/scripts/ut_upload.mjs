// Upload the files in state/moe_upload/upload_list.json to the director's own UploadThing app
// (token in the UPLOADTHING_TOKEN repo secret; never printed). Resumable: entries already in
// state/moe_upload/uploaded.json are skipped. Each file is re-hashed before upload.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { UTApi, UTFile } from "uploadthing/server";

const LIST = "state/moe_upload/upload_list.json";
const OUT = "state/moe_upload/uploaded.json";
if (!process.env.UPLOADTHING_TOKEN) { console.error("UPLOADTHING_TOKEN secret is not set"); process.exit(2); }
const utapi = new UTApi({ token: process.env.UPLOADTHING_TOKEN });
const list = JSON.parse(readFileSync(LIST, "utf8")).files;
const done = existsSync(OUT) ? JSON.parse(readFileSync(OUT, "utf8")) : { files: {} };
const todo = list.filter((f) => !done.files[f.srcId]);
console.log(`${list.length} listed, ${list.length - todo.length} already uploaded, ${todo.length} to go`);
const save = () => writeFileSync(OUT, JSON.stringify(done, null, 1) + "\n");
let failed = 0;
for (let i = 0; i < todo.length; i += 10) {
  const batch = todo.slice(i, i + 10);
  const files = batch.map((f) => {
    const buf = readFileSync(f.path);
    const sha = createHash("sha256").update(buf).digest("hex");
    if (sha !== f.sha256) throw new Error(`hash mismatch ${f.path}`);
    return new UTFile([buf], f.file, { type: "image/webp" });
  });
  const res = await utapi.uploadFiles(files);
  res.forEach((r, j) => {
    const f = batch[j];
    if (r.error || !r.data) { failed++; console.error(`FAIL ${f.file}: ${r.error?.message ?? "no data"}`); return; }
    done.files[f.srcId] = { file: f.file, sha256: f.sha256, key: r.data.key, url: r.data.ufsUrl ?? r.data.url };
  });
  save();
  console.log(`uploaded ${Math.min(i + 10, todo.length)}/${todo.length}`);
}
done.at = new Date().toISOString();
save();
console.log(`done: ${Object.keys(done.files).length}/${list.length}, failed ${failed}`);
process.exit(failed ? 1 : 0);
