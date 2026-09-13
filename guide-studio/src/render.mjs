import sanitize from "../compatibility/runtime/sanitize.mjs";
import {
  escape,
  heroCard,
  mechanicCard,
  referenceCard,
  summonCard,
} from "./cards.mjs";
import { effectText } from "./effects.mjs";
import { resolveTemplate } from "./template.mjs";
import { sha256 } from "./hash.mjs";
import { encodeBase64, validateHighlight } from "./schema.mjs";
export async function renderGuide(
  d,
  registry,
  assetOrigin,
  submissionId = "preview",
) {
  const t = resolveTemplate(d, registry),
    origin = new URL(assetOrigin).origin,
    assets = [];
  const para = (text) =>
    String(text)
      .split(/\n\s*\n/)
      .filter((s) => s.trim())
      .map((s) => `<p>${escape(s).replace(/\n/g, "<br />")}</p>`)
      .join("");
  const graphic = async (svg, alt, role) => {
    const hash = await sha256(svg),
      url = `${origin}/guide-assets/${submissionId}/${hash}.svg`;
    assets.push({
      url,
      sha256: hash,
      mime: "image/svg+xml",
      body: svg,
      alt,
      role,
    });
    // The pinned game sanitizer only keeps img.src; captions preserve native context.
    return `<figure><img src="${url}" /><figcaption>${escape(alt)}</figcaption></figure>`;
  };
  let html = draftIntro();
  function draftIntro() {
    return t.intro.map(para).join("");
  }
  html += await graphic(
    heroCard(t, registry),
    `${t.name} · ${t.identity}`,
    "hero",
  );
  html +=
    '<h2 id="bloodline-overview">Bloodline Overview</h2>' + para(t.overview);
  const b = registry.bloodlines.find((b) => b.id === t.bloodlineId);
  html +=
    `<p><strong>${escape(b.rank)} rank · ${escape(b.classification)} classification · ${escape(b.traits?.trim() || t.identity)}</strong></p><ul>` +
    b.effects.map((e) => `<li>${escape(effectText(e))}</li>`).join("") +
    `</ul><p><small>Bloodline values at level ${b.level}; player jutsu at level 25. Formula power is not final damage.</small></p>`;
  html +=
    '<h2 id="bloodline-kit">Bloodline Kit</h2><p>The complete bloodline kit is included below, independently of the player’s selected build.</p>';
  for (const id of t.coreKit) {
    const j = registry.jutsu.find((j) => j.id === id);
    html += await graphic(mechanicCard(j, t, registry), j.name, "core-kit");
  }
  for (const m of t.modules) {
    html +=
      `<h2 id="${escape(m.id)}">${escape(m.title)}</h2>` + para(m.description);
    const gate = registry.summons.find((s) => s.id === m.gateId);
    for (const id of gate.jutsuIds) {
      const j = registry.jutsu.find((j) => j.id === id);
      html += await graphic(
        mechanicCard(j, t, registry),
        `Underworld Gate · ${j.name}`,
        "summon-link",
      );
    }
    for (const s of m.summons) {
      html += await graphic(summonCard(s, registry, t), s.name, "summon");
      for (const id of s.jutsuIds) {
        const j = registry.jutsu.find((j) => j.id === id);
        html += await graphic(
          mechanicCard(j, t, registry),
          `${s.name} · ${j.name}`,
          "summon-ability",
        );
      }
    }
  }
  for (const m of t.modules) {
    const utility = [
      ...new Set(m.summons.flatMap((s) => s.utilityJutsuIds || [])),
    ];
    for (const id of utility) {
      const j = registry.jutsu.find((j) => j.id === id);
      html += await graphic(
        mechanicCard(j, t, registry),
        "Shared summon departure routine",
        "summon-utility",
      );
    }
  }
  html +=
    '<hr /><h2 id="my-build">My PvP Loadout</h2>' +
    para(`A player’s perspective · ${d.author || "Your display name"}`) +
    para(d.summary);
  for (const choice of d.loadout) {
    const j = registry.jutsu.find((j) => j.id === choice.jutsuId);
    html += await graphic(
      t.coreKit.includes(j.id)
        ? referenceCard(j, t, registry, "")
        : mechanicCard(j, t, registry),
      `${j.name} · HOW I USE IT`,
      "build",
    );
    if (choice.howIUseIt)
      html += "<p><strong>HOW I USE IT</strong></p>" + para(choice.howIUseIt);
  }
  const chapters = t.chapters.filter(
    (c) => !c.hidden && d.strategy[c.id]?.trim(),
  );
  if (chapters.length) {
    html += '<h2 id="strategy">Rotations &amp; Game Plan</h2>';
    for (const c of chapters)
      html +=
        `<h3 id="chapter-${c.id}">${escape(c.title)}</h3>` +
        para(d.strategy[c.id]);
  }
  if (d.highlights.length) {
    html += '<h2 id="combat-highlights">Combat Highlights</h2>';
    for (const h of d.highlights) {
      const { bytes } = validateHighlight(h),
        hash = await sha256(bytes),
        url = `${origin}/guide-assets/${submissionId}/${hash}.webp`;
      assets.push({
        url,
        sha256: hash,
        mime: "image/webp",
        data: h.data,
        alt: h.caption,
        role: "highlight",
      });
      html += `<figure><img src="${url}" /><figcaption>${escape(h.caption)}</figcaption></figure>`;
    }
  }
  html +=
    "<hr />" +
    para(
      `${t.shortName} · Guide by ${d.author || "you"}. Bloodline foundation by TNR. Build choices and tactical notes by the author.`,
    );
  return { html: sanitize(html), assets, template: t };
}
export function previewDocument(rendered) {
  let content = rendered.html;
  for (const a of rendered.assets) {
    const src = a.body
      ? "data:image/svg+xml;base64," +
        encodeBase64(new TextEncoder().encode(a.body))
      : a.data;
    content = content
      .split(`src="${a.url}"`)
      .join(`src="${src}" alt="${escape(a.alt)}"`);
  }
  return `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'"><title>${escape(rendered.template?.name || "TNR guide")}</title><style>*{box-sizing:border-box}body{margin:0;padding:24px 18px 60px;background:#fffbed;color:#34170b;font:17px/1.65 Arial,sans-serif}article{max-width:720px;margin:auto;overflow-wrap:anywhere}h2{font-size:24px;margin:40px 0 16px;line-height:1.25}h3{font-size:21px;margin:32px 0 12px}p{margin:16px 0}figure{margin:22px 0 32px}img{display:block;max-width:100%;width:512px;height:auto}figcaption{font-size:13px;margin-top:7px;color:#735d44}hr{border:0;border-top:1px solid #d8c7a3;margin:44px 0}ul{padding-left:22px}small{font-size:13px}a{color:#965b18}@media(max-width:420px){body{padding:20px 12px;font-size:16px}}</style><article>${content}</article></html>`;
}
