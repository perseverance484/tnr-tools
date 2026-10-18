# Round-total Bloodright review

Applied the approved Taiyo design to all 24 other captured A/S trees. D–B ranks remain outside this pass.

**4/25 trees pass both normal and symmetric-pressure score screens across their intended kits.** All 25 pass the structural, finished-percentage and cap checks. The remaining proposals need balance review.

**Rules:** Four independent paths; one tag per Foundation/Hidden; 1 BP per node; intended full build 3+2. Percentages progress 2/3/5 and finish at 5/10. Damage uses approved clean amounts, including 0.6, and totals at most 5 across eligible rows. No Wound upgrades.

**Read the numbers:** Scores measure added seven-round combat utility using the same formula and fixtures. Secondary% compares the weakest and strongest two-node addition to a completed path. 90% is the working review screen. No per-tree score normalization.

| Bloodright | Kit |3 BP score|5 BP score|Secondary minimum|Review|
|---|---|---:|---:|---:|---|
|Aerathiel|Standard|7.59–8.30|8.28–14.68|9.8%|Needs balance review|
|Arashima|Standard|3.45–3.56|4.70–4.83|95.3%|Pass|
|Bakuhatsu|Standard|5.60–7.51|7.32–10.81|38.4%|Needs balance review|
|Blood-Enchanted Eyes|Reaper|1.49–2.88|1.77–3.71|22.9%|Needs balance review|
|Blood-Enchanted Eyes|Wraith|1.88–3.49|2.80–4.45|47.7%|Needs balance review|
|Blue Blade Eyes|Blue Blade|3.47–10.52|3.47–12.75|0.0%|Needs balance review|
|Blue Blade Eyes|Threefold|1.88–5.11|3.01–6.29|64.4%|Needs balance review|
|Cosmic Ascendant|Standard|3.64–4.55|5.17–6.50|62.2%|Needs balance review|
|Crystal Essence|Standard|2.93–4.34|3.84–6.72|38.0%|Needs balance review|
|Ethereal Monarch|Standard|3.57–3.68|4.82–5.36|74.1%|Needs balance review|
|Eyes of the Forsaken King|Standard|4.71–5.11|5.98–8.19|41.2%|Needs balance review|
|Heavenly Sonata|Standard|3.53–3.62|4.86–5.01|90.8%|Pass|
|Houkyuken|Standard|8.36–8.84|9.30–15.46|14.2%|Needs balance review|
|Hyouga Yui|Standard|4.08–8.91|5.60–13.36|25.4%|Constraint demonstrated|
|Itojinsei|Standard|1.52–6.45|3.11–8.66|25.3%|Constraint demonstrated|
|Kyuko-sei|Standard|7.18–11.37|8.38–13.33|16.5%|Needs balance review|
|Oblivion Seal|Standard|3.64–4.06|5.39–5.82|84.3%|Needs balance review|
|Shadow Weaver|Standard|1.52–8.84|2.79–10.11|18.5%|Constraint demonstrated|
|Shakunetsu Sakura|Standard|3.61–4.22|5.54–6.22|77.9%|Needs balance review|
|Shinrai Ou|Standard|1.95–16.79|3.22–19.38|12.1%|Constraint demonstrated|
|Shinseina Ki|Standard|5.00–11.61|5.60–14.68|10.3%|Constraint demonstrated|
|Shiroi Youso|Standard|8.33–9.59|10.54–14.94|37.0%|Needs balance review|
|Shiroi Youso|Standard / variant 2|5.79–10.55|7.63–13.40|32.4%|Needs balance review|
|Shiroi Youso|Standard / variant 3|5.62–10.59|7.60–15.19|28.8%|Needs balance review|
|Shiroi Youso|Standard / variant 4|5.64–11.77|7.50–17.27|22.0%|Needs balance review|
|Suragu|Standard|4.08–4.70|6.11–7.02|76.6%|Needs balance review|
|Taiyo Kami|Standard|3.56–3.69|4.74–4.96|90.8%|Pass|
|Teno Yuki|Standard|3.80–3.93|5.07–5.26|95.2%|Pass|
|Tenohira Musei|Standard|5.77–10.36|7.04–14.34|31.9%|Constraint demonstrated|
|Vaporia|Standard|3.84–4.40|5.81–6.82|76.6%|Needs balance review|

## Unresolved constraints

For the following six kits, an optimistic exhaustive capstone check still cannot reach 90% secondary parity within the current four-distinct-root, one-tag, approved-amount design space. This is a model/constraint result, not a claim about every possible architecture or PvP matchup. They require a native-kit or design-rule change to pass that screen.

| Bloodright | Optimistic secondary ceiling |
|---|---:|
|Hyouga Yui|33.0%|
|Itojinsei|57.3%|
|Shadow Weaver|30.2%|
|Shinrai Ou|15.9%|
|Shinseina Ki|10.6%|
|Tenohira Musei|33.9%|

BBE and BEE retain their explicit keystone and tag-placement rules. Their unresolved healing/coverage gaps remain in the audit. Zero useful healing in a full-health scenario is not assigned an artificial price. Other failed trees are bounded-search results, not proven infeasible.

## Files and verification

- [Tree data](proposal_trees.json): all 25 current proposals; accepted Taiyo is preserved exactly.
- [Naming review](naming/review.csv): all 300 names, previous names, effects and theme rationale. Names are unique across the current roster and do not duplicate captured native jutsu names.
- [Naming checks](naming/audit.json): name-only revision; tags, values, prerequisites and numerical results are unchanged. Historical proposals and presentation files retain their old names.
- [Compact scores](summary.csv): one row per loadout.
- [Full audit](audit.json): node values, 3-BP/5-BP combinations, all legal allocations, tag coverage, seven scenarios and review flags.
- [Constraint evidence](feasibility_diagnostics.json): independently optimized capstone bounds for the six sparse kits.
- [Accepted Taiyo](accepted_taiyo/acceptance.json): the user approval and mechanics fingerprint.

Final audit: 30 loadouts × 106 legal allocations × 7 scenarios = 22,260 checks. All intended full builds have distinct, non-dominated native bonus vectors. Persistent score disadvantages across scenarios are reported separately. Larger loadouts receive a wider-policy sensitivity check.

No SVG, PDF or workbook regenerated. No live game changes. Scores use captured kits and pinned source; this is not fresh PvP validation.

Reproduce from the tools repository:
```bash
OPENBLAS_NUM_THREADS=1 python scripts/bloodright/round_total_roster.py --refine --workers 3
OPENBLAS_NUM_THREADS=1 python scripts/bloodright/round_total_feasibility.py
OPENBLAS_NUM_THREADS=1 python scripts/bloodright/round_total_roster_audit.py --workers 3
python scripts/bloodright/round_total_roster_review.py
```

The search reapplies reviewed names only when their reviewed bonuses still match. Changed effects flag a fresh naming review. Verify the current name-only snapshot with `python scripts/bloodright/round_total_names.py`.
