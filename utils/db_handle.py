# Set-ups
import sqlite3

# Get database
def get_db(db_file):
    return sqlite3.connect(db_file, timeout=10)

# UPDATE DB
# Insert job on upload susccessfully
def insert_job(job_id, file_name, callback_url):

    db = get_db("jobs.db")
    db.execute(
        """
        INSERT INTO jobs (job_id, file_name, submitted_at, status, callback_URL)
        VALUES (?, ?, datetime('now'), ?, ?)
        """,
        (job_id, file_name, "PENDING", callback_url)
    )

    db.commit()
    db.close()

# Update job on job start and finish
def mark_started(job_id):

    db = get_db("jobs.db")
    db.execute(
        """
        UPDATE jobs
        SET started_at = datetime('now'),
            status = ?
        WHERE job_id = ?
        """,
        ("STARTED", job_id)
    )

    db.commit()
    db.close()

def mark_done(job_id, status, error=None):

    db = get_db("jobs.db")
    db.execute(
        """
        UPDATE jobs
        SET finished_at = datetime('now'),
            status = ?,
            error = ?,
            runtime = (
                strftime('%s', finished_at) - strftime('%s', started_at) 
            )
        WHERE job_id = ?
        """,
        (status, error, job_id) # seconds runtime
    )

    db.commit()
    db.close()

# Update data
def count_data(job_id, num_f):

    db = get_db("jobs.db")
    db.execute(
        """
        UPDATE jobs
        SET num_data_files = ?
        WHERE job_id = ?
        """,
        (num_f, job_id)
    )

    db.commit()
    db.close()

# Update util
def count_util(job_id, num_f):

    db = get_db("jobs.db")
    db.execute(
        """
        UPDATE jobs
        SET num_util_files = ?
        WHERE job_id = ?
        """,
        (num_f, job_id)
    )

    db.commit()
    db.close()

# Insert cpu_power
def insert_cpu_power(job_id, cpu_power):
    db = get_db("jobs.db")
    db.execute(
        """
        UPDATE jobs
        SET cpu_power = ?
        WHERE job_id = ?
        """,
        (cpu_power, job_id)
    )

    db.commit()
    db.close()

# QUERY DATA
# Get all data
def get_all_data(job_id):
    db = get_db("jobs.db")
    cursor = db.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    data = cursor.fetchone()
    db.close()
    return data if data else None

# Get callback url
def get_callback_url(job_id):
    
    db = get_db("jobs.db")
    url = db.execute("SELECT callback_URL FROM jobs WHERE job_id = ? ", (job_id,)).fetchone()
    db.close()
    return url[0] if url else None

# Get error
def get_error(job_id):
    
    db = get_db("jobs.db")
    error = db.execute("SELECT error FROM jobs WHERE job_id = ? ", (job_id,)).fetchone()
    db.close()
    return error[0] if error else None

# Get filename
def get_filename(job_id):

    db = get_db("jobs.db")
    name = db.execute("SELECT file_name FROM jobs WHERE job_id = ? ", (job_id,)).fetchone()
    db.close()
    return name[0] if name else None