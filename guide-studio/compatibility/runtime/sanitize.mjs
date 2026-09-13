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
var sanitize = (html) => sanitizeHtml(html, sanitizeOptions);
var sanitize_default = sanitize;
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
var htmlToModerationText = (html) => htmlToText(html, "\n", /[^\S\n]+/g);
var sanitizeVariantText = (html) => sanitizeHtml(html, {
  allowedTags: sanitizeHtml.defaults.allowedTags,
  allowedAttributes: sanitizeHtml.defaults.allowedAttributes
});
var stripBlockquotes = (html) => sanitizeHtml(html, {
  ...sanitizeOptions,
  exclusiveFilter: (frame) => frame.tag === "blockquote"
});
var capitalizeFirstLetter = (string) => {
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
};
export {
  capitalizeFirstLetter,
  sanitize_default as default,
  htmlToModerationText,
  htmlToPlainText,
  sanitizeVariantText,
  stripBlockquotes
};
