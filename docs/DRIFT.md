# DRIFT.md - upstream contract drift (2026-09-27)

Upstream: studie-tech/TheNinjaRPG@8e3cde418ad5f75ff84899837c496c8172def0b1

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==
ADDITIONS
  enum-member  AllObjectives.tag_usage_win.tagType  decreasepotency
  enum-member  AllObjectives.tag_usage_win.tagType  increasepotency
  enum-member  AllTags.decreasepotency.affectedElements  ...BasicElementName
  enum-member  AllTags.decreasepotency.affectedElements  Boil
  enum-member  AllTags.decreasepotency.affectedElements  Crystal
  enum-member  AllTags.decreasepotency.affectedElements  Dust
  enum-member  AllTags.decreasepotency.affectedElements  Explosion
  enum-member  AllTags.decreasepotency.affectedElements  Ice
  enum-member  AllTags.decreasepotency.affectedElements  Lava
  enum-member  AllTags.decreasepotency.affectedElements  Light
  enum-member  AllTags.decreasepotency.affectedElements  Magnet
  enum-member  AllTags.decreasepotency.affectedElements  Metal
  enum-member  AllTags.decreasepotency.affectedElements  None
  enum-member  AllTags.decreasepotency.affectedElements  Sand
  enum-member  AllTags.decreasepotency.affectedElements  Scorch
  enum-member  AllTags.decreasepotency.affectedElements  Shadow
  enum-member  AllTags.decreasepotency.affectedElements  Storm
  enum-member  AllTags.decreasepotency.affectedElements  Wood
  enum-member  AllTags.decreasepotency.affectedElements  Yin-Yang
  enum-member  AllTags.decreasepotency.affectedTag  all
  enum-member  AllTags.decreasepotency.affectedTag  none
  enum-member  AllTags.decreasepotency.calculation  percentage
  enum-member  AllTags.decreasepotency.calculation  static
  enum-member  AllTags.decreasepotency.friendlyFire  ALL
  enum-member  AllTags.decreasepotency.friendlyFire  ENEMIES
  enum-member  AllTags.decreasepotency.friendlyFire  FRIENDLY
  enum-member  AllTags.decreasepotency.target  INHERIT
  enum-member  AllTags.decreasepotency.target  SELF
  enum-member  AllTags.increasepotency.affectedElements  ...BasicElementName
  enum-member  AllTags.increasepotency.affectedElements  Boil
  enum-member  AllTags.increasepotency.affectedElements  Crystal
  enum-member  AllTags.increasepotency.affectedElements  Dust
  enum-member  AllTags.increasepotency.affectedElements  Explosion
  enum-member  AllTags.increasepotency.affectedElements  Ice
  enum-member  AllTags.increasepotency.affectedElements  Lava
  enum-member  AllTags.increasepotency.affectedElements  Light
  enum-member  AllTags.increasepotency.affectedElements  Magnet
  enum-member  AllTags.increasepotency.affectedElements  Metal
  enum-member  AllTags.increasepotency.affectedElements  None
  enum-member  AllTags.increasepotency.affectedElements  Sand
  enum-member  AllTags.increasepotency.affectedElements  Scorch
  enum-member  AllTags.increasepotency.affectedElements  Shadow
  enum-member  AllTags.increasepotency.affectedElements  Storm
  enum-member  AllTags.increasepotency.affectedElements  Wood
  enum-member  AllTags.increasepotency.affectedElements  Yin-Yang
  enum-member  AllTags.increasepotency.affectedTag  all
  enum-member  AllTags.increasepotency.affectedTag  none
  enum-member  AllTags.increasepotency.calculation  percentage
  enum-member  AllTags.increasepotency.calculation  static
  enum-member  AllTags.increasepotency.friendlyFire  ALL
  enum-member  AllTags.increasepotency.friendlyFire  ENEMIES
  enum-member  AllTags.increasepotency.friendlyFire  FRIENDLY
  enum-member  AllTags.increasepotency.target  INHERIT
  enum-member  AllTags.increasepotency.target  SELF
  enum-member  allObjectiveSchema.tag_usage_win.tagType  decreasepotency
  enum-member  allObjectiveSchema.tag_usage_win.tagType  increasepotency
  union-variant  AllTags  decreasepotency
  union-variant  AllTags  increasepotency

no breaking changes: 58 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==
CHANGES
  now-required  item  isFarmFertilizer  optional -> required
  now-required  item  farmYieldItemId  optional -> required
  now-required  item  farmSellValue  optional -> required
  now-required  item  farmTimeReductionSeconds  optional -> required
  now-required  item  isFarmSeed  optional -> required
  now-required  item  farmPlantExperience  optional -> required
  now-required  item  farmExtractSeedItemId  optional -> required
  now-required  item  farmFertilizerExperience  optional -> required
  now-required  item  farmExtractSeedCount  optional -> required
  now-required  item  farmHarvestExperience  optional -> required
  now-required  item  farmGrowTimeSeconds  optional -> required
  now-required  item  farmMinLevel  optional -> required
ADDITIONS
  field  item  farmExtractSeedCount
  field  item  farmExtractSeedItemId
  field  item  farmFertilizerExperience
  field  item  farmGrowTimeSeconds
  field  item  farmHarvestExperience
  field  item  farmMinLevel
  field  item  farmPlantExperience
  field  item  farmSellValue
  field  item  farmTimeReductionSeconds
  field  item  farmYieldItemId
  field  item  isFarmFertilizer
  field  item  isFarmSeed
  field  quest  requiredFarmingLevel
  ftype  item  farmExtractSeedCount  number
  ftype  item  farmExtractSeedItemId  string
  ftype  item  farmFertilizerExperience  number
  ftype  item  farmGrowTimeSeconds  number
  ftype  item  farmHarvestExperience  number
  ftype  item  farmMinLevel  number
  ftype  item  farmPlantExperience  number
  ftype  item  farmSellValue  number
  ftype  item  farmTimeReductionSeconds  number
  ftype  item  farmYieldItemId  string
  ftype  item  isFarmFertilizer  boolean
  ftype  item  isFarmSeed  boolean
  ftype  quest  requiredFarmingLevel  number

BREAKING: 12 change(s) - DO NOT ADOPT (exit 1)
== 45e_DATA_constants ==
ADDITIONS
  const-member  AvailableEffectTypes  decreasepotency
  const-member  AvailableEffectTypes  increasepotency
  const-member  ContentTypes  guide
  const-member  GUIDE_HUB_CATEGORY_ORDER  bloodlines
  const-member  GUIDE_HUB_CATEGORY_ORDER  combat
  const-member  GUIDE_HUB_CATEGORY_ORDER  economy
  const-member  GUIDE_HUB_CATEGORY_ORDER  farming
  const-member  GUIDE_HUB_CATEGORY_ORDER  getting-started
  const-member  GUIDE_HUB_CATEGORY_ORDER  ranks
  const-member  GUIDE_HUB_CATEGORY_ORDER  reference
  const-member  GUIDE_HUB_CATEGORY_ORDER  villages
  const-member  GUIDE_HUB_CATEGORY_ORDER  world
  const-member  GUIDE_RESERVED_SLUGS  edit
  const-member  GUIDE_RESERVED_SLUGS  new
  const-member  GuideCategories  bloodlines
  const-member  GuideCategories  combat
  const-member  GuideCategories  economy
  const-member  GuideCategories  farming
  const-member  GuideCategories  getting-started
  const-member  GuideCategories  ranks
  const-member  GuideCategories  reference
  const-member  GuideCategories  villages
  const-member  GuideCategories  world
  const-member  ItemTypes  COOKING
  const-member  LIVE_ACTIVITY_KINDS  hospital
  const-member  LIVE_ACTIVITY_KINDS  training
  const-member  LIVE_ACTIVITY_KINDS  war
  const-member  LOG_TYPES  guide
  const-member  NonActionItemTypes  COOKING
  const-member  OBJECTIVE_TAG_TYPES  decreasepotency
  const-member  OBJECTIVE_TAG_TYPES  increasepotency
  const-member  PUSH_CATEGORIES  clan
  const-member  PUSH_CATEGORIES  combat
  const-member  PUSH_CATEGORIES  recovery
  const-member  PUSH_CATEGORIES  social
  const-member  PUSH_CATEGORIES  system
  const-member  PUSH_CATEGORIES  trade
  const-member  PUSH_CATEGORIES  training
  const-member  PUSH_CATEGORIES  war
  const-member  PUSH_PLATFORMS  android
  const-member  PUSH_PLATFORMS  ios
  const-member  PUSH_PLATFORMS  web
  const-member  PotencyTagTypes  afterburn
  const-member  PotencyTagTypes  damage
  const-member  PotencyTagTypes  decreasedamagegiven
  const-member  PotencyTagTypes  decreasedamagetaken
  const-member  PotencyTagTypes  heal
  const-member  PotencyTagTypes  increasedamagegiven
  const-member  PotencyTagTypes  increasedamagetaken
  const-member  PotencyTagTypes  increaseheal
  const-member  PotencyTagTypes  lifesteal
  const-member  PotencyTagTypes  reflect
  const-member  STORE_PLATFORMS  APPLE
  const-member  STORE_PLATFORMS  GOOGLE
  const-member  SimpleTasks  farming_collection_log
  const-member  SimpleTasks  farming_level
  const-member  SimpleTasks  plants_fertilized
  const-member  SimpleTasks  plants_harvested
  const-member  SimpleTasks  plants_watered
  const-member  SimpleTasks  seeds_planted
  ... 14 more

no breaking changes: 74 addition(s), safe to adopt (exit 0)
~~~
