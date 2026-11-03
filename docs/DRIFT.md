# DRIFT.md - upstream contract drift (2026-11-03)

Upstream: studie-tech/TheNinjaRPG@c4c1231ef2d211ee0140c3e922e9d8dfdc47a42c

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==
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
  enum-member  allObjectiveSchema.tag_usage_win.tagType  curse
  enum-member  allObjectiveSchema.tag_usage_win.tagType  parry
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
  ... 20 more

no breaking changes: 80 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==
ADDITIONS
  field  gameAsset  lpcConfig
  field  item  lpcColor
  field  item  lpcProfile
  field  itemVariant  lpcColor
  field  itemVariant  lpcProfile

no breaking changes: 5 addition(s), safe to adopt (exit 0)
== 45e_DATA_constants ==
ADDITIONS
  const-member  ActiveBanStates  BAN_ACTIVATED
  const-member  ActiveBanStates  BAN_ESCALATED
  const-member  AvailableEffectTypes  curse
  const-member  AvailableEffectTypes  parry
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

no breaking changes: 20 addition(s), safe to adopt (exit 0)
~~~
