import { resolveTemplate } from "./template.mjs";
import { sha256 } from "./hash.mjs";
import { encodeBase64 } from "./schema.mjs";

// Only a selected guide's art is fetched, from the same-origin immutable cache.
// SVGs displayed as images cannot rely on external image references: verified
// bytes are embedded at preview time to match the server's self-contained cards.
export function createPreviewLoader(
  registry,
  fetcher = (...args) => fetch(...args),
) {
  const cache = new Map();
  function load(image) {
    const key = image.url + ":" + image.sha256;
    if (!cache.has(key)) {
      const pending = (async () => {
        const response = await fetcher(image.url, {
          credentials: "omit",
          redirect: "error",
          cache: "force-cache",
        });
        if (!response.ok)
          throw Error(
            "Official artwork could not load. Close the preview and try again.",
          );
        const bytes = new Uint8Array(await response.arrayBuffer());
        if ((await sha256(bytes)) !== image.sha256)
          throw Error("Official artwork failed its integrity check.");
        return "data:image/webp;base64," + encodeBase64(bytes);
      })();
      cache.set(key, pending);
      // A network/integrity failure must be retryable, never a cached blank card.
      pending.catch(() => cache.delete(key));
    }
    return cache.get(key);
  }
  return async (draft) => {
    const t = resolveTemplate(draft, registry);
    const jutsuIds = new Set([
      ...t.coreKit,
      ...draft.loadout.map((j) => j.jutsuId),
    ]);
    const images = new Map([[t.hero.url, t.hero]]);
    for (const m of t.modules) {
      const gate = registry.summons.find((s) => s.id === m.gateId);
      gate.jutsuIds.forEach((id) => jutsuIds.add(id));
      for (const s of m.summons) {
        const record = registry.summons.find((r) => r.id === s.id);
        images.set(record.image.url, record.image);
        [...s.jutsuIds, ...(s.utilityJutsuIds || [])].forEach((id) =>
          jutsuIds.add(id),
        );
      }
    }
    for (const id of jutsuIds) {
      const j = registry.jutsu.find((j) => j.id === id);
      if (!j) throw Error("Unknown build jutsu.");
      images.set(j.image.url, j.image);
    }
    const approvedImages = [...images.values()];
    for (const image of approvedImages)
      if (
        !/^\/assets\/[a-f0-9]{24}\.webp$/.test(image.url) ||
        registry.assetHashes[image.url] !== image.sha256
      )
        throw Error("Official artwork is not in this catalog.");
    const entries = await Promise.all(
      approvedImages.map(async (image) => [image.url, await load(image)]),
    );
    return { ...registry, imageData: Object.fromEntries(entries) };
  };
}
