# Design options, as written

These are the independent proposals the recommendations in sections D, D_VISUAL_SYSTEM and F were weighed from. They are committed so a reviewer can open the input rather than take the recommendation on trust.

Each file is one option, argued by an agent that read the code and the binding rulings and was told to make the strongest honest case for its own position, to cite what it opened, and to list its own weaknesses.

| File | Family | What it argues |
|---|---|---|
| `ia-operation.json` | information architecture | destinations are the consequence the operator is about to have; content type is a filter |
| `ia-content-type.json` | information architecture | destinations are content types; operations are actions inside them |
| `arch-evolve.json` | architecture | keep the current rendering and layer boundaries, add a headless facade and a render discipline |
| `arch-replace-ui.json` | architecture | replace the UI layer outright with an in-house component runtime, leave the execution core closed |
| `arch-core-shell.json` | architecture | extract a headless core with an explicit API, treat today's overlay as one host among several |
| `queue-model.json` | data | the repository review package is the queue index and the live game is the state column |
| `capture-model.json` | data | capture tiers, the registry expansion policy and the projection mode |
| `visual-a.json`, `visual-b.json`, `visual-c.json` | visual | three directions explored before the director ruled the north star; kept as the graft sources the synthesis names |
| `synth-visual.json` | visual | the synthesis that `D_VISUAL_SYSTEM.md` is rendered from |

What is not here: a judged panel synthesis for the architecture and data families. The judging stage was stopped to keep the pass moving, so sections D, F and I say in their own words that the recommendation is the planning owner's, built from these options rather than from a scored panel. The two information-architecture options are the only ones where a third option was planned and not written; D.1 names it.

These files are inputs, not evidence about the repository. Where an option asserts a fact, the section that adopted it re-verified the citation first.
