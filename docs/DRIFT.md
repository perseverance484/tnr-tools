# DRIFT.md - upstream contract drift (2026-11-02)

Upstream: studie-tech/TheNinjaRPG@03f5669f7209bce8e85da58a8a4b17f5f1d2aa33

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
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
  const-member  GameAssetTypes  LPC
  const-member  allState  spriteAction
  const-member  allState  spriteAppearance
  const-member  publicState  spriteAction
  const-member  publicState  spriteAppearance

no breaking changes: 7 addition(s), safe to adopt (exit 0)
~~~
