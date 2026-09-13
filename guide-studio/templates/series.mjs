export const templateDefinitions = [
  {
    slug: "aerathiel",
    version: 1,
    bloodlineId: "1C34syOOEKp6k3UKweYT6",
    shortName: "Aerathiel",
    identity: "Sustained pressure. Favourable trades.",
    accent: "#94d9d2",
    ink: "#0b2428",
    intro: [
      "Aerathiel is an A-rank bloodline built around pressure, control, and layered damage. Its kit rewards players who maintain momentum, force favourable trades, and turn small openings into lasting advantage.",
      "Wind, Earth, and Dust give Aerathiel its identity. The foundation below brings together its full bloodline kit; the player’s build and tactical choices follow after it.",
    ],
    overview:
      "Control the distance, make each exchange costly, and create a clear window for Particle Cannon. Atomic Shield, Decaying Touch, Death’s March, and Windshear Decay provide different ways to shape that exchange.",
    coreKit: [
      "FGSJC-7Zd0BYh7-tvsUdH",
      "UgYXqNIJNjLGkAS5b5udH",
      "Zr6Zo2NcXxWuL13ufQsHw",
      "VmoEzExhfgtzme2b5RuzJ",
      "egtCp5UC5pRwxz7egJm7J",
    ],
    modules: [],
    chapters: [
      [
        "philosophy",
        "Build Philosophy",
        "Describe the fights your build wants to take, and the trades it avoids.",
        true,
      ],
      [
        "coreLoop",
        "Pressure, Then Cash Out",
        "Walk the reader through the decisions that keep your pressure moving.",
        true,
      ],
      [
        "opening",
        "Opening Control",
        "Explain what changes when you move first or second.",
      ],
      [
        "defense",
        "Trade & Reset",
        "Show how you recover without giving away the next exchange.",
      ],
      [
        "pressure",
        "Create the Clear Window",
        "Explain how you recognise an opening worth committing to.",
      ],
      [
        "synergies",
        "The Pieces That Connect",
        "Pick the combinations that make your loadout work as a whole.",
      ],
      [
        "matchups",
        "Adaptation & Matchups",
        "Explain how you change your plan against different opponents.",
        true,
      ],
      [
        "mistakes",
        "Mistakes to Avoid",
        "Name the tempting plays you have learned to leave alone.",
      ],
    ],
  },
  {
    slug: "night-parade",
    version: 1,
    bloodlineId: "r_99Xg8SIOYw2awCMSR7e",
    shortName: "Night Parade",
    identity: "Keep the gate open. Win the long fight.",
    accent: "#d1b2ed",
    ink: "#241831",
    intro: [
      "Night Parade of A Thousand Demons is an H-rank summoning bloodline. A pact with the underworld gives its wielder a supporting cast of demons, turning a single shinobi’s battle into a sustained procession.",
      "Its elemental identity spans Shadow, Earth, Water, Wind, and non-elemental techniques. The Underworld Gate, complete bloodline kit, and summon abilities are included below, before the player’s own strategy begins.",
    ],
    overview:
      "The gate gives the bloodline its rhythm. Around it, the core kit combines damage, control, and sustain: Possessing Yurei disrupts action points, Oni Hammer Swing reduces damage given, and Otherworldly Conduit supports a committed exchange.",
    coreKit: [
      "CBcRFjQB4mxsJNnVIA9Pk",
      "5eNrb23-iEMkmWVe57mEx",
      "6Y4wBoFOoT-oaYK-9pt1B",
      "MpQ0tVX3TAHF0MDwRvEdN",
      "lOZKV2Jsdi3YmGuu9_k_z",
    ],
    modules: [
      {
        id: "underworld-procession",
        title: "The Underworld Procession",
        description:
          "The Gate’s captured summon links lead to these three patrons. Their abilities are part of the bloodline foundation, separate from the jutsu you equip. AI ability values below use their captured equipped level, not the player-jutsu level.",
        gateId: "1NGM2WYa_2dakRAZFKc3f",
        summons: [
          {
            id: "oqeo5ssoyR4XlfOEWENbp",
            name: "Nue · Pestilence",
            identity: "Drain and recoil",
            jutsuIds: ["jhjmPXwx0NflEdCgvEzPs"],
            utilityJutsuIds: ["fc7DtHKJy50qdmdwLIvaa"],
          },
          {
            id: "JWdRhAsPRDODnXy0pfWVM",
            name: "Shuten-Doji",
            identity: "Raise costs. Reduce pressure.",
            jutsuIds: ["lEkVV6vGhmjPX6NAtVsz7"],
          },
          {
            id: "CJIymnUOxaIntPLmwABoz",
            name: "Jurogumo",
            identity: "Restore allies. Expose the enemy.",
            jutsuIds: ["xs-8r_KRJS8QQMpBDyhUv", "tGz6tBq4EfMNwbH14SdVb"],
            utilityJutsuIds: ["fc7DtHKJy50qdmdwLIvaa"],
          },
        ],
      },
    ],
    chapters: [
      [
        "philosophy",
        "Win the Long Fight",
        "Describe your balance between survival and accumulating pressure.",
        true,
      ],
      [
        "coreLoop",
        "Keep the Gate Open",
        "Explain how you build a repeatable plan around the gate.",
        true,
      ],
      [
        "opening",
        "The First Invitation",
        "Show the reader how you establish the opening safely.",
      ],
      [
        "defense",
        "Absorb & Endure",
        "Describe when you maintain sustain and when you must reset.",
      ],
      [
        "pressure",
        "Force the Cleanse",
        "Explain how you create pressure that demands an answer.",
      ],
      [
        "synergies",
        "Turn Defense into Offense",
        "Connect your support jutsu to a decisive bloodline play.",
      ],
      [
        "matchups",
        "When the Parade Meets Resistance",
        "Show how you adapt to burst, control, or a drawn-out fight.",
        true,
      ],
      [
        "mistakes",
        "Do Not Empty the Gate",
        "Share the commitments and timing errors to avoid.",
      ],
    ],
  },
].map((t) => ({
  ...t,
  published: true,
  chapterFamilyVersion: 1,
  chapters: t.chapters.map(([id, title, prompt, required = false]) => ({
    id,
    title,
    prompt,
    required,
    hidden: false,
  })),
  provenance: {
    contractSha: "87fb673938d915c0732351d2efb208d05ef38c7c",
    editor: "Astra",
    copyStatus: "Implementation proposal for independent/director review",
    reference:
      t.slug === "aerathiel"
        ? "aerathiel_guide_v2_SELF_CONTAINED (1).html"
        : "Guide to Night Parade of a Thousand Demons_260912_130148.pdf",
  },
}));
