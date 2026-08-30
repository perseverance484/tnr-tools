# DRIFT.md - upstream contract drift (2026-08-30)

Upstream: studie-tech/TheNinjaRPG@c97137327bed8b0fb62143ebe23f9d4075184d05

The extracted 45x contract hashes changed vs the last sentinel
baseline. SIGNAL ONLY: nothing was adopted. Adoption is manual
through the schema_diff gate (docs/00_INDEX.md regen row).

Structural diff, SHIPPED vs upstream:

~~~
== 45c_DATA_constructors ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
== 45d_DATA_entity_schemas ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
== 45e_DATA_constants ==

no breaking changes: 0 addition(s), safe to adopt (exit 0)
~~~
