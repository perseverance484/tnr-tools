# DRIFT.md - upstream contract drift (2026-08-31)

Upstream: studie-tech/TheNinjaRPG@b3981ef19958d1ecb7637a6b7b71f25293d1df97

The extracted 45x contract hashes changed vs the last sentinel
baseline. SIGNAL ONLY: nothing was adopted. Adoption is manual
through the schema_diff gate (docs/00_INDEX.md regen row).

Structural diff, SHIPPED vs upstream:

~~~
== 45c_DATA_constructors ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==
CHANGES
  now-required  item  isFarmSeed  optional -> required
  now-required  item  farmExtractSeedItemId  optional -> required
  now-required  item  farmPlantExperience  optional -> required
  now-required  item  isFarmFertilizer  optional -> required
  now-required  item  farmExtractSeedCount  optional -> required
  now-required  item  farmTimeReductionSeconds  optional -> required
  now-required  item  farmGrowTimeSeconds  optional -> required
  now-required  item  farmSellValue  optional -> required
  now-required  item  farmYieldItemId  optional -> required
  now-required  item  farmHarvestExperience  optional -> required
  now-required  item  farmMinLevel  optional -> required
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
  const-member  ItemTypes  COOKING
  const-member  NonActionItemTypes  COOKING
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

no breaking changes: 20 addition(s), safe to adopt (exit 0)
~~~
