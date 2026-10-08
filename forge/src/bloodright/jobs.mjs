// A lease covers active tabs, not a paused job whose last create may have landed.
// Keep that obligation until its ambiguous/unverified items have been resolved.
const UNRESOLVED = new Set(["SENT", "ORPHANED", "CONFIRMED"]);
export function unresolvedBloodrightJob(journal, bloodlineId, exceptJobId = null) {
  if (!bloodlineId) return null;
  if (!journal || typeof journal.listJobs !== "function") throw new Error("Bloodright import requires the persistent journal");
  return journal.listJobs().find(job => job.jobId !== exceptJobId &&
    (job.bloodrightImport?.bloodlineId === bloodlineId || job.items.some(it =>
      it.entity === "skillTree" && it.srcId?.startsWith(`br:${bloodlineId}:`))) &&
    job.items.some(it => UNRESOLVED.has(it.state))) ?? null;
}
export function assertBloodrightAvailable(journal, bloodlineId) {
  const job = unresolvedBloodrightJob(journal, bloodlineId);
  if (job) throw new Error(`unresolved Bloodright job ${job.jobId}: resume or resolve its pending writes before preparing another import for this bloodline`);
}
