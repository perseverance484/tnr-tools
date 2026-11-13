// POST-PIN EFFECT TAG KEY. Upstream 8bd670153 (2026-11-09, "Allow animation sizing per combat
// effect") added animationScale to BaseAttributes (validators/combat.ts: z.coerce.number().min(1)
// .max(3).prefault(1)), so every combat tag that spreads BaseAttributes accepts it, and the live
// jutsu.update schema lists it on every tag. nested.json and the Bloodright contract are pinned
// before it, so without this list a manifest that sets a clip's size would be refused as an
// unknown key. Additive and backward compatible. Shared by runner/validate.mjs (general effects)
// and bloodright/validate.mjs (skill-tree effects, which are upstream AllTags too). A full re-pin
// supersedes this list.
export const EFFECT_POST_PIN_KEYS = Object.freeze(["animationScale"]);
