# DRIFT.md - upstream contract drift (2026-10-29)

Upstream: studie-tech/TheNinjaRPG@cd04ebf5cde5524448a48b03b9830f039dd6a5df

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==
ADDITIONS
  union-variant  AllTags  decreasecookingtime
  union-variant  AllTags  decreasecraftingtime
  union-variant  AllTags  decreasefarmingtime
  union-variant  AllTags  decreasegatheringtime
  union-variant  AllTags  increasegatheringyield
  union-variant  AllTags  increasehuntingyield
  union-variant  AllTags  increasejutsuslots
  variant-field  AllTags.decreasecookingtime  appearAnimation
  variant-field  AllTags.decreasecookingtime  appearSfx
  variant-field  AllTags.decreasecookingtime  calculation
  variant-field  AllTags.decreasecookingtime  coordinateTargeting
  variant-field  AllTags.decreasecookingtime  description
  variant-field  AllTags.decreasecookingtime  direction
  variant-field  AllTags.decreasecookingtime  disappearAnimation
  variant-field  AllTags.decreasecookingtime  disappearSfx
  variant-field  AllTags.decreasecookingtime  friendlyFire
  variant-field  AllTags.decreasecookingtime  power
  variant-field  AllTags.decreasecookingtime  powerPerLevel
  variant-field  AllTags.decreasecookingtime  rounds
  variant-field  AllTags.decreasecookingtime  staticAnimation
  variant-field  AllTags.decreasecookingtime  staticAssetPath
  variant-field  AllTags.decreasecookingtime  target
  variant-field  AllTags.decreasecookingtime  timeTracker
  variant-field  AllTags.decreasecookingtime  type
  variant-field  AllTags.decreasecraftingtime  appearAnimation
  variant-field  AllTags.decreasecraftingtime  appearSfx
  variant-field  AllTags.decreasecraftingtime  calculation
  variant-field  AllTags.decreasecraftingtime  coordinateTargeting
  variant-field  AllTags.decreasecraftingtime  description
  variant-field  AllTags.decreasecraftingtime  direction
  variant-field  AllTags.decreasecraftingtime  disappearAnimation
  variant-field  AllTags.decreasecraftingtime  disappearSfx
  variant-field  AllTags.decreasecraftingtime  friendlyFire
  variant-field  AllTags.decreasecraftingtime  power
  variant-field  AllTags.decreasecraftingtime  powerPerLevel
  variant-field  AllTags.decreasecraftingtime  rounds
  variant-field  AllTags.decreasecraftingtime  staticAnimation
  variant-field  AllTags.decreasecraftingtime  staticAssetPath
  variant-field  AllTags.decreasecraftingtime  target
  variant-field  AllTags.decreasecraftingtime  timeTracker
  variant-field  AllTags.decreasecraftingtime  type
  variant-field  AllTags.decreasefarmingtime  appearAnimation
  variant-field  AllTags.decreasefarmingtime  appearSfx
  variant-field  AllTags.decreasefarmingtime  calculation
  variant-field  AllTags.decreasefarmingtime  coordinateTargeting
  variant-field  AllTags.decreasefarmingtime  description
  variant-field  AllTags.decreasefarmingtime  direction
  variant-field  AllTags.decreasefarmingtime  disappearAnimation
  variant-field  AllTags.decreasefarmingtime  disappearSfx
  variant-field  AllTags.decreasefarmingtime  friendlyFire
  variant-field  AllTags.decreasefarmingtime  power
  variant-field  AllTags.decreasefarmingtime  powerPerLevel
  variant-field  AllTags.decreasefarmingtime  rounds
  variant-field  AllTags.decreasefarmingtime  staticAnimation
  variant-field  AllTags.decreasefarmingtime  staticAssetPath
  variant-field  AllTags.decreasefarmingtime  target
  variant-field  AllTags.decreasefarmingtime  timeTracker
  variant-field  AllTags.decreasefarmingtime  type
  variant-field  AllTags.decreasegatheringtime  appearAnimation
  variant-field  AllTags.decreasegatheringtime  appearSfx
  ... 66 more

no breaking changes: 126 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==
REMOVALS
  field  petSpecies  skillTarget

BREAKING: 1 change(s) - DO NOT ADOPT (exit 1)
== 45e_DATA_constants ==
REMOVALS
  const-member  COPY_PRIORITY_TIERS  ["increaseheal"]
ADDITIONS
  const-member  AvailableEffectTypes  decreasecookingtime
  const-member  AvailableEffectTypes  decreasecraftingtime
  const-member  AvailableEffectTypes  decreasefarmingtime
  const-member  AvailableEffectTypes  decreasegatheringtime
  const-member  AvailableEffectTypes  increasegatheringyield
  const-member  AvailableEffectTypes  increasehuntingyield
  const-member  BattleTypes  TERRITORY_WAR
  const-member  COPY_PRIORITY_TIERS  // Static HP must not compete with percentage-based absorb/reflect power.
  ["increaseheal"]
  const-member  DiscordTokenSources  CLERK
  const-member  DiscordTokenSources  OAUTH
  const-member  DiscordUnlinkReasons  ACCOUNT_DELETED
  const-member  DiscordUnlinkReasons  STAFF
  const-member  DiscordUnlinkReasons  USER
  const-member  MPVP_BATTLE_TYPES  TERRITORY_WAR
  const-member  PetGenders  FEMALE
  const-member  PetGenders  MALE
  const-member  PveBattleTypes  TERRITORY_WAR
  const-member  activityBonusTypes  decreasecookingtime
  const-member  activityBonusTypes  decreasecraftingtime
  const-member  activityBonusTypes  decreasefarmingtime
  const-member  activityBonusTypes  decreasegatheringtime
  const-member  activityBonusTypes  increasegatheringyield
  const-member  activityBonusTypes  increasehuntingyield
  const-member  tagTypes  decreasecookingtime
  const-member  tagTypes  decreasecraftingtime
  const-member  tagTypes  decreasefarmingtime
  const-member  tagTypes  decreasegatheringtime
  const-member  tagTypes  increasegatheringyield
  const-member  tagTypes  increasehuntingyield
  const-member  tagTypes  increasejutsuslots

BREAKING: 1 change(s) - DO NOT ADOPT (exit 1)
~~~
