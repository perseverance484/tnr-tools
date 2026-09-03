// DOM helpers. createElement and CSSOM only; no innerHTML anywhere (repo law).

export function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === "class") el.className = v;
    else if (k === "style" && typeof v === "object") Object.assign(el.style, v);
    else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2).toLowerCase(), v);
    else if (k === "dataset") Object.assign(el.dataset, v);
    else if (k in el && typeof v !== "string") el[k] = v;
    else el.setAttribute(k, String(v));
  }
  append(el, children);
  return el;
}

export function append(el, children) {
  for (const c of children.flat(Infinity)) {
    if (c == null || c === false) continue;
    el.appendChild(typeof c === "string" || typeof c === "number" ? document.createTextNode(String(c)) : c);
  }
  return el;
}

export function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); return el; }
export function replace(el, ...children) { clear(el); return append(el, children); }

/** Install a stylesheet through CSSOM (adoptedStyleSheets, falling back to insertRule). */
export function installCss(cssText, doc = document) {
  try {
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(cssText);
    doc.adoptedStyleSheets = [...(doc.adoptedStyleSheets || []), sheet];
    return sheet;
  } catch {
    const style = doc.createElement("style");
    (doc.head || doc.documentElement).appendChild(style);
    const sheet = style.sheet;
    for (const rule of splitRules(cssText)) { try { sheet.insertRule(rule, sheet.cssRules.length); } catch { /* skip */ } }
    return sheet;
  }
}
function splitRules(css) {
  const out = []; let depth = 0, start = 0;
  for (let i = 0; i < css.length; i++) {
    const ch = css[i];
    if (ch === "{") depth++;
    else if (ch === "}") { depth--; if (depth === 0) { out.push(css.slice(start, i + 1).trim()); start = i + 1; } }
  }
  return out.filter(Boolean);
}

export const fmtAgo = (iso, now = Date.now()) => {
  if (!iso) return "";
  const s = Math.max(0, Math.round((now - new Date(iso).getTime()) / 1000));
  if (s < 60) return s + "s ago";
  if (s < 3600) return Math.round(s / 60) + "m ago";
  if (s < 86400) return Math.round(s / 3600) + "h ago";
  return Math.round(s / 86400) + "d ago";
};
export const fmtBytes = (n) => n < 1024 ? n + " B" : n < 1048576 ? (n / 1024).toFixed(1) + " KB" : (n / 1048576).toFixed(2) + " MB";
export const fmtCountdown = (untilMs, now = Date.now()) => { const s = Math.max(0, Math.ceil((untilMs - now) / 1000)); return s ? `${s}s` : "now"; };
