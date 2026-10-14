import { z } from "zod";
import {
  ElementNames,
  StatTypes,
  GeneralTypes,
  MAX_CAP,
  DEFAULT_DELAY,
} from "@/drizzle/constants";
import { makeCappedNullableNumber, strictNullOnly } from "@/validators/base";
import { rewardFields } from "@/validators/rewards";

const msg = (defaultString: string) => {
  return z.string().prefault(defaultString);
};

const type = (defaultString: string) => {
  return z.literal(defaultString).prefault(defaultString);
};

const BaseTargets = ["INHERIT", "SELF"] as const;
const ActionTargets = [...BaseTargets, "COORDINATES"] as const;

const BaseAttributes = {
  power: z.coerce.number().min(-100).max(100).prefault(1),
  powerPerLevel: z.coerce.number().min(-1).max(1).prefault(0),
  direction: type("offence"),
  target: z.enum(ActionTargets).optional().prefault("INHERIT"),
  calculation: z.enum(["static"]).prefault("static"),
};

const PowerAttributes = {
  power: z.coerce.number().min(0).prefault(1),
};

const IncludeStats = {
  statTypes: z
    .array(
      z
        .enum([...StatTypes, "Highest"])
        .transform((value) => (value === "Highest" ? "None" : value)),
    )
    .optional(),
  generalTypes: z.array(z.enum(GeneralTypes)).optional(),
};

export const DamageTag = z.object({
  ...BaseAttributes,
  ...PowerAttributes,
  ...IncludeStats,
  type: z.literal("damage").prefault("damage"),
  description: msg("Deals damage, {braces} and, commas"),
  elements: z.array(z.enum(ElementNames)).optional(),
  rounds: z.coerce
    .number()
    .int()
    .min(0)
    .max(DEFAULT_DELAY)
    .prefault(DEFAULT_DELAY),
  boundProbe: z.array(z.number().max(MAX_CAP)).optional(),
  outerBound: z.array(z.number()).max(MAX_CAP).optional(),
  options: z
    .array(
      z.object({
        text: z.string(),
        leaked: z.string().optional(),
      }),
    )
    .prefault([]),
  ...rewardFields,
});

export const OverrideTag = z.object({
  calculation: z.enum(["percentage"]).prefault("percentage"),
  ...BaseAttributes,
  type: z.literal("override").prefault("override"),
  allowFlag: z.boolean().prefault(false),
  nullDefault: z.string().nullable().prefault(null),
});

export const AllTags = z.union([DamageTag, OverrideTag]);

export const ItemValidatorRawSchema = z
  .object({
    name: z.string(),
    requiredStrength: makeCappedNullableNumber(MAX_CAP),
    strictCapped: strictNullOnly(MAX_CAP),
    maxDelay: z.coerce.number().int().max(MAX_CAP).prefault(DEFAULT_DELAY),
    // QW0A-A-R1 probes: omission is NOT established by these callbacks
    negatedInput: z.preprocess((v) => (v !== undefined ? null : v), z.number().nullable()),
    constrainedInput: z.preprocess((v) => (v === undefined && false ? null : v), z.number().nullable()),
    nestedNullableInput: z.preprocess((v) => (v === undefined ? null : v), z.array(z.number().nullable())),
    // ...and these establish it (pinned-source forms)
    validInput: z.preprocess((v) => (v === undefined ? null : v), z.number().nullable()),
    looseInput: z.preprocess((value) => (value === "" || value == null ? null : value), z.number().nullable()),
    passThroughInput: z.preprocess((v) => (v === "" ? null : v), z.enum(StatTypes).nullish()),
    // QW0A-A-R1 re-review: undefined -> null reaches a non-nullable inner schema,
    // so the inner optional/default never applies and omission is rejected
    rejectedOptionalInput: z.preprocess((v) => (v === undefined ? null : v), z.number().optional()),
    rejectedDefaultInput: z.preprocess((v) => (v === undefined ? null : v), z.number().default(7)),
    rejectedPrefaultInput: z.preprocess((v) => (v === undefined ? null : v), z.number().prefault(7)),
    // ...while a pass-through callback lets undefined reach the inner default
    acceptedDefaultInput: z.preprocess((v) => (v === "" ? null : v), z.number().default(7)),
    acceptedPrefaultInput: z.preprocess((v) => (v === "" ? null : v), z.number().prefault(7)),
    // unclassified callback over an inner optional: conservatively required
    negatedOptionalInput: z.preprocess((v) => (v !== undefined ? null : v), z.number().optional()),
    // QW0A-A-R2 probes: bounds/coercion of a nested schema are not the field's
    nestedBoundInput: z.array(z.number().max(MAX_CAP)).optional(),
    outerBoundInput: z.array(z.number()).max(MAX_CAP),
    craftingRequirements: z
      .array(
        z.object({
          ids: z.array(z.string()),
          number: z.coerce
            .number()
            .int()
            .min(1)
            .max(MAX_CAP),
        }),
      )
      .prefault([])
      .optional()
      .nullish(),
  })
  .superRefine((value, ctx) => {
    if (value.name === "x") ctx.addIssue({ code: "custom", message: "no" });
  });

export const JutsuValidatorRawSchema = z.object({
  requiredStrength: makeCappedNullableNumber(MAX_CAP),
});
