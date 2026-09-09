// Stable payload hashing. Used to detect that a manifest changed under a resumed job.
// Not a security hash: FNV-1a 32-bit over a key-sorted JSON encoding is enough to notice
// drift, and it is synchronous, which matters because the journal write path must be.

export function stableStringify(v) {
  if (v && typeof v === "object" && typeof v.toJSON === "function") v = v.toJSON(); // Date etc., like JSON.stringify
  if (v === undefined) return "null"; // only reachable inside arrays; JSON.stringify emits null there
  if (v === null || typeof v !== "object") return JSON.stringify(v);
  if (Array.isArray(v)) return "[" + v.map(stableStringify).join(",") + "]";
  const keys = Object.keys(v).filter((k) => v[k] !== undefined).sort(); // JSON.stringify omits undefined
  return "{" + keys.map((k) => JSON.stringify(k) + ":" + stableStringify(v[k])).join(",") + "}";
}

export function fnv1a32(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h.toString(16).padStart(8, "0");
}

export function payloadHash(payload) {
  return fnv1a32(stableStringify(payload === undefined ? null : payload));
}
