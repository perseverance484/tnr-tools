import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import registry from "../catalog/browser.v1.json";
import { createPreviewLoader } from "./preview-assets.mjs";
import aerathiel from "../fixtures/aerathiel.submission.json";
import nightParade from "../fixtures/night-parade.submission.json";
import { newDraft, checklist, validateDraft } from "./schema.mjs";
import { restoreDraft, saveDraft, clearDraft } from "./drafts.mjs";
import { renderGuide, previewDocument } from "./render.mjs";
import { effectText } from "./effects.mjs";
import { prepareHighlight } from "./highlights.mjs";
import { ReceiptLookup } from "./Receipt.jsx";
import { draftFingerprint } from "./drafts.mjs";
import { Admin } from "./Admin.jsx";
import "./studio.css";
const examples = { aerathiel: aerathiel, "night-parade": nightParade };
const config = window.STUDIO_CONFIG || {};
const origin = location.origin;
const loadPreviewRegistry = createPreviewLoader(registry);
function download(name, content, mime = "application/json") {
  const url = URL.createObjectURL(new Blob([content], { type: mime }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export function Preview({ draft, onClose, rendered: provided }) {
  const [document, setDocument] = useState(""),
    [width, setWidth] = useState("phone"),
    [error, setError] = useState("");
  const ref = useRef(null);
  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const r =
          provided ||
          (await renderGuide(draft, await loadPreviewRegistry(draft), origin));
        if (active) setDocument(previewDocument(r));
      } catch (e) {
        if (active) setError(e.message);
      }
    })();
    return () => {
      active = false;
    };
  }, [draft, provided]);
  useEffect(() => {
    ref.current.showModal();
  }, []);
  return (
    <dialog ref={ref} className="preview-dialog" onCancel={onClose}>
      <div className="preview-toolbar">
        <div>
          <span className="eyebrow">FINAL GUIDE</span>
          <strong>Exactly what you’re making</strong>
        </div>
        <div className="segmented">
          <button
            aria-pressed={width === "phone"}
            onClick={() => setWidth("phone")}
          >
            Phone
          </button>
          <button
            aria-pressed={width === "desktop"}
            onClick={() => setWidth("desktop")}
          >
            Desktop
          </button>
        </div>
        <button
          className="icon-button"
          aria-label="Close preview and return to editor"
          onClick={onClose}
        >
          ✕
        </button>
      </div>
      {error ? (
        <p role="alert">{error}</p>
      ) : (
        <div className={"preview-stage " + width}>
          {!document && <p role="status">Preparing your guide and artwork…</p>}
          <iframe
            title="Final rendered TNR guide"
            sandbox=""
            srcDoc={document}
          />
        </div>
      )}
    </dialog>
  );
}
function Picker({ draft, template, onChange, onClose }) {
  const [search, setSearch] = useState(""),
    [filter, setFilter] = useState("all");
  const dialog = useRef();
  useEffect(() => {
    dialog.current.showModal();
  }, []);
  const available = registry.jutsu.filter(
    (j) =>
      !j.hidden &&
      j.type !== "AI" &&
      (!j.bloodlineId || j.bloodlineId === template.bloodlineId),
  );
  const results = available.filter(
    (j) =>
      (filter !== "core" || template.coreKit.includes(j.id)) &&
      `${j.name} ${j.rank} ${j.effects.map(effectText).join(" ")}`
        .toLowerCase()
        .includes(search.toLowerCase()),
  );
  return (
    <dialog ref={dialog} className="picker-dialog" onCancel={onClose}>
      <header>
        <div>
          <span className="eyebrow">BUILD YOUR LOADOUT</span>
          <h2>Find your next move.</h2>
        </div>
        <button
          className="icon-button"
          aria-label="Close jutsu picker"
          onClick={onClose}
        >
          ✕
        </button>
      </header>
      <label className="search-label">
        Search jutsu or effects
        <input
          autoFocus
          type="search"
          placeholder="Try absorb, healing, or a jutsu name"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </label>
      <div className="picker-filters">
        <button
          aria-pressed={filter === "all"}
          onClick={() => setFilter("all")}
        >
          All available
        </button>
        <button
          aria-pressed={filter === "core"}
          onClick={() => setFilter("core")}
        >
          Bloodline kit
        </button>
        <span>{draft.loadout.length}/20 selected</span>
      </div>
      <div className="picker-results">
        {results.map((j) => {
          const selected = draft.loadout.some((c) => c.jutsuId === j.id);
          return (
            <article className="picker-row" key={j.id}>
              <img src={j.image.url} alt={j.name + " official art"} />
              <div>
                <h3>{j.name}</h3>
                <span className="tiny">
                  {j.rank} rank · {j.action} AP · range {j.range}
                </span>
                <p>{j.effects.slice(0, 2).map(effectText).join(" / ")}</p>
              </div>
              <button
                disabled={selected || draft.loadout.length >= 20}
                onClick={() =>
                  onChange({
                    ...draft,
                    loadout: [
                      ...draft.loadout,
                      { jutsuId: j.id, howIUseIt: "" },
                    ],
                  })
                }
              >
                {selected ? "Added" : "Add"}
              </button>
            </article>
          );
        })}
        {!results.length && (
          <p>No jutsu match. Try a different name or effect.</p>
        )}
      </div>
      <footer>
        <button className="primary" onClick={onClose}>
          Write my notes · {draft.loadout.length} selected
        </button>
      </footer>
    </dialog>
  );
}
function Studio() {
  const [selected, setSelected] = useState(null),
    [draft, setDraft] = useState(null),
    [step, setStep] = useState("foundation"),
    [chapter, setChapter] = useState(0),
    [preview, setPreview] = useState(null),
    [picker, setPicker] = useState(false),
    [saveStatus, setSaveStatus] = useState("Saved on this device"),
    [error, setError] = useState(""),
    [receipt, setReceipt] = useState(null),
    [busy, setBusy] = useState(false),
    [turnstileToken, setTurnstileToken] = useState("");
  const turnstileRef = useRef();
  const draftRef = useRef(null),
    savedFingerprint = useRef(null);
  const [parent, setParent] = useState(null);
  const t = registry.templates.find((t) => t.slug === selected),
    chapters = t?.chapters.filter((c) => !c.hidden) || [],
    errors = draft ? checklist(draft, t) : [];
  function start(template) {
    const restored = restoreDraft(localStorage, template.slug, registry);
    if (restored.error) {
      setError(restored.error);
      download("guide-draft-recovery.json", restored.raw);
      return;
    }
    const d = restored.draft || newDraft(template, registry);
    setSelected(template.slug);
    setDraft(d);
    draftRef.current = d;
    savedFingerprint.current = draftFingerprint(d);
    setParent(null);
    setStep("foundation");
    setReceipt(null);
    setError("");
    if (!restored.draft) saveDraft(localStorage, d);
  }
  function update(d, { recover = false } = {}) {
    setDraft(d);
    draftRef.current = d;
    try {
      const existing = restoreDraft(localStorage, d.template.slug, registry);
      if (
        !recover &&
        (existing.error ||
          (existing.draft &&
            savedFingerprint.current &&
            draftFingerprint(existing.draft) !== savedFingerprint.current))
      )
        throw Error("Another tab changed this draft");
      saveDraft(localStorage, d);
      savedFingerprint.current = draftFingerprint(d);
      setSaveStatus("Saved on this device");
    } catch (e) {
      setSaveStatus("Unsaved changes · download backup");
      setError(
        e.message === "Another tab changed this draft"
          ? "Another tab changed this draft. Your open work is safe here; download it before reloading."
          : "Device storage could not save. Download a backup before leaving.",
      );
    }
  }
  useEffect(() => {
    function changed(event) {
      if (event.key === "tnr-guide-studio:drafts:v2")
        setError(
          "A draft changed in another tab. Download your current work before continuing here.",
        );
    }
    window.addEventListener("storage", changed);
    return () => window.removeEventListener("storage", changed);
  }, []);
  useEffect(() => {
    if (step !== "finish" || !selected || config.localHarness) return;
    let timer, widget;
    const mount = () => {
      if (window.turnstile && turnstileRef.current) {
        widget = window.turnstile.render(turnstileRef.current, {
          sitekey: config.turnstileSiteKey,
          action: "guide-submit",
          callback: setTurnstileToken,
          "expired-callback": () => setTurnstileToken(""),
          "error-callback": () => setTurnstileToken(""),
        });
      } else timer = setTimeout(mount, 250);
    };
    if (config.turnstileSiteKey) mount();
    return () => {
      clearTimeout(timer);
      if (widget !== undefined) window.turnstile?.remove(widget);
    };
  }, [step, selected]);
  async function submit() {
    setBusy(true);
    setError("");
    try {
      validateDraft(draft, registry, { complete: true });
      const r = await fetch("/api/submissions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          draft,
          ...(parent ? { parentId: parent.id, parentToken: parent.token } : {}),
          turnstileToken: config.localHarness
            ? "local-harness"
            : turnstileToken,
        }),
      });
      const data = await r.json();
      if (!r.ok) throw Error(data.error);
      setReceipt(data);
      localStorage.setItem(
        "tnr-guide-studio:receipt:" + data.id,
        JSON.stringify(data),
      );
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
      setTurnstileToken("");
      window.turnstile?.reset();
    }
  }
  const navigate = (next) => {
    setStep(next);
    setError("");
    window.scrollTo({ top: 0, behavior: "instant" });
  };
  return (
    <div className={"app " + (t?.slug || "")}>
      <header className="masthead">
        <a
          href="/"
          className="brand"
          onClick={(e) => {
            e.preventDefault();
            setSelected(null);
            setDraft(null);
          }}
        >
          <span className="brand-mark">T</span>
          <span>
            TNR <b>Guide Studio</b>
          </span>
        </a>
        <div className="masthead-right">
          {draft && (
            <span className="save-state" role="status">
              <i />
              {saveStatus}
            </span>
          )}
          <a href="/staff">Staff review ↗</a>
        </div>
      </header>
      {error && (
        <div className="notice" role="alert">
          {error}
          {draft && (
            <button
              onClick={() =>
                download("tnr-guide-draft.json", JSON.stringify(draft, null, 2))
              }
            >
              Download backup
            </button>
          )}
          <button aria-label="Dismiss message" onClick={() => setError("")}>
            ✕
          </button>
        </div>
      )}
      {!draft ? (
        <main className="welcome">
          <div className="welcome-heading">
            <div>
              <span className="eyebrow">THE FIELD GUIDE SERIES / VOL. 01</span>
              <h1>
                Your experience.
                <br />
                <em>A guide worth sharing.</em>
              </h1>
            </div>
            <p>
              The bloodline, artwork, and mechanics are already here. Bring the
              build, the decisions, and the lessons only a player can teach.
            </p>
          </div>
          <div className="selector">
            {registry.templates
              .filter((t) => t.published)
              .map((t, i) => (
                <article key={t.slug} className={"template-tile " + t.slug}>
                  <div className="tile-art">
                    <img
                      src={t.hero.url}
                      alt={t.name + " official bloodline art"}
                    />
                    <span className="tile-number">0{i + 1}</span>
                    <div className="tile-art-label">TNR BLOODLINE SERIES</div>
                  </div>
                  <div className="tile-copy">
                    <span className="eyebrow">
                      {
                        registry.bloodlines.find((b) => b.id === t.bloodlineId)
                          .rank
                      }{" "}
                      RANK ·{" "}
                      {t.modules.length ? "SUMMONING" : "PRESSURE & CONTROL"}
                    </span>
                    <h2>{t.shortName}</h2>
                    <p>{t.identity}</p>
                    <div className="foundation-stamp">
                      ✓ Complete kit & official art included
                    </div>
                    <div className="tile-actions">
                      <button className="primary" onClick={() => start(t)}>
                        {restoreDraft(localStorage, t.slug, registry).draft
                          ? "Continue my guide"
                          : "Create guide"}{" "}
                        <span>↗</span>
                      </button>
                      <button
                        className="text-button"
                        onClick={() => setPreview(examples[t.slug])}
                      >
                        Read example
                      </button>
                    </div>
                  </div>
                </article>
              ))}
          </div>
          <ReceiptLookup
            onRevise={(result, r) => {
              const d = validateDraft(result.submission, registry);
              setSelected(d.template.slug);
              setParent(r);
              setReceipt(null);
              setStep("build");
              update(d, { recover: true });
              setError(result.notes);
            }}
          />
          <footer className="welcome-foot">
            <span>BUILT AROUND YOUR KNOWLEDGE</span>
            <p>No HTML. No image hunting. No mechanic values to enter.</p>
            <span>YOUR DRAFT STAYS ON YOUR DEVICE</span>
          </footer>
        </main>
      ) : (
        <div className="workspace">
          <nav className="chapter-rail" aria-label="Guide sections">
            <div className="rail-intro">
              <span className="eyebrow">YOUR GUIDE</span>
              <strong>{t.shortName}</strong>
            </div>
            {[
              ["foundation", "01", "The foundation"],
              ["build", "02", "Your build"],
              ["chapters", "03", "Your strategy"],
              ["finish", "04", "Review & submit"],
            ].map(([id, n, label]) => (
              <button
                key={id}
                aria-current={step === id ? "step" : undefined}
                onClick={() => navigate(id)}
              >
                <span>{id === "foundation" ? "✓" : n}</span>
                {label}
              </button>
            ))}
            <button className="rail-preview" onClick={() => setPreview(draft)}>
              ↗ Live preview
            </button>
            <div className="rail-bottom">
              <button
                onClick={() =>
                  download(
                    "tnr-guide-draft.json",
                    JSON.stringify(draft, null, 2),
                  )
                }
              >
                Download draft
              </button>
              <label className="import-draft">
                Recover from backup
                <input
                  type="file"
                  accept="application/json,.json"
                  onChange={async (e) => {
                    try {
                      const file = e.target.files[0];
                      if (!file || file.size > 2_200_000)
                        throw Error("Choose a valid draft backup");
                      const d = validateDraft(
                        JSON.parse(await file.text()),
                        registry,
                      );
                      setSelected(d.template.slug);
                      update(d, { recover: true });
                      setError("Backup recovered.");
                    } catch (err) {
                      setError(err.message);
                    }
                    e.target.value = "";
                  }}
                />
              </label>
              <button
                onClick={() => {
                  if (
                    window.confirm(
                      "Clear this bloodline’s saved draft from this device?",
                    )
                  ) {
                    clearDraft(localStorage, t.slug);
                    setDraft(null);
                    setSelected(null);
                  }
                }}
              >
                Clear draft
              </button>
            </div>
          </nav>
          <main className="editing-canvas">
            <div className="canvas-top">
              <span className="eyebrow">
                {step === "foundation"
                  ? "FINISHED FOR YOU"
                  : "THE PLAYER’S PERSPECTIVE"}
              </span>
              <button
                className="preview-link"
                onClick={() => setPreview(draft)}
              >
                Preview guide ↗
              </button>
            </div>
            {step === "foundation" && (
              <>
                <div className="workspace-hero">
                  <div>
                    <span className="eyebrow">TNR FOUNDATION · COMPLETE</span>
                    <h1>{t.shortName}</h1>
                    <p>{t.identity}</p>
                    <span className="small-lock">
                      ◆ Artwork & mechanics by TNR
                    </span>
                  </div>
                  <img
                    src={t.hero.url}
                    alt={t.name + " official bloodline art"}
                  />
                </div>
                <section className="foundation-intro">
                  <span className="eyebrow">THE WORLD IS ALREADY HERE</span>
                  <h2>You write the interesting part.</h2>
                  <p>{t.intro[0]}</p>
                  <div className="foundation-inventory">
                    <div>
                      <b>05</b>
                      <span>
                        core jutsu
                        <br />
                        always included
                      </span>
                    </div>
                    <div>
                      <b>{t.modules.length ? "03" : "✓"}</b>
                      <span>
                        {t.modules.length
                          ? "summon patrons"
                          : "official artwork"}
                        <br />
                        ready to go
                      </span>
                    </div>
                    <button onClick={() => setPreview(draft)}>
                      See the full foundation ↗
                    </button>
                  </div>
                </section>
                <details className="locked-kit">
                  <summary>
                    ◆ Your complete bloodline kit <span>View 5 jutsu</span>
                  </summary>
                  <div>
                    {t.coreKit.map((id) => {
                      const j = registry.jutsu.find((j) => j.id === id);
                      return (
                        <article key={id}>
                          <img
                            src={j.image.url}
                            alt={j.name + " official art"}
                          />
                          <div>
                            <h3>{j.name}</h3>
                            <p>{j.effects.map(effectText).join(" / ")}</p>
                          </div>
                        </article>
                      );
                    })}
                  </div>
                </details>
                <section className="byline-section">
                  <span className="eyebrow">AND NOW, YOUR PERSPECTIVE</span>
                  <h2>Put your name on it.</h2>
                  <label>
                    Author / display name
                    <input
                      maxLength={48}
                      placeholder="Your player name"
                      autoComplete="nickname"
                      value={draft.author}
                      onChange={(e) =>
                        update({ ...draft, author: e.target.value })
                      }
                    />
                  </label>
                  <label>
                    A line about your playstyle <span>Optional</span>
                    <textarea
                      rows={2}
                      maxLength={400}
                      placeholder="The approach that makes this build yours…"
                      value={draft.summary}
                      onChange={(e) =>
                        update({ ...draft, summary: e.target.value })
                      }
                    />
                  </label>
                </section>
                <button
                  className="primary next-button"
                  onClick={() => navigate("build")}
                >
                  Shape my build <span>→</span>
                </button>
              </>
            )}
            {step === "build" && (
              <>
                <div className="section-heading">
                  <span className="chapter-number">02</span>
                  <h1>
                    Make every
                    <br />
                    <em>choice count.</em>
                  </h1>
                  <p>
                    Your full bloodline kit is already included. Choose the
                    jutsu that define your build.
                  </p>
                </div>
                <div className="build-toolbar">
                  <span>{draft.loadout.length} jutsu in your build</span>
                  <button className="primary" onClick={() => setPicker(true)}>
                    ＋ Add jutsu
                  </button>
                </div>
                {!draft.loadout.length && (
                  <div className="empty-build">
                    <span>✦</span>
                    <h2>Start with your defining move.</h2>
                    <p>
                      Add a jutsu, then explain how you use it while the idea is
                      fresh.
                    </p>
                    <button onClick={() => setPicker(true)}>
                      Browse the catalog ↗
                    </button>
                  </div>
                )}
                <div className="loadout">
                  {draft.loadout.map((choice, i) => {
                    const j = registry.jutsu.find(
                      (j) => j.id === choice.jutsuId,
                    );
                    const move = (to) => {
                      const items = [...draft.loadout];
                      items.splice(to, 0, items.splice(i, 1)[0]);
                      update({ ...draft, loadout: items });
                    };
                    return (
                      <article className="loadout-entry" key={j.id}>
                        <header>
                          <span className="entry-index">
                            {String(i + 1).padStart(2, "0")}
                          </span>
                          <img
                            src={j.image.url}
                            alt={j.name + " official art"}
                          />
                          <div>
                            <h2>{j.name}</h2>
                            <span className="tiny">
                              {t.coreKit.includes(j.id)
                                ? "CORE KIT · SEE ABOVE"
                                : `${j.rank} RANK · ${j.action} AP · SUPPORT JUTSU`}
                            </span>
                          </div>
                          <div className="reorder">
                            <button
                              disabled={i === 0}
                              aria-label={"Move " + j.name + " up"}
                              onClick={() => move(i - 1)}
                            >
                              ↑
                            </button>
                            <button
                              disabled={i === draft.loadout.length - 1}
                              aria-label={"Move " + j.name + " down"}
                              onClick={() => move(i + 1)}
                            >
                              ↓
                            </button>
                            <button
                              aria-label={"Remove " + j.name + " from build"}
                              onClick={() =>
                                update({
                                  ...draft,
                                  loadout: draft.loadout.filter(
                                    (c) => c.jutsuId !== j.id,
                                  ),
                                })
                              }
                            >
                              ×
                            </button>
                          </div>
                        </header>
                        <details className="mechanic-reference">
                          <summary>Mechanics at a glance</summary>
                          <ul>
                            {j.effects.map((e, n) => (
                              <li key={n}>{effectText(e)}</li>
                            ))}
                          </ul>
                        </details>
                        <label className="tactical-note">
                          <span>HOW I USE IT</span>
                          <textarea
                            maxLength={1800}
                            rows={3}
                            placeholder="When do you reach for this? What does it set up?"
                            value={choice.howIUseIt}
                            onChange={(e) =>
                              update({
                                ...draft,
                                loadout: draft.loadout.map((c) =>
                                  c.jutsuId === j.id
                                    ? { ...c, howIUseIt: e.target.value }
                                    : c,
                                ),
                              })
                            }
                          />
                        </label>
                      </article>
                    );
                  })}
                </div>
                <button
                  className="primary next-button"
                  onClick={() => navigate("chapters")}
                >
                  Write the game plan <span>→</span>
                </button>
              </>
            )}
            {step === "chapters" && (
              <>
                <div className="section-heading">
                  <span className="chapter-number">03</span>
                  <h1>
                    Teach the way
                    <br />
                    <em>you see the fight.</em>
                  </h1>
                  <p>A collection of chapters. Your own strategic voice.</p>
                </div>
                <div className="chapter-editor">
                  <nav aria-label="Strategy chapters">
                    {t.chapters
                      .filter((c) => !c.hidden)
                      .map((c, i) => (
                        <button
                          key={c.id}
                          aria-current={chapter === i ? "page" : undefined}
                          onClick={() => setChapter(i)}
                        >
                          <span>
                            {draft.strategy[c.id]?.trim()
                              ? "✓"
                              : String(i + 1).padStart(2, "0")}
                          </span>
                          {c.title}
                          {!c.required && <small>Optional</small>}
                        </button>
                      ))}
                  </nav>
                  <section className="manuscript">
                    <div className="eyebrow">
                      CHAPTER {String(chapter + 1).padStart(2, "0")} /{" "}
                      {chapters[chapter].required
                        ? "YOUR ESSENTIALS"
                        : "OPTIONAL"}
                    </div>
                    <h2>{chapters[chapter].title}</h2>
                    <p className="coaching">{chapters[chapter].prompt}</p>
                    <label className="sr-only" htmlFor="chapter-text">
                      {chapters[chapter].title}
                    </label>
                    <textarea
                      id="chapter-text"
                      rows={12}
                      maxLength={6500}
                      placeholder="Start with the decision you want the reader to understand…"
                      value={draft.strategy[chapters[chapter].id] || ""}
                      onChange={(e) =>
                        update({
                          ...draft,
                          strategy: {
                            ...draft.strategy,
                            [chapters[chapter].id]: e.target.value,
                          },
                        })
                      }
                    />
                    <footer>
                      <span>
                        {(draft.strategy[chapters[chapter].id] || "").length}
                        /6500 · autosaved
                      </span>
                      <button
                        disabled={chapter === chapters.length - 1}
                        onClick={() => setChapter(chapter + 1)}
                      >
                        Next chapter →
                      </button>
                    </footer>
                  </section>
                </div>
                <section className="highlights">
                  <div>
                    <span className="eyebrow">SHOW THE MOMENT / OPTIONAL</span>
                    <h2>Combat highlights</h2>
                    <p>
                      A screenshot and a short caption can make a lesson click.
                    </p>
                  </div>
                  <label className="upload-button">
                    ＋ Add screenshot
                    <input
                      type="file"
                      accept="image/png,image/jpeg,image/webp"
                      disabled={draft.highlights.length >= 4 || busy}
                      onChange={async (e) => {
                        const file = e.target.files[0];
                        if (!file) return;
                        setBusy(true);
                        try {
                          const data = await prepareHighlight(file);
                          const current = draftRef.current;
                          if (current?.template.slug !== draft.template.slug)
                            throw Error(
                              "Return to this guide to add its screenshot",
                            );
                          update({
                            ...current,
                            highlights: [
                              ...current.highlights,
                              { caption: "", data },
                            ],
                          });
                        } catch (e) {
                          setError(e.message);
                        } finally {
                          setBusy(false);
                        }
                        e.target.value = "";
                      }}
                    />
                  </label>
                  <p className="tiny">
                    Up to 4 screenshots. Images are resized on your device.
                  </p>
                  {draft.highlights.map((h, i) => (
                    <article key={i} className="highlight-editor">
                      <img
                        src={h.data}
                        alt={h.caption || "Combat screenshot to caption"}
                      />
                      <label>
                        What should the reader notice?
                        <textarea
                          rows={2}
                          maxLength={500}
                          value={h.caption}
                          onChange={(e) =>
                            update({
                              ...draft,
                              highlights: draft.highlights.map((x, n) =>
                                n === i ? { ...x, caption: e.target.value } : x,
                              ),
                            })
                          }
                        />
                      </label>
                      <button
                        onClick={() =>
                          update({
                            ...draft,
                            highlights: draft.highlights.filter(
                              (_, n) => n !== i,
                            ),
                          })
                        }
                      >
                        Remove screenshot
                      </button>
                    </article>
                  ))}
                </section>
                <button
                  className="primary next-button"
                  onClick={() => navigate("finish")}
                >
                  Give it a final read <span>→</span>
                </button>
              </>
            )}
            {step === "finish" &&
              (receipt ? (
                <section className="receipt">
                  <span className="eyebrow">SUBMITTED FOR STAFF REVIEW</span>
                  <h1>
                    Your perspective
                    <br />
                    <em>is in good hands.</em>
                  </h1>
                  <p>
                    Your guide has been submitted. Staff will review the
                    finished guide. Approval and publication are separate steps.
                  </p>
                  <code>{receipt.id}</code>
                  <button
                    className="primary"
                    onClick={() =>
                      download(
                        "tnr-guide-receipt.json",
                        JSON.stringify(receipt, null, 2),
                      )
                    }
                  >
                    Save my private receipt
                  </button>
                  <p className="tiny">
                    Keep this receipt to check review notes or submit a
                    revision. Your local draft is still saved.
                  </p>
                  <button onClick={() => setPreview(draft)}>
                    Read my guide ↗
                  </button>
                </section>
              ) : (
                <>
                  <div className="section-heading">
                    <span className="chapter-number">04</span>
                    <h1>
                      A final read.
                      <br />
                      <em>Then pass it on.</em>
                    </h1>
                    <p>
                      Staff will review the finished guide you see in preview.
                    </p>
                  </div>
                  <button
                    className="review-preview-button"
                    onClick={() => setPreview(draft)}
                  >
                    <img
                      src={t.hero.url}
                      alt={t.name + " official bloodline art"}
                    />
                    <div>
                      <span className="eyebrow">YOUR FINISHED GUIDE</span>
                      <h2>{t.shortName}</h2>
                      <p>
                        {draft.author
                          ? "By " + draft.author
                          : "Add your display name"}{" "}
                        · Open live preview ↗
                      </p>
                    </div>
                  </button>
                  <ul className="submission-checklist">
                    <li>✓ Complete bloodline foundation</li>
                    <li>
                      {draft.author ? "✓" : "○"} Author{" "}
                      {draft.author || "still needed"}
                    </li>
                    <li>
                      {draft.loadout.length ? "✓" : "○"} {draft.loadout.length}{" "}
                      build choices ·{" "}
                      {draft.loadout.filter((j) => j.howIUseIt.trim()).length}{" "}
                      tactical notes
                    </li>
                    <li>
                      ✓{" "}
                      {
                        t.chapters.filter((c) => draft.strategy[c.id]?.trim())
                          .length
                      }{" "}
                      strategy chapters written
                    </li>
                    <li>✓ {draft.highlights.length} combat highlights</li>
                  </ul>
                  {errors.length > 0 && (
                    <div className="finish-errors">
                      <strong>A few finishing touches</strong>
                      <ul>
                        {errors.map((e) => (
                          <li key={e}>{e}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <details className="version-details">
                    <summary>Bloodline and guide versions</summary>
                    <p>
                      {t.name} · template {t.version}
                      <br />
                      {registry.version}
                    </p>
                  </details>
                  <div ref={turnstileRef} />
                  {!config.localHarness && !config.turnstileSiteKey && (
                    <p className="notice">
                      Submissions will open when staff completes service setup.
                      You can keep writing and save your draft.
                    </p>
                  )}
                  <button
                    className="primary next-button"
                    disabled={
                      busy ||
                      errors.length > 0 ||
                      (!config.localHarness && !turnstileToken)
                    }
                    onClick={submit}
                  >
                    {busy ? "Submitting…" : "Submit for staff review"}{" "}
                    <span>→</span>
                  </button>
                  <p className="tiny">
                    This submits for review. It does not publish your guide.
                  </p>
                </>
              ))}
          </main>
          <aside className="editor-margin">
            <div className="margin-line" />
            <span className="eyebrow">THE FOUNDATION</span>
            <p>
              Bloodline.
              <br />
              Artwork.
              <br />
              Complete kit.
            </p>
            <span className="margin-check">All taken care of.</span>
            <div className="margin-line" />
            <span className="eyebrow">YOUR CONTRIBUTION</span>
            <p>
              The build.
              <br />
              The decisions.
              <br />
              The experience.
            </p>
            <button onClick={() => setPreview(draft)}>
              See it come together ↗
            </button>
          </aside>
          <div className="mobile-dock">
            <button onClick={() => setPreview(draft)}>↗ Preview</button>
            <span role="status">{saveStatus}</span>
          </div>
        </div>
      )}
      {preview && <Preview draft={preview} onClose={() => setPreview(null)} />}{" "}
      {picker && (
        <Picker
          draft={draft}
          template={t}
          onChange={update}
          onClose={() => setPicker(false)}
        />
      )}
    </div>
  );
}
createRoot(document.getElementById("root")).render(
  location.pathname.startsWith("/staff") ? (
    <Admin registry={registry} />
  ) : (
    <Studio />
  ),
);
