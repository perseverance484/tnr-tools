export function assertTemplate(t, registry) {
  const fail = (why) => {
    throw new Error(`Incomplete template ${t.slug}: ${why}`);
  };
  const hasImage = (x) => x?.url && x.sha256 && registry.imageData[x.url];
  if (
    !t.bloodlineId ||
    !t.name ||
    !t.version ||
    !t.identity ||
    t.intro.length !== 2 ||
    t.intro.some((x) => !x.trim()) ||
    !t.overview ||
    !hasImage(t.hero)
  )
    fail("foundation");
  if (!registry.bloodlines.some((b) => b.id === t.bloodlineId))
    fail("bloodline");
  const expected = registry.jutsu
    .filter(
      (j) =>
        j.bloodlineId === t.bloodlineId && j.type === "BLOODLINE" && !j.hidden,
    )
    .map((j) => j.id)
    .sort();
  if (
    !expected.length ||
    JSON.stringify([...t.coreKit].sort()) !== JSON.stringify(expected)
  )
    fail("core kit membership");
  if (
    new Set(t.chapters.map((c) => c.id)).size !== t.chapters.length ||
    !t.chapters.length
  )
    fail("chapters");
  for (const id of t.coreKit) {
    const j = registry.jutsu.find((j) => j.id === id);
    if (!j?.effects.length || !hasImage(j.image)) fail("jutsu " + id);
  }
  for (const mod of t.modules) {
    const gate = registry.summons.find((s) => s.id === mod.gateId);
    if (!gate || !mod.summons?.length) fail("summon system");
    const linked = gate.jutsuIds
      .flatMap(
        (id) =>
          registry.jutsu
            .find((j) => j.id === id)
            ?.effects.filter((e) => e.summonId)
            .map((e) => e.summonId) ?? [],
      )
      .sort();
    if (
      JSON.stringify(linked) !==
      JSON.stringify(mod.summons.map((s) => s.id).sort())
    )
      fail("summon linkage");
    for (const s of mod.summons) {
      const record = registry.summons.find((x) => x.id === s.id);
      if (!hasImage(record?.image) || !s.jutsuIds.length) fail("summon assets");
      const ids = [...s.jutsuIds, ...(s.utilityJutsuIds || [])];
      if (
        JSON.stringify([...ids].sort()) !==
        JSON.stringify([...record.jutsuIds].sort())
      )
        fail("incomplete summon abilities");
      for (const id of ids) {
        const j = registry.jutsu.find((j) => j.id === id);
        if (
          !record.jutsuIds.includes(id) ||
          !j?.effects.length ||
          !hasImage(j.image)
        )
          fail("summon kit " + id);
      }
    }
  }
  return true;
}
export function resolveTemplate(draft, registry) {
  if (draft.catalogVersion !== registry.version)
    throw Error(
      "This draft uses a different catalog. Keep its recovery copy and open it with that version.",
    );
  const t = registry.templates.find(
    (t) =>
      t.slug === draft.template.slug && t.version === draft.template.version,
  );
  if (!t || !t.published)
    throw Error(
      "This template version is unavailable. Your saved draft has been kept.",
    );
  assertTemplate(t, registry);
  return t;
}
