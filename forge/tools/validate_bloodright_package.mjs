// Offline check of a Bloodright collection package for repository Python tools (validate.py).
// Runs Forge's own prepareCollection, so preview and this check cannot disagree on anything
// that does not depend on live data. Designs are read from this checkout with `git show
// <ref>:<path>`; no network. The live inventory is replaced by hidden stand-ins for the probe
// and every bound record, so live-only facts (bindings exist and are hidden, no global name
// collision, folder name free) are NOT checked here: Forge proves them at preview.
// Image-pack blobs ARE checked here: each exists at the pack ref, its SHA-256 and byte count
// match, it is within Forge's upload ceiling, and the ref is on a pushed (remote) branch.
// Usage: node tools/validate_bloodright_package.mjs REPO_ROOT < package.json  ->  JSON problem list
import { readFileSync, realpathSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { pathToFileURL } from "node:url";
import { prepareCollection } from "../src/bloodright/collection.mjs";
import { bloodrightProblems } from "../src/bloodright/validate.mjs";
import { SLUGS } from "../src/transport/upload.mjs";

const COMMIT = /^[a-f0-9]{40}$/;
const UPLOAD_CEILING = SLUGS.imageUploader.maxBytes;

function memoryStorage() {
  const m = new Map();
  return { getItem: k => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)), removeItem: k => m.delete(k) };
}

// Only ever hand git an exact commit and a plain repository path, never an option.
function gitShow(root, ref, path, encoding) {
  if (!COMMIT.test(ref ?? "") || typeof path !== "string" || !path || path.startsWith("-") || path.includes("..")) throw new Error(`refusing git read of ${ref}:${path}`);
  try { return execFileSync("git", ["-C", root, "show", "--end-of-options", `${ref}:${path}`], { encoding, stdio: ["ignore", "pipe", "pipe"], maxBuffer: 64 * 1024 * 1024 }); }
  catch {
    let known = false;
    try { execFileSync("git", ["-C", root, "cat-file", "-e", `${ref}^{commit}`], { stdio: "ignore" }); known = true; } catch { /* commit absent */ }
    throw new Error(known ? `${path} does not exist at ${ref.slice(0, 7)}` : `${path}: commit ${ref.slice(0, 7)} is not in this checkout; fetch it first`);
  }
}

/** Offline checks of the pack's repository blobs; Forge repeats them against GitHub at preview. */
export function packBlobProblems(pack, root) {
  if (!pack) return [];
  const out = [];
  if (!COMMIT.test(pack.ref ?? "")) return [`imagePack ref must be a 40-hex commit, got ${pack.ref}`];
  let pushed = "";
  try { pushed = execFileSync("git", ["-C", root, "branch", "-r", "--contains", pack.ref], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }).trim(); } catch { /* unknown commit: reported per file below */ }
  // Approximation of "GitHub serves it": a remote-tracking branch contains the commit.
  if (!pushed) out.push(`imagePack ref ${pack.ref.slice(0, 7)} is not on any pushed branch; Forge fetches icons from GitHub`);
  for (const [name, f] of Object.entries(pack.files ?? {})) {
    let bytes;
    try { bytes = gitShow(root, pack.ref, f?.path); } catch (e) { out.push(`icon ${name}: ${e.message}`); continue; }
    const digest = createHash("sha256").update(bytes).digest("hex");
    if (digest !== f.sha256) out.push(`icon ${name}: sha256 ${digest.slice(0, 12)} does not match the pack's ${String(f.sha256).slice(0, 12)}`);
    if (bytes.length !== f.bytes) out.push(`icon ${name}: ${bytes.length} bytes, pack says ${f.bytes}`);
    if (bytes.length > UPLOAD_CEILING) out.push(`icon ${name}: ${bytes.length} bytes exceeds the ${UPLOAD_CEILING}-byte upload ceiling`);
  }
  return out;
}

export async function packageProblems(pkg, root, { blobs = true } = {}) {
  const c = pkg?.bloodrightCollection;
  if (!c || !Array.isArray(c.trees)) return ["not a bloodrightCollection package"];
  const text = (path, ref) => gitShow(root, ref, path, "utf8");
  // Stand-in inventory: only what the package itself binds.
  const skills = new Map(), folders = new Map();
  for (const t of c.trees) {
    let design;
    try { design = JSON.parse(text(t.source?.path, t.source?.ref)); } catch { continue; } // prepareCollection reports it
    const bl = design?.bloodline?.id;
    if (typeof t.hiddenProbeId === "string") skills.set(t.hiddenProbeId, skills.get(t.hiddenProbeId) ?? { id: t.hiddenProbeId, name: `probe ${t.hiddenProbeId}`, pathType: "BLOODRIGHT", bloodlineId: "probe", hidden: true });
    for (const [node, id] of Object.entries(t.bindings?.nodes ?? {})) {
      const n = design?.nodes?.find(x => x.id === node);
      skills.set(id, { id, name: n?.name ?? node, image: "https://offline.invalid/bound.webp", description: "", target: "SELF", tier: n?.tier ?? 1, requiredSkillIds: [], costSkillPoints: 1, pathType: "BLOODRIGHT", bloodlineId: bl, seichiSilverCost: 0, hidden: true, skillType: "DEFAULT", folderId: t.bindings?.folderId ?? null, effects: [] });
    }
    if (t.bindings?.folderId) folders.set(t.bindings.folderId, { id: t.bindings.folderId, name: `bound folder ${t.bindings.folderId}`, image: "", description: "", order: 0, hidden: false });
  }
  const page = data => ({ ok: true, data: structuredClone(data) });
  const reader = {
    get: async (_path, id) => page(skills.get(id) ?? null),
    list: async path => page(path === "skillTree.getAllFolders" ? [...folders.values()] : [...skills.values()]),
  };
  const ctx = { github: { text }, reader, storage: memoryStorage(), auth: { assert() {} }, journal: { listJobs: () => [] },
    validator: { problems: (entity, data, live) => bloodrightProblems(entity, data, live) } };
  let problems;
  try { problems = (await prepareCollection(ctx, pkg)).problems; } catch (e) { problems = [e.message]; }
  return blobs ? [...problems, ...packBlobProblems(pkg.imagePack, root)] : problems;
}

const entry = (() => { try { return pathToFileURL(realpathSync(process.argv[1])).href; } catch { return null; } })();
if (import.meta.url === entry) {
  const root = process.argv[2];
  let out;
  try { out = root ? await packageProblems(JSON.parse(readFileSync(0, "utf8")), root) : ["usage: validate_bloodright_package.mjs REPO_ROOT < package.json"]; }
  catch (e) { out = [e.message]; }
  process.stdout.write(JSON.stringify(out));
}
