# DRIFT.md - upstream contract drift (2026-10-06)

Upstream: studie-tech/TheNinjaRPG@485066e50c8d8330402accb924bacf49ebf5c2e4

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
  now-required  item  farmFertilizerExperience  optional -> required
  now-required  item  farmTimeReductionSeconds  optional -> required
  now-required  item  farmHarvestExperience  optional -> required
  now-required  item  farmSellValue  optional -> required
  now-required  item  farmMinLevel  optional -> required
  now-required  item  farmYieldItemId  optional -> required
  now-required  item  farmExtractSeedItemId  optional -> required
  now-required  item  farmPlantExperience  optional -> required
  now-required  item  farmExtractSeedCount  optional -> required
  now-required  item  isFarmFertilizer  optional -> required
  now-required  item  isFarmSeed  optional -> required
  now-required  item  farmGrowTimeSeconds  optional -> required
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
  field  jutsu  elementClassification
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
  ftype  jutsu  elementClassification  enum
  ftype  quest  requiredFarmingLevel  number

BREAKING: 12 change(s) - DO NOT ADOPT (exit 1)
== 45e_DATA_constants ==
ADDITIONS
  const-member  AvailableEffectTypes  decreasepotency
  const-member  AvailableEffectTypes  increasepotency
  const-member  ContentAuditFocuses  animation
  const-member  ContentAuditFocuses  balance
  const-member  ContentAuditFocuses  consistency
  const-member  ContentAuditFocuses  grammar
  const-member  ContentAuditFocuses  new_content
  const-member  ContentAuditFocuses  sound
  const-member  ContentAuditFocuses  visual
  const-member  ContentProposalBasisRoles  CONTEXT
  const-member  ContentProposalBasisRoles  TARGET
  const-member  ContentProposalCategories  ANIMATION
  const-member  ContentProposalCategories  BALANCE
  const-member  ContentProposalCategories  CONSISTENCY
  const-member  ContentProposalCategories  GRAMMAR
  const-member  ContentProposalCategories  NEW_CONTENT
  const-member  ContentProposalCategories  SOUND
  const-member  ContentProposalCategories  VISUAL
  const-member  ContentProposalEntityTypes  AI
  const-member  ContentProposalEntityTypes  BADGE
  const-member  ContentProposalEntityTypes  BLOODLINE
  const-member  ContentProposalEntityTypes  GAME_ASSET
  const-member  ContentProposalEntityTypes  ITEM
  const-member  ContentProposalEntityTypes  JUTSU
  const-member  ContentProposalEntityTypes  QUEST
  const-member  ContentProposalMediaKinds  ANIMATION
  const-member  ContentProposalMediaKinds  IMAGE
  const-member  ContentProposalMediaKinds  SFX
  const-member  ContentProposalMediaSources  CATALOG
  const-member  ContentProposalMediaSources  EPIDEMIC
  const-member  ContentProposalMediaSources  GENERATED
  const-member  ContentProposalOperations  CREATE
  const-member  ContentProposalOperations  UPDATE
  const-member  ContentProposalRejectReasons  FACTUALLY_WRONG
  const-member  ContentProposalRejectReasons  NOT_AN_IMPROVEMENT
  const-member  ContentProposalRejectReasons  OTHER
  const-member  ContentProposalRejectReasons  STYLE_MISMATCH
  const-member  ContentProposalRejectReasons  WRONG_CHANGE
  const-member  ContentProposalSources  AGENT
  const-member  ContentProposalSources  STAFF
  const-member  ContentProposalStatuses  APPLIED
  const-member  ContentProposalStatuses  OUTDATED
  const-member  ContentProposalStatuses  PENDING
  const-member  ContentProposalStatuses  REJECTED
  const-member  ContentProposalStatuses  REVERTED
  const-member  ContentTypes  guide
  const-member  FACTION_VILLAGE_TYPES  HIDEOUT
  const-member  FACTION_VILLAGE_TYPES  TOWN
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
  ... 83 more

no breaking changes: 143 addition(s), safe to adopt (exit 0)
~~~
