// Deterministic serialization of a rendered Forge screen.
//
// Phase 0 moves orchestration out of the view layer under a byte-identity guarantee: the five
// released screens must render exactly the same tree before and after the extraction. A DOM
// comparison cannot prove that on its own, because attribute order, whitespace and handler
// identity all vary run to run. This produces one canonical string per screen instead, so the
// guarantee is a byte comparison against a committed fixture rather than a judgement call.
//
// What is deliberately captured: tag, every non-handler attribute (sorted), disabled/readOnly/
// value/checked property state that never appears as an attribute, and text. What is deliberately
// dropped: event handlers (function identity is not stable and is not presentation) and empty
// text nodes.

const DROP_ATTRS = new Set(["data-render-seq"]);

function attrsOf(el) {
  const out = [];
  for (const a of el.attributes || []) {
    if (DROP_ATTRS.has(a.name)) continue;
    out.push([a.name, a.value]);
  }
  // Properties the DOM keeps off the attribute map. Without these a disabled button and an
  // enabled one serialize identically, which is exactly the kind of regression this guards.
  for (const p of ["disabled", "readOnly", "checked"]) {
    if (el[p] === true) out.push([`:${p}`, "true"]);
  }
  if (el.tagName === "TEXTAREA" || el.tagName === "INPUT") {
    if (typeof el.value === "string" && el.value !== "") out.push([":value", el.value]);
  }
  out.sort((x, y) => (x[0] < y[0] ? -1 : x[0] > y[0] ? 1 : 0));
  return out;
}

function walk(node, depth, lines) {
  const pad = "  ".repeat(depth);
  if (node.nodeType === 3) {
    const text = String(node.nodeValue ?? "");
    if (!text.trim()) return;
    lines.push(`${pad}#text ${JSON.stringify(text)}`);
    return;
  }
  if (node.nodeType !== 1) return;
  const attrs = attrsOf(node).map(([k, v]) => `${k}=${JSON.stringify(v)}`).join(" ");
  lines.push(`${pad}<${node.tagName.toLowerCase()}${attrs ? " " + attrs : ""}>`);
  for (const child of node.childNodes) walk(child, depth + 1, lines);
}

/**
 * @param {Node|Node[]|null} rendered  whatever a screen function returned
 * @returns {string} canonical text, newline-terminated
 */
export function serializeScreen(rendered) {
  const nodes = rendered == null ? [] : Array.isArray(rendered) ? rendered : [rendered];
  const lines = [];
  for (const node of nodes) {
    if (node == null) continue;
    walk(node, 0, lines);
  }
  return lines.join("\n") + "\n";
}
