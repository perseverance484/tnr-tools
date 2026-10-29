// Badges and titles, read at studie-tech/TheNinjaRPG@2af4b32066c39e2868efae5dba6b339278701dca.
//
//   routers/badge.ts:72-138  create takes no input and inserts "New Badge - <id>" with the default
//                            avatar image and an empty description, answering {success, message: id};
//                            update {id, data: BadgeValidator} saves the whole record and refuses a
//                            name another badge holds. get {id}; getAllNames lists {id, name, image}.
//   routers/title.ts:93-185  create inserts "New Title - <id>" (unarchived, no effects); update
//                            {id, data: TitleValidator} saves the whole record. get {id} and getAll
//                            are staff-only; getAllNames lists unarchived catalog titles.
//   drizzle/schema.ts:4710-4757  neither table has a `hidden` column. Badge.description is
//                            varchar(500) while BadgeValidator allows 512.
//   server/utils/titleRewards.ts:9-37  quest and item saves refuse reward_titles naming an
//                            archived title (lints.mjs).
//
// A create carries hidden:true for law 16b like every entity; it is stripped by the pinned-field
// merge and never diffed. `archived` is the only visibility-like switch a title has, and it is
// required explicitly on a create: false makes the title referenceable by (hidden) rewards and lists
// it in title.getAllNames; true makes the server refuse every save that rewards it.
export const HIDDENLESS = Object.freeze(["petSpecies", "badge", "title"]);
const REQUIRED = { badge: ["name", "image", "description"], title: ["name", "archived"] };

// validators/badge.ts and validators/title.ts bounds, checked here because zod refuses them only at
// the update, after the create has minted a placeholder that badge.getAll / title.getAllNames list.
const MASTERY = ["Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu", "Sage", "Bloodline"]; // constants.ts:413
export function catalogProblems(entity, data, { preCreate = false } = {}) {
  const out = [], d = data, str = (v) => typeof v === "string";
  if ("hidden" in d && d.hidden !== true) out.push(`hidden: ${entity} has no hidden column; send hidden:true (law 16b)`);
  if (preCreate) for (const k of REQUIRED[entity]) if (d[k] === undefined) out.push(`${k} is required on a ${entity} create`);
  if ("name" in d && !(str(d.name) && d.name.trim() && d.name.trim().length <= 191)) out.push("name: 1-191 characters");
  // the Badge column holds 500, the validator 512: a longer badge description fails the save
  const cap = entity === "badge" ? 500 : 512;
  if ("description" in d && !(str(d.description) && d.description.length <= cap && (entity === "title" || d.description))) out.push(entity === "badge" ? "description: 1-500 characters (the Badge column holds 500)" : "description: at most 512 characters");
  if ("image" in d && !(str(d.image) && (d.image.startsWith("@img:") || /^https?:\/\/\S+$/.test(d.image) && d.image.length <= 191))) out.push("image: an @img ref or a URL of at most 191 characters");
  if ("archived" in d && typeof d.archived !== "boolean") out.push("archived must be a boolean");
  if ("effects" in d) {
    if (!Array.isArray(d.effects) || d.effects.length > 20) out.push("effects: an array of at most 20"); // TITLE_MAX_EFFECTS
    else d.effects.forEach((f, i) => {
      if (!(typeof f?.power === "number" && Number.isFinite(f.power) && f.power >= 0)) out.push(`effects[${i}]: power must be a finite number >= 0`);
      if (f?.type === "increasemastery" && !(Array.isArray(f.masteryTypes) && f.masteryTypes.length && f.masteryTypes.every((m) => MASTERY.includes(m)))) out.push(`effects[${i}]: masteryTypes needs 1+ of ${MASTERY.join("/")}`);
    });
  }
  return out;
}
