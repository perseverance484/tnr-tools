// QW-0A fixture: constants module (mirrors app/drizzle/constants.ts idioms)
export const BasicElementName = ["Fire", "Water"] as const;
export const ElementNames = [
  ...BasicElementName,
  "Ice",
  // a comment, with a comma and a ] bracket
  "None",
] as const;
export const NestedNames = [...ElementNames, "Extra"] as const;
export const StatTypes = ["None", "Ninjutsu", "Genjutsu"] as const;
export const GeneralTypes = ["Highest", "Strength"] as const;
export const MasteryNames = ["ninjutsuMastery", "sageMastery"] as const;
export const UserStatNames = [...StatTypes, ...MasteryNames] as const;
export const MAX_CAP = 400_000;
export const DEFAULT_DELAY = 3;
