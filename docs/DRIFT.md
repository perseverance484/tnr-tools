# DRIFT.md - upstream contract drift (2026-10-22)

Upstream: studie-tech/TheNinjaRPG@dc74ffba8900778abcf8e36dd0098f3e0fe084e9

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==
ADDITIONS
  enum-member  AllObjectives.tag_usage_win.tagType  siphon
  enum-member  AllTags.siphon.calculation  percentage
  enum-member  AllTags.siphon.friendlyFire  ALL
  enum-member  AllTags.siphon.friendlyFire  ENEMIES
  enum-member  AllTags.siphon.friendlyFire  FRIENDLY
  enum-member  AllTags.siphon.target  COORDINATES
  enum-member  AllTags.siphon.target  INHERIT
  enum-member  AllTags.siphon.target  SELF
  enum-member  allObjectiveSchema.tag_usage_win.tagType  siphon
  union-variant  AllTags  siphon
  variant-field  AllTags.siphon  appearAnimation
  variant-field  AllTags.siphon  appearSfx
  variant-field  AllTags.siphon  calculation
  variant-field  AllTags.siphon  coordinateTargeting
  variant-field  AllTags.siphon  description
  variant-field  AllTags.siphon  direction
  variant-field  AllTags.siphon  disappearAnimation
  variant-field  AllTags.siphon  disappearSfx
  variant-field  AllTags.siphon  friendlyFire
  variant-field  AllTags.siphon  power
  variant-field  AllTags.siphon  powerPerLevel
  variant-field  AllTags.siphon  rounds
  variant-field  AllTags.siphon  shieldRounds
  variant-field  AllTags.siphon  staticAnimation
  variant-field  AllTags.siphon  staticAssetPath
  variant-field  AllTags.siphon  target
  variant-field  AllTags.siphon  timeTracker
  variant-field  AllTags.siphon  type

no breaking changes: 28 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
== 45e_DATA_constants ==
ADDITIONS
  const-member  AvailableEffectTypes  siphon
  const-member  OBJECTIVE_TAG_TYPES  siphon
  const-member  POST_DAMAGE_MODIFIER_TYPES  siphon
  const-member  PetArtProviders  GPT
  const-member  PetArtProviders  NANO_BANANA
  const-member  PotencyTagTypes  siphon
  const-member  SHARED_COOLDOWN_TAGS  siphon
  const-member  tagTypes  siphon

no breaking changes: 8 addition(s), safe to adopt (exit 0)
~~~
