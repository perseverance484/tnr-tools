# DRIFT.md - upstream contract drift (2026-10-27)

Upstream: studie-tech/TheNinjaRPG@3a1acf4ec8a6ef1abfa9f83582ecacdc43f804f3

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==
ADDITIONS
  enum-member  AllObjectives.SimpleObjective.task  overworld_ai_fought
  enum-member  AllObjectives.SimpleObjective.task  pvp_participated
  enum-member  AllObjectives.SimpleObjective.task  ranked_participated
  enum-member  AllObjectives.SimpleObjective.task  ranked_wins
  enum-member  AllObjectives.SimpleObjective.task  spars_participated
  enum-member  AllObjectives.tag_usage_win.tagType  siphon
  enum-member  AllTags.siphon.calculation  percentage
  enum-member  AllTags.siphon.friendlyFire  ALL
  enum-member  AllTags.siphon.friendlyFire  ENEMIES
  enum-member  AllTags.siphon.friendlyFire  FRIENDLY
  enum-member  AllTags.siphon.target  COORDINATES
  enum-member  AllTags.siphon.target  INHERIT
  enum-member  AllTags.siphon.target  SELF
  enum-member  allObjectiveSchema.SimpleObjective.task  overworld_ai_fought
  enum-member  allObjectiveSchema.SimpleObjective.task  pvp_participated
  enum-member  allObjectiveSchema.SimpleObjective.task  ranked_participated
  enum-member  allObjectiveSchema.SimpleObjective.task  ranked_wins
  enum-member  allObjectiveSchema.SimpleObjective.task  spars_participated
  enum-member  allObjectiveSchema.tag_usage_win.tagType  siphon
  union-variant  AllTags  decreasecookingtime
  union-variant  AllTags  decreasecraftingtime
  union-variant  AllTags  decreasefarmingtime
  union-variant  AllTags  decreasegatheringtime
  union-variant  AllTags  increasegatheringyield
  union-variant  AllTags  increasehuntingyield
  union-variant  AllTags  increasejutsuslots
  union-variant  AllTags  siphon
  variant-field  AllObjectives.InstantWinLoseObjective  reward_level
  variant-field  AllObjectives.InstantWinLoseObjective  reward_pet_experience
  variant-field  AllObjectives.InstantWinLoseObjective  reward_stats
  variant-field  AllObjectives.RaidObjective  reward_level
  variant-field  AllObjectives.RaidObjective  reward_pet_experience
  variant-field  AllObjectives.RaidObjective  reward_stats
  variant-field  AllObjectives.SimpleObjective  reward_level
  variant-field  AllObjectives.SimpleObjective  reward_pet_experience
  variant-field  AllObjectives.SimpleObjective  reward_stats
  variant-field  AllObjectives.bloodline_collection  reward_level
  variant-field  AllObjectives.bloodline_collection  reward_pet_experience
  variant-field  AllObjectives.bloodline_collection  reward_stats
  variant-field  AllObjectives.buy_item  reward_level
  variant-field  AllObjectives.buy_item  reward_pet_experience
  variant-field  AllObjectives.buy_item  reward_stats
  variant-field  AllObjectives.collect_item  reward_level
  variant-field  AllObjectives.collect_item  reward_pet_experience
  variant-field  AllObjectives.collect_item  reward_stats
  variant-field  AllObjectives.complete_specific_quest  reward_level
  variant-field  AllObjectives.complete_specific_quest  reward_pet_experience
  variant-field  AllObjectives.complete_specific_quest  reward_stats
  variant-field  AllObjectives.craft_specific_item  reward_level
  variant-field  AllObjectives.craft_specific_item  reward_pet_experience
  variant-field  AllObjectives.craft_specific_item  reward_stats
  variant-field  AllObjectives.damage_dealt  reward_level
  variant-field  AllObjectives.damage_dealt  reward_pet_experience
  variant-field  AllObjectives.damage_dealt  reward_stats
  variant-field  AllObjectives.defeat_opponents  reward_level
  variant-field  AllObjectives.defeat_opponents  reward_pet_experience
  variant-field  AllObjectives.defeat_opponents  reward_stats
  variant-field  AllObjectives.deliver_item  reward_level
  variant-field  AllObjectives.deliver_item  reward_pet_experience
  variant-field  AllObjectives.deliver_item  reward_stats
  ... 210 more

no breaking changes: 270 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
== 45e_DATA_constants ==
REMOVALS
  const-member  ACTIVE_VOTING_SITES  bbogd
ADDITIONS
  const-member  AvailableEffectTypes  decreasecookingtime
  const-member  AvailableEffectTypes  decreasecraftingtime
  const-member  AvailableEffectTypes  decreasefarmingtime
  const-member  AvailableEffectTypes  decreasegatheringtime
  const-member  AvailableEffectTypes  increasegatheringyield
  const-member  AvailableEffectTypes  increasehuntingyield
  const-member  AvailableEffectTypes  siphon
  const-member  BattleTypes  TERRITORY_WAR
  const-member  CombatActivityTasks  overworld_ai_fought
  const-member  CombatActivityTasks  pvp_participated
  const-member  CombatActivityTasks  ranked_participated
  const-member  CombatActivityTasks  ranked_wins
  const-member  CombatActivityTasks  spars_participated
  const-member  DiscordTokenSources  CLERK
  const-member  DiscordTokenSources  OAUTH
  const-member  DiscordUnlinkReasons  ACCOUNT_DELETED
  const-member  DiscordUnlinkReasons  STAFF
  const-member  DiscordUnlinkReasons  USER
  const-member  LOG_TYPES  village
  const-member  MPVP_BATTLE_TYPES  TERRITORY_WAR
  const-member  OBJECTIVE_TAG_TYPES  siphon
  const-member  POST_DAMAGE_MODIFIER_TYPES  siphon
  const-member  PetArtProviders  GPT
  const-member  PetArtProviders  NANO_BANANA
  const-member  PetGenders  FEMALE
  const-member  PetGenders  MALE
  const-member  PotencyTagTypes  siphon
  const-member  PveBattleTypes  TERRITORY_WAR
  const-member  SHARED_COOLDOWN_TAGS  siphon
  const-member  SimpleTasks  overworld_ai_fought
  const-member  SimpleTasks  pvp_participated
  const-member  SimpleTasks  ranked_participated
  const-member  SimpleTasks  ranked_wins
  const-member  SimpleTasks  spars_participated
  const-member  WEB_REP_PRESETS  100
  const-member  WEB_REP_PRESETS  20
  const-member  WEB_REP_PRESETS  250
  const-member  WEB_REP_PRESETS  50
  const-member  WEB_REP_PRESETS  500
  const-member  activityBonusTypes  decreasecookingtime
  const-member  activityBonusTypes  decreasecraftingtime
  const-member  activityBonusTypes  decreasefarmingtime
  const-member  activityBonusTypes  decreasegatheringtime
  const-member  activityBonusTypes  increasegatheringyield
  const-member  activityBonusTypes  increasehuntingyield
  const-member  allObjectiveTasks  overworld_ai_fought
  const-member  allObjectiveTasks  pvp_participated
  const-member  allObjectiveTasks  ranked_participated
  const-member  allObjectiveTasks  ranked_wins
  const-member  allObjectiveTasks  spars_participated
  const-member  allState  isMasked
  const-member  publicState  isMasked
  const-member  tagTypes  decreasecookingtime
  const-member  tagTypes  decreasecraftingtime
  const-member  tagTypes  decreasefarmingtime
  const-member  tagTypes  decreasegatheringtime
  const-member  tagTypes  increasegatheringyield
  const-member  tagTypes  increasehuntingyield
  const-member  tagTypes  increasejutsuslots
  const-member  tagTypes  siphon

BREAKING: 1 change(s) - DO NOT ADOPT (exit 1)
~~~
