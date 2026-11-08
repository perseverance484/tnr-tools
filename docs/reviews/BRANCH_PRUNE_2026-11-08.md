# Branch prune, 2026-11-08

Remote branches deleted because they were **fully merged into main** (their head is an ancestor of `main@05982ffa`) and untouched for 3+ days, so no work is lost. `builder-app` is kept (grandfathered implementation branch, CLAUDE.md §4). Restore any of them with `git push origin <sha>:refs/heads/<name>`.

Branches **not** merged into main are kept and listed below for their owners to merge, close or delete; nothing unmerged was deleted.

## Deleted (152)

| Branch | Head SHA | Idle (days) |
|---|---|---|
| art-village-scrolls | `7f1808fadbc15335d75ed019d42448e83ad8bfd3` | 18 |
| art-village-scrolls-2 | `a27eed866566f82349c2b8406a9251b78f87e74f` | 18 |
| art-village-scrolls-3 | `0d91d1a4c001b15e7f56388c5c4c68c598aabb4e` | 18 |
| astra/guide-studio-implementation | `8ef59a19e129657184f703044cd8fe1e7555c8f1` | 56 |
| ccr-0a13c59a-q1el4g | `48f355fbee8b75207a3f9e65580145ff576fcc2f` | 22 |
| ccr-71fd390f-0j0g78 | `3f825562ea051306a3803f47428b742ae5100011` | 27 |
| ccr-9fb18f2c-0wrhlu | `2cc3a0901361f43b6285c098b0b1ef42848942ed` | 33 |
| ccr-c49f311f-79gnvc | `4a3b7fb064aedbec271f27ed189288cc82b277ff` | 13 |
| ccr-d998b825-q58zf8 | `76ae8462f83587a6e9967f577f1b15a79d2e73a8` | 39 |
| ccr-f0d2b974-k6121h | `f4a0d1d18ebdf7728d397761c828a925d5dc5fec` | 20 |
| chatgpt/aerathiel-guide-assets-temp | `305a28f992e33194fbba279a3f32e698dfb2b67f` | 57 |
| chatgpt/bee-pilot-values | `484d554b65954c18d04b62b00b31ad2b9057bfec` | 30 |
| chatgpt/bloodright-balance-review-method-20261004 | `f2f8b98cbb69528f27d3405588d4e0fb64aae015` | 35 |
| chatgpt/bloodright-balance-team-package-foundation-20261004 | `db4752efbdc3717f2b812625038a224eee51bdfa` | 34 |
| chatgpt/bloodright-baseline-20261003 | `c0de9592772d4ffe0cb3ccc2aabb8f1aa3f43f1c` | 36 |
| chatgpt/bloodright-collection-icons-20261016 | `cfa3db8fe7edce8b8fe3ef708128a9c60fe3675a` | 23 |
| chatgpt/bloodright-director-rulings-20261003 | `1ada593ae2ea172ff493a903ce1ead66aa7fd37e` | 35 |
| chatgpt/bloodright-poster-standard-20261003 | `ad0bb49f162a499f122a5af51e590984689dc89a` | 36 |
| chatgpt/bloodright-presentation-scope-20261003 | `f507588685103cfabdbaa5c3fd9db7df6ab10269` | 36 |
| chatgpt/dai-kenja-jutsu-art-capture-20261004 | `95c8edc035dd6b301f84cbf953364474e6135978` | 34 |
| chatgpt/elementaldamage-damage-investigation-20261020 | `90ea9b1a452a763b6f7523a2af7a45124f4c8754` | 19 |
| chatgpt/forge-bloodright-import | `3ad5f8fe781226c370c0b21b7784526ddd953126` | 30 |
| chatgpt/forge-capture-only-fix | `961fb12e21f868e3e81e5f17cfdc38310b368a95` | 59 |
| chatgpt/forge-full-capture-brief | `b99747f4bebaf2b2b23a7511310efbe1b227ec75` | 59 |
| chatgpt/forge-loader-self-update | `603e418ee6651066f3ac1f0e79ac404cf4a5ee63` | 59 |
| chatgpt/forge-presentation-studio-closeout | `566e4cd91d593d3dd9fc4ac3f77d66db589cff7d` | 49 |
| chatgpt/ghost-ship-skyglass-manifest-roadmap | `0dbd54c04f2025a1a652712a9ea6df94e35cf8f5` | 28 |
| chatgpt/horizontal-item-progression-v2-20261004 | `2dc9351c27ed815e353cd299d697717503abb5e9` | 35 |
| chatgpt/isolated-art-generation-protocol-20261014 | `accd14e935443de4fcec30492fb07c71a0f0765f` | 25 |
| chatgpt/jellyfish-beach-quest-clean-20261004 | `73e9bea6dd56558287731eb19234ceea9e0e6416` | 34 |
| chatgpt/jellyfish-coast-recovery-20261004 | `f988831ffc18fd5ffa5952a926652621c09b6f52` | 34 |
| chatgpt/jellyfish-targeting-repair-20261004 | `c81d2bf3df1c91acf83dc0522a7e9e9817b6b556` | 34 |
| chatgpt/jutsu-census-batches-20261005 | `de34073311ac618d16580e1941d748dda05f47f4` | 33 |
| chatgpt/jutsu-census-recovery-20261005 | `0f00b5df6afd70f6823e8da365ebc30f636a6b66` | 33 |
| chatgpt/jutsu-icon-d4-docs-20261019 | `a6e97d458025fbac80599fad9f99bcc44d61dc2f` | 19 |
| chatgpt/jutsu-icon-p0-quality-gates-20261019 | `558c6223be0ed83155979e7b6d7439d75b18ad6c` | 20 |
| chatgpt/night-parade-asset-acquisition | `9735e70e3bac15e5f29980ea0f7a7a9165c4e70e` | 56 |
| chatgpt/night-parade-asset-followup | `d772d43fb2a5f9eb693bef844566060a20e9db15` | 56 |
| chatgpt/one-perfect-crop-roadmap-20260911 | `4b1cfd9a5ab1906009b37c82be7f7c4896c6194f` | 58 |
| chatgpt/opc-asset-repair-20260929 | `6393c668d4457858dabb35a98b383729480d590a` | 40 |
| chatgpt/opc-core-manifest-freeze-20260916 | `e35633160bdb7bb03238e30c22faf9f2b4af057c` | 52 |
| chatgpt/opc-roadmap-closeout-20260923 | `3458175ae50cb0133a8d920f53228944b8f36a84` | 44 |
| chatgpt/opc-roadmap-finalize-tmp | `daa91ab93d0a2ac48640739bcd4572736464fbcc` | 58 |
| chatgpt/opc-roadmap-finalize-tmp-2 | `daa91ab93d0a2ac48640739bcd4572736464fbcc` | 58 |
| chatgpt/opc-roadmap-finalize-tmp-3 | `daa91ab93d0a2ac48640739bcd4572736464fbcc` | 58 |
| chatgpt/plan-art-generation-preflight | `fc56baf17409c1752f42e04d22529ec59a759465` | 57 |
| chatgpt/player-guide-series-style | `6848a7805d912378f7f8eb27f52c9625dd10ac54` | 56 |
| chatgpt/repo-simplification-audit | `6f68ac3641f38a0028a57bfd34075969f7dcd9e8` | 59 |
| chatgpt/repo-simplification-audit-contract-probe | `d35889d2034872046faf817f5f16bc904a8e7747` | 60 |
| chatgpt/repo-simplification-audit-provenance-fix | `d35889d2034872046faf817f5f16bc904a8e7747` | 60 |
| chatgpt/repo-simplification-audit-reconcile-run | `d35889d2034872046faf817f5f16bc904a8e7747` | 60 |
| chatgpt/repo-simplification-audit-temp-probe | `d35889d2034872046faf817f5f16bc904a8e7747` | 60 |
| chatgpt/review-forge-protected-auth-r2-copy | `3b6c566eef5459fe16f104d5ee21accbc4e0f6c8` | 58 |
| chatgpt/review-qw0a-contract-alignment-20261012 | `e2c10ee1717d1311951bc8a7f6e621229ebf4b5f` | 27 |
| chatgpt/review-qw1-corrections-20261014 | `6c4af7f8d568c9789b92e83f413cefb83c29f131` | 25 |
| chatgpt/stormrender-highest-scaling-manifest-20261020 | `590c0d8968d21aa53713276ef2faacf2fb42b84c` | 19 |
| chatgpt/wind-ruins-validation-20260929 | `c996a5be33c2cb6271cae5725119e1e2d42e9b6e` | 40 |
| claude/bloodright-collection-icons-review-3r8yo3 | `1cd5101a28d6200003e21f76d167dbe810c34f06` | 22 |
| claude/content-workstream-bootstrap-0ff07z | `3212969a562e1d7b6e11cb3c5cc21821ab8bc7c4` | 58 |
| claude/forge-godstorm-defects-repair-rxxwky | `6d1df298f906a794973045ea0c8fb311899cec30` | 50 |
| claude/forge-presentation-studio-p1-y1wbiq | `13b313d8eaf0687907178ceedc406a7154e0a473` | 49 |
| claude/forge-protected-auth-uodup2 | `e2bab901cdcab15018a80eadefefe64ae565d0e5` | 58 |
| claude/md-file-prompt-ot7tdb | `ef15445374fda3aaefa117a2d27493d6b939819d` | 57 |
| claude/prompt-forge-full-capture-8sxvli | `58323b0af0eeafc3204cfbd5c31cb068a3cf5a88` | 59 |
| claude/repo-backed-image-packs-qke6mb | `dcaa1465eb0eb58001ced42ac4b3f60f2a12d6db` | 50 |
| claude/stormrender-highest-scaling-yj2nef | `e48d3fb0952092b421961bc3edfb369370d59e09` | 19 |
| content-132-133-main | `3e23a29af5324f283c73ef64fa295e15dcc555d9` | 18 |
| content-133-rationale | `68020521199b0a0cdc6ffa202a21f1a231f73d5c` | 18 |
| content-134-suragu | `52c0e91ef468049a5f7fb55aa2892025e84790ca` | 18 |
| content-134-withdraw | `5d12b5db13da49d52d5751c6fa3f01e549a3a966` | 18 |
| content-135-tetsugan | `1cd4fca62735f81013d490ce48c80af66fce0bef` | 18 |
| content-136-jutsu-text | `c3e0d4eb2b017f5e941b478557c7b7d018171c86` | 18 |
| content-136-titles | `ded2f66481ce8cac65d7c382a230fb63a4926fdb` | 18 |
| content-137-accuracy | `8b0bf44200aeb7277730feba5693e0d604b5294e` | 18 |
| content-137-item-desc | `2553abb28e0aaaf8e069f74ab06d9796f9d25f01` | 18 |
| content-138-grammar | `675aeb6c7913009ff5c6621b8fe28e74b07638ab` | 18 |
| content-139-keel-walk | `e25a064b94ea4fc4594cb9406a47e02414542d61` | 18 |
| content-140-portraits | `e30bdeef354066c9a163d9e83b84f48ce5c01825` | 18 |
| content-141-medallion | `54f32109792c9df3f5712b687ce1a1c7a20bf120` | 18 |
| content-142-bakuhatsu-icons | `da0b97c6e2e8d5c8e1a97917da6cdb5fd52ae22b` | 18 |
| content-143-jutsu-targets | `54f686568a3b2a91bf123fdb972d6de8c5073616` | 18 |
| content-144-frost-warden | `277bb844d873ae3fc209e3cdbb9bdc3e0ffd1b00` | 18 |
| content-148-replacement-technique-icon | `0d083bb6397db7fe8048de465ce8a50b7ec6262c` | 18 |
| content-149-searing-might-icon | `0d99d7cf00da2445c55a6d6d6b69a5ce327ab367` | 18 |
| content-150-poisonous-senbon-icon | `618c58a081016e86ae49736233b80091d2d7c251` | 18 |
| content-151-sonic-slash-icon | `5f4f06f151e264c0862831f54239bd2ec7074b62` | 18 |
| content-152-soul-shackles-icon | `c8bd6d8469a61cb37d01509484798638e7610153` | 18 |
| content-153-venomous-phobia-icon | `9c753d5feada9ae3cc0bf891dba7ae675a2a60c6` | 18 |
| content-frost-warden-shelved | `a2e6a456763ad81cd2e27d5985c15c47b9787a3c` | 18 |
| docs-art-director-prompts | `8d730fa28cf45473683ae59b936e604920605f66` | 18 |
| docs-bakuhatsu-approved-icons | `f6c6535914a8c556063c400af6261787fa680ac2` | 18 |
| docs-bakuhatsu-family-accepted | `89badedefd5ef4199e36101f5fca9452710a247b` | 18 |
| docs-ghost-ship-chest-art | `318f30ef0081cdbfe02929571334549be7fa5f0f` | 18 |
| docs-qa-revisit | `6a7dc46a77992140b173d85a8ac84f635aba09f3` | 18 |
| docs-starter-jutsu-icons | `60b9567eb3473817942f9154d28b59f85de348fd` | 18 |
| docs-starter-jutsu-refs | `9d76de312cc78cf161cd04398dc7a8c765dcb4d4` | 18 |
| docs-village-scroll-art | `eae20e04d3355d5a2117f779aa30cc2191df283b` | 18 |
| fable/bloodright-25-tree-import-20261017 | `10fe056cebb8c3cc7ae3f106261a3ad93c9eec7a` | 22 |
| fable/bloodright-a-image-readback-20261019 | `d9cccc68090f24e78c831be8c96a525e040c0275` | 20 |
| fable/bloodright-classification-readback-20261018 | `8776a7ed1280e96d290479c3ae306872adb1cf8f` | 20 |
| fable/bloodright-classification-stage1-20261018 | `3239a1995af8ad25063faf6a1885460061f23ea9` | 20 |
| fable/bloodright-classification-stage2-20261018 | `4e4a01998ab195d5f228bad8ab3a5e83a372b78e` | 20 |
| fable/bloodright-collection-open-20261019 | `9fcb94677962352d474f22447922c2dddb40e1b9` | 20 |
| fable/bloodright-collection-review-fixes-20261017 | `68169f1d4fba823af6ac94b80cca1f7eb4fa54d1` | 22 |
| fable/bloodright-icons-final-20261019 | `cff9930579210ded3fd87c934150649e74fd6396` | 20 |
| fable/bloodright-legacy-trees-20261017 | `457cceeba938455199446fbc06353e32012fc079` | 22 |
| fable/bloodright-package-validate-20261018 | `8ffe1b8b49e6b62b6b7cbdf422a6f4a96da738b1` | 21 |
| fable/bloodright-potency-repin-20261017 | `7355b980a1b23f6ec102c5707d5eda7ab0cc1ec4` | 22 |
| fable/bloodright-readback-pinned-effects-20261018 | `59247f32563e4fdc5b0516e9b186ac130746fccc` | 20 |
| fable/bloodright-reassign-hp-20261019 | `fc7f358fa3fe680bc27283c7b0b85ff62f70d40e` | 20 |
| fable/bloodright-restore-unequipped-20261018 | `30b6dd992e3ed95f2c51b4429eb141783eadf2de` | 20 |
| fable/bloodright-round-total-rulings-20261018 | `5fdc8a0c2d342b40df5f985199d3a7c3bdeb01fb` | 20 |
| fable/bloodright-scorer-20261018 | `74d9d2e3e0464c6c31c8768bf150470dab9289db` | 20 |
| fable/ca-sy-keep-ruling-20261018 | `acf0bf7aefe834687e755a6aa9a59f69864342ba` | 20 |
| fable/content-workstream-bootstrap | `3212969a562e1d7b6e11cb3c5cc21821ab8bc7c4` | 58 |
| fable/forge-basic-attack-rule | `f1de1c2500884525dd4b613ef034a15394c8392c` | 8 |
| fable/forge-binding-detail-20261019 | `4c0554ca778076d2362659286f8cc89cbf6cb201` | 20 |
| fable/forge-bound-read-retry-20261019 | `c44e67ea9bc8dc8786986432ef3a96533bf3dc8b` | 20 |
| fable/forge-dungeon-coop-path | `a70e59c6ea7d6ef3d39b04e8be93f4907f4df97a` | 13 |
| fable/forge-dungeon-recipe | `dd8b3caebe883c0365442e496ecc2bd80d2ba891` | 13 |
| fable/forge-fields-repin-20261018 | `6aee2ac8ddec2f1cedb4b1f5f744e12515eb4317` | 20 |
| fable/forge-journal-space-20261019 | `20f2dd4936781ebf722d4329c96db3eeb2319734` | 20 |
| fable/forge-l16-ai-exempt | `c2c5f68b3a82dceac0acf684e58b1c18e18c30ef` | 5 |
| fable/forge-launcher-20261018 | `ea277ac769b53aaec128d1644cf9ff65a2dedfb7` | 20 |
| fable/forge-next-phase0 | `3130f9433810cca4f8eca78b80aeb4dc8eb7ddb0` | 52 |
| fable/forge-pet-catalogue-reads | `169353d1d7dad20a8445bc08d2f2e3e118d43763` | 8 |
| fable/forge-protected-auth | `e2bab901cdcab15018a80eadefefe64ae565d0e5` | 58 |
| fable/forge-qa-fixes-20261019 | `df53328353d2e09d7cb9c20e8b26bad350dc2b91` | 20 |
| fable/forge-require-raw-20261019 | `3ab73a7e497239063cf0dc616e221165b9ac1aac` | 20 |
| fable/forge-suggest-mode-20261019 | `4dc96cff4c308f58f63d757fa91a64cc377bfa90` | 20 |
| fable/forge-upload-verdict-20261019 | `f53405781ffdd897174d465fb5cfc39c41e315ec` | 20 |
| fable/ghost-ship-active-consume-20261011 | `fcd79e5a3401dc8d95abbdaa05d0d4664c04a6e2` | 27 |
| fable/ghost-ship-director-decisions-20261012 | `8a78115367feda143e9591f524b739a7d56330af` | 27 |
| fable/ghost-ship-final-items-crowned-20261011 | `4369f404dbfd83563d11508c2bcc2e0e17f9a786` | 27 |
| fable/ghost-ship-release-closeout-20261012 | `eaeaee3761115863f60580c3792fa10075c0102e` | 27 |
| fable/ghost-ship-release-manifest-20261012 | `7f70e59446468ca643e4d74424011da530e0c362` | 27 |
| fable/ghost-ship-sentinel-repair-20261012 | `758925d49b36ae448f1039ac1a73268272be600d` | 27 |
| fable/ghost-ship-skyglass-sentinel-repair-20261012 | `0ca96a963efd257c401d0d67d8ed852ef7809829` | 27 |
| fable/hungry-pulse-icon-ruling-20261017 | `7d3c16434515fe5737e22286c5b4f8469dc65a37` | 22 |
| fable/jutsu-icon-suggestions-20261019 | `ef817296d3e56221f95e5eda7484a53d142290b5` | 20 |
| fable/particle-cannon-retry-20261019 | `8440d86ec81a1efad32a9569f7efea530137f087` | 19 |
| fable/pet-species-builder | `c5a99e680a29cba85cef8cf8efcbf970d1bc585e` | 10 |
| fable/qw0a-contract-alignment-20261012 | `5fefb70b88f140c3212d0b9d94209e70be44f2bb` | 27 |
| fable/qw1-workstream-starter-20261012 | `1b14f9974912e8cf0d00dc9ca3ad1b34ca7e10b9` | 25 |
| fable/recipe-capture | `e0ea1cbc20fc289ba7decce650876d272e44a913` | 10 |
| fable/skyglass-check-update | `cf4ea7c26bdcf93a8d276fd3902bf3578d6b9301` | 9 |
| fable/skyglass-consistency-check | `40a5a47b77a0f10079a81ca437309727bf002ea4` | 9 |
| fable/suggest-rationale-20261019 | `3e88122686db0d30205261b1c1dcdd1ddf083078` | 20 |
| fable/variant-builder | `3c3bf622074233c7f8979211c21aedb340d5d9d4` | 9 |
| fable/variant-capture-reads | `5c5e6867f3af92f76d152da19cb378ef2f87c917` | 9 |
| fable/wayward-challenge-candidate | `d65ce6b9f82cc0565bbc2e343617d9eb0f67ce87` | 30 |
| integrate/forge-dungeon-recipe | `8f6e359861e66156c95969ebe6835764ae4dce6d` | 13 |

## Kept: not merged into main (199)

| Branch | Head SHA | Idle (days) | Commits not on main |
|---|---|---|---|
| perseverance484-patch-1 | `ce76fe79faf047f688bccc8e5b20ceec2b439a34` | 130 | 1 |
| client-contract-audit | `e86c4b411f9a17085a8b4ee3030830622fcfe823` | 66 | 1 |
| client-contract-verification | `9323a79e85a2ce638f82b95962bf46125295a429` | 66 | 1 |
| law-provenance | `21df8ec610095a597d6ff1f96d7644d18778be02` | 66 | 3 |
| chatgpt/builder-app-readiness-brief | `b8f9dbf533dd51c119eb8d530e9c2fe3506e43b4` | 61 | 1 |
| chatgpt/collaboration-bootstrap | `1e819f53de066f7d5854423611fe76039d3b8c96` | 61 | 23 |
| chatgpt/review-builder-app-4062268 | `08382eebcffcbcc464c93d348f83598fc219dd76` | 61 | 1 |
| chatgpt/review-builder-app-readiness-5ffb735 | `b4a36ac61b50a130ba20de142f41164bf29bffed` | 60 | 1 |
| chatgpt/review-builder-app-readiness-c388ea6 | `06392fbbe1d2893a98ff16ee4f430e9ee0218297` | 60 | 1 |
| claude/builder-app-production-readiness-kelsib | `e5d7ef447ac0512cfb09b3fe2c6dd46ccc7b70f3` | 60 | 1 |
| chatgpt/review-forge-full-capture | `7c540824af54004000c0210569fca65618cecfa5` | 59 | 1 |
| chatgpt/review-forge-full-capture-r2 | `11f6475fbeadd14d0c626482d17a38402cbfbcbc` | 59 | 1 |
| chatgpt/one-perfect-crop-art-refs-20260911 | `cccaaf41a85e32b81026fd56f4041d701c7a5ae8` | 58 | 2 |
| chatgpt/review-content-workstream-bootstrap | `36560e6ae79f8f3e8e515a2b34ced599f76a0231` | 58 | 1 |
| chatgpt/review-content-workstream-bootstrap-r2 | `83d8bc280c2a357f336a5ae0fb334720bc4b7b53` | 58 | 1 |
| chatgpt/review-forge-protected-auth | `30741283b7de08c86def3fab1299def3f0fd353d` | 58 | 1 |
| chatgpt/review-forge-protected-auth-r2 | `24c703bf676f6fffa2fc9fb33be97da279a9e4db` | 58 | 1 |
| chatgpt/review-forge-protected-auth-r3 | `fdc86bb843c9121e8b0f20a38e6a6c7f2db0f049` | 58 | 1 |
| chatgpt/aerathiel-guide-assets | `32a5d60859b146fd66049de32a86acdb5f23ebc6` | 57 | 15 |
| chatgpt/review-art-generation-preflight | `fdc704586a24eb48fa94ffb93131b9cf963137c0` | 57 | 7 |
| claude/art-generation-preflight-sq6j3n | `05c43de9eba065a59605d84378f45b7badca4664` | 57 | 6 |
| fable/art-generation-preflight | `05c43de9eba065a59605d84378f45b7badca4664` | 57 | 6 |
| chatgpt/forge-next-planning | `88680fb52e208747bb353ce1e37e7d33e3f41231` | 56 | 32 |
| chatgpt/forge-next-planning-workspace-temp | `91ba77d9c36482612d5555a144085d20d22b9ea3` | 56 | 23 |
| chatgpt/forge-next-planning-workspace-temp2 | `91ba77d9c36482612d5555a144085d20d22b9ea3` | 56 | 23 |
| chatgpt/guide-studio-spec | `87fb673938d915c0732351d2efb208d05ef38c7c` | 56 | 6 |
| chatgpt/night-parade-official-pack | `af6f25e6fb763ebc1dbe81e8aa1b03fec3485c45` | 56 | 2 |
| chatgpt/review-forge-carrier-disappears | `efec065368383b45da1c0aba38472017b3025559` | 56 | 1 |
| chatgpt/review-forge-next-planning | `a991abc2e6af0dfe25ae06e032541a0b73409e8d` | 56 | 48 |
| claude/forge-quest-studio-audit-j4jhcf | `43b8ef1c4b6f80042a52c5a73fd64a1314dd030a` | 56 | 1 |
| astra/guide-studio-staging-handoff | `0b1ab2b5affb846018153f500b48a391c8471b34` | 55 | 1 |
| chatgpt/godstorm-pyramid-final-audit | `18e3367a5f45a9d4a81ad0bdec955eb22556a522` | 55 | 1 |
| chatgpt/godstorm-pyramid-readiness | `943cb0d3175bbe1002afe54fd6e2da82ad40101a` | 55 | 2 |
| claude/forge-next-planning-v3frzi | `22f1fc43f8e316d0ec8412d5595a7cd0936f98d0` | 55 | 51 |
| chatgpt/godstorm-two-pyramid-release-plan-20260915 | `bad3d731520b7079ab4a98e2a882ac55060cff5b` | 54 | 2 |
| chatgpt/godstorm-art-recovery | `1bca57eeb0c1836a49334dc2f49196a5a3db24c7` | 53 | 17 |
| chatgpt/godstorm-source-art-pack | `549b13b3a0202e6740a683a54eab300b5b64a69f` | 53 | 14 |
| chatgpt/review-forge-next-planning-r2 | `2aabc28bf99bda4d1cf2e7c454f969067df260b3` | 53 | 52 |
| chatgpt/forge-next-phase1-brief | `4848b0851495faecc587bc6515d0f4ea8d555937` | 52 | 1 |
| chatgpt/forge-next-unified-contract | `efbdc2a4a2f35b12b425ba88a4d415f66f79f2c0` | 52 | 3 |
| chatgpt/forge-quest-studio-final-fix | `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` | 52 | 121 |
| chatgpt/forge-quest-studio-foundation | `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` | 52 | 121 |
| chatgpt/forge-quest-studio-source-push-temp | `2f0e656d1102cf8ca64530255ba8990faab9cf47` | 52 | 99 |
| chatgpt/forge-quest-studio-source-push-temp2 | `2f0e656d1102cf8ca64530255ba8990faab9cf47` | 52 | 99 |
| chatgpt/forge-quest-studio-source-push-work | `1f6a1097e33108d595ca27067a7240cf14b98ded` | 52 | 114 |
| chatgpt/review-forge-next-phase0 | `a8c01ecce498820e41334f32e65c4cd250affeea` | 52 | 2 |
| chatgpt/review-forge-next-phase0-final | `057b61d3ed5740d8cd94da883606c308761e1b73` | 52 | 1 |
| chatgpt/review-forge-next-phase0-integration | `ad6a82f385219859b457dbabc0b46c4303152c70` | 52 | 1 |
| chatgpt/review-opc-core-manifest-20260916 | `439b7f88e74ec5be9d8559bb8b8730b1e1cff557` | 52 | 2 |
| chatgpt/review-opc-forge041-r2-20260916 | `fba3e54c86bfdb681ca9bd9c3b884d2c475add4f` | 52 | 1 |
| claude/forge-next-planning-reconciled | `ba51a28a99a7748e61de0c2768bd73ab9c65c856` | 52 | 52 |
| claude/handoff-format-standard | `d6669a7aca5cde7fa126bbba4eed3265ae6a6916` | 52 | 1 |
| claude/one-perfect-crop-manifest-9wsry6 | `1f514b392707926c76b08a005c992b7848f7fa8e` | 52 | 1 |
| claude/quest-studio-final-review | `82bb686370f3f8cbbe57068fe42b887c90fdf48d` | 52 | 122 |
| claude/quest-studio-source-push-review | `10658b817b51a77efcc18470ef8ef9b9e89e1dbe` | 52 | 115 |
| chatgpt/godstorm-two-pyramid-plan | `4d5ee40c62dad55b30854f8bfa242cf6ef0936fb` | 50 | 37 |
| chatgpt/review-godstorm-forge-defects-repair | `f378a6320c84490931d1eb3bf04a79c0e0c611e9` | 50 | 1 |
| chatgpt/review-repo-backed-image-packs | `2618043433e06519fbfad450cbd06a3314822c7a` | 50 | 1 |
| chatgpt/review-repo-backed-image-packs-correction1 | `c0baa26b003a21ff1e04d47be372a81e92d3d83d` | 50 | 1 |
| chatgpt/forge-presentation-studio-design | `4532ef917a1dfb40d00c554fd7f065e13216afc7` | 49 | 1 |
| chatgpt/forge-presentation-studio-plan | `b326b6a4d05cc9de5a251092f56100357ff707f8` | 49 | 5 |
| chatgpt/review-forge-presentation-studio-p1 | `9a9a3ea03d56cdcd1f6cf40f75d73c5ba4b2d985` | 49 | 1 |
| chatgpt/review-forge-presentation-studio-p1-r2 | `fb47225a150e89ee74028b38cb31b0aed809c20a` | 49 | 1 |
| chatgpt/review-forge-presentation-studio-p1-r3 | `939168b6045e2469ec2c9934429b2c61b4ef1a9a` | 49 | 1 |
| chatgpt/tag-design-audit | `c71afeb8d6415b2c2a1df44cb3744d642eb7584e` | 48 | 1 |
| chatgpt/one-perfect-crop-scene-characters-20260923 | `f24a343ee6792ddfd105b7f38abba9dae2476f3f` | 45 | 6 |
| chatgpt/opc-art-final-validation-20260927 | `879f107103ebee0b204ac87a6f8b14cb4a9decb9` | 41 | 1 |
| chatgpt/opc-art-final-validation2-20260927 | `0c1ef25bc0b60d8eaa7e4ed11eb8efbf03571a05` | 41 | 1 |
| chatgpt/opc-art-final-validation3-20260927 | `207f8de682ead594a4a4d26420ff7f7e4e3b3251` | 41 | 1 |
| chatgpt/opc-launch-final-integration-check-20260928 | `dfeb22d87bf7ee844ab4406528d8ca60bf300ebc` | 41 | 1 |
| chatgpt/opc-launch-finalization-20260924 | `0b997636731f55e99d278518c034f26a2c58aab6` | 41 | 2 |
| chatgpt/opc-launch-finalization-ci-20260926 | `9d24098aa05cc14d54f3ed0d905140a72ce5088c` | 41 | 7 |
| chatgpt/opc-partial-failure-repair-brief-20260928 | `3c9211d7e6c2eed00cd7c72d4c60a5c40e35c87b` | 41 | 4 |
| chatgpt/opc-render-final-20260927 | `6b80090ff5005a1c207f446847ef6ee89b036b4d` | 41 | 2 |
| chatgpt/opc-scene-asset-stage-20260927 | `93fb74d13ff6153e1f1e4485c5ecb4e623831b72` | 41 | 23 |
| chatgpt/opc-scene-finalize-gen-20260927 | `eff426fb2fbdf7adc3343ebd6a94227830c70fe8` | 41 | 2 |
| chatgpt/opc-scene-finalize-gen2-20260927 | `558f833bdeb246a22a7c9732a311766f25e6de5f` | 41 | 2 |
| chatgpt/opc-asset-repair-ci-20260929 | `0a76d585d273f8c4d6e1b613d453235e2b9eb8a4` | 40 | 2 |
| chatgpt/potency-chakra-mandala-design-20260929 | `c4cb44ba3c08308cd2776738689f5956f2b49ea6` | 39 | 6 |
| claude/forge-next-phase1-uwhcn1 | `319987f4979767e39d3ea09f0dd6da654a293989` | 39 | 16 |
| fable/forge-next-phase1 | `319987f4979767e39d3ea09f0dd6da654a293989` | 39 | 16 |
| chatgpt/ghost-ship-skyglass-art-20261001 | `a18c19631c8827a738eaf696a4545737efd69a49` | 38 | 8 |
| chatgpt/bloodright-planning-handoff-20261002 | `4ea6605a8657439ea32eeb0b4d1e7b603e2bd830` | 36 | 4 |
| chatgpt/taiyo-kami-capture-20261002 | `ee43182a41850f09d10d4876fec9d376c861adca` | 36 | 3 |
| chatgpt/horizontal-item-progression-acquisition-20261004 | `f16734f5b4a79fae1e915dd88a15c24bf9021851` | 35 | 1 |
| chatgpt/bloodline-reskin-commerce-proposal-20261005 | `3936aa6c4f879c137748fbc3141b5cbaebe9a0fc` | 34 | 1 |
| chatgpt/jellyfish-beach-quest-20261004 | `eea80baa053a0e794f3038c93c747d32795ecfc9` | 34 | 11 |
| fable/bloodright-planning-20261003 | `7c1dfdd5e3ee163b90c22694dbb2de94ede08866` | 34 | 67 |
| chatgpt/review-jutsu-art-20261005 | `b330b3eeeb8cf2dcda22b0d7eacdcd84c3dcb4d0` | 33 | 1 |
| chatgpt/review-jutsu-art-corrections-20261006 | `806fb2208df819e1656cdf3d66937b63a4df4b4b` | 33 | 1 |
| chatgpt/task-first-restructure | `0ef20144fa8a32ce27a321c49254f1699278c084` | 33 | 1 |
| chatgpt/art-weapon-master-parity | `8cddf21905937a20ce0c621993872367dfd56714` | 32 | 8 |
| chatgpt/genin-battle-pyramids-plan-20261005 | `457ca8f437740011414f095098d395572a4338c9` | 32 | 8 |
| chatgpt/bloodright-icon-production-tracker-20261008 | `c85c1ea834e24315b5688f73a65c35479b8963e6` | 31 | 6 |
| claude/ai-jutsu-reequip-validation-7ywxag | `62ad0cf2f0b9253964f19ef72ef385b485d1d055` | 30 | 1 |
| chatgpt/quest-workflow-skyglass-retrospective-20261012 | `c34f7de572337b0d2cfe397b9331502aa6548e27` | 27 | 5 |
| chatgpt/review-qw1-workstream-starter-20261012 | `8d91512d98165a031f8e04859e8d45c862320080` | 26 | 1 |
| chatgpt/review-resort-in-need-20261013 | `72eaefb15de6889e54c0e8fc052ce58029dc59fd` | 26 | 9 |
| claude/crafting-recipe-census-pln5za | `eb625ca192fa440b76b204d48d13dbd89576ff7f` | 26 | 1 |
| chatgpt/qw0a-continuation-brief-20261014 | `2d2390e769587bc307b83971923ba4700a63e80d` | 25 | 2 |
| chatgpt/qw1-integration-checkpoint-20261014 | `7a9578d42dfff0e0cbb61c6430c84f3bc30436eb` | 25 | 1 |
| chatgpt/review-qw0a-extractor-20261014 | `3f64e065e5f79ab0ce1daad42d9fcbadc2e75d0a` | 25 | 2 |
| chatgpt/review-qw0a-extractor-corrections-20261014 | `f517edd4b12e386bf88b76d8a2bc76c3dd49eb51` | 25 | 3 |
| chatgpt/silent-bastion-content-execution-plan-20261014 | `c9f30ee7c6dfb444ac28851d1fd4c8dd8f46f4d1` | 25 | 25 |
| chatgpt/silent-bastion-design-20261013 | `450c47bf88b38758477b5783569ea6ab7a0c146a` | 25 | 20 |
| claude/silent-bastion-phase1-validation-9628h6 | `33be3cd2fe504d508ade2ab04d15e45f4c752ed3` | 25 | 24 |
| chatgpt/bbe-jutsu-art-studio-20261014 | `5b21279495a4a8404160d1762dd63dcf27ca93c7` | 24 | 6 |
| fable/qw0a-extractor-fidelity-20261014 | `f69889cf1f6c0d6a659462448f0a7ee4525f8e04` | 24 | 3 |
| chatgpt/bloodright-icon-studio-20261016 | `792742c264c70c29733306f22962d7b4aad48fad` | 23 | 11 |
| chatgpt/bloodright-reference-library-brief-20261016 | `1b3b93b3ac939afc2fed1c63390fe68ed0d261d6` | 23 | 1 |
| chatgpt/houkyuken-jutsu-art-studio-20261016 | `6e3b138674e02892a41610f04b8574a2393ef899` | 23 | 27 |
| chatgpt/recipe-aligned-reward-caches-20261016 | `fb744e713873a99812b7c6e9ec8631769ef9ff9a` | 23 | 1 |
| chatgpt/review-silent-bastion-c99-20261016 | `b370490fb364debf1956b77a64ff9755b1eced2f` | 23 | 42 |
| chatgpt/silent-bastion-alt99-approval-20261016 | `c54a96883113979223d7989c1080ae25a480337e` | 23 | 45 |
| chatgpt/silent-bastion-caches-claude-handoff-20261016 | `25d2b2e159d9fb9b0769db5483571e0db87991f6` | 23 | 1 |
| chatgpt/silent-bastion-node-budget-20261015 | `2af1ffd808f692d241b80c1d2c87e6e6d967016b` | 23 | 38 |
| chatgpt/vaporia-jutsu-art-studio-20261015 | `730f5393d4428282402f5f66ef2aeea3d156e405` | 23 | 19 |
| claude/recipe-cache-native-proof-69za5u | `b133d73286df9e48ba1015b21dd694c69c9ea090` | 23 | 1 |
| claude/silent-bastion-budget-validation-69za5u | `74eeb328f05d4258056b0a1c531619ffcf852ce3` | 23 | 41 |
| chatgpt/bbe-final-export-closeout-20261017 | `e5aa3b13eb4896e93b3e85799b8f0ec2eaedeb9f` | 22 | 1 |
| chatgpt/bee-jutsu-art-studio-20261014 | `1f6010be0967d1ed42645a1a7476b8a1ec2a75e2` | 22 | 79 |
| chatgpt/bloodline-jutsu-studio-zip-first-20261017 | `d04a87c05999c7037af8667db2b2b79324a53d3c` | 22 | 15 |
| chatgpt/bloodright-factory-pilot-closeout-20261017 | `2df5957f6dfd63f43be85766fd87eebb99d71243` | 22 | 24 |
| chatgpt/bloodright-remainder-factory-plan-20261017 | `7d9830318606562cbc9b1c420fc302d3a463c9e5` | 22 | 19 |
| chatgpt/bloodright-structural-priority-20261017 | `620223109623ab044f0580b78ad1ebe5eac2b83c` | 22 | 3 |
| chatgpt/bloodright-wave02-art-closeout-20261017 | `8009ebad7d45a1046b550542d4e89071c22f4dd6` | 22 | 28 |
| chatgpt/bloodright-wave03-art-studio-20261017 | `47e6a374478654d93fdf7d6d15e3f1ee68730955` | 22 | 69 |
| chatgpt/ethereal-monarch-bloodright-art-qc-20261017 | `4cb46b4ee2076aaf3b122d197cb4c615d24c08eb` | 22 | 13 |
| chatgpt/review-bbe-final-closeout-pr41-20261017 | `c45d6b346f0f67ffa167d3278d446c0f38d46f35` | 22 | 3 |
| chatgpt/review-jutsu-icon-alpha-20261016 | `0763effd1986115a156ae8c5fdc0614565bcbebb` | 22 | 2 |
| chatgpt/review-silent-bastion-authoring-20261016 | `ba4fbaf581d1100badb64fc802984c18cef52012` | 22 | 8 |
| chatgpt/review-silent-bastion-authoring-r2-20261017 | `ecc94a206434bb21e27bea01aa8f6e606ff7fa9e` | 22 | 2 |
| claude/silent-bastion-authoring-69za5u | `6271e1f7fef4b1009c29756bdbab1d25f1467f1f` | 22 | 1 |
| fable/bloodright-reference-library-20261016 | `bf6c3c5fe5fcc793c06373da106d29ddb3226c34` | 22 | 7 |
| chatgpt/bloodright-wave04-art-studio-20261017 | `374589b77410a42384e9fe15ca625aa5913f5b0a` | 21 | 99 |
| chatgpt/bloodright-wave05-art-studio-20261017 | `5512aa0e8faad6153e13122c262e5277e58c6a08` | 21 | 142 |
| claude/bloodline-jutsu-icon-studio-3nmvc2 | `18f52dd308eb59f8027e1e9e6892427842f98578` | 21 | 17 |
| chatgpt/aerathiel-jutsu-art-studio-20261019 | `2994305e5cd4894953a14b7c1d8727ddfc00fdd3` | 20 | 7 |
| chatgpt/bbe-midnight-alloy-foundation-pilot-20261018 | `9bd0c2621d0c10ee91fbf92b5ae86f6880806cb4` | 20 | 185 |
| chatgpt/bbe-midnight-alloy-trio-20261018 | `c016a4d8230666e3fd265379023ce6a03546e598` | 20 | 188 |
| chatgpt/bbe-pale-blue-source-correction-20261018 | `557ed266567d45324b746a40e467c0f0635ae8ce` | 20 | 196 |
| chatgpt/bbe-tier-geometry-diagnosis-20261018 | `65132ecfae542d56c9f17422ca473c9e29d776f2` | 20 | 183 |
| chatgpt/bee-bloodright-tier-studio-20261018 | `8b6edf8045b5f51331a7ac3f9c011e8907fe326d` | 20 | 205 |
| chatgpt/bloodright-approved-original-sizepass-20261018 | `e2883b1c627434d569ae32d68e6295978250980d` | 20 | 182 |
| chatgpt/bloodright-pixelart-wave01-20261018 | `da68f34d6d400cd11a9244ebbff66079be53b3fc` | 20 | 175 |
| chatgpt/bloodright-wave06-art-studio-20261018 | `b9150dd7c05701fe443c8b41472a2cfc9744057a` | 20 | 173 |
| chatgpt/itojinsei-blackwire-finalization-20261018 | `9031f8d2af522677ff2dfe643fe7d188d42157e1` | 20 | 216 |
| chatgpt/review-jutsu-icon-p1-20261019 | `c2c77af27baae456c39e312e0acc007ae558bc79` | 20 | 3 |
| fable/forge-suggest-scope-20261019 | `ed8ac9a7c31f2c7de54f92d12dc6d353095ef009` | 20 | 1 |
| chatgpt/elementaldamage-godstorm-capture-review-20261020 | `dcccb8a7b7bade48993ceb98a2a9db2fd1450cef` | 19 | 1 |
| chatgpt/elementaldamage-weapon-census-handoff-20261020 | `38740f228958020ec183bbf0950e288e455c5698` | 19 | 1 |
| chatgpt/premium-pet-visual-prompt-proposal-20261020 | `f8059013dc44f26e4e0bd6f09bfec4b7fb6dc601` | 19 | 9 |
| chatgpt/review-elementaldamage-census-round2-20261020 | `e2fc3c20d927ff521523cd04af13f64c91935dda` | 19 | 4 |
| chatgpt/review-elementaldamage-weapon-census-20261020 | `3a30a604399d3b179b17f7cc3e833e985f72afd6` | 19 | 3 |
| chatgpt/review-pr76-integration-20261020 | `62b81061d644054e798261e6ab82661caa147f09` | 19 | 1 |
| chatgpt/review-pr76-round2-20261020 | `4791ebc6397c1e157a839a7579353e8d950b82f4` | 19 | 1 |
| chatgpt/shinseina-ki-jutsu-art-studio-20261019 | `33a349cfaeff0deadf44d9189c289238b0fe4c51` | 19 | 18 |
| ccr-504cc1a9-bljl5m | `7e9cbf5e5428f9f42eae6894388ce102949ad657` | 18 | 1 |
| ccr-9a2d53da-6kh6du | `ff12461c4eeaf847541462c8b8b3f77edcc771da` | 18 | 11 |
| chatgpt/ash-jutsu-prompt-desk-20261019 | `05c74ceb86a14ed69378ebe3e4416256ac6fcea7` | 18 | 11 |
| chatgpt/bakuhatsu-jutsu-art-studio-20261019 | `fca659fec26af61ae4fe99b5ad2752440177cc42` | 18 | 53 |
| chatgpt/living-lineages-kitsune-workdesk-20261020 | `1c641818de9e96007ea598e27cfe30bb96cf0f16` | 18 | 70 |
| chatgpt/master-asset-processing-handoff-20261020 | `788722af4170357efbc62b3b197fad21f7cb99aa` | 18 | 1 |
| chatgpt/review-elementaldamage-census-round3-20261020 | `f82251b1c43089626ad67007a9f529d5fd88bd11` | 18 | 5 |
| claude/elemental-damage-weapon-census-235ynv | `8b5bf9d87ca46f84027c702bdff86a30338c7ddb` | 18 | 4 |
| claude/tnr-content-tickets-tcbi34 | `9bf6a7ed9de149eddc2ca776ffd9015b0ad790a3` | 18 | 4 |
| content-146-frost-warden-direct | `1c79771b631b48cdc4e11b191960d46c8de8c348` | 18 | 1 |
| chatgpt/crystal-essence-jutsu-art-studio-20261020 | `0371302eb7e273cb692d511d2b14d2934c7aac22` | 17 | 54 |
| chatgpt/ghost-ship-chest-icon-art-studio-20261020 | `d7080bd4551cd8b454a34b4941234774d93ff0eb` | 17 | 121 |
| fable/contracts-107d7a8 | `999a6bba25e07f0e97b7ea609abd0b292c3f719c` | 17 | 6 |
| chatgpt/art-tempest-cleave-premium-refinement-20261024 | `d55c1f6b7ab8796b4fbf355cc6d2ba73f7b68caf` | 15 | 7 |
| fable/pixel-art-snap | `850833a473a484d460e83c01d05fea1f5832b5b7` | 15 | 3 |
| chatgpt/ethereal-rebirth-fox-ribbon-pass2-plan-20261024 | `0d76c5fc7950481f13fa6b067684006af29eb06d` | 14 | 1 |
| chatgpt/ethereal-rebirth-fox-ribbon-refinement-20261024 | `94bbc2e2170bc9f93e4acfc24692569cf12f279c` | 14 | 1 |
| fable/forge-suggest-create | `92d8103afd5f5d2ccc5b0ca2ffcd265805d4d233` | 14 | 1 |
| fable/skyglass-art-bible-v04 | `4cf82b3514a67d74eddd89147cf32e49f634435c` | 13 | 2 |
| fable/validate-stale-rules | `271d11032507553baee30472acb3754f9693926b` | 13 | 2 |
| chatgpt/aura-of-despair-art-lock-20261026 | `f2de962f4b3ed7190960a0c00c37ea7f7e4d0eb4` | 12 | 2 |
| chatgpt/hellfire-harvest-art-approval-20261026 | `1ae8e3d0a5e7c371a485980ebe9720d5a472c730` | 12 | 2 |
| fable/badge-builder | `c75d676ba3437816d5d30397769bb12946951689` | 10 | 1 |
| fable/crowned-captain-sim | `035212efb922e1cceec5fb8e4490740b49872de2` | 10 | 14 |
| fable/skyglass-charts-sim | `f76946765c4238deb73d8ab4b2db814271fd9dd5` | 10 | 14 |
| fable/skyglass-hunts-sim | `aac4a2219962995406080ca6dd9593141906d2f5` | 10 | 11 |
| fable/skyglass-wreck-sim | `ce25fac8ccbc621dd2e33f50a848f185457602dc` | 10 | 17 |
| fable/skyglass-final-sim | `d5957e793f0eeced2e771e0f606c070c68fd049c` | 9 | 54 |
| fable/skyglass-haul-sim | `b973ff284ed62da45ebe417b73412ed9dc622ec3` | 9 | 25 |
| fable/skyglass-haul-fit | `6ad2a102a9b0845411100f1c6f6cf08a63691c93` | 8 | 55 |
| fable/skyglass-kite-sim | `c546b0d7670719c7a010b101d51c8bf60899fd16` | 7 | 76 |
| fable/skyglass-rule-cap | `3e345c2067e10aa9260efd73d7e2368eb2167354` | 7 | 76 |
| chatgpt/premium-seichi-item-icon-overhaul-v10 | `cf2cfbb7706b47cff00453e3cea7d19071e0bb73` | 5 | 15 |
| fable/skyglass-economy-model | `5f44191b0c50976980fb4b63874fd253d7099e80` | 5 | 2 |
| fable/early-game-sim | `0e83cb94ea86e1a1a29808545793fbba7cfbf116` | 3 | 5 |
| fable/mother-of-echoes-act3 | `11ec84e4fb088e982b4a776b4c139473d3943344` | 2 | 108 |
| fable/mother-of-echoes-sim | `fd3531153df7a1dfa9f4e559b39d1ad50055a0f6` | 2 | 115 |
| claude/quest-cleanup-2026-11-07 | `710620bb919216d3cb514f8d34fbfc77f3fe39ab` | 1 | 1 |
| duet/moe-uploadthing | `5d63cb2f878e2a4320237bc44cec31b74478a0b8` | 0 | 14 |
| fable/forge-bundle-rebuild | `908e96dba9e988d79425b2bae8f71b8cb6d58247` | 0 | 2 |
| fable/rulings-split | `19325017a894aef8a9b3fb9a32029ace5eee3a97` | 0 | 1 |
| fable/state-refresh | `75d919fa5dd4980b2c1b1b5ceb47ebcd9b6a190a` | 0 | 1 |

## Kept: merged but active in the last 3 days (3)

- origin `05982ffa73e98b86c448fc55a29682827760cc9d`
- fable/forge-mcp-runner `edaeb6599286a5e559e33e991a6b2fa6db4fee9e`
- fable/run-lock `526752b28c9a973f362ebd2420c630bfd833853a`
- builder-app `4062268f` (grandfathered)

