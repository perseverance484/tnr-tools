# Stage 8: Art

Design names the art; it does not make it. Each asset is a row in `art.slots`.

## Template (one slot)

```json
{ "id": "<slug>", "for": "<what it depicts and where it is used>", "target": "<art spec target>",
  "handoff": "producing-tnr-art | animating-tnr-combat", "note": "<what the design needs from it>" }
```

Still art (icons, avatars, scene art) goes to `producing-tnr-art`. Anything that moves in a
battle goes to `animating-tnr-combat`. Art direction is the director's: describe what the
design needs the picture to say, not how it must look.

## Exit checklist

- [ ] Every enemy that appears in dialog has a scene character slot as well as an avatar
      (engine law 49).
- [ ] Every telegraph has a mark slot and every payoff an animation slot.
- [ ] The receiving skill's own gates are the acceptance; none are restated here.
