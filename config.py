import os

# Central configuration for the Student Database System.
# Change these values in one place instead of hunting through main.py.

DB_PATH = os.getenv("STUDENT_DB_PATH", "student.db")
EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
APP_TITLE = os.getenv("APP_TITLE", "Student Database System")

# Validation rules
MIN_NAME_LEN = 2
MAX_NAME_LEN = 60
ALLOWED_BRANCHES = [
    "CSE", "IT", "ECE", "EEE", "MECH", "CIVIL", "AI", "DS", "OTHER"
]