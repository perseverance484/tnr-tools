// compatibility/guide-validator.ts
import { z } from "zod";

// compatibility/constants.ts
var GuideCategories = [
  "getting-started",
  "combat",
  "world",
  "villages",
  "bloodlines",
  "farming",
  "economy",
  "ranks",
  "reference"
];
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

// compatibility/guide-html.ts
var isReservedGuideSlug = (slug) => GUIDE_RESERVED_SLUGS.includes(slug);

// compatibility/guide-validator.ts
var GuideFaqItemSchema = z.object({
  question: z.string().trim().min(1).max(200),
  answer: z.string().trim().min(1).max(1e3)
});
var GuideSlugSchema = z.string().trim().min(1).max(80).regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "Use lowercase letters, numbers and hyphens").refine((slug) => !isReservedGuideSlug(slug), {
  message: "That slug is reserved"
});
var GuideArticleValidator = z.object({
  slug: GuideSlugSchema,
  title: z.string().trim().min(1).max(191),
  subtitle: z.string().trim().max(255).optional().nullable(),
  excerpt: z.string().trim().max(500).optional().nullable(),
  seoTitle: z.string().trim().max(70).optional().nullable(),
  seoDescription: z.string().trim().max(160).optional().nullable(),
  category: z.enum(GuideCategories),
  content: z.string().min(1).max(2e5),
  image: z.union([z.url(), z.literal("")]).optional().nullable(),
  faq: z.array(GuideFaqItemSchema).max(12).optional().nullable(),
  sortOrder: z.coerce.number().int().min(0).max(1e4),
  published: z.boolean(),
  relatedBloodlineId: z.string().max(191).optional().nullable(),
  relatedItemId: z.string().max(191).optional().nullable(),
  relatedJutsuId: z.string().max(191).optional().nullable(),
  sourceUrl: z.union([z.url(), z.literal("")]).optional().nullable(),
  reviewNotes: z.string().trim().max(4e3).optional().nullable()
});
var GuideListFilterSchema = z.object({
  includeDrafts: z.boolean().optional()
});
export {
  GuideArticleValidator,
  GuideFaqItemSchema,
  GuideListFilterSchema,
  GuideSlugSchema
};
