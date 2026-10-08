import { CONTRACT, bloodrightProblems, writableSnapshot } from "./validate.mjs";
import { diffAsserted } from "../runner/validate.mjs";
import { readIdmap } from "../storage/compat.mjs";

export const scopeKey = (bloodlineId, nodeId) => `br:${bloodlineId}:${nodeId}`;
const object = v => !!v && typeof v === "object" && !Array.isArray(v);
const id = v => typeof v === "string" && /^[A-Za-z0-9_-]+$/.test(v);
const sameName = (a, b) => a.normalize("NFKC").trim().toLowerCase() === b.normalize("NFKC").trim().toLowerCase();

/** Pure, deterministic compiler. Inventory must be freshly collected by prepareBloodright. */
export function compileBloodright({ design, config, skills, folders, idmap = {} }) {
  const problems = [], preview = [], items = [];
  const fail = text => problems.push(text);
  const bl = design?.bloodline?.id;
  if (!id(bl)) fail("design requires a literal bloodline ID");
  if (!/^[a-f0-9]{40}$/.test(config?.source?.ref ?? "") || !config?.source?.path) fail("source must name a repository path at an exact 40-character commit");
  const nodes = design?.nodes;
  if (!Array.isArray(nodes) || !nodes.length || nodes.length > 24) return { problems: [...problems, "design needs 1..24 structural nodes"], preview, manifest: null };
  const rules = design.build_rules;
  if (rules?.max_bp !== 5 || rules?.skill_cost !== 1 || rules?.prerequisites !== "ALL") fail("this importer requires the approved five-BP, one-point, ALL-prerequisites design format");
  const elements = design.classification?.qualifying_elements;
  if (!Array.isArray(elements) || !elements.length || elements.some(v => !CONTRACT.elements.includes(v))) fail("design qualifying elements are unresolved or unsupported");
  const byId = new Map(), names = new Set();
  for (const n of nodes) {
    if (!id(n.id) || n.id === "folder" || byId.has(n.id)) fail(`invalid or duplicate node ID: ${n.id}`);
    byId.set(n.id, n);
    if (typeof n.name !== "string" || !n.name.trim()) fail(`${n.id}: name required`);
    else { const name = n.name.normalize("NFKC").trim().toLowerCase(); if (names.has(name)) fail(`duplicate design name: ${n.name}`); names.add(name); }
    if (n.cost !== 1 || n.parent_rule !== "ALL" || !Array.isArray(n.parents)) fail(`${n.id}: one point and ALL parents required`);
    if (!Number.isInteger(n.tier) || n.tier < 1 || n.tier > 10) fail(`${n.id}: tier must be 1..10`);
    if (!object(n.bonuses) || !Object.keys(n.bonuses).length) fail(`${n.id}: structural bonuses required; legacy modifiers are not implicitly converted`);
    for (const [tag, power] of Object.entries(n.bonuses ?? {})) if (!CONTRACT.tags.includes(tag) || !Number.isFinite(power) || power === 0) fail(`${n.id}: unsupported bonus ${tag}=${power}`);
  }
  for (const n of nodes) for (const p of n.parents ?? []) {
    if (!byId.has(p) || byId.get(p).tier >= n.tier) fail(`${n.id}: prerequisite ${p} must exist at a lower tier (cycles refused)`);
  }
  if (problems.length) return { problems, preview, manifest: null };
  // Small five-point allocation search, not 2^N: only legal parent-first selections survive.
  const ordered = [...nodes].sort((a, b) => a.tier - b.tier || a.id.localeCompare(b.id));
  let allocations = 0, advanced = 0;
  function visit(i, chosen, adv) {
    if (i === ordered.length) { allocations++; advanced = Math.max(advanced, adv); return; }
    visit(i + 1, chosen, adv);
    const n = ordered[i];
    if (chosen.size < 5 && n.parents.every(p => chosen.has(p))) { chosen.add(n.id); visit(i + 1, chosen, adv + (n.category === "Advanced Art" ? 1 : 0)); chosen.delete(n.id); }
  }
  visit(0, new Set(), 0);
  if (Number.isInteger(rules.max_advanced_reachable) && advanced !== rules.max_advanced_reachable) fail(`design reachable Advanced Art count is ${advanced}, expected ${rules.max_advanced_reachable}`);
  if (Number.isInteger(rules.max_advanced) && advanced > rules.max_advanced) fail("design exceeds its Advanced Art limit");
  const bindings = config.bindings ?? {};
  for (const key of Object.keys(bindings.nodes ?? {})) if (!byId.has(key)) fail(`binding names unknown node ${key}`);
  for (const key of Object.keys(config.nodes ?? {})) if (!byId.has(key)) fail(`settings name unknown node ${key}`);
  const bound = (node, explicit) => {
    const remembered = idmap[scopeKey(bl, node)];
    if (explicit && remembered && explicit !== remembered) fail(`${node}: explicit binding conflicts with saved ID ${remembered}`);
    return explicit || remembered || null;
  };
  const folderId = bound("folder", bindings.folderId);
  const folder = folders.find(f => f.id === folderId);
  const folderKey = scopeKey(bl, "folder");
  if (folderId && !folder) fail(`bound folder ${folderId} is not visible; check hidden-content access and binding`);
  if (!folderId && !config.folder?.name) fail("bind an existing folder ID or explicitly configure a new folder");
  const folderData = folder ? writableSnapshot("skillTreeFolder", folder) : { image: "", description: "", order: 0, ...config.folder, hidden: true };
  if (!folderId && folders.some(f => sameName(f.name, folderData.name ?? ""))) fail("a folder with this name exists; bind its ID explicitly");
  if (folder || !folderId) {
    for (const p of bloodrightProblems("skillTreeFolder", folderData)) fail(`folder: ${p}`);
    const it = { entity: "skillTreeFolder", slot: folder ? "edit" : "create", srcId: folderKey, name: folderData.name, ...(folder ? { targetId: folderId, expected: folderData } : {}), data: folderData };
    items.push(it); preview.push({ name: folderData.name, operation: folder ? "reuse" : "create", targetId: folderId, changes: [] });
  }
  const claimed = new Set();
  for (const n of ordered) {
    const settings = config.nodes?.[n.id] ?? {};
    for (const key of Object.keys(settings)) if (!["rounds", "seichiSilverCost", "description", "image"].includes(key)) fail(`${n.name}: unsupported setting ${key}`);
    const targetId = bound(n.id, bindings.nodes?.[n.id]);
    const live = skills.find(s => s.id === targetId);
    if (targetId) {
      if (claimed.has(targetId)) fail(`${n.name}: ID ${targetId} is bound twice`);
      claimed.add(targetId);
      if (!live) fail(`${n.name}: bound record ${targetId} is not visible; check access/binding`);
      else if (live.pathType !== "BLOODRIGHT" || live.bloodlineId !== bl) fail(`${n.name}: binding belongs to another bloodline or SKILL path`);
      else if (!live.hidden) fail(`${n.name}: bound skill is already visible; this importer stages hidden content only`);
    }
    if (skills.some(s => s.id !== targetId && sameName(s.name, n.name))) fail(`${n.name}: global name collision; bind the intended record explicitly or rename the design`);
    const effects = Object.entries(n.bonuses).map(([tag, amount]) => ({
      type: amount > 0 ? "increasepotency" : "decreasepotency", target: "INHERIT", direction: "offence",
      rounds: settings.rounds, power: Math.abs(amount), powerPerLevel: 0, calculation: "static",
      affectedTag: tag, affectedElements: [...elements],
      staticAssetPath: "", staticAnimation: "", appearAnimation: "", disappearAnimation: "", appearSfx: "", disappearSfx: "",
      description: `${amount > 0 ? "Increase" : "Decrease"} ${tag} potency on ${elements.join("/")} jutsu by ${Math.abs(amount)} points.`,
    }));
    const data = { name: n.name, description: settings.description ?? effects.map(e => e.description).join(" "),
      target: "SELF", tier: n.tier, requiredSkillIds: n.parents.map(p => `@skillTree:${scopeKey(bl, p)}`),
      costSkillPoints: n.cost, pathType: "BLOODRIGHT", bloodlineId: bl, seichiSilverCost: settings.seichiSilverCost,
      hidden: true, skillType: "DEFAULT", folderId: `@skillTreeFolder:${folderKey}`, effects,
      ...(live?.image ? { image: live.image } : {}), ...(settings.image !== undefined ? { image: settings.image } : {}),
    };
    for (const p of bloodrightProblems("skillTree", data, null, { preCreate: true })) fail(`${n.name}: ${p}`);
    const resolved = { ...data, folderId: folderId ?? data.folderId, requiredSkillIds: n.parents.map(p => bound(p, bindings.nodes?.[p]) ?? `@skillTree:${scopeKey(bl, p)}`) };
    const changes = live ? diffAsserted("skillTree", resolved, live) : Object.entries(data).map(([key, sent]) => ({ key, sent }));
    const it = { entity: "skillTree", srcId: scopeKey(bl, n.id), name: n.name, slot: targetId ? "edit" : "create", ...(targetId ? { targetId, expected: live ? writableSnapshot("skillTree", live) : null } : {}), data };
    items.push(it);
    preview.push({ nodeId: n.id, name: n.name, targetId, operation: targetId ? changes.length ? "update" : "reuse" : "create", changes });
  }
  const provenance = { version: 1, source: config.source, gamePin: CONTRACT._meta.pin, bloodlineId: bl, bindings: Object.fromEntries(items.filter(it => it.targetId).map(it => [it.srcId, it.targetId])), hiddenProbeId: config.hiddenProbeId };
  return { problems, preview, allocations, maxAdvanced: advanced, manifest: problems.length ? null : { _note: `Bloodright: ${design.title}`, dedupNames: true, bloodrightImport: provenance, items } };
}

/** Read-only preparation; the caller freezes the returned manifest for Start and reload. */
export async function prepareBloodright({ config, github, reader, storage, auth }) {
  if (config?.version !== 1) throw new Error("unsupported Bloodright package version");
  if (!/^[a-f0-9]{40}$/.test(config.source?.ref ?? "")) throw new Error("Bloodright source requires an exact commit");
  auth?.assert("skillTree.create");
  if (!id(config.hiddenProbeId)) throw new Error("name a known hidden skill ID to verify staff-visible inventory");
  const probe = await reader.get("skillTree.get", config.hiddenProbeId, { fresh: true });
  if (!probe.ok || probe.data?.hidden !== true) throw new Error("hidden-content access not established: the known hidden skill is not visible; check the session, role, and probe ID");
  const design = JSON.parse(await github.text(config.source.path, config.source.ref));
  const all = await reader.list("skillTree.getAll", { fresh: true });
  const folders = await reader.list("skillTree.getAllFolders", { fresh: true });
  if (!all.ok || !folders.ok) throw new Error("Bloodright inventory failed; no preview or writes available");
  if (!all.data.some(s => s.id === config.hiddenProbeId)) throw new Error("hidden probe missing from inventory; incomplete access or changed session");
  // Full point records for every bound skill, including remembered imports; never infer binding by name.
  const map = readIdmap(storage);
  const boundIds = [...new Set(design.nodes.map(n => config.bindings?.nodes?.[n.id] || map[scopeKey(design.bloodline.id, n.id)]).filter(Boolean))];
  for (const target of boundIds) {
    const r = await reader.get("skillTree.get", target, { fresh: true });
    if (!r.ok || !r.data) throw new Error(`bound skill ${target} is unreadable`);
    const index = all.data.findIndex(s => s.id === target);
    if (index < 0) throw new Error(`bound skill ${target} absent from complete inventory`);
    all.data[index] = r.data;
  }
  return compileBloodright({ design, config, skills: all.data, folders: folders.data, idmap: map });
}
