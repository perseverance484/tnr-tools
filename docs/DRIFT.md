# DRIFT.md - upstream contract drift (2026-11-27)

Upstream: studie-tech/TheNinjaRPG@6f8b58f4d8090f577b723304daa867f5094d50a1

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
  enum-member  AllObjectives.win_card_duel.reward_mastery_rank  ADEPT
  enum-member  AllObjectives.win_card_duel.reward_mastery_rank  LEGENDARY
  enum-member  AllObjectives.win_card_duel.reward_mastery_rank  MASTER
  enum-member  AllObjectives.win_card_duel.reward_mastery_rank  NONE
  enum-member  AllObjectives.win_card_duel.reward_mastery_rank  NOVICE
  enum-member  AllObjectives.win_card_duel.reward_mastery_stat  None
  enum-member  AllObjectives.win_card_duel.reward_rank  CHUNIN
  enum-member  AllObjectives.win_card_duel.reward_rank  ELDER
  enum-member  AllObjectives.win_card_duel.reward_rank  ELITE JONIN
  enum-member  AllObjectives.win_card_duel.reward_rank  GENIN
  enum-member  AllObjectives.win_card_duel.reward_rank  JONIN
  enum-member  AllObjectives.win_card_duel.reward_rank  NONE
  enum-member  AllObjectives.win_card_duel.reward_rank  STUDENT
  enum-member  AllObjectives.win_card_duel.reward_village_membership  AKASUMI
  enum-member  AllObjectives.win_card_duel.reward_village_membership  AKIKAZE
  enum-member  AllObjectives.win_card_duel.reward_village_membership  HYORIN
  enum-member  AllObjectives.win_card_duel.reward_village_membership  NONE
  enum-member  AllObjectives.win_card_duel.reward_village_membership  SHIROHANA
  enum-member  AllObjectives.win_card_duel.reward_village_membership  TSUKIMORI
  enum-member  AllObjectives.win_card_duel.tier  ANY
  enum-member  AllObjectives.win_chakra_storm.locationType  random
  enum-member  AllObjectives.win_chakra_storm.locationType  specific
  enum-member  AllObjectives.win_chakra_storm.reward_mastery_rank  ADEPT
  enum-member  AllObjectives.win_chakra_storm.reward_mastery_rank  LEGENDARY
  enum-member  AllObjectives.win_chakra_storm.reward_mastery_rank  MASTER
  enum-member  AllObjectives.win_chakra_storm.reward_mastery_rank  NONE
  enum-member  AllObjectives.win_chakra_storm.reward_mastery_rank  NOVICE
  enum-member  AllObjectives.win_chakra_storm.reward_mastery_stat  None
  enum-member  AllObjectives.win_chakra_storm.reward_rank  CHUNIN
  enum-member  AllObjectives.win_chakra_storm.reward_rank  ELDER
  enum-member  AllObjectives.win_chakra_storm.reward_rank  ELITE JONIN
  enum-member  AllObjectives.win_chakra_storm.reward_rank  GENIN
  enum-member  AllObjectives.win_chakra_storm.reward_rank  JONIN
  enum-member  AllObjectives.win_chakra_storm.reward_rank  NONE
  enum-member  AllObjectives.win_chakra_storm.reward_rank  STUDENT
  enum-member  AllObjectives.win_chakra_storm.reward_village_membership  AKASUMI
  enum-member  AllObjectives.win_chakra_storm.reward_village_membership  AKIKAZE
  enum-member  AllObjectives.win_chakra_storm.reward_village_membership  HYORIN
  enum-member  AllObjectives.win_chakra_storm.reward_village_membership  NONE
  enum-member  AllObjectives.win_chakra_storm.reward_village_membership  SHIROHANA
  enum-member  AllObjectives.win_chakra_storm.reward_village_membership  TSUKIMORI
  enum-member  AllObjectives.win_chakra_storm.sectorType  current_sector
  enum-member  AllObjectives.win_chakra_storm.sectorType  enemy_village
  enum-member  AllObjectives.win_chakra_storm.sectorType  from_list
  enum-member  AllObjectives.win_chakra_storm.sectorType  random
  enum-member  AllObjectives.win_chakra_storm.sectorType  specific
  enum-member  AllObjectives.win_chakra_storm.sectorType  user_village
  enum-member  AllObjectives.win_chakra_storm.stage  akasumi
  enum-member  AllObjectives.win_chakra_storm.stage  akikaze
  enum-member  AllObjectives.win_chakra_storm.stage  horizon
  enum-member  AllObjectives.win_chakra_storm.stage  hyorin
  enum-member  AllObjectives.win_chakra_storm.stage  mei
  enum-member  AllObjectives.win_kessen_challenge.locationType  random
  enum-member  AllObjectives.win_kessen_challenge.locationType  specific
  enum-member  AllObjectives.win_kessen_challenge.reward_mastery_rank  ADEPT
  enum-member  AllObjectives.win_kessen_challenge.reward_mastery_rank  LEGENDARY
  enum-member  AllObjectives.win_kessen_challenge.reward_mastery_rank  MASTER
  enum-member  AllObjectives.win_kessen_challenge.reward_mastery_rank  NONE
  ... 646 more

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
  field  item  canBeEnhanced
  field  item  cardData
  field  item  craftingOutputQuantity
  field  item  lpcColor
  field  item  lpcMaterialColors
  field  item  lpcProfile
  field  item  villageId
  field  item  warehouseItem
  field  itemVariant  lpcColor
  field  itemVariant  lpcMaterialColors
  field  itemVariant  lpcProfile
  field  petSpecies  potentialMax
  field  petSpecies  potentialMin
  field  petSpecies  potentialMode
  field  petSpecies  potentialValue
  field  petSpecies  potentialWeights
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
  ... 197 more
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
  const-member  ACTIVE_VOTING_SITES  topRankinGames
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
  const-member  BALANCE_IDLE_ACTION_IDS  flee
  const-member  BALANCE_IDLE_ACTION_IDS  wait
  const-member  BANDIT_RANKS  BANDIT CHIEF
  const-member  BANDIT_RANKS  HIGHWAYMAN
  const-member  BANDIT_RANKS  MARAUDER
  const-member  BULK_SELL_WARN_RARITIES  EPIC
  const-member  BULK_SELL_WARN_RARITIES  LEGENDARY
  const-member  BULK_SELL_WARN_RARITIES  RARE
  const-member  BattleDataEntryType  participant
  const-member  BattleOutcomes  Draw
  const-member  BattleOutcomes  Fled
  const-member  BattleOutcomes  Lost
  const-member  BattleOutcomes  Won
  const-member  BattleTypes  CARAVAN
  const-member  BossFightBattleTypes  ARENA
  const-member  BossFightBattleTypes  HUNTING
  const-member  BossFightBattleTypes  OVERWORLD
  const-member  BossFightBattleTypes  QUEST
  const-member  BossFightBattleTypes  RANDOM_ENCOUNTER
  const-member  CARAVAN_DISCOVERY_KINDS  LOCATION
  const-member  CARAVAN_DISCOVERY_KINDS  ROUTE
  const-member  CARAVAN_ENCOUNTER_STATUSES  FIGHTING
  const-member  CARAVAN_ENCOUNTER_STATUSES  PENDING
  const-member  CARAVAN_ENCOUNTER_STATUSES  RESOLVED
  const-member  CARAVAN_ENCOUNTER_STATUSES  STARTING
  const-member  CARAVAN_ENCOUNTER_TYPES  AMBUSH
  const-member  CARAVAN_ENCOUNTER_TYPES  INTERCEPTION
  const-member  CARAVAN_ENCOUNTER_TYPES  INTERVENTION
  const-member  CARAVAN_ENCOUNTER_TYPES  MARKER_ASSAULT
  ... 252 more

BREAKING: 257 change(s) - DO NOT ADOPT (exit 1)
~~~
