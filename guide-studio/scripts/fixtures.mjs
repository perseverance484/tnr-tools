import { readFile, writeFile } from "node:fs/promises";
import { newDraft } from "../src/schema.mjs";
const registry = JSON.parse(
  await readFile(new URL("../catalog/catalog.v1.json", import.meta.url)),
);
const notes = {
  "Dragon King's Impact":
    "I use this when the opening is already real. The damage and follow-through are worth committing to only when the opponent cannot simply clear my setup and take a free exchange.",
  "Particle Cannon":
    "This is my cash-out. I wait until the target is exposed and my damage increases outweigh their reduction, then turn the earlier control into a meaningful hit.",
  "Tempest Cleave":
    "This keeps pressure on a target that wants to reset. I use it when its lasting effects matter more than another isolated hit.",
  "Decaying Touch":
    "This is one of my main trades. I pair recoil with absorb so the opponent pays for hitting me while I soften the hit on my side.",
  "Chakra Resonance":
    "If I want disruption instead of immediate damage, I follow my pull with AP pressure. The point is to make their next setup awkward.",
  "Danse Macabre":
    "I use this to restrict a response I expect, especially when the opponent needs a clean setup round to regain control.",
  Netherblight:
    "This is pressure that also helps me remain in the exchange. I use it when the fight is becoming a contest of sustain.",
  "Atomic Shield":
    "I use it early and often. By itself, the opponent either hits into reflect or spends a clear on a small setup; I pair it with another buff before a bigger round.",
  "Windshear Decay":
    "At range, I pull the opponent back out and start the next exchange on my terms. If they are already trapped in a wall, I avoid wasting the movement.",
  "Drops of Renewal":
    "I want absorb active before I take a trade. This makes the next exchange less expensive and supports the pressure that follows.",
  "Chakra Overflow":
    "This is a setup tool, not a button to press on cooldown. I use it when I have a credible follow-up and enough room to survive the reply.",
  "Eternal Darkness":
    "I use this when I must slow a dangerous exchange from both sides. It buys a more manageable round without requiring a full retreat.",
  "Seal of Nullification":
    "I use this to deny the opponent a fresh setup after a clear. Turn order matters: I want prevention to cover the moment they would rebuild.",
  "Blazing Reprisal":
    "I bring this in when the opponent intends to keep attacking. I want their commitment to create value for me as well.",
  Seimyaku:
    "When the opponent depends on recovery, I use this to keep pressure meaningful while protecting myself through the exchange.",
  "Summoning: Underworld Gate":
    "I establish the Gate when I can afford the opening commitment. Keeping it present gives the rest of the fight a source of pressure beyond my own actions.",
  "Otherworldly Conduit":
    "I use this to move from surviving an exchange into threatening the next one. I watch for clears before committing another setup.",
  "Herald of the Black Night":
    "I use its reach and buff prevention to make an exposed opponent stay exposed. It is strongest when they are trying to rebuild.",
  "Possessing Yurei":
    "After the opponent has spent a defensive answer, I use Yurei to combine damage with disruption. AP pressure can stop their next chain before it starts.",
  "Oni Hammer Swing":
    "I use this when I want to trade damage while reducing the opponent’s next hit. It keeps a committed exchange from becoming one-sided.",
  "Aqua Dragon Barrage":
    "I pair pressure now with healing on the following round. It is useful when I can survive the response and let the delayed recovery matter.",
  Mizukumi:
    "This lets me attack while establishing absorb for the next exchanges. I value the protection before I am already in trouble.",
  "Hollow Veil":
    "When the opponent has an immediate threat, I use this to reduce damage given and establish absorb. I use the extra reach to stabilise without chasing.",
  "Phantom Requiem":
    "I use the pool drain to force an uncomfortable answer. If it draws an early cleanse, my later pressure has a much clearer path.",
  "Subaku Palace":
    "This is another way to make a dangerous exchange manageable. I look at the ground pattern and enemy position before choosing it.",
  "Kinjutsu: Black Thorn Rose":
    "I use this to suppress the opponent’s recovery while reducing the damage I take. I am buying a better sustained exchange, not adding a direct damage hit.",
};
const aerNames = [
  "Dragon King's Impact",
  "Particle Cannon",
  "Tempest Cleave",
  "Decaying Touch",
  "Chakra Resonance",
  "Danse Macabre",
  "Netherblight",
  "Atomic Shield",
  "Windshear Decay",
  "Drops of Renewal",
  "Chakra Overflow",
  "Eternal Darkness",
  "Seal of Nullification",
  "Blazing Reprisal",
  "Seimyaku",
];
const nightNames = [
  "Summoning: Underworld Gate",
  "Otherworldly Conduit",
  "Herald of the Black Night",
  "Possessing Yurei",
  "Oni Hammer Swing",
  "Aqua Dragon Barrage",
  "Mizukumi",
  "Hollow Veil",
  "Phantom Requiem",
  "Chakra Overflow",
  "Subaku Palace",
  "Kinjutsu: Black Thorn Rose",
];
const strategy = {
  aerathiel: {
    philosophy:
      "I care less about having the strongest jutsu individually than about whether each slot helps me build pressure, force a response, or avoid a bad trade. I want every round to prepare the next one.",
    coreLoop:
      "Start by controlling the exchange. Establish a useful buff, trade where recoil or absorb favours me, and keep the target under pressure. Cash out when their defenses are actually open.\n\nIf the opening disappears, reset. A setup is not a promise that I must attack next.",
    opening:
      "At range, Windshear Decay pulls the opponent into the exchange. Chakra Resonance can then disrupt the setup they wanted to take.\n\nWhen a wall already limits their movement, I do not spend the pull simply because it is available.",
    defense:
      "I want absorb in place before the trade, not after it. If the opponent commits to a buffed hit, I compare the incoming threat with the pressure I can keep. Sometimes the strongest play is to refuse a bad trade and recover.",
    pressure:
      "Turn order changes the clear window. Moving first can mean preparing prevention before the round in which I clear. Moving second can let me clear and apply prevention in the same exchange. The goal is to stop the opponent from immediately replacing what I removed.",
    synergies:
      "Atomic Shield asks the opponent a question even before I use another jutsu. Decaying Touch and absorb make attacking me costly. Those exchanges create the opening that Particle Cannon wants.",
    matchups:
      "Against burst, I prioritise the incoming threat and preserve a reset. Against sustain, I keep pressure on recovery and avoid empty setup rounds. Against control, I pay close attention to turn order and leave myself a way to respond.",
    mistakes:
      "Do not mistake a completed setup for a good attack. Do not use a pull when movement is already constrained. Do not spend every defensive option to save a trade that was never worth taking.",
  },
  "night-parade": {
    philosophy:
      "The plan is sustain plus pressure. I am not racing for the earliest possible win. I want the opponent to fight through my protection while their resources and comfortable answers gradually disappear.",
    coreLoop:
      "Establish the Gate when the opening is safe. Maintain absorb where possible, then use Water-based support to remain in the fight while continuing to apply pressure.\n\nWhen the opponent has spent a key defensive answer, turn that defensive footing into a committed offensive sequence.",
    opening:
      "My first priority is to understand what the opponent can threaten immediately. If I can safely establish the Gate, I do. If not, I stabilise the exchange before spending that commitment.",
    defense:
      "Absorb is most valuable when it is present across the exchanges I actually take. I combine it with healing and damage reduction, and I avoid assuming any single layer makes me safe from a full setup.",
    pressure:
      "Phantom Requiem makes the opponent decide whether to tolerate pool pressure or spend a cleanse earlier than they want. I watch that decision closely. A used defensive answer can be more valuable than an extra isolated hit.",
    synergies:
      "Chakra Overflow is the bridge into offense. I use it when Possessing Yurei or Aqua Dragon Barrage has a useful follow-up window, rather than treating the buff as automatic damage. The summon’s current contribution also changes which exchange I want.",
    matchups:
      "Against burst, keep a defensive answer available and do not overcommit just to establish the Gate. Against recovery, use healing reduction to keep earlier pressure meaningful. In a long fight, manage pools as carefully as health.",
    mistakes:
      "Do not unload every tool at once. Do not assume summon timing from a remembered rotation without checking the current fight. Do not let the desire to keep pressure moving stop you from making a necessary reset.",
  },
};
for (const t of registry.templates) {
  const d = newDraft(t, registry);
  d.author = "Example author";
  d.summary =
    t.slug === "aerathiel"
      ? "Control the exchange, take the good trade, then cash out."
      : "Sustain, summon support, and patient pressure for the long fight.";
  d.loadout = (t.slug === "aerathiel" ? aerNames : nightNames).map((name) => ({
    jutsuId: registry.jutsu.find((j) => j.name === name).id,
    howIUseIt: notes[name],
  }));
  d.strategy = strategy[t.slug];
  const path = new URL(
      `../fixtures/${t.slug}.submission.json`,
      import.meta.url,
    ),
    text = JSON.stringify(d, null, 2) + "\n";
  if (process.argv.includes("--check")) {
    if ((await readFile(path, "utf8")) !== text)
      throw Error("Stale fixture " + t.slug);
  } else await writeFile(path, text);
}
console.log(
  "Generated Aerathiel (15 choices) and Night Parade (12 choices) acceptance submissions.",
);
