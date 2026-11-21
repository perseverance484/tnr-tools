# Proposed "sector 210" lines

Status: **proposal, awaiting the director.** These are text only. Each one is a live write later (quest or item
edit, full record, on his go). The current wording below comes from the latest repo writes, not a live read.

| Where | Today | Proposed addition |
| --- | --- | --- |
| Watch Log 81+ pages: Stolen Stores (`AgGR962c3XNo6Pr0up2qT`) and Her Invitation (`I_cEOGSfFuahaJlR3FnWC`, push/519-520) | No sector given | **Stolen Stores: built** (README row 1: a line under the hook, in `stolen_stores_pages/`). Her Invitation: the same, still to build. |
| Watch Log Shallows page (Stolen Stores (Shallows), new) | Its daily challenge says "Find her in sector 210, by the Wrecks." | **Built**, same as the 81+ page (README row 1). |
| Wreck Salvage (`mW6_ZGtGcCSuXGPhn-H4o`, last write push/580) | `<i>Brass fittings, glass shards and rope pulled out of the Skyglass Wreck.</i><br><br>The salvager trades charts for it.` | Append `<br>Find the Wrecks, and the salvager, in sector 210.` |
| Chart items (23, live text push/609; strings in release_nov13/chart_text/CT1_chart_text.json) | `<i>flavour</i><br><b>Run</b> · Level…<br>Difficulty…<br><b>Chance drops:</b>…<br><b>Choose one:</b>…` | Append a last line: `<br>Salvaged from the Wrecks in sector 210.` |

One thing to weigh:

- The chart line adds a sixth line to the chart text layout the director set on Nov 13. It also says where charts
  come from, not where to use one (runs open in the Battle Arena), so a player could read it as "go to 210 to run
  this". Dropping the chart line is the safe choice.
