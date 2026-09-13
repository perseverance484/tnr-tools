import { readPackageZip } from "../src/artifact.mjs";
import { previewDocument } from "../src/render.mjs";
import {
  verifyApproval,
  reconcileCreation,
  importApproved,
  StorageJournal,
} from "./engine.mjs";
import { nativeTransport } from "./transport.mjs";
// Build-time public configuration. No session material or private signing key belongs here.
const trust = IMPORTER_TRUST;
export function mountImporter({
  host = document.body,
  api,
  journal = new StorageJournal(localStorage),
  configuration = trust,
} = {}) {
  const root = document.createElement("div");
  host.append(root);
  const shadow = root.attachShadow({ mode: "open" });
  shadow.innerHTML = `<style>:host{all:initial}button,input{font:inherit}button{cursor:pointer;padding:12px;border-radius:6px;border:1px solid #8aa6a0}dialog{width:min(1000px,94vw);height:90vh;padding:20px;background:#14272a;color:#f5edd7;border:1px solid #bb9c60;font:16px/1.5 Arial}dialog::backdrop{background:#000b}.bar{display:flex;gap:14px;align-items:center;flex-wrap:wrap}h2{margin:0 20px 0 0;font:28px Georgia}iframe{width:100%;height:58vh;border:0;margin:14px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}a{color:#a8e2d7}.launch{position:fixed;bottom:18px;right:18px;z-index:99999;background:#162f32;color:#faefca}.primary{background:#bee6d7}button:disabled{opacity:.5}</style><button class="launch">Guide Studio import</button><dialog><div class="bar"><h2>Import an approved guide</h2><button class="close">Close</button></div><p>Choose the approved package, review its final content, then import it as an unpublished native guide.</p><input aria-label="Approved guide package" type="file" accept=".zip,application/zip"><p class="status" role="status"></p><iframe sandbox="" title="Approved guide to import"></iframe><div class="bar"><button class="primary" disabled>Import draft guide</button><button class="receipt" hidden>Download verified receipt</button></div><details><summary>Recover an interrupted creation</summary><p>Only if the importer reported an unknown create outcome: find the untouched New guide article in TNR, confirm its creation time, and supply its ID. This attaches it without changing its content.</p><input class="reconcile-id" aria-label="Untouched placeholder guide ID"><button class="reconcile">Attach verified empty draft</button></details><pre class="result"></pre></dialog>`;
  const q = (s) => shadow.querySelector(s),
    dialog = q("dialog"),
    status = q(".status"),
    button = q(".primary");
  let selected, receipt;
  q(".launch").onclick = () => dialog.showModal();
  q(".close").onclick = () => dialog.close();
  q("input").onchange = async (e) => {
    button.disabled = true;
    selected = null;
    receipt = null;
    q(".receipt").hidden = true;
    q(".result").textContent = "";
    try {
      const file = e.target.files[0];
      if (!file || file.size > 8_000_000)
        throw Error("Select a package under 8 MB");
      const parsed = await readPackageZip(
        new Uint8Array(await file.arrayBuffer()),
      );
      const checked = await verifyApproval(
        parsed.artifact,
        parsed.approval,
        configuration,
      );
      selected = parsed;
      q("iframe").srcdoc = previewDocument(parsed.artifact.rendered);
      status.textContent = `Verified approval · ${checked.game.title} · ${checked.meta.packageHash}`;
      button.disabled = false;
    } catch (error) {
      status.textContent = error.message;
    }
  };
  button.onclick = async () => {
    button.disabled = true;
    try {
      if (!selected) throw Error("Choose a verified package first");
      if (!navigator.locks)
        throw Error(
          "This browser must support Web Locks to protect imports across tabs.",
        );
      status.textContent = "Importing into the native guide model…";
      receipt = await navigator.locks.request(
        "tnr-guide-import",
        { mode: "exclusive" },
        () =>
          importApproved({
            ...selected,
            trust: configuration,
            api: api || nativeTransport({ origin: location.origin }),
            journal,
          }),
      );
      status.textContent = `Imported and verified: ${receipt.guideId}. Unpublished.`;
      q(".result").textContent = JSON.stringify(receipt, null, 2);
      q(".receipt").hidden = false;
    } catch (error) {
      status.textContent = error.message;
      button.disabled = false;
    }
  };
  q(".reconcile").onclick = async () => {
    try {
      if (!selected) throw Error("Choose the approved package first");
      if (!navigator.locks) throw Error("Web Locks required");
      const id = await navigator.locks.request("tnr-guide-import", () =>
        reconcileCreation({
          ...selected,
          trust: configuration,
          api: api || nativeTransport({ origin: location.origin }),
          journal,
          guideId: q(".reconcile-id").value.trim(),
        }),
      );
      status.textContent =
        "Attached " + id + ". Choose Import draft guide to continue.";
      button.disabled = false;
    } catch (error) {
      status.textContent = error.message;
    }
  };
  q(".receipt").onclick = () => {
    const a = document.createElement("a"),
      url = URL.createObjectURL(
        new Blob([JSON.stringify(receipt, null, 2)], {
          type: "application/json",
        }),
      );
    a.href = url;
    a.download = "tnr-import-receipt.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  return root;
}
if (location.origin === "https://www.theninja-rpg.com") mountImporter();
