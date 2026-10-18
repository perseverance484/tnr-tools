// Offline check of a Bloodright collection package for repository Python tools (validate.py).
// Runs Forge's own prepareCollection, so preview and this check cannot disagree on anything
// that does not depend on live data. Designs are read from this checkout with `git show
// <ref>:<path>`; no network. The live inventory is replaced by hidden stand-ins for the probe
// and every bound record, so live-only facts (bindings exist and are hidden, no global name
// collision, folder name free) are NOT checked here: Forge proves them at preview.
// Usage: node tools/validate_bloodright_package.mjs REPO_ROOT < package.json  ->  JSON problem list
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { prepareCollection } from "../src/bloodright/collection.mjs";
import { bloodrightProblems } from "../src/bloodright/validate.mjs";

function memoryStorage() {
  const m = new Map();
  return { getItem: k => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)), removeItem: k => m.delete(k) };
}

export async function packageProblems(pkg, root) {
  const c = pkg?.bloodrightCollection;
  if (!c || !Array.isArray(c.trees)) return ["not a bloodrightCollection package"];
  const text = (path, ref) => execFileSync("git", ["-C", root, "show", `${ref}:${path}`], { encoding: "utf8" });
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
  try {
    return (await prepareCollection(ctx, pkg)).problems;
  } catch (e) { return [e.message]; }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const root = process.argv[2];
  let out;
  try { out = root ? await packageProblems(JSON.parse(readFileSync(0, "utf8")), root) : ["usage: validate_bloodright_package.mjs REPO_ROOT < package.json"]; }
  catch (e) { out = [e.message]; }
  process.stdout.write(JSON.stringify(out));
}
