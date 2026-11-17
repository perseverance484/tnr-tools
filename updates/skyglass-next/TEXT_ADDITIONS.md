# Proposed "sector 210" lines

Status: **proposal, awaiting the director.** These are text only. Each one is a live write later (quest or item
edit, full record, on his go). The current wording below comes from the latest repo writes, not a live read.

| Where | Today | Proposed addition |
| --- | --- | --- |
| Watch Log 81+ pages: Stolen Stores (`AgGR962c3XNo6Pr0up2qT`, built in `stolen_stores_pages/`) and Her Invitation (`I_cEOGSfFuahaJlR3FnWC`, push/519-520) | No sector given | First line of the **Rules** block: `The Wrecks are in sector 210.` |
| Watch Log Shallows pages (Stolen Stores (Shallows), new) | Already says "Find her in sector 210, by the Wrecks." | Optional, the same Rules line, so both bands read alike. |
| Wreck Salvage (`mW6_ZGtGcCSuXGPhn-H4o`, last write push/580) | `<i>Brass fittings, glass shards and rope pulled out of the Skyglass Wreck.</i><br><br>The salvager trades charts for it.` | Append `<br>Find the Wrecks, and the salvager, in sector 210.` |
| Chart items (23, live text push/609; strings in release_nov13/chart_text/CT1_chart_text.json) | `<i>flavour</i><br><b>Run</b> · Level…<br>Difficulty…<br><b>Chance drops:</b>…<br><b>Choose one:</b>…` | Append a last line: `<br>Salvaged from the Wrecks in sector 210.` |

Two things to weigh:

- The chart line adds a sixth line to the chart text layout the director set on Nov 13. It also says where charts
  come from, not where to use one (runs open in the Battle Arena), so a player could read it as "go to 210 to run
  this". Dropping the chart line is the safe choice.
- The Watch Log line no longer names Salvager's Bearing, since the crew hunt reaches players without the board.
