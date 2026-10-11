# DRIFT.md - upstream contract drift (2026-10-11)

Upstream: studie-tech/TheNinjaRPG@21b8f0eb0569fa16e6af2b1f1ed95e7b5a879f55

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==
REMOVALS
  enum-member  AllTags.absorb.statTypes  Bukijutsu
  enum-member  AllTags.absorb.statTypes  Genjutsu
  enum-member  AllTags.absorb.statTypes  Highest
  enum-member  AllTags.absorb.statTypes  Ninjutsu
  enum-member  AllTags.absorb.statTypes  Taijutsu
  enum-member  AllTags.afterburn.statTypes  Bukijutsu
  enum-member  AllTags.afterburn.statTypes  Genjutsu
  enum-member  AllTags.afterburn.statTypes  Highest
  enum-member  AllTags.afterburn.statTypes  Ninjutsu
  enum-member  AllTags.afterburn.statTypes  Taijutsu
  enum-member  AllTags.damage.statTypes  Bukijutsu
  enum-member  AllTags.damage.statTypes  Genjutsu
  enum-member  AllTags.damage.statTypes  Highest
  enum-member  AllTags.damage.statTypes  Ninjutsu
  enum-member  AllTags.damage.statTypes  Taijutsu
  enum-member  AllTags.decreasedamagegiven.generalTypes  Highest
  enum-member  AllTags.decreasedamagegiven.generalTypes  Intelligence
  enum-member  AllTags.decreasedamagegiven.generalTypes  Speed
  enum-member  AllTags.decreasedamagegiven.generalTypes  Strength
  enum-member  AllTags.decreasedamagegiven.generalTypes  Willpower
  enum-member  AllTags.decreasedamagegiven.statTypes  Bukijutsu
  enum-member  AllTags.decreasedamagegiven.statTypes  Genjutsu
  enum-member  AllTags.decreasedamagegiven.statTypes  Highest
  enum-member  AllTags.decreasedamagegiven.statTypes  Ninjutsu
  enum-member  AllTags.decreasedamagegiven.statTypes  Taijutsu
  enum-member  AllTags.decreasedamagetaken.generalTypes  Highest
  enum-member  AllTags.decreasedamagetaken.generalTypes  Intelligence
  enum-member  AllTags.decreasedamagetaken.generalTypes  Speed
  enum-member  AllTags.decreasedamagetaken.generalTypes  Strength
  enum-member  AllTags.decreasedamagetaken.generalTypes  Willpower
  enum-member  AllTags.decreasedamagetaken.statTypes  Bukijutsu
  enum-member  AllTags.decreasedamagetaken.statTypes  Genjutsu
  enum-member  AllTags.decreasedamagetaken.statTypes  Highest
  enum-member  AllTags.decreasedamagetaken.statTypes  Ninjutsu
  enum-member  AllTags.decreasedamagetaken.statTypes  Taijutsu
  enum-member  AllTags.decreasemaxpools.poolsAffected  Chakra
  enum-member  AllTags.decreasemaxpools.poolsAffected  Health
  enum-member  AllTags.decreasemaxpools.poolsAffected  Stamina
  enum-member  AllTags.decreasestat.statTypes  Bukijutsu
  enum-member  AllTags.decreasestat.statTypes  Genjutsu
  enum-member  AllTags.decreasestat.statTypes  Highest
  enum-member  AllTags.decreasestat.statTypes  Ninjutsu
  enum-member  AllTags.decreasestat.statTypes  Taijutsu
  enum-member  AllTags.elementalseal.elements  ...BasicElementName
  enum-member  AllTags.elementalseal.elements  Boil
  enum-member  AllTags.elementalseal.elements  Crystal
  enum-member  AllTags.elementalseal.elements  Dust
  enum-member  AllTags.elementalseal.elements  Explosion
  enum-member  AllTags.elementalseal.elements  Ice
  enum-member  AllTags.elementalseal.elements  Lava
  enum-member  AllTags.elementalseal.elements  Light
  enum-member  AllTags.elementalseal.elements  Magnet
  enum-member  AllTags.elementalseal.elements  Metal
  enum-member  AllTags.elementalseal.elements  None
  enum-member  AllTags.elementalseal.elements  Sand
  enum-member  AllTags.elementalseal.elements  Scorch
  enum-member  AllTags.elementalseal.elements  Shadow
  enum-member  AllTags.elementalseal.elements  Storm
  enum-member  AllTags.elementalseal.elements  Wood
  enum-member  AllTags.elementalseal.elements  Yin-Yang
  ... 159 more
ADDITIONS
  enum-member  AllObjectives.bloodline_collection.bloodlineRank  ALL
  enum-member  AllObjectives.tag_usage_win.tagType  decreasemastery
  enum-member  AllObjectives.tag_usage_win.tagType  decreasepotency
  enum-member  AllObjectives.tag_usage_win.tagType  diffuse
  enum-member  AllObjectives.tag_usage_win.tagType  increasemastery
  enum-member  AllObjectives.tag_usage_win.tagType  increasepotency
  enum-member  AllObjectives.train_specific_jutsu.masteryType  None
  enum-member  AllObjectives.use_specific_jutsu_combat.combatType  Any
  enum-member  AllObjectives.use_specific_jutsu_combat.combatType  PVE
  enum-member  AllObjectives.use_specific_jutsu_combat.combatType  PVP
  enum-member  AllObjectives.use_specific_jutsu_combat.masteryType  None
  enum-member  AllTags.absorb.target  COORDINATES
  enum-member  AllTags.activatesagemode.target  COORDINATES
  enum-member  AllTags.afterburn.target  COORDINATES
  enum-member  AllTags.barrier.target  COORDINATES
  enum-member  AllTags.buffprevent.target  COORDINATES
  enum-member  AllTags.cleanse.target  COORDINATES
  enum-member  AllTags.cleanseprevent.target  COORDINATES
  enum-member  AllTags.clear.target  COORDINATES
  enum-member  AllTags.clearprevent.target  COORDINATES
  enum-member  AllTags.clone.target  COORDINATES
  enum-member  AllTags.consume.target  COORDINATES
  enum-member  AllTags.copy.target  COORDINATES
  enum-member  AllTags.damage.target  COORDINATES
  enum-member  AllTags.debuffprevent.target  COORDINATES
  enum-member  AllTags.decreasecooldown.target  COORDINATES
  enum-member  AllTags.decreasedamagegiven.target  COORDINATES
  enum-member  AllTags.decreasedamagetaken.target  COORDINATES
  enum-member  AllTags.decreaseheal.target  COORDINATES
  enum-member  AllTags.decreasemastery.calculation  percentage
  enum-member  AllTags.decreasemastery.calculation  static
  enum-member  AllTags.decreasemastery.friendlyFire  ALL
  enum-member  AllTags.decreasemastery.friendlyFire  ENEMIES
  enum-member  AllTags.decreasemastery.friendlyFire  FRIENDLY
  enum-member  AllTags.decreasemastery.masteryTypes  Bloodline
  enum-member  AllTags.decreasemastery.masteryTypes  Bukijutsu
  enum-member  AllTags.decreasemastery.masteryTypes  Genjutsu
  enum-member  AllTags.decreasemastery.masteryTypes  Ninjutsu
  enum-member  AllTags.decreasemastery.masteryTypes  Sage
  enum-member  AllTags.decreasemastery.masteryTypes  Taijutsu
  enum-member  AllTags.decreasemastery.target  COORDINATES
  enum-member  AllTags.decreasemastery.target  INHERIT
  enum-member  AllTags.decreasemastery.target  SELF
  enum-member  AllTags.decreasemaxpools.poolsAffected  ...PoolTypes
  enum-member  AllTags.decreasemaxpools.poolsAffected  Energy
  enum-member  AllTags.decreasemaxpools.target  COORDINATES
  enum-member  AllTags.decreasepoolcost.target  COORDINATES
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
  ... 170 more

BREAKING: 219 change(s) - DO NOT ADOPT (exit 1)
== 45d_DATA_entity_schemas ==
REMOVALS
  field  aiRule  action
  field  aiRule  conditions
  field  item  requiredBukijutsuDefence
  field  item  requiredBukijutsuOffence
  field  item  requiredGenjutsuDefence
  field  item  requiredGenjutsuOffence
  field  item  requiredNinjutsuDefence
  field  item  requiredNinjutsuOffence
  field  item  requiredTaijutsuDefence
  field  item  requiredTaijutsuOffence
  field  jutsu  requiredBukijutsuDefence
  field  jutsu  requiredBukijutsuOffence
  field  jutsu  requiredGenjutsuDefence
  field  jutsu  requiredGenjutsuOffence
  field  jutsu  requiredNinjutsuDefence
  field  jutsu  requiredNinjutsuOffence
  field  jutsu  requiredTaijutsuDefence
  field  jutsu  requiredTaijutsuOffence
  ftype  aiRule  action  object
  ftype  aiRule  conditions  array
  ftype  item  requiredBukijutsuDefence  preprocess
  ftype  item  requiredBukijutsuOffence  preprocess
  ftype  item  requiredGenjutsuDefence  preprocess
  ftype  item  requiredGenjutsuOffence  preprocess
  ftype  item  requiredIntelligence  preprocess
  ftype  item  requiredNinjutsuDefence  preprocess
  ftype  item  requiredNinjutsuOffence  preprocess
  ftype  item  requiredSpeed  preprocess
  ftype  item  requiredStrength  preprocess
  ftype  item  requiredTaijutsuDefence  preprocess
  ftype  item  requiredTaijutsuOffence  preprocess
  ftype  item  requiredWillpower  preprocess
  ftype  jutsu  requiredBukijutsuDefence  preprocess
  ftype  jutsu  requiredBukijutsuOffence  preprocess
  ftype  jutsu  requiredGenjutsuDefence  preprocess
  ftype  jutsu  requiredGenjutsuOffence  preprocess
  ftype  jutsu  requiredIntelligence  preprocess
  ftype  jutsu  requiredNinjutsuDefence  preprocess
  ftype  jutsu  requiredNinjutsuOffence  preprocess
  ftype  jutsu  requiredSpeed  preprocess
  ftype  jutsu  requiredStrength  preprocess
  ftype  jutsu  requiredTaijutsuDefence  preprocess
  ftype  jutsu  requiredTaijutsuOffence  preprocess
  ftype  jutsu  requiredWillpower  preprocess
CHANGES
  now-required  item  farmPlantExperience  optional -> required
  now-required  item  farmExtractSeedCount  optional -> required
  now-required  jutsu  requiredNinjutsuMastery  optional -> required
  now-required  item  farmExtractSeedItemId  optional -> required
  now-required  item  requiredBloodlineMastery  optional -> required
  now-required  item  requiredBukijutsuMastery  optional -> required
  now-required  item  farmFertilizerExperience  optional -> required
  now-required  jutsu  requiredBloodlineMastery  optional -> required
  now-required  jutsu  requiredBukijutsuMastery  optional -> required
  now-required  item  farmYieldItemId  optional -> required
  now-required  item  requiredSageMastery  optional -> required
  now-required  item  farmMinLevel  optional -> required
  now-required  item  farmTimeReductionSeconds  optional -> required
  now-required  item  requiredGenjutsuMastery  optional -> required
  now-required  item  farmGrowTimeSeconds  optional -> required
  now-required  item  requiredTaijutsuMastery  optional -> required
  now-required  jutsu  requiredSageMastery  optional -> required
  now-required  item  isFarmSeed  optional -> required
  now-required  item  farmSellValue  optional -> required
  now-required  item  requiredNinjutsuMastery  optional -> required
  now-required  item  farmHarvestExperience  optional -> required
  now-required  jutsu  requiredGenjutsuMastery  optional -> required
  now-required  item  isFarmFertilizer  optional -> required
  now-required  jutsu  requiredTaijutsuMastery  optional -> required
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
  field  item  requiredBloodlineMastery
  field  item  requiredBukijutsuMastery
  field  item  requiredGenjutsuMastery
  field  item  requiredNinjutsuMastery
  field  item  requiredSageMastery
  field  item  requiredSkillId
  field  item  requiredTaijutsuMastery
  field  jutsu  bloodlineReskinId
  field  jutsu  elementClassification
  field  jutsu  requiredBloodlineMastery
  field  jutsu  requiredBukijutsuMastery
  field  jutsu  requiredGenjutsuMastery
  field  jutsu  requiredNinjutsuMastery
  field  jutsu  requiredSageMastery
  field  jutsu  requiredSkillId
  field  jutsu  requiredTaijutsuMastery
  field  jutsu  reskinParentJutsuId
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
  ftype  item  requiredSkillId  string
  ftype  jutsu  bloodlineReskinId  string
  ftype  jutsu  elementClassification  enum
  ftype  jutsu  requiredSkillId  string
  ftype  jutsu  reskinParentJutsuId  string
  ftype  quest  requiredFarmingLevel  number

BREAKING: 42 change(s) - DO NOT ADOPT (exit 1)
== 45e_DATA_constants ==
REMOVALS
  const-member  StatNames  bukijutsuDefence
  const-member  StatNames  bukijutsuOffence
  const-member  StatNames  genjutsuDefence
  const-member  StatNames  genjutsuOffence
  const-member  StatNames  ninjutsuDefence
  const-member  StatNames  ninjutsuOffence
  const-member  StatNames  taijutsuDefence
  const-member  StatNames  taijutsuOffence
  const-member  StatTypes  Highest
  const-member  UserStatNames  bukijutsuDefence
  const-member  UserStatNames  bukijutsuOffence
  const-member  UserStatNames  genjutsuDefence
  const-member  UserStatNames  genjutsuOffence
  const-member  UserStatNames  intelligence
  const-member  UserStatNames  ninjutsuDefence
  const-member  UserStatNames  ninjutsuOffence
  const-member  UserStatNames  speed
  const-member  UserStatNames  strength
  const-member  UserStatNames  taijutsuDefence
  const-member  UserStatNames  taijutsuOffence
  const-member  UserStatNames  willpower
  const-member  privateState  bukijutsuDefence
  const-member  privateState  bukijutsuOffence
  const-member  privateState  genjutsuDefence
  const-member  privateState  genjutsuOffence
  const-member  privateState  highestDefence
  const-member  privateState  highestOffence
  const-member  privateState  ninjutsuDefence
  const-member  privateState  ninjutsuOffence
  const-member  privateState  taijutsuDefence
  const-member  privateState  taijutsuOffence
  const-member  privateState  updatedAt
  const-member  publicState  anbuId
  const-member  publicState  basicActions
  const-member  publicState  dailySageActivations
  const-member  publicState  items
  const-member  publicState  jutsus
  const-member  publicState  location
  const-member  publicState  medicalExperience
  const-member  publicState  regeneration
  const-member  publicState  relationIds
  const-member  publicState  sageMasteryExperience
  const-member  publicState  sageModeId
  const-member  publicState  sector
  const-member  publicState  warIds
ADDITIONS
  const-member  AUCTION_OFFER_TYPES  REQUEST
  const-member  AUCTION_OFFER_TYPES  TRADE
  const-member  AttackMethods  COORDINATES
  const-member  AvailableActionTargets  COORDINATE
  const-member  AvailableEffectTypes  decreasemastery
  const-member  AvailableEffectTypes  decreasepotency
  const-member  AvailableEffectTypes  diffuse
  const-member  AvailableEffectTypes  increasemastery
  const-member  AvailableEffectTypes  increasepotency
  const-member  AvailableTargets  HIGHEST_MAX_HEALTH_ALLY
  const-member  AvailableTargets  HIGHEST_MAX_HEALTH_OPPONENT
  const-member  AvailableTargets  LOWEST_HEALTH_OPPONENT
  const-member  AvailableTargets  LOWEST_MAX_HEALTH_ALLY
  const-member  BaseTagTargets  COORDINATES
  const-member  CombatStatNames  defence
  const-member  CombatStatNames  intelligence
  const-member  CombatStatNames  offence
  const-member  CombatStatNames  speed
  const-member  CombatStatNames  strength
  const-member  CombatStatNames  willpower
  const-member  CombatStatTypes  Defence
  const-member  CombatStatTypes  Offence
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
  ... 190 more

BREAKING: 45 change(s) - DO NOT ADOPT (exit 1)
~~~
