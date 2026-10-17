import { prepareBloodright } from "./compiler.mjs";
import { parseManifest, planOrder } from "../runner/manifest.mjs";
import { collectRefs } from "../runner/refs.mjs";
import { readIdmap } from "../storage/compat.mjs";

// A collection is a preview/execution envelope, not a multi-bloodline runner manifest.
// Every child retains its own provenance, lease, preimages, frozen text and recovery.
export async function prepareCollection(ctx, pkg) {
  const c = pkg.bloodrightCollection;
  if (pkg.bloodright || pkg.items || pkg.jutsu || pkg.capture || c?.version !== 1 || !Array.isArray(c.trees) || !c.trees.length || c.trees.length > 100) throw new Error("collection needs version 1 and 1..100 trees, without other manifest operations");
  const trees = [], problems = [], names = new Map(), bloodlines = new Set();
  for (const [index, config] of c.trees.entries()) {
    try {
      const bloodright = await prepareBloodright({ ...ctx, config, imagePack: pkg.imagePack, imgSizes: pkg.imgSizes, requireIcons: true });
      if (bloodright.problems.length) { problems.push(...bloodright.problems.map(p => `tree ${index + 1}: ${p}`)); continue; }
      const text = JSON.stringify(bloodright.manifest), manifest = parseManifest(text);
      const bl = manifest.policy.bloodrightImport.bloodlineId;
      if (bloodlines.has(bl)) problems.push(`duplicate bloodline ${bl} in collection`);
      bloodlines.add(bl);
      const plan = planOrder(manifest, readIdmap(ctx.storage));
      for (const it of plan) {
        const name = `${it.entity}:${it.name.normalize("NFKC").trim().toLowerCase()}`;
        const prior = names.get(name);
        if (prior && !(it.entity === "skillTreeFolder" && it.targetId && prior.targetId === it.targetId)) problems.push(`cross-tree name collision: ${it.name}`);
        names.set(name, it);
        problems.push(...ctx.validator.problems(it.entity, it.data, null).map(p => `${it.name}: ${p}`));
      }
      const images = [...new Set(plan.flatMap(it => collectRefs(it.data).filter(r => r.pfx === "img").map(r => r.key)))];
      for (const name of images) if (!manifest.imagePack?.files[name]) problems.push(`collection icon ${name} needs an immutable imagePack binding`);
      trees.push({ text, manifest, plan, images, bloodright, pack: manifest.imagePack, problems: [] });
    } catch (e) { problems.push(`tree ${index + 1}: ${e.message}`); }
  }
  return { trees, problems, plan: trees.flatMap(t => t.plan), images: [...new Set(trees.flatMap(t => t.images))],
    manifest: { capture: { before: [], after: [] }, imgSizes: pkg.imgSizes ?? {}, warnings: [], imagePack: trees[0]?.pack ?? null },
    bloodright: { preview: trees.flatMap(t => t.bloodright.preview), trees: trees.map(t => ({ bloodlineId: t.manifest.policy.bloodrightImport.bloodlineId, allocations: t.bloodright.allocations, maxAdvanced: t.bloodright.maxAdvanced })) } };
}
