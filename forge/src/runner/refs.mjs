// @refs. `@jutsu:key`, `@ai:key`, `@item:key`, `@quest:key`, `@bloodline:key`, `@scene:key`
// (asset) resolve to ids minted by an earlier create in this job or by a previous job (the
// retained tnr_bk_idmap_v1). `@img:name` resolves to an uploaded URL.
//
// The lesson from push/16 (unresolved pool codes shipped as literals and were stripped
// server-side with a green row): resolution is checked, and an unresolved ref at send time is
// a hard failure, never a payload.

export const REF_RE = /^@(jutsu|ai|scene|item|quest|bloodline|img):(.+)$/;
export const DOUBLED_RE = /^@\w+:@\w+:/; // law 45: a doubled prefix survives a naive sweep

export function isRef(v) { return typeof v === "string" && REF_RE.test(v); }

/** Walk any value and collect refs as {pfx, key, path}. */
export function collectRefs(o, out = [], path = "") {
  if (Array.isArray(o)) o.forEach((x, i) => collectRefs(x, out, `${path}[${i}]`));
  else if (o && typeof o === "object") for (const k of Object.keys(o)) collectRefs(o[k], out, path ? `${path}.${k}` : k);
  else if (typeof o === "string") {
    if (DOUBLED_RE.test(o)) out.push({ pfx: "DOUBLED", key: o, path });
    else { const m = o.match(REF_RE); if (m) out.push({ pfx: m[1], key: m[2], path }); }
  }
  return out;
}

/**
 * Substitute refs. `lookup(pfx, key)` returns the id/url or undefined. Returns
 * {value, unresolved: [{pfx, key, path}]}. Never substitutes partially: the caller refuses
 * to send when unresolved is non-empty.
 */
export function resolveRefs(o, lookup) {
  const unresolved = [];
  const walk = (v, path) => {
    if (Array.isArray(v)) return v.map((x, i) => walk(x, `${path}[${i}]`));
    if (v && typeof v === "object") { const n = {}; for (const k of Object.keys(v)) n[k] = walk(v[k], path ? `${path}.${k}` : k); return n; }
    if (typeof v === "string") {
      if (DOUBLED_RE.test(v)) { unresolved.push({ pfx: "DOUBLED", key: v, path }); return v; }
      const m = v.match(REF_RE);
      if (m) {
        const r = lookup(m[1], m[2]);
        if (r === undefined || r === null || r === "") { unresolved.push({ pfx: m[1], key: m[2], path }); return v; }
        return r;
      }
    }
    return v;
  };
  return { value: walk(o, ""), unresolved };
}

/** Does a string still contain any unresolved ref anywhere in a serialized payload? */
export function hasRefLiteral(payload) {
  return /@(jutsu|ai|scene|item|quest|bloodline|img):[^"]{1,80}/.test(JSON.stringify(payload) || "");
}
