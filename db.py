import logging
import sqlite3

from config import DB_PATH

logger = logging.getLogger(__name__)


def get_connection():
    """Return a new SQLite connection. Row factory set for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the table if it does not exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS STUD_REGISTRATION (
                STU_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                STU_NAME TEXT NOT NULL,
                STU_CONTACT TEXT NOT NULL,
                STU_EMAIL TEXT NOT NULL,
                STU_ROLLNO TEXT NOT NULL UNIQUE,
                STU_BRANCH TEXT NOT NULL
            )
            """
        )
    logger.info("Database initialised at %s", DB_PATH)


def insert_student(name, contact, email, rollno, branch):
    """Insert a new student. Returns (success, message)."""
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO STUD_REGISTRATION
                    (STU_NAME, STU_CONTACT, STU_EMAIL, STU_ROLLNO, STU_BRANCH)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, contact, email, rollno, branch.upper()),
            )
        logger.info("Inserted student: %s (%s)", name, rollno)
        return True, "Stored successfully"
    except sqlite3.IntegrityError:
        logger.warning("Duplicate rollno: %s", rollno)
        return False, f"Roll number '{rollno}' already exists."
    except sqlite3.Error as e:
        logger.error("DB insert error: %s", e)
        return False, f"Database error: {e}"


def fetch_all_students():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM STUD_REGISTRATION").fetchall()


def search_students_by_name(name):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM STUD_REGISTRATION WHERE STU_NAME LIKE ?",
            (f"%{name}%",),
        ).fetchall()


def delete_student_by_id(stu_id):
    try:
        with get_connection() as conn:
            conn.execute(
                "DELETE FROM STUD_REGISTRATION WHERE STU_ID = ?", (stu_id,)
            )
        logger.info("Deleted student id=%s", stu_id)
        return True, "Deleted successfully"
    except sqlite3.Error as e:
        logger.error("DB delete error: %s", e)
        return False, f"Delete failed: {e}"