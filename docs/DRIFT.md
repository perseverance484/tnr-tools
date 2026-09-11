# DRIFT.md - upstream contract drift (2026-09-11)

Upstream: studie-tech/TheNinjaRPG@98d0eca5c2e922f3b41e56120f096c072645c1f0

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==
CHANGES
  now-required  item  isFarmSeed  optional -> required
  now-required  item  farmMinLevel  optional -> required
  now-required  item  farmExtractSeedItemId  optional -> required
  now-required  item  farmHarvestExperience  optional -> required
  now-required  item  farmExtractSeedCount  optional -> required
  now-required  item  isFarmFertilizer  optional -> required
  now-required  item  farmSellValue  optional -> required
  now-required  item  farmGrowTimeSeconds  optional -> required
  now-required  item  farmTimeReductionSeconds  optional -> required
  now-required  item  farmPlantExperience  optional -> required
  now-required  item  farmYieldItemId  optional -> required
  now-required  item  farmFertilizerExperience  optional -> required
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
  const-member  STORE_PLATFORMS  APPLE
  const-member  STORE_PLATFORMS  GOOGLE
  const-member  SimpleTasks  farming_collection_log
  const-member  SimpleTasks  farming_level
  const-member  SimpleTasks  plants_fertilized
  const-member  SimpleTasks  plants_harvested
  const-member  SimpleTasks  plants_watered
  const-member  SimpleTasks  seeds_planted
  const-member  TavernColorPresets  CHARCOAL
  const-member  TavernColorPresets  COBALT
  const-member  TavernColorPresets  CRIMSON
  const-member  TavernColorPresets  DEFAULT
  const-member  TavernColorPresets  FUCHSIA
  const-member  TavernColorPresets  GOLD
  const-member  TavernColorPresets  LIME
  const-member  TavernColorPresets  MIDNIGHT
  const-member  TavernColorPresets  MINT
  const-member  TavernColorPresets  NAVY
  const-member  TavernColorPresets  SLATE
  const-member  TavernColorPresets  YELLOW

no breaking changes: 58 addition(s), safe to adopt (exit 0)
~~~
