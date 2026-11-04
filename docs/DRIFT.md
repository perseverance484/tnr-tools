# DRIFT.md - upstream contract drift (2026-11-04)

Upstream: studie-tech/TheNinjaRPG@d0fc2210740543ece8b3a9464e7de1018b060c4e

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==
REMOVALS
  enum-member  allObjectiveSchema.SimpleObjective.reward_mastery_rank  ADEPT
  enum-member  allObjectiveSchema.SimpleObjective.reward_mastery_rank  LEGENDARY
  enum-member  allObjectiveSchema.SimpleObjective.reward_mastery_rank  MASTER
  enum-member  allObjectiveSchema.SimpleObjective.reward_mastery_rank  NONE
  enum-member  allObjectiveSchema.SimpleObjective.reward_mastery_rank  NOVICE
  enum-member  allObjectiveSchema.SimpleObjective.reward_mastery_stat  None
  enum-member  allObjectiveSchema.SimpleObjective.reward_rank  CHUNIN
  enum-member  allObjectiveSchema.SimpleObjective.reward_rank  ELDER
  enum-member  allObjectiveSchema.SimpleObjective.reward_rank  ELITE JONIN
  enum-member  allObjectiveSchema.SimpleObjective.reward_rank  GENIN
  enum-member  allObjectiveSchema.SimpleObjective.reward_rank  JONIN
  enum-member  allObjectiveSchema.SimpleObjective.reward_rank  NONE
  enum-member  allObjectiveSchema.SimpleObjective.reward_rank  STUDENT
  enum-member  allObjectiveSchema.SimpleObjective.reward_village_membership  AKASUMI
  enum-member  allObjectiveSchema.SimpleObjective.reward_village_membership  AKIKAZE
  enum-member  allObjectiveSchema.SimpleObjective.reward_village_membership  HYORIN
  enum-member  allObjectiveSchema.SimpleObjective.reward_village_membership  NONE
  enum-member  allObjectiveSchema.SimpleObjective.reward_village_membership  SHIROHANA
  enum-member  allObjectiveSchema.SimpleObjective.reward_village_membership  TSUKIMORI
  enum-member  allObjectiveSchema.SimpleObjective.task  a_crimes_total
  enum-member  allObjectiveSchema.SimpleObjective.task  a_missions_total
  enum-member  allObjectiveSchema.SimpleObjective.task  arena_kills
  enum-member  allObjectiveSchema.SimpleObjective.task  b_crimes_total
  enum-member  allObjectiveSchema.SimpleObjective.task  b_missions_total
  enum-member  allObjectiveSchema.SimpleObjective.task  battle_pyramids_completed
  enum-member  allObjectiveSchema.SimpleObjective.task  c_crimes_total
  enum-member  allObjectiveSchema.SimpleObjective.task  c_missions_total
  enum-member  allObjectiveSchema.SimpleObjective.task  combined_mission_effort
  enum-member  allObjectiveSchema.SimpleObjective.task  crafting_experience
  enum-member  allObjectiveSchema.SimpleObjective.task  crafting_experience_gained
  enum-member  allObjectiveSchema.SimpleObjective.task  creatures_hunted
  enum-member  allObjectiveSchema.SimpleObjective.task  d_crimes_total
  enum-member  allObjectiveSchema.SimpleObjective.task  d_missions_total
  enum-member  allObjectiveSchema.SimpleObjective.task  days_as_kage
  enum-member  allObjectiveSchema.SimpleObjective.task  days_in_village
  enum-member  allObjectiveSchema.SimpleObjective.task  dungeons_completed
  enum-member  allObjectiveSchema.SimpleObjective.task  errands_total
  enum-member  allObjectiveSchema.SimpleObjective.task  espionage
  enum-member  allObjectiveSchema.SimpleObjective.task  events_completed
  enum-member  allObjectiveSchema.SimpleObjective.task  farming_collection_log
  enum-member  allObjectiveSchema.SimpleObjective.task  farming_level
  enum-member  allObjectiveSchema.SimpleObjective.task  gathering_experience
  enum-member  allObjectiveSchema.SimpleObjective.task  gathering_experience_gained
  enum-member  allObjectiveSchema.SimpleObjective.task  herbs_gathered
  enum-member  allObjectiveSchema.SimpleObjective.task  hunting_experience
  enum-member  allObjectiveSchema.SimpleObjective.task  hunting_experience_gained
  enum-member  allObjectiveSchema.SimpleObjective.task  items_crafted
  enum-member  allObjectiveSchema.SimpleObjective.task  jutsus_mastered
  enum-member  allObjectiveSchema.SimpleObjective.task  medical_experience
  enum-member  allObjectiveSchema.SimpleObjective.task  medical_experience_gained
  enum-member  allObjectiveSchema.SimpleObjective.task  minutes_passed
  enum-member  allObjectiveSchema.SimpleObjective.task  minutes_training
  enum-member  allObjectiveSchema.SimpleObjective.task  overworld_ai_fought
  enum-member  allObjectiveSchema.SimpleObjective.task  overworld_quests_completed
  enum-member  allObjectiveSchema.SimpleObjective.task  plants_fertilized
  enum-member  allObjectiveSchema.SimpleObjective.task  plants_harvested
  enum-member  allObjectiveSchema.SimpleObjective.task  plants_watered
  enum-member  allObjectiveSchema.SimpleObjective.task  pvp_kills
  enum-member  allObjectiveSchema.SimpleObjective.task  pvp_participated
  enum-member  allObjectiveSchema.SimpleObjective.task  raids_completed
  ... 1248 more
ADDITIONS
  enum-member  AllObjectives.tag_usage_win.tagType  curse
  enum-member  AllObjectives.tag_usage_win.tagType  parry
  enum-member  AllTags.curse.friendlyFire  ALL
  enum-member  AllTags.curse.friendlyFire  ENEMIES
  enum-member  AllTags.curse.friendlyFire  FRIENDLY
  enum-member  AllTags.curse.target  COORDINATES
  enum-member  AllTags.curse.target  INHERIT
  enum-member  AllTags.curse.target  SELF
  enum-member  AllTags.parry.elements  Boil
  enum-member  AllTags.parry.elements  Crystal
  enum-member  AllTags.parry.elements  Dust
  enum-member  AllTags.parry.elements  Earth
  enum-member  AllTags.parry.elements  Explosion
  enum-member  AllTags.parry.elements  Fire
  enum-member  AllTags.parry.elements  Ice
  enum-member  AllTags.parry.elements  Lava
  enum-member  AllTags.parry.elements  Light
  enum-member  AllTags.parry.elements  Lightning
  enum-member  AllTags.parry.elements  Magnet
  enum-member  AllTags.parry.elements  Metal
  enum-member  AllTags.parry.elements  None
  enum-member  AllTags.parry.elements  Sand
  enum-member  AllTags.parry.elements  Scorch
  enum-member  AllTags.parry.elements  Shadow
  enum-member  AllTags.parry.elements  Storm
  enum-member  AllTags.parry.elements  Water
  enum-member  AllTags.parry.elements  Wind
  enum-member  AllTags.parry.elements  Wood
  enum-member  AllTags.parry.elements  Yin-Yang
  enum-member  AllTags.parry.friendlyFire  ALL
  enum-member  AllTags.parry.friendlyFire  ENEMIES
  enum-member  AllTags.parry.friendlyFire  FRIENDLY
  enum-member  AllTags.parry.generalTypes  Highest
  enum-member  AllTags.parry.generalTypes  Intelligence
  enum-member  AllTags.parry.generalTypes  Speed
  enum-member  AllTags.parry.generalTypes  Strength
  enum-member  AllTags.parry.generalTypes  Willpower
  enum-member  AllTags.parry.target  COORDINATES
  enum-member  AllTags.parry.target  INHERIT
  enum-member  AllTags.parry.target  SELF
  union-variant  AllTags  curse
  union-variant  AllTags  parry
  variant-field  AllTags.curse  appearAnimation
  variant-field  AllTags.curse  appearSfx
  variant-field  AllTags.curse  calculation
  variant-field  AllTags.curse  coordinateTargeting
  variant-field  AllTags.curse  description
  variant-field  AllTags.curse  direction
  variant-field  AllTags.curse  disappearAnimation
  variant-field  AllTags.curse  disappearSfx
  variant-field  AllTags.curse  friendlyFire
  variant-field  AllTags.curse  power
  variant-field  AllTags.curse  powerPerLevel
  variant-field  AllTags.curse  rounds
  variant-field  AllTags.curse  staticAnimation
  variant-field  AllTags.curse  staticAssetPath
  variant-field  AllTags.curse  target
  variant-field  AllTags.curse  timeTracker
  variant-field  AllTags.curse  type
  variant-field  AllTags.parry  appearAnimation
  ... 18 more

BREAKING: 1308 change(s) - DO NOT ADOPT (exit 1)
== 45d_DATA_entity_schemas ==
ADDITIONS
  field  gameAsset  lpcConfig
  field  item  lpcColor
  field  item  lpcProfile
  field  itemVariant  lpcColor
  field  itemVariant  lpcProfile

no breaking changes: 5 addition(s), safe to adopt (exit 0)
== 45e_DATA_constants ==
REMOVALS
  const-member  CURRENCY_TYPES  MONEY
  const-member  CURRENCY_TYPES  REPUTATION
  const-member  CURRENCY_TYPES  SEICHI_SILVER
  const-member  IMG_URL_ASSISTANT_ALTERNATIVES  https://ui0arpl8sm.ufs.sh/f/content-2bwqugh_JdcS55ALvzfhV.webp
  const-member  IMG_URL_ASSISTANT_ALTERNATIVES  https://ui0arpl8sm.ufs.sh/f/content-6jMP1VF5X1Zu2wppt4vec.webp
  const-member  IMG_URL_ASSISTANT_ALTERNATIVES  https://ui0arpl8sm.ufs.sh/f/content-NBVEXpYD8aRhwFof6jq45.webp
  const-member  IMG_URL_ASSISTANT_ALTERNATIVES  https://ui0arpl8sm.ufs.sh/f/content-jMcyVJrtGlAclqlBlbJFR.webp
  const-member  IMG_URL_ASSISTANT_ALTERNATIVES  https://ui0arpl8sm.ufs.sh/f/content-jlYDeVvWQIv0UDYJndtBn.webp
  const-member  IMG_URL_ASSISTANT_ALTERNATIVES  https://ui0arpl8sm.ufs.sh/f/content-r6_prvN1P_dntlkbOEJSL.webp
  const-member  PveBattleTypes  ARENA
  const-member  PveBattleTypes  CLAN_CHALLENGE
  const-member  PveBattleTypes  HUNTING
  const-member  PveBattleTypes  OVERWORLD
  const-member  PveBattleTypes  QUEST
  const-member  PveBattleTypes  RAID
  const-member  PveBattleTypes  RANDOM_ENCOUNTER
  const-member  PveBattleTypes  TERRITORY_WAR
  const-member  PveBattleTypes  TRAINING
  const-member  PveBattleTypes  VILLAGE_PROTECTOR
ADDITIONS
  const-member  ActiveBanStates  BAN_ACTIVATED
  const-member  ActiveBanStates  BAN_ESCALATED
  const-member  AvailableEffectTypes  curse
  const-member  AvailableEffectTypes  parry
  const-member  FARM_SHOP_ENTRY_TYPES  EXTRACTOR
  const-member  FARM_SHOP_ENTRY_TYPES  FERTILIZER
  const-member  FARM_SHOP_ENTRY_TYPES  PLOT
  const-member  FARM_SHOP_ENTRY_TYPES  SEED
  const-member  GameAssetTypes  LPC
  const-member  OBJECTIVE_TAG_TYPES  curse
  const-member  OBJECTIVE_TAG_TYPES  parry
  const-member  POST_DAMAGE_MODIFIER_TYPES  parry
  const-member  POST_PIERCE_TAGS  parry
  const-member  PotencyTagTypes  curse
  const-member  PotencyTagTypes  parry
  const-member  allState  spriteAction
  const-member  allState  spriteAppearance
  const-member  damageDerivedTagTypes  parry
  const-member  publicState  spriteAction
  const-member  publicState  spriteAppearance
  const-member  questBuffTypes  curse
  const-member  questBuffTypes  parry
  const-member  tagTypes  curse
  const-member  tagTypes  parry

BREAKING: 19 change(s) - DO NOT ADOPT (exit 1)
~~~
