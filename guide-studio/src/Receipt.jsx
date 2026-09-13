import React, { useState } from "react";
export function ReceiptLookup({ onRevise }) {
  const [receipt, setReceipt] = useState(null),
    [result, setResult] = useState(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  async function check(r) {
    setBusy(true);
    setError("");
    try {
      if (!/^[a-f0-9-]{36}$/.test(r.id) || typeof r.token !== "string")
        throw Error("Choose your private receipt file.");
      const response = await fetch("/api/receipt/" + r.id, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: r.token }),
      });
      const data = await response.json();
      if (!response.ok) throw Error(data.error);
      setReceipt(r);
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  const saved = Object.keys(localStorage).filter((k) =>
    k.startsWith("tnr-guide-studio:receipt:"),
  );
  return (
    <details className="receipt-lookup">
      <summary>
        Already submitted? Read staff feedback or send a revision.
      </summary>
      <div>
        <label className="upload-button">
          Open private receipt
          <input
            type="file"
            accept=".json,application/json"
            disabled={busy}
            onChange={async (e) => {
              try {
                const f = e.target.files[0];
                if (!f || f.size > 10000)
                  throw Error("Choose a receipt under 10 KB");
                await check(JSON.parse(await f.text()));
              } catch (e) {
                setError(e.message);
              }
            }}
          />
        </label>
        {saved.length > 0 && (
          <label>
            Receipts on this device
            <select
              aria-label="Saved submission receipts"
              defaultValue=""
              onChange={(e) => {
                if (e.target.value)
                  check(JSON.parse(localStorage.getItem(e.target.value)));
              }}
            >
              <option value="">Choose a submission</option>
              {saved.map((k) => (
                <option key={k} value={k}>
                  {k.split(":").at(-1)}
                </option>
              ))}
            </select>
          </label>
        )}
        {error && <p role="alert">{error}</p>}
        {result && (
          <>
            <h3>{result.status}</h3>
            <p>{result.notes || "Staff has not left feedback yet."}</p>
            {result.status === "Changes requested" && (
              <button
                className="primary"
                onClick={() => onRevise(result, receipt)}
              >
                Revise this guide
              </button>
            )}
          </>
        )}
      </div>
    </details>
  );
}
