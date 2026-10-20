# TNR Pet Art — Reference-Led Evolutions

**The goal:** Every pet of the same species should share a recognizable design and premium TNR pixel-art quality, while each player's pet remains unique.

**1. One base reference per species.** I'll supply an approved image for each species, like our Kitsune, Dragon and Phoenix examples. It establishes **anatomy, silhouette and art quality** — *not* fixed colours, markings, aura or pose.

**2. Generate the player's first pet (Rank 1).** Give the generator that species' base image, the player's **rolled palette + marking + aura**, and an editable **Rank 1 concept**. It creates a unique pet image. **Save that image as this individual pet's reference.**

**3. Evolve the same pet (Ranks 2–10).** From then on, give the generator the pet's **latest accepted image** (not the generic base image) plus an **editable evolution concept for this species and rank**. Make the change clear and logical: a tiger develops its own musculature, fangs or fur, *not feathers*. Keep the pet's unique colours, markings and recognizable identity. The accepted new image becomes the reference for the next rank.

> **Flow:** Species base image → unique Rank 1 pet → Rank 2 → … → Rank 10. Each arrow after Rank 1 uses the previous accepted pet image.

### What I'd like added

- **Species editor:** one uploadable **base reference image** and **10 editable rank concepts** per species (Rank 1 plus nine evolutions).
- **Generation logic:** use the species image **only for initial creation**, then reuse each pet's last accepted image for rank-ups; keep player cosmetics and same-rank redraws intact.
- **Quality:** premium crisp, detailed pixel art like the approved examples; clean transparent full-body sprites, correct species anatomy, no background or ground shadow. Keep the existing cutout, moderation and visual-review checks.

**I'll provide the base images and rank-by-rank descriptions.** No nine fixed uploads per species and **no multi-image reference system needed for this flow**: the current generator already accepts one reference image for evolutions.

*Design handoff, not a deployed change. Source checked: `studie-tech/TheNinjaRPG@19e2010f9cd3f9be26fff96cca0bf6dece322f11`.*
