// compatibility/constants.ts
var GUIDE_RESERVED_SLUGS = ["edit", "new"];

// compatibility/sanitize.ts
import { decodeHTML } from "entities";
import sanitizeHtml from "sanitize-html";
var sanitizeOptions = {
  allowedTags: sanitizeHtml.defaults.allowedTags.concat([
    "img",
    "blockquote",
    "iframe"
  ]),
  allowedAttributes: {
    ...sanitizeHtml.defaults.allowedAttributes,
    img: ["src"],
    p: ["style"],
    div: ["style"],
    span: ["style"],
    h2: ["id"],
    h3: ["id"],
    blockquote: ["author", "date"],
    iframe: [
      "src",
      "width",
      "height",
      "title",
      "allow",
      "allowfullscreen",
      "frameborder",
      "class",
      "id",
      "style"
    ]
  },
  allowedStyles: {
    "*": {
      color: [
        /^(#[0-9a-fA-F]{3,8}|rgba?\(\s*[\d.]+[\s,]+[\d.]+[\s,]+[\d.]+[\s,\d.]*\)|hsla?\(\s*[\d.]+[\s,]+[\d.%]+[\s,]+[\d.%]+[\s,\d.]*\)|[a-zA-Z]+)$/
      ],
      "text-align": [/^(left|right|center|justify)$/],
      "font-weight": [/^\d+$|^bold$|^normal$/],
      "font-style": [/^(italic|normal)$/],
      "text-decoration": [/^(underline|line-through|none)$/]
    }
  }
};
var PLAIN_TEXT_SEPARATOR_TAGS = /* @__PURE__ */ new Set([
  "address",
  "article",
  "aside",
  "blockquote",
  "br",
  "dd",
  "div",
  "dl",
  "dt",
  "figcaption",
  "figure",
  "footer",
  "h1",
  "h2",
  "h3",
  "h4",
  "h5",
  "h6",
  "header",
  "hr",
  "li",
  "main",
  "nav",
  "ol",
  "p",
  "pre",
  "section",
  "script",
  "style",
  "table",
  "td",
  "th",
  "tr",
  "ul"
]);
var htmlToText = (html, breakText, collapse) => {
  let needsBreak = false;
  const text = sanitizeHtml(html, {
    allowedTags: [],
    allowedAttributes: {},
    onOpenTag: (tagName) => {
      if (PLAIN_TEXT_SEPARATOR_TAGS.has(tagName)) needsBreak = true;
    },
    onCloseTag: (tagName) => {
      if (PLAIN_TEXT_SEPARATOR_TAGS.has(tagName)) needsBreak = true;
    },
    textFilter: (chunk) => {
      if (!needsBreak) return chunk;
      needsBreak = false;
      return `${breakText}${chunk}`;
    }
  });
  return decodeHTML(text).replace(/\r\n?/g, "\n").replace(collapse, " ").trim();
};
var htmlToPlainText = (html) => htmlToText(html, " ", /\s+/g);

// compatibility/guide-html.ts
var HEADING_RE = /<h([23])(\s[^>]*)?>([\s\S]*?)<\/h\1>/gi;
var slugifyGuideTitle = (title) => {
  const slug = title.toLowerCase().normalize("NFKD").replace(/['’]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 80);
  return slug;
};
var isReservedGuideSlug = (slug) => GUIDE_RESERVED_SLUGS.includes(slug);
var uniqueHeadingId = (text, used) => {
  const base = slugifyGuideTitle(text) || "section";
  let id = base;
  let n = 2;
  while (used.has(id)) {
    id = `${base}-${n}`;
    n += 1;
  }
  used.add(id);
  return id;
};
var prepareGuideHtml = (html) => {
  const used = /* @__PURE__ */ new Set();
  const headings = [];
  const nextHtml = html.replace(
    HEADING_RE,
    (_full, level, attrs, inner) => {
      const text = htmlToPlainText(inner);
      const existingId = attrs?.match(/\sid=["']([^"']+)["']/i)?.[1];
      const id = existingId || uniqueHeadingId(text, used);
      if (existingId) used.add(existingId);
      if (text) {
        headings.push({ id, text, level: Number(level) });
      }
      const cleanedAttrs = (attrs ?? "").replace(/\s+id=["'][^"']*["']/i, "");
      return `<h${level} id="${id}"${cleanedAttrs}>${inner}</h${level}>`;
    }
  );
  return { html: nextHtml, headings };
};
export {
  isReservedGuideSlug,
  prepareGuideHtml,
  slugifyGuideTitle
};
