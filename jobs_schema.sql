CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    file_name TEXT,
    num_util_files INTEGER,
    submitted_at TEXT,
    started_at TEXT,
    finished_at TEXT,
    num_data_files INTEGER,
    status TEXT,
    runtime REAL,
    error TEXT,
    callback_URL TEXT,
    cpu_power REAL
)

