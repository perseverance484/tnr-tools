CREATE TABLE IF NOT EXISTS guide_submissions (
  id TEXT PRIMARY KEY,
  revision INTEGER NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('Submitted','In review','Changes requested','Approved for import','Imported','Rejected/archived')),
  document TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS guide_submissions_status ON guide_submissions(status, id);
