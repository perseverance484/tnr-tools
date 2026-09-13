import { effectText } from "./effects.mjs";
export const escape = (s) =>
  String(s ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
// Deterministic word wrapping, with a hard split for unbroken strings.
export function wrap(text, limit = 49) {
  const lines = [];
  for (const para of String(text).split("\n")) {
    let line = "";
    for (const word of para.split(/\s+/).filter(Boolean)) {
      const pieces = word.match(new RegExp(`.{1,${limit}}`, "gu")) || [];
      for (const p of pieces) {
        if ((line + " " + p).trim().length > limit) {
          lines.push(line);
          line = p;
        } else line = (line + " " + p).trim();
      }
    }
    lines.push(line);
  }
  return lines;
}
const textLines = (
  lines,
  x,
  y,
  { size = 26, color = "#d5e4df", weight = 400, lineHeight = 36 } = {},
) =>
  lines
    .map(
      (s, i) =>
        `<text x="${x}" y="${y + i * lineHeight}" font-size="${size}" fill="${color}" font-weight="${weight}">${escape(s)}</text>`,
    )
    .join("");
const shell = (height, t, body, label) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="720" height="${height}" viewBox="0 0 720 ${height}" role="img"><title>${escape(label)}</title><rect width="720" height="${height}" rx="12" fill="${t.ink}"/><rect x="10" y="10" width="700" height="${height - 20}" rx="9" fill="none" stroke="#aa9870" stroke-width="1"/><g font-family="Arial, Helvetica, sans-serif">${body}</g></svg>`;
export function heroCard(t, registry) {
  const title = wrap(t.shortName, 20),
    identity = wrap(t.identity, 29);
  let body = `<image href="${registry.imageData[t.hero.url]}" x="370" y="0" width="350" height="390" preserveAspectRatio="xMidYMid slice"/><rect width="390" height="390" fill="${t.ink}"/><path d="M390 0L480 0L390 390Z" fill="${t.ink}"/><text x="32" y="58" font-size="16" letter-spacing="3" fill="${t.accent}">TNR · BLOODLINE FIELD GUIDE</text>`;
  body += textLines(title, 32, 132, {
    size: 47,
    color: "#f6ebca",
    weight: 700,
    lineHeight: 56,
  });
  body += textLines(identity, 32, 220, {
    size: 21,
    color: t.accent,
    lineHeight: 32,
  });
  body += `<path d="M32 310H315" stroke="#aa9870"/><text x="32" y="347" font-size="17" fill="#d5e4df">${escape(registry.bloodlines.find((b) => b.id === t.bloodlineId).rank)} RANK / TNR GUIDE SERIES</text>`;
  return shell(390, t, body, t.name);
}
export function mechanicCard(j, t, registry, note = "") {
  const title = wrap(j.name, 25);
  const metaY = Math.max(107, 61 + title.length * 35 + 11);
  let y = metaY + 48;
  let body = `<image href="${registry.imageData[j.image.url]}" x="28" y="28" width="100" height="100"/><rect x="28" y="28" width="100" height="100" rx="8" fill="none" stroke="${t.accent}"/>`;
  body += textLines(title, 148, 61, {
    size: 30,
    color: "#f6ebca",
    weight: 700,
    lineHeight: 35,
  });
  body += `<text x="148" y="${metaY}" font-size="18" letter-spacing="1" fill="${t.accent}">${j.action} AP · RANGE ${j.range} · COOLDOWN ${j.cooldown}</text>`;
  if (j.description) {
    const lines = wrap(j.description, 47);
    body += textLines(lines, 28, y, { size: 26, lineHeight: 37 });
    y += lines.length * 37 + 18;
  }
  body += `<path d="M28 ${y}H692" stroke="#8f8563"/>`;
  y += 40;
  for (const e of j.effects) {
    const lines = wrap(effectText(e), 34);
    body += textLines(lines, 28, y, {
      size: 28,
      color: "#f1e4b4",
      weight: 600,
      lineHeight: 39,
    });
    y += lines.length * 39 + 22;
  }
  body += `<text x="28" y="${y}" font-size="18" fill="${t.accent}">${j.type === "AI" ? "SUMMON ABILITY" : "JUTSU"} LEVEL ${j.level} · CATALOG VALUES</text>`;
  y += 36;
  if (note) {
    body += `<path d="M28 ${y}H692" stroke="#8f8563"/><text x="28" y="${y + 37}" font-size="19" letter-spacing="2" font-weight="700" fill="${t.accent}">HOW I USE IT</text>`;
    y += 76;
    const lines = wrap(note, 48);
    body += textLines(lines, 28, y, { size: 26, lineHeight: 37 });
    y += lines.length * 37 + 14;
  }
  return shell(
    y + 16,
    t,
    body,
    `${j.name}. ${j.effects.map(effectText).join(". ")}${note ? ". How I use it: " + note : ""}`,
  );
}
export function referenceCard(j, t, registry, note) {
  let y = 165;
  let body =
    `<image href="${registry.imageData[j.image.url]}" x="28" y="28" width="80" height="80"/>` +
    textLines(wrap(j.name, 31), 130, 60, {
      size: 29,
      color: "#f6ebca",
      weight: 700,
      lineHeight: 36,
    });
  body += `<text x="28" y="${y}" font-size="22" fill="${t.accent}">CORE KIT · SEE ABOVE</text><path d="M28 ${y + 28}H692" stroke="#8f8563"/><text x="28" y="${y + 66}" font-size="19" letter-spacing="2" fill="${t.accent}">HOW I USE IT</text>`;
  y += 104;
  if (!note)
    return shell(
      210,
      t,
      body.slice(0, body.indexOf('<path d="M28 193')),
      j.name + ". Core kit reference",
    );
  const lines = wrap(note, 48);
  body += textLines(lines, 28, y, { size: 26, lineHeight: 37 });
  return shell(
    y + lines.length * 37 + 28,
    t,
    body,
    j.name + ". How I use it: " + note,
  );
}
export function summonCard(s, registry, t) {
  const r = registry.summons.find((x) => x.id === s.id);
  let body = `<image href="${registry.imageData[r.image.url]}" x="440" y="0" width="280" height="310" preserveAspectRatio="xMidYMid slice"/><rect width="440" height="310" fill="${t.ink}"/><text x="28" y="50" font-size="18" letter-spacing="2" fill="${t.accent}">THE GATE’S PATRONS</text>`;
  body += textLines(wrap(s.name, 22), 28, 111, {
    size: 37,
    color: "#f6ebca",
    weight: 700,
    lineHeight: 45,
  });
  body += textLines(wrap(s.identity, 28), 28, 220, {
    size: 24,
    color: t.accent,
    lineHeight: 34,
  });
  return shell(310, t, body, s.name + ". " + s.identity);
}
