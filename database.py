import sqlite3
def create_database():
    conn=sqlite3.connect("jobs.db")
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS jobs(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   company TEXT,
                   role TEXT,
                   date_applied TEXT,
                   status TEXT,
                   notes TEXT)""")
    conn.commit()
    conn.close()

def save_job(company, role, date_applied, status, notes):
    conn=sqlite3.connect("jobs.db")
    cursor=conn.cursor()
    cursor.execute("""INSERT INTO jobs(company, role, date_applied, status, notes)
                   VALUES(?, ?, ?, ?, ?)""", (company, role, str(date_applied), status, notes))
    conn.commit()
    conn.close()

def get_all_jobs():
    conn=sqlite3.connect("jobs.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    rows=cursor.fetchall()
    conn.close()
    return rows

def delete_job(job_id):
    conn=sqlite3.connect("jobs.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id=?",(job_id,))
    conn.commit()
    conn.close()

def filter_jobs(status):
    conn=sqlite3.connect("jobs.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE status=?", (status,))
    jobs=cursor.fetchall()
    conn.close()
    return jobs

def update_job_status(job_id,new_status):
    conn=sqlite3.connect("jobs.db")
    cursor=conn.cursor()
    cursor.execute("UPDATE jobs SET status=? WHERE id=?",(new_status,job_id))
    conn.commit()
    conn.close()

def get_job_stats():
    conn=sqlite3.connect("jobs.db")
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Applied'")
    applied=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Interview'")
    interview=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Offer'")
    offer=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='Rejected'")
    rejected=cursor.fetchone()[0]
    conn.close()
    return total, applied, interview, offer, rejected

def search_jobs(company_name):
    conn=sqlite3.connect("jobs.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE company LIKE ?",('%'+company_name+'%',))
    jobs=cursor.fetchall()
    conn.close()
    return jobs