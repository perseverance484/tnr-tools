**RETIRED 2026-08-30 by dauntless. Archived record only - not an open item, not a Terr relay, not a blocker on anything. Do not re-derive from this file.**

**Addendum to the stuck-rows note: new finding, may connect**

The quest edit page is crashing client-side on **every** quest, not just the three stuck ones. Verified on a known-good record (Chalk and Corner, reads back fine over tRPC).

Error: `Duplicate discriminator value "undefined"`, thrown from the objectives union during parse. Chunk: `0n-1xi0p-e_84.js`. This is Zod 4 building the task-discriminated union lazily on first parse, which means two variants in the shared objectives schema are missing (or mis-declaring) their `task` literal. It ships fine and only explodes when an edit page opens. Greppable in source: look for a recently added objective type without its literal.

**[CORRECTION 2026-08-30 - this half is disproven. The three rows were never stuck: The Waystation was tripping our own rate limiter, since patched. Only the Zod editor-page crash above stands.]**

**Possible connection to the stuck rows:** the three quests were filled as consecutive writes in a 17:11 window on 08-28. If a deploy landed in or near that window, a restart mid-batch would kill in-flight transactions, which is a clean explanation for locks or half-written content on exactly those rows, and the same deploy would have shipped the broken schema. Worth checking deploy timestamps against 17:11 on 08-28.

The earlier two-step ask still stands: open locks on the three row IDs first, then a raw SELECT of the content column.
