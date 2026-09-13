import { z } from "zod";
import { resolveTemplate } from "./template.mjs";
export const SOURCE_SHA = "36c5873b7b6ee5fd3af717008d7c51b0f185b756";
export const DraftSchema = z
  .object({
    schema: z.literal("tnrguide/v2"),
    template: z
      .object({
        slug: z.string().max(80),
        version: z.number().int().positive(),
      })
      .strict(),
    catalogVersion: z.string().max(80),
    author: z.string().trim().max(48),
    summary: z.string().trim().max(400),
    loadout: z
      .array(
        z
          .object({
            jutsuId: z.string().max(191),
            howIUseIt: z.string().trim().max(1800),
          })
          .strict(),
      )
      .max(20),
    strategy: z.record(z.string().max(80), z.string().trim().max(6500)),
    highlights: z
      .array(
        z
          .object({
            caption: z.string().trim().max(500),
            data: z.string().max(480_000),
          })
          .strict(),
      )
      .max(4),
  })
  .strict();
export function newDraft(t, registry) {
  return {
    schema: "tnrguide/v2",
    template: { slug: t.slug, version: t.version },
    catalogVersion: registry.version,
    author: "",
    summary: "",
    loadout: [],
    strategy: {},
    highlights: [],
  };
}
export function validateDraft(input, registry, { complete = false } = {}) {
  const d = DraftSchema.parse(input),
    t = resolveTemplate(d, registry);
  const ids = new Set();
  for (const j of d.loadout) {
    if (ids.has(j.jutsuId)) throw Error("A jutsu appears twice in your build.");
    ids.add(j.jutsuId);
    const entry = registry.jutsu.find((x) => x.id === j.jutsuId);
    if (
      !entry ||
      entry.hidden ||
      entry.type === "AI" ||
      (entry.bloodlineId && entry.bloodlineId !== t.bloodlineId)
    )
      throw Error("This jutsu is not available for your build.");
  }
  for (const id of Object.keys(d.strategy))
    if (!t.chapters.some((c) => c.id === id && !c.hidden))
      throw Error("Unknown strategy chapter.");
  d.highlights.forEach(validateHighlight);
  if (complete) {
    const issues = checklist(d, t);
    if (issues.length) throw Error(issues.join(" "));
  }
  return d;
}
export function checklist(d, t) {
  return [
    !d.author && "Add your display name.",
    !d.loadout.length && "Choose at least one build jutsu.",
    d.loadout.some((j) => !j.howIUseIt.trim()) &&
      "Add a HOW I USE IT note to every selected jutsu.",
    ...t.chapters
      .filter((c) => c.required && !c.hidden && !d.strategy[c.id]?.trim())
      .map((c) => `Write ${c.title}.`),
    d.highlights.some((h) => !h.caption.trim()) &&
      "Caption each combat highlight.",
  ].filter(Boolean);
}
export function decodeBase64(base64) {
  const binary = atob(base64);
  return Uint8Array.from(binary, (c) => c.charCodeAt(0));
}
export function encodeBase64(bytes) {
  let s = "";
  for (let i = 0; i < bytes.length; i += 8192)
    s += String.fromCharCode(...bytes.subarray(i, i + 8192));
  return btoa(s);
}
export function validateHighlight(h) {
  if (!/^data:image\/webp;base64,[A-Za-z0-9+/]+=*$/.test(h.data))
    throw Error("Highlights must be processed WebP images.");
  const bytes = decodeBase64(h.data.split(",")[1]);
  if (bytes.length > 350_000 || bytes.length < 30)
    throw Error("Highlight size limit is 350 KB.");
  const tag = (a, b) => new TextDecoder().decode(bytes.subarray(a, b));
  const view = new DataView(bytes.buffer);
  if (
    tag(0, 4) !== "RIFF" ||
    tag(8, 12) !== "WEBP" ||
    view.getUint32(4, true) + 8 !== bytes.length
  )
    throw Error("Invalid WebP image.");
  let width = 0,
    height = 0,
    seenImage = false,
    offset = 12;
  for (; offset + 8 <= bytes.length; ) {
    const name = tag(offset, offset + 4),
      size = view.getUint32(offset + 4, true),
      start = offset + 8;
    if (
      start + size > bytes.length ||
      !["VP8 ", "VP8L", "VP8X", "ALPH"].includes(name)
    )
      throw Error(
        "Unsupported image chunk. Animated images and metadata are not accepted.",
      );
    if (name === "VP8X") {
      if (size !== 10 || (bytes[start] & ~0x10) !== 0)
        throw Error("Unsupported WebP extensions.");
      width =
        1 +
        bytes[start + 4] +
        (bytes[start + 5] << 8) +
        (bytes[start + 6] << 16);
      height =
        1 +
        bytes[start + 7] +
        (bytes[start + 8] << 8) +
        (bytes[start + 9] << 16);
    }
    if (name === "VP8 ") {
      if (seenImage) throw Error("Multiple image frames.");
      if (
        size < 10 ||
        bytes[start + 3] !== 0x9d ||
        bytes[start + 4] !== 1 ||
        bytes[start + 5] !== 0x2a
      )
        throw Error("Invalid WebP frame.");
      const w = view.getUint16(start + 6, true) & 0x3fff,
        hh = view.getUint16(start + 8, true) & 0x3fff;
      if (width && (width !== w || height !== hh))
        throw Error("Inconsistent image dimensions.");
      width = w;
      height = hh;
      seenImage = true;
    }
    if (name === "VP8L") {
      if (seenImage) throw Error("Multiple image frames.");
      if (size < 5 || bytes[start] !== 0x2f)
        throw Error("Invalid lossless WebP frame.");
      const n = view.getUint32(start + 1, true),
        w = (n & 0x3fff) + 1,
        hh = ((n >>> 14) & 0x3fff) + 1;
      if (width && (width !== w || height !== hh))
        throw Error("Inconsistent image dimensions.");
      width = w;
      height = hh;
      seenImage = true;
    }
    offset = start + size + (size % 2);
    if (offset > bytes.length) throw Error("Truncated image.");
  }
  if (
    offset !== bytes.length ||
    !seenImage ||
    width < 1 ||
    height < 1 ||
    width > 1600 ||
    height > 1600
  )
    throw Error("Highlight dimensions must be at most 1600 × 1600.");
  return { bytes, width, height, mime: "image/webp" };
}
