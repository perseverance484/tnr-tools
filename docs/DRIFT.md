# DRIFT.md - upstream contract drift (2026-11-14)

Upstream: studie-tech/TheNinjaRPG@25800453300bd613a6e7b9bbbd718127ecd45cb8

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==
REMOVALS
  enum-member  AllTags.absorb.calculation  percentage
  enum-member  AllTags.absorb.elements  Boil
  enum-member  AllTags.absorb.elements  Crystal
  enum-member  AllTags.absorb.elements  Dust
  enum-member  AllTags.absorb.elements  Earth
  enum-member  AllTags.absorb.elements  Explosion
  enum-member  AllTags.absorb.elements  Fire
  enum-member  AllTags.absorb.elements  Ice
  enum-member  AllTags.absorb.elements  Lava
  enum-member  AllTags.absorb.elements  Light
  enum-member  AllTags.absorb.elements  Lightning
  enum-member  AllTags.absorb.elements  Magnet
  enum-member  AllTags.absorb.elements  Metal
  enum-member  AllTags.absorb.elements  None
  enum-member  AllTags.absorb.elements  Sand
  enum-member  AllTags.absorb.elements  Scorch
  enum-member  AllTags.absorb.elements  Shadow
  enum-member  AllTags.absorb.elements  Storm
  enum-member  AllTags.absorb.elements  Water
  enum-member  AllTags.absorb.elements  Wind
  enum-member  AllTags.absorb.elements  Wood
  enum-member  AllTags.absorb.elements  Yin-Yang
  enum-member  AllTags.absorb.friendlyFire  ALL
  enum-member  AllTags.absorb.friendlyFire  ENEMIES
  enum-member  AllTags.absorb.friendlyFire  FRIENDLY
  enum-member  AllTags.absorb.generalTypes  Highest
  enum-member  AllTags.absorb.generalTypes  Intelligence
  enum-member  AllTags.absorb.generalTypes  Speed
  enum-member  AllTags.absorb.generalTypes  Strength
  enum-member  AllTags.absorb.generalTypes  Willpower
  enum-member  AllTags.absorb.poolsAffected  Chakra
  enum-member  AllTags.absorb.poolsAffected  Health
  enum-member  AllTags.absorb.poolsAffected  Stamina
  enum-member  AllTags.absorb.target  COORDINATES
  enum-member  AllTags.absorb.target  INHERIT
  enum-member  AllTags.absorb.target  SELF
  enum-member  AllTags.activatesagemode.calculation  static
  enum-member  AllTags.activatesagemode.friendlyFire  ALL
  enum-member  AllTags.activatesagemode.friendlyFire  ENEMIES
  enum-member  AllTags.activatesagemode.friendlyFire  FRIENDLY
  enum-member  AllTags.activatesagemode.target  COORDINATES
  enum-member  AllTags.activatesagemode.target  INHERIT
  enum-member  AllTags.activatesagemode.target  SELF
  enum-member  AllTags.afterburn.calculation  percentage
  enum-member  AllTags.afterburn.calculation  static
  enum-member  AllTags.afterburn.elements  Boil
  enum-member  AllTags.afterburn.elements  Crystal
  enum-member  AllTags.afterburn.elements  Dust
  enum-member  AllTags.afterburn.elements  Earth
  enum-member  AllTags.afterburn.elements  Explosion
  enum-member  AllTags.afterburn.elements  Fire
  enum-member  AllTags.afterburn.elements  Ice
  enum-member  AllTags.afterburn.elements  Lava
  enum-member  AllTags.afterburn.elements  Light
  enum-member  AllTags.afterburn.elements  Lightning
  enum-member  AllTags.afterburn.elements  Magnet
  enum-member  AllTags.afterburn.elements  Metal
  enum-member  AllTags.afterburn.elements  None
  enum-member  AllTags.afterburn.elements  Sand
  enum-member  AllTags.afterburn.elements  Scorch
  ... 4434 more
ADDITIONS
  enum-member  AllObjectives.tag_usage_win.tagType  curse
  enum-member  AllObjectives.tag_usage_win.tagType  parry
  enum-member  AllTags.DecreaseStatTag.calculation  percentage
  enum-member  AllTags.DecreaseStatTag.calculation  static
  enum-member  AllTags.DecreaseStatTag.direction  both
  enum-member  AllTags.DecreaseStatTag.direction  defence
  enum-member  AllTags.DecreaseStatTag.direction  offence
  enum-member  AllTags.DecreaseStatTag.elements  Boil
  enum-member  AllTags.DecreaseStatTag.elements  Crystal
  enum-member  AllTags.DecreaseStatTag.elements  Dust
  enum-member  AllTags.DecreaseStatTag.elements  Earth
  enum-member  AllTags.DecreaseStatTag.elements  Explosion
  enum-member  AllTags.DecreaseStatTag.elements  Fire
  enum-member  AllTags.DecreaseStatTag.elements  Ice
  enum-member  AllTags.DecreaseStatTag.elements  Lava
  enum-member  AllTags.DecreaseStatTag.elements  Light
  enum-member  AllTags.DecreaseStatTag.elements  Lightning
  enum-member  AllTags.DecreaseStatTag.elements  Magnet
  enum-member  AllTags.DecreaseStatTag.elements  Metal
  enum-member  AllTags.DecreaseStatTag.elements  None
  enum-member  AllTags.DecreaseStatTag.elements  Sand
  enum-member  AllTags.DecreaseStatTag.elements  Scorch
  enum-member  AllTags.DecreaseStatTag.elements  Shadow
  enum-member  AllTags.DecreaseStatTag.elements  Storm
  enum-member  AllTags.DecreaseStatTag.elements  Water
  enum-member  AllTags.DecreaseStatTag.elements  Wind
  enum-member  AllTags.DecreaseStatTag.elements  Wood
  enum-member  AllTags.DecreaseStatTag.elements  Yin-Yang
  enum-member  AllTags.DecreaseStatTag.friendlyFire  ALL
  enum-member  AllTags.DecreaseStatTag.friendlyFire  ENEMIES
  enum-member  AllTags.DecreaseStatTag.friendlyFire  FRIENDLY
  enum-member  AllTags.DecreaseStatTag.generalTypes  Highest
  enum-member  AllTags.DecreaseStatTag.generalTypes  Intelligence
  enum-member  AllTags.DecreaseStatTag.generalTypes  Speed
  enum-member  AllTags.DecreaseStatTag.generalTypes  Strength
  enum-member  AllTags.DecreaseStatTag.generalTypes  Willpower
  enum-member  AllTags.DecreaseStatTag.statTypes  Bukijutsu
  enum-member  AllTags.DecreaseStatTag.statTypes  Genjutsu
  enum-member  AllTags.DecreaseStatTag.statTypes  Highest
  enum-member  AllTags.DecreaseStatTag.statTypes  Ninjutsu
  enum-member  AllTags.DecreaseStatTag.statTypes  None
  enum-member  AllTags.DecreaseStatTag.statTypes  Taijutsu
  enum-member  AllTags.DecreaseStatTag.target  COORDINATES
  enum-member  AllTags.DecreaseStatTag.target  INHERIT
  enum-member  AllTags.DecreaseStatTag.target  SELF
  enum-member  AllTags.IncreaseStatTag.calculation  percentage
  enum-member  AllTags.IncreaseStatTag.calculation  static
  enum-member  AllTags.IncreaseStatTag.direction  both
  enum-member  AllTags.IncreaseStatTag.direction  defence
  enum-member  AllTags.IncreaseStatTag.direction  offence
  enum-member  AllTags.IncreaseStatTag.elements  Boil
  enum-member  AllTags.IncreaseStatTag.elements  Crystal
  enum-member  AllTags.IncreaseStatTag.elements  Dust
  enum-member  AllTags.IncreaseStatTag.elements  Earth
  enum-member  AllTags.IncreaseStatTag.elements  Explosion
  enum-member  AllTags.IncreaseStatTag.elements  Fire
  enum-member  AllTags.IncreaseStatTag.elements  Ice
  enum-member  AllTags.IncreaseStatTag.elements  Lava
  enum-member  AllTags.IncreaseStatTag.elements  Light
  enum-member  AllTags.IncreaseStatTag.elements  Lightning
  ... 220 more

BREAKING: 4494 change(s) - DO NOT ADOPT (exit 1)
== 45d_DATA_entity_schemas ==
CHANGES
  now-required  item  parentItemId  optional -> required
  now-required  item  requiredSkillId  optional -> required
  now-required  jutsu  bloodlineReskinId  optional -> required
  now-required  jutsu  parentJutsuId  optional -> required
  now-required  jutsu  requiredPetSpeciesId  optional -> required
  now-required  jutsu  requiredSkillId  optional -> required
  now-required  jutsu  reskinParentJutsuId  optional -> required
  type-changed  item  parentItemId  string -> (none)
  type-changed  jutsu  bloodlineReskinId  string -> (none)
  type-changed  jutsu  parentJutsuId  string -> (none)
  type-changed  jutsu  reskinParentJutsuId  string -> (none)
  type-changed  quest  petTaskMinutes  preprocess -> ref
ADDITIONS
  field  gameAsset  lpcConfig
  field  item  lpcColor
  field  item  lpcProfile
  field  itemVariant  lpcColor
  field  itemVariant  lpcProfile
  field  quest  raidMaxPlayers
  field  quest  teamMaxPlayers

BREAKING: 12 change(s) - DO NOT ADOPT (exit 1)
== 45e_DATA_constants ==
REMOVALS
  const-member  AvailableEffectTypes  absorb
  const-member  AvailableEffectTypes  activatesagemode
  const-member  AvailableEffectTypes  afterburn
  const-member  AvailableEffectTypes  barrier
  const-member  AvailableEffectTypes  buffprevent
  const-member  AvailableEffectTypes  cleanse
  const-member  AvailableEffectTypes  cleanseprevent
  const-member  AvailableEffectTypes  clear
  const-member  AvailableEffectTypes  clearprevent
  const-member  AvailableEffectTypes  clone
  const-member  AvailableEffectTypes  consume
  const-member  AvailableEffectTypes  copy
  const-member  AvailableEffectTypes  damage
  const-member  AvailableEffectTypes  debuffprevent
  const-member  AvailableEffectTypes  decreaseaggro
  const-member  AvailableEffectTypes  decreasecooldown
  const-member  AvailableEffectTypes  decreasedamagegiven
  const-member  AvailableEffectTypes  decreasedamagetaken
  const-member  AvailableEffectTypes  decreaseheal
  const-member  AvailableEffectTypes  decreasemastery
  const-member  AvailableEffectTypes  decreasemaxpools
  const-member  AvailableEffectTypes  decreasepoolcost
  const-member  AvailableEffectTypes  decreasepotency
  const-member  AvailableEffectTypes  decreasestat
  const-member  AvailableEffectTypes  diffuse
  const-member  AvailableEffectTypes  disarm
  const-member  AvailableEffectTypes  drain
  const-member  AvailableEffectTypes  elementalseal
  const-member  AvailableEffectTypes  finalstand
  const-member  AvailableEffectTypes  flee
  const-member  AvailableEffectTypes  fleeprevent
  const-member  AvailableEffectTypes  heal
  const-member  AvailableEffectTypes  healprevent
  const-member  AvailableEffectTypes  immunity
  const-member  AvailableEffectTypes  increaseaggro
  const-member  AvailableEffectTypes  increasecooldown
  const-member  AvailableEffectTypes  increasedamagegiven
  const-member  AvailableEffectTypes  increasedamagetaken
  const-member  AvailableEffectTypes  increaseheal
  const-member  AvailableEffectTypes  increasemastery
  const-member  AvailableEffectTypes  increasemaxpools
  const-member  AvailableEffectTypes  increasepoolcost
  const-member  AvailableEffectTypes  increasepotency
  const-member  AvailableEffectTypes  increaserange
  const-member  AvailableEffectTypes  increaseregeneration
  const-member  AvailableEffectTypes  increasestat
  const-member  AvailableEffectTypes  injectjutsus
  const-member  AvailableEffectTypes  lifesteal
  const-member  AvailableEffectTypes  marriageslotincrease
  const-member  AvailableEffectTypes  mirror
  const-member  AvailableEffectTypes  move
  const-member  AvailableEffectTypes  moveprevent
  const-member  AvailableEffectTypes  noncombatconsumereward
  const-member  AvailableEffectTypes  noncombatgainskill
  const-member  AvailableEffectTypes  noncombatincreasereskins
  const-member  AvailableEffectTypes  noncombatquest
  const-member  AvailableEffectTypes  onehitkill
  const-member  AvailableEffectTypes  onehitkillprevent
  const-member  AvailableEffectTypes  pierce
  const-member  AvailableEffectTypes  poison
  ... 165 more
ADDITIONS
  const-member  ABANDONABLE_QUEST_TYPES  battlepyramid
  const-member  ABANDONABLE_QUEST_TYPES  crime
  const-member  ABANDONABLE_QUEST_TYPES  errand
  const-member  ABANDONABLE_QUEST_TYPES  event
  const-member  ABANDONABLE_QUEST_TYPES  gathering
  const-member  ABANDONABLE_QUEST_TYPES  hunting
  const-member  ABANDONABLE_QUEST_TYPES  mastery
  const-member  ABANDONABLE_QUEST_TYPES  medical
  const-member  ABANDONABLE_QUEST_TYPES  mission
  const-member  ABANDONABLE_QUEST_TYPES  overworld
  const-member  ABANDONABLE_QUEST_TYPES  pvp
  const-member  ABANDONABLE_QUEST_TYPES  special
  const-member  ABANDONABLE_QUEST_TYPES  story
  const-member  ABANDONABLE_QUEST_TYPES  war
  const-member  ActiveBanStates  BAN_ACTIVATED
  const-member  ActiveBanStates  BAN_ESCALATED
  const-member  ActiveSilenceStates  SILENCE_ACTIVATED
  const-member  ActiveSilenceStates  TIMEOUT_ACTIVATED
  const-member  AdClickConsents  granted
  const-member  AdClickConsents  unanswered
  const-member  AdClickIdTypes  gbraid
  const-member  AdClickIdTypes  gclid
  const-member  AdClickIdTypes  wbraid
  const-member  AdConversionActions  register
  const-member  AdConversionActions  tutorialComplete
  const-member  AvailableEffectTypes  DecreaseStatTag
  const-member  AvailableEffectTypes  IncreaseStatTag
  const-member  AvailableEffectTypes  RedirectionTag
  const-member  AvailableEffectTypes  defence
  const-member  AvailableEffectTypes  offence
  const-member  BULK_SELL_WARN_RARITIES  EPIC
  const-member  BULK_SELL_WARN_RARITIES  LEGENDARY
  const-member  BULK_SELL_WARN_RARITIES  RARE
  const-member  BossFightBattleTypes  ARENA
  const-member  BossFightBattleTypes  HUNTING
  const-member  BossFightBattleTypes  OVERWORLD
  const-member  BossFightBattleTypes  QUEST
  const-member  BossFightBattleTypes  RANDOM_ENCOUNTER
  const-member  FARM_SHOP_ENTRY_TYPES  EXTRACTOR
  const-member  FARM_SHOP_ENTRY_TYPES  FERTILIZER
  const-member  FARM_SHOP_ENTRY_TYPES  PLOT
  const-member  FARM_SHOP_ENTRY_TYPES  SEED
  const-member  GameAssetTypes  LPC
  const-member  HP_DAMAGE_KEYS  afterburn
  const-member  HP_DAMAGE_KEYS  damage
  const-member  HP_DAMAGE_KEYS  drain_hp
  const-member  HP_DAMAGE_KEYS  poison
  const-member  HP_DAMAGE_KEYS  residual
  const-member  HP_DAMAGE_KEYS  wound
  const-member  INITIATIVE_PVP_STREAK_BONUSES  0.0025
  const-member  INITIATIVE_PVP_STREAK_BONUSES  0.005
  const-member  INITIATIVE_PVP_STREAK_BONUSES  0.01
  const-member  INITIATIVE_PVP_STREAK_BONUSES  0.015
  const-member  INITIATIVE_PVP_STREAK_BONUSES  0.02
  const-member  MISSION_HALL_QUEST_TYPES  crime
  const-member  MISSION_HALL_QUEST_TYPES  errand
  const-member  MISSION_HALL_QUEST_TYPES  medical
  const-member  MISSION_HALL_QUEST_TYPES  mission
  const-member  MISSION_HALL_QUEST_TYPES  pvp
  const-member  MISSION_HALL_QUEST_TYPES  war
  ... 124 more

BREAKING: 225 change(s) - DO NOT ADOPT (exit 1)
~~~
