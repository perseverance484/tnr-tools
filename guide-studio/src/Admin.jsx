import React, { useEffect, useState } from "react";
import { previewDocument } from "./render.mjs";
export function Admin() {
  const [rows, setRows] = useState([]),
    [record, setRecord] = useState(null),
    [artifact, setArtifact] = useState(null),
    [error, setError] = useState(""),
    [notes, setNotes] = useState(""),
    [busy, setBusy] = useState(false),
    [cursor, setCursor] = useState(null);
  async function request(path, options) {
    const response = await fetch(path, options);
    const result = await response.json();
    if (!response.ok) throw Error(result.error);
    return result;
  }
  async function queue(next = false) {
    try {
      const result = await request(
        "/api/staff/submissions" +
          (next && cursor ? "?cursor=" + encodeURIComponent(cursor) : ""),
      );
      setRows(next ? [...rows, ...result.records] : result.records);
      setCursor(result.next);
    } catch (e) {
      setError(e.message);
    }
  }
  async function open(id) {
    setBusy(true);
    setError("");
    try {
      const result = await request("/api/staff/submissions/" + id);
      setRecord(result.record);
      setArtifact(result.artifact);
      setNotes(result.record.notes || "");
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  useEffect(() => {
    queue();
  }, []);
  async function transition(status, receipt) {
    setBusy(true);
    setError("");
    try {
      const result = await request(
        `/api/staff/submissions/${record.id}/transition`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            revision: record.revision,
            status,
            packageHash: record.packageHash,
            notes,
            ...(receipt ? { receipt } : {}),
          }),
        },
      );
      setRecord(result);
      queue();
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  async function download() {
    setBusy(true);
    try {
      const response = await fetch(
        `/api/staff/submissions/${record.id}/package`,
      );
      if (!response.ok) throw Error((await response.json()).error);
      const url = URL.createObjectURL(await response.blob()),
        a = document.createElement("a");
      a.href = url;
      a.download = `tnr-guide-${record.id}.zip`;
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="admin">
      <header className="masthead">
        <a className="brand" href="/">
          <span className="brand-mark">T</span>
          <span>
            TNR <b>Content review</b>
          </span>
        </a>
        <a href="/">Back to Guide Studio ↗</a>
      </header>
      <main className="staff-main">
        <div className="staff-title">
          <div>
            <span className="eyebrow">EDITORIAL DESK</span>
            <h1>
              {record ? "Review the finished guide." : "The review queue."}
            </h1>
          </div>
          {record && (
            <button
              onClick={() => {
                setRecord(null);
                setArtifact(null);
              }}
            >
              ← All submissions
            </button>
          )}
        </div>
        {error && (
          <p className="notice" role="alert">
            {error}
          </p>
        )}
        {!record ? (
          <>
            <div className="queue-description">
              <p>
                Open the guide, read the final representation, then make a
                decision.
              </p>
              <button onClick={() => queue()}>Refresh queue</button>
            </div>
            {rows.length ? (
              <div className="queue">
                {rows.map((r) => (
                  <button
                    className="queue-row"
                    key={r.id}
                    onClick={() => open(r.id)}
                  >
                    <div>
                      <span className="eyebrow">{r.status}</span>
                      <h2>{r.bloodline}</h2>
                      <p>
                        By {r.author} ·{" "}
                        {new Date(r.createdAt).toLocaleDateString()}
                      </p>
                    </div>
                    <span>Read guide ↗</span>
                  </button>
                ))}
              </div>
            ) : (
              <p className="empty-queue">
                {error
                  ? "Staff access is required to read submissions."
                  : "No submissions are waiting here yet."}
              </p>
            )}
            {cursor && <button onClick={() => queue(true)}>Load more</button>}
          </>
        ) : (
          <div className="review-layout">
            <section className="review-render">
              <div className="review-render-heading">
                <strong>Final game-facing guide</strong>
                <span>{record.status}</span>
              </div>
              <iframe
                sandbox=""
                title="Actual submitted guide for staff review"
                srcDoc={previewDocument(artifact.rendered)}
              />
            </section>
            <aside className="review-controls">
              <span className="eyebrow">SUBMISSION</span>
              <h2>{record.author}</h2>
              <p>{record.bloodline}</p>
              <p className="tiny">{record.id}</p>
              <details>
                <summary>Provenance & validation</summary>
                <dl>
                  <dt>Catalog</dt>
                  <dd>{artifact.metadata.catalogVersion}</dd>
                  <dt>Template</dt>
                  <dd>
                    {artifact.metadata.template.slug} · v
                    {artifact.metadata.template.version}
                  </dd>
                  <dt>Game source</dt>
                  <dd>{artifact.metadata.sourceSha}</dd>
                  <dt>Content hash</dt>
                  <dd>{artifact.metadata.contentHash}</dd>
                  <dt>Package hash</dt>
                  <dd>{record.packageHash}</dd>
                </dl>
                <p>
                  ✓ Server-validated authorship
                  <br />✓ Complete pinned foundation
                  <br />✓ Native guide contract
                  <br />✓ Draft, published false
                </p>
              </details>
              <details>
                <summary>Player-authored fields</summary>
                <pre>
                  {JSON.stringify(
                    {
                      ...artifact.submission,
                      highlights: artifact.submission.highlights.map((h) => ({
                        caption: h.caption,
                      })),
                    },
                    null,
                    2,
                  )}
                </pre>
              </details>
              <details>
                <summary>Review history</summary>
                <ol>
                  {record.history.map((h, i) => (
                    <li key={i}>
                      {h.status} · {h.at}
                      {h.notes && <p>{h.notes}</p>}
                    </li>
                  ))}
                </ol>
              </details>
              <label>
                Review notes
                <textarea
                  rows={5}
                  maxLength={4000}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  disabled={!!record.approval}
                />
              </label>
              <div className="staff-actions">
                {record.status === "Submitted" && (
                  <button
                    className="primary"
                    disabled={busy}
                    onClick={() => transition("In review")}
                  >
                    Begin review
                  </button>
                )}
                {["In review", "Changes requested"].includes(record.status) && (
                  <>
                    {record.status === "Changes requested" ? (
                      <button
                        disabled={busy}
                        onClick={() => transition("In review")}
                      >
                        Return to review
                      </button>
                    ) : (
                      <>
                        <button
                          className="primary"
                          disabled={busy}
                          onClick={() => transition("Approved for import")}
                        >
                          Approve & freeze this guide
                        </button>
                        <button
                          disabled={busy || !notes.trim()}
                          onClick={() => transition("Changes requested")}
                        >
                          Request changes
                        </button>
                      </>
                    )}
                  </>
                )}
                {["Submitted", "In review", "Changes requested"].includes(
                  record.status,
                ) && (
                  <button
                    disabled={busy}
                    onClick={() => transition("Rejected/archived")}
                  >
                    Reject / archive
                  </button>
                )}
                {record.approval && (
                  <>
                    <div className="approval-status">
                      ✓ Approved artifact frozen
                    </div>
                    <button
                      className="primary"
                      disabled={busy}
                      onClick={download}
                    >
                      Download game-ready package
                    </button>
                    <p>
                      Open the TNR-side importer in your authenticated game
                      session. Select this package, then choose{" "}
                      <strong>Import draft guide</strong>.
                    </p>
                    <a href="/tnr-guide-importer.user.js" download>
                      Download staff importer
                    </a>
                    <p className="tiny">
                      The game must have the matching approval public key
                      configured. Publishing remains a separate staff action.
                    </p>
                    {record.status === "Approved for import" && (
                      <label className="upload-button">
                        Record verified import receipt
                        <input
                          type="file"
                          accept="application/json,.json"
                          onChange={async (e) => {
                            try {
                              const f = e.target.files[0];
                              if (!f || f.size > 30000)
                                throw Error(
                                  "Choose an importer receipt under 30 KB",
                                );
                              await transition(
                                "Imported",
                                JSON.parse(await f.text()),
                              );
                            } catch (e) {
                              setError(e.message);
                            }
                          }}
                        />
                      </label>
                    )}
                    {record.importReceipt && (
                      <p>
                        Imported as guide{" "}
                        <strong>{record.importReceipt.guideId}</strong>.
                        Unpublished.
                      </p>
                    )}
                  </>
                )}
              </div>
            </aside>
          </div>
        )}
      </main>
    </div>
  );
}
