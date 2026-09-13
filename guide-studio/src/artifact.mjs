import { zipSync, unzipSync, strToU8, strFromU8 } from "fflate";
import {
  GuideArticleValidator,
  validateDraft,
  SOURCE_SHA,
  encodeBase64,
} from "./schema.mjs";
import { renderGuide } from "./render.mjs";
import { sha256, stableStringify } from "./hash.mjs";
export async function createArtifact(input, registry, origin, id) {
  const d = validateDraft(input, registry, { complete: true });
  if (!/^[a-f0-9-]{16,64}$/.test(id))
    throw Error("Invalid server submission ID");
  const rendered = await renderGuide(d, registry, origin, id),
    t = rendered.template;
  const title = `${t.shortName}: ${d.author}’s Guide`;
  const game = GuideArticleValidator.parse({
    slug: `${t.slug}-${id.replaceAll("-", "")}`,
    title,
    subtitle: d.summary.slice(0, 255) || t.identity,
    excerpt:
      d.summary ||
      `${t.name}: a player’s loadout and strategy guide by ${d.author}.`,
    seoTitle: title.slice(0, 70),
    seoDescription: (
      d.summary ||
      `${t.name}: builds, complete bloodline kit, and strategy by ${d.author}.`
    ).slice(0, 160),
    category: "bloodlines",
    content: rendered.html,
    image: null, // Native cover is optional; the ordered body already contains the hero.
    faq: null,
    sortOrder: 100,
    published: false,
    relatedBloodlineId: t.bloodlineId,
    relatedItemId: null,
    relatedJutsuId: null,
    sourceUrl: `${new URL(origin).origin}/`,
    reviewNotes: `Guide Studio ${id}; ${registry.version}; ${t.slug}@${t.version}; game source ${SOURCE_SHA}. Approval is not publication.`,
  });
  const manifest = {
    schema: "tnr-guide-assets/v1",
    generated: rendered.assets.map(({ body, data, ...meta }) => meta),
    official: [
      ...registry.jutsu
        .filter(
          (j) =>
            t.coreKit.includes(j.id) ||
            d.loadout.some((c) => c.jutsuId === j.id) ||
            t.modules.some(
              (m) =>
                m.summons.some(
                  (s) =>
                    s.jutsuIds.includes(j.id) ||
                    s.utilityJutsuIds?.includes(j.id),
                ) ||
                registry.summons
                  .find((s) => s.id === m.gateId)
                  ?.jutsuIds.includes(j.id),
            ),
        )
        .map((j) => ({ id: j.id, ...j.image })),
      ...registry.summons
        .filter((s) =>
          t.modules.some(
            (m) => m.gateId === s.id || m.summons.some((x) => x.id === s.id),
          ),
        )
        .map((s) => ({ id: s.id, ...s.image })),
    ],
    hero: t.hero,
  };
  const files = {
    "submission.json": stableStringify(d) + "\n",
    "game-guide.json": stableStringify(game) + "\n",
    "content.html": game.content,
    "assets-manifest.json": stableStringify(manifest) + "\n",
  };
  const metadata = {
    schema: "tnr-approved-guide/v1",
    submissionId: id,
    sourceSha: SOURCE_SHA,
    bloodlineId: t.bloodlineId,
    catalogVersion: registry.version,
    template: d.template,
    templateHash: await sha256(stableStringify(t)),
    contentHash: await sha256(game.content),
    files: Object.fromEntries(
      await Promise.all(
        Object.entries(files).map(async ([n, v]) => [n, await sha256(v)]),
      ),
    ),
  };
  // Include generated asset bytes in the manifest's signed package hash as well.
  metadata.packageHash = await sha256(stableStringify(metadata));
  files["metadata.json"] = stableStringify(metadata) + "\n";
  return { files, metadata, game, submission: d, rendered };
}
export async function verifyArtifact(artifact) {
  const { files } = artifact,
    meta = JSON.parse(files["metadata.json"]);
  if (meta.schema !== "tnr-approved-guide/v1" || meta.sourceSha !== SOURCE_SHA)
    throw Error("Unsupported package contract");
  const { packageHash, ...unsigned } = meta;
  if ((await sha256(stableStringify(unsigned))) !== packageHash)
    throw Error("Package metadata hash mismatch");
  for (const name of [
    "submission.json",
    "game-guide.json",
    "content.html",
    "assets-manifest.json",
  ]) {
    if (!files[name] || (await sha256(files[name])) !== meta.files[name])
      throw Error("Package file hash mismatch: " + name);
  }
  const game = GuideArticleValidator.parse(
    JSON.parse(files["game-guide.json"]),
  );
  if (artifact.rendered && artifact.rendered.html !== game.content)
    throw Error("Preview content differs from the approved file");
  if (artifact.game && stableStringify(artifact.game) !== stableStringify(game))
    throw Error("Game snapshot differs from the approved file");
  if (
    artifact.metadata &&
    stableStringify(artifact.metadata) !== stableStringify(meta)
  )
    throw Error("Metadata snapshot differs from the approved file");
  const draft = JSON.parse(files["submission.json"]),
    manifest = JSON.parse(files["assets-manifest.json"]);
  if (
    game.content !== files["content.html"] ||
    (await sha256(game.content)) !== meta.contentHash ||
    game.published ||
    game.category !== "bloodlines" ||
    game.relatedBloodlineId !== meta.bloodlineId
  )
    throw Error("Invalid approved draft guide");
  if (
    draft.catalogVersion !== meta.catalogVersion ||
    stableStringify(draft.template) !== stableStringify(meta.template)
  )
    throw Error("Version mismatch");
  const referenced = [...game.content.matchAll(/<img src="([^"]+)"/g)].map(
    (m) => m[1],
  );
  if (
    referenced.some((u) => !manifest.generated.some((a) => a.url === u)) ||
    (game.image && !manifest.generated.some((a) => a.url === game.image))
  )
    throw Error("Unmanifested image");
  for (const a of artifact.rendered?.assets ?? []) {
    const data =
      a.body ??
      Uint8Array.from(atob(a.data.split(",")[1]), (c) => c.charCodeAt(0));
    if (
      (await sha256(data)) !== a.sha256 ||
      !manifest.generated.some((m) => m.sha256 === a.sha256)
    )
      throw Error("Asset integrity mismatch");
  }
  return { meta, game, draft, manifest };
}
export function exportZip(artifact, approval) {
  const entries = {};
  for (const [name, body] of Object.entries(artifact.files))
    entries[name] = strToU8(body);
  entries["approval.json"] = strToU8(stableStringify(approval) + "\n");
  entries["README.txt"] = strToU8(
    "TNR Guide Studio\nVerify approval.json with the deployment approval public key. Import game-guide.json using the TNR-side importer. Assets are immutable and included under assets/. Approval and import do not publish this guide.\n",
  );
  for (const a of artifact.rendered.assets) {
    const name = a.url.split("/").at(-1);
    entries["assets/" + name] = a.body
      ? strToU8(a.body)
      : Uint8Array.from(atob(a.data.split(",")[1]), (c) => c.charCodeAt(0));
  }
  return zipSync(entries, {
    level: 6,
    mtime: new Date("2026-01-01T00:00:00Z"),
  });
}
export async function readPackageZip(bytes) {
  if (bytes.length > 8_000_000) throw Error("Package exceeds 8 MB");
  const seen = new Set();
  let total = 0,
    count = 0;
  const entries = unzipSync(bytes, {
    filter: (e) => {
      if (seen.has(e.name)) throw Error("Duplicate ZIP entry");
      seen.add(e.name);
      total += e.originalSize;
      count++;
      if (
        total > 24_000_000 ||
        count > 150 ||
        e.originalSize > 3_000_000 ||
        !/^(README\.txt|[a-z-]+\.(json|html)|assets\/[a-f0-9]{64}\.(svg|webp))$/.test(
          e.name,
        )
      )
        throw Error("Invalid or oversized package entry");
      return true;
    },
  });
  const files = {};
  for (const name of [
    "submission.json",
    "game-guide.json",
    "content.html",
    "assets-manifest.json",
    "metadata.json",
  ]) {
    if (!entries[name]) throw Error("Missing " + name);
    files[name] = strFromU8(entries[name]);
  }
  const { manifest } = await verifyArtifact({ files });
  const assets = [];
  for (const a of manifest.generated) {
    const data = entries["assets/" + a.url.split("/").at(-1)];
    if (!data || (await sha256(data)) !== a.sha256)
      throw Error("Missing or changed packaged asset");
    assets.push({
      ...a,
      ...(a.mime === "image/svg+xml"
        ? { body: strFromU8(data) }
        : { data: "data:image/webp;base64," + encodeBase64(data) }),
    });
  }
  return {
    artifact: { files, rendered: { html: files["content.html"], assets } },
    approval: JSON.parse(strFromU8(entries["approval.json"])),
  };
}
