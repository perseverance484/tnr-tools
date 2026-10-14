import { z } from "zod";

const LeftAttributes = {
  ...RightAttributes,
  left: z.string(),
};

const RightAttributes = {
  ...LeftAttributes,
  right: z.string(),
};

export const DamageTag = z.object({
  ...LeftAttributes,
  type: z.literal("damage").prefault("damage"),
});

export const AllTags = z.union([DamageTag]);
