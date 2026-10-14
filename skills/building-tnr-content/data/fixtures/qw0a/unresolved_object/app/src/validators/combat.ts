import { z } from "zod";

export const DamageTag = z.object({
  ...MissingAttributes,
  type: z.literal("damage").prefault("damage"),
});

export const AllTags = z.union([DamageTag]);
