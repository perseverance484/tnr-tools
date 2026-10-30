# DRIFT.md - upstream contract drift (2026-10-30)

Upstream: studie-tech/TheNinjaRPG@9756c4127f88400443a67d1daeaf1e4e55f9e9c2

Signal only. Nothing below is adopted until the structural diff gate passes.

~~~
== 45c_DATA_constructors ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==
ADDITIONS
  field  item  lpcColor
  field  item  lpcProfile
  field  itemVariant  lpcColor
  field  itemVariant  lpcProfile

no breaking changes: 4 addition(s), safe to adopt (exit 0)
== 45e_DATA_constants ==
ADDITIONS
  const-member  allState  spriteAction
  const-member  allState  spriteAppearance
  const-member  publicState  spriteAction
  const-member  publicState  spriteAppearance

no breaking changes: 4 addition(s), safe to adopt (exit 0)
~~~
