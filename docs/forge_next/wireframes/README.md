# Forge Next planning wireframes

Static planning artifacts, not production UI. Each page shows the same screen at phone width (390 x 844) and desktop width (1280 x 800) and lists the open director decisions it depends on and the evidence it is drawn from.

- `index.html` links every screen and shows the theme token tiles.
- `wf01` to `wf17` are the screens, ending with the degraded and refused states (session not ready, an action the role cannot perform, the rate limiter tripped, a read whose body did not persist, storage the browser would not make durable); `review/` holds rendered captures of 7 of them (JPEG, 1400 px wide) for reviewers without a browser.
- `src/` regenerates everything: `python3 src/gen.py <out dir>` renders `src/specs.json` with `src/themes.json`; `python3 src/build_specs.py` rebuilds `specs.json` from the screen definitions.

Navigation labels, operation-mode names and colours, and lane names are the recommendation's defaults and remain open (K-20 to K-24, pending predecessor-transcript reconciliation). The theme switcher on each page shows the approved direction ("Forge"), a neutral wireframe theme, and the two superseded explorations for reference only.

Everything is self-contained HTML with inline CSS and no external resources; nothing here contacts any host.
