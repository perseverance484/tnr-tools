# DRIFT.md - upstream contract drift (2026-10-26)

Upstream: studie-tech/TheNinjaRPG@dd2de3bb7f3430fe86640a90471c86bae48ea688

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
  variant-field  AllObjectives.dialog  reward_level
  variant-field  AllObjectives.dialog  reward_pet_experience
  variant-field  AllObjectives.dialog  reward_stats
  variant-field  AllObjectives.move_to_location  reward_level
  variant-field  AllObjectives.move_to_location  reward_pet_experience
  variant-field  AllObjectives.move_to_location  reward_stats
  variant-field  AllObjectives.new_quest  reward_level
  ... 84 more

no breaking changes: 144 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
== 45e_DATA_constants ==
REMOVALS
  const-member  ACTIVE_VOTING_SITES  bbogd
ADDITIONS
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
  const-member  allObjectiveTasks  overworld_ai_fought
  const-member  allObjectiveTasks  pvp_participated
  const-member  allObjectiveTasks  ranked_participated
  const-member  allObjectiveTasks  ranked_wins
  const-member  allObjectiveTasks  spars_participated
  const-member  allState  isMasked
  const-member  publicState  isMasked
  const-member  tagTypes  siphon

BREAKING: 1 change(s) - DO NOT ADOPT (exit 1)
~~~
