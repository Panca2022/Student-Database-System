# Student Database System

A desktop application built with Python, Tkinter, and SQLite for managing student records. It supports adding, searching, viewing, deleting, and exporting student data through a clean graphical interface.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Architecture](#4-architecture)
5. [Folder Structure](#5-folder-structure)
6. [Features](#6-features)
7. [How It Works](#7-how-it-works)
8. [Installation](#8-installation)
9. [Usage](#9-usage)
10. [Module Reference](#10-module-reference)
11. [Why These Design Decisions](#11-why-these-design-decisions)
12. [Reliability Engineering](#12-reliability-engineering)
13. [Testing](#13-testing)
14. [Observations](#14-observations)
15. [Limitations](#15-limitations)
16. [Future Improvements](#16-future-improvements)
17. [Interview Notes](#17-interview-notes)

---

## 1. Project Overview

The Student Database System is a lightweight desktop application (Create, Read and Delete are implemented; Update is planned) that stores student information in a local SQLite database.

It was originally a single-file Tkinter app. It has been refactored into modules with validation, logging, error handling, and export functionality.

---

## 2. Problem Statement

Managing student data manually is time-consuming and error-prone. Duplicates, invalid emails, and lost records are common. A simple, offline, reliable desktop tool is needed for small institutions, coaching centres, or individual teachers.

---

## 3. Objectives

- Provide a simple GUI to add, search, view, and delete student records.
- Validate input before saving (name, contact, email, roll number, branch).
- Prevent duplicate roll numbers.
- Log all actions for auditing.
- Export records to CSV.
- Handle database errors gracefully.
- Make the code modular, testable, and maintainable.

---

## 4. Architecture

```text
[ Tkinter GUI ]
       |
       v
[ validators.py ]  <- clean data
       |
       v
[ db.py ]          <- CRUD operations
       |
       v
[ SQLite student.db ]
       |
       v
[ exporter.py ]    <- CSV output

[ logger.py ]  writes to student_app.log
[ config.py ]  stores paths and rules
```

---

## 5. Folder Structure

```text
Student-Database-System-main/
├── main.py
├── config.py
├── logger.py
├── validators.py
├── db.py
├── exporter.py
├── requirements.txt
├── .gitignore
├── README.md
├── tests/
│   └── test_validators.py
└── student.db          <- created at runtime
```

---

## 6. Features

### Core Features

- Add a new student
- Search by name (partial match)
- View all students
- Delete selected student
- Reset form and view

### Reliability Features

- Input validation (email format, contact digits, name length, branch list)
- Unique roll number enforcement
- Duplicate prevention at DB level
- Parameterised SQL queries
- Structured logging to file
- Graceful error messages via popups
- CSV export
- Unit tests
- Configurable paths

---

## 7. How It Works

1. On startup, `main()` calls `init_db()`, creating `student.db` if missing.
2. The GUI is built from `DisplayForm()`.
3. When the user clicks **Submit**, `register()` runs:
   - `validate_all()` checks every field
   - `insert_student()` writes to SQLite
   - Errors (like a duplicate roll number) are caught and shown
4. **Search** filters by name using SQL `LIKE`.
5. **Delete** asks for confirmation, then calls `delete_student_by_id()` using a parameterised query.
6. **Export CSV** writes current records to `exports/students_export.csv`.
7. Every action is logged to `student_app.log`.

---

## 8. Installation

```bash
git clone https://github.com/Panca2022/Student-Database-System.git
cd Student-Database-System
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

`tkinter` and `sqlite3` come with Python. Only `pytest` is an external package.

---

## 9. Usage

```bash
python main.py
```

- Click **Submit** to add a student.
- Click any row and then **Delete** to remove it.
- Click **Export CSV** to save records.

---

## 10. Module Reference

| Module                     | Purpose                              |
|----------------------------|--------------------------------------|
| `main.py`                  | GUI and event handlers               |
| `config.py`                | Paths, titles, validation rules      |
| `logger.py`                | Logging configuration                |
| `validators.py`            | Field-by-field validation            |
| `db.py`                    | SQLite CRUD, safe queries            |
| `exporter.py`              | CSV export                           |
| `tests/test_validators.py` | Unit tests                           |

---

## 11. Why These Design Decisions

**Why split the single file into modules?**
The original `main.py` mixed GUI, validation, DB access, and business logic. Splitting into modules makes the code testable and easier to change. If you later replace SQLite with PostgreSQL, only `db.py` changes.

**Why validators?**
The original code only checked for empty strings. A user could enter "abc" as an email. Regex validation catches real mistakes.

**Why parameterised queries?**
The original `DELETE FROM STUD_REGISTRATION WHERE STU_ID = %d` used string formatting, which is an SQL injection risk. Parameterised queries (`?`) are safe.

**Why UNIQUE on roll number?**
Students should not be duplicated. Enforcing uniqueness at the database level is stronger than checking in Python.

**Why logging?**
Tkinter apps can fail silently. Logging records every insert, search, and delete. It is useful for debugging and auditing.

**Why CSV export?**
It is a natural feature for a database app and demonstrates file handling.

---

## 12. Reliability Engineering

| Feature                  | Implementation                | Why                        |
|--------------------------|-------------------------------|----------------------------|
| Validation               | `validators.py`               | Prevent bad data           |
| Duplicate prevention     | `UNIQUE` constraint           | Data integrity             |
| SQL injection protection | Parameterised queries         | Security                   |
| Error handling           | `try / except sqlite3.Error`  | No silent crashes          |
| Logging                  | `logging` file handler        | Post-mortem debugging      |
| Config                   | `config.py`                   | Single source of truth     |
| Tests                    | `pytest`                      | Safe refactors             |
| CSV export               | `exporter.py`                 | Data portability           |

---

## 13. Testing

```bash
pytest -q
```

Covers name, contact, email, roll number, and branch validation, plus the combined validator.

---

## 14. Observations

- Most student databases fail because of duplicate entries. `UNIQUE` fixes that.
- Input validation is the single biggest improvement. It prevents bad data from ever reaching the database.
- Logging helps diagnose problems that don't reproduce easily.
- Modular code is easier to extend later (for example attendance, marks, or fees).

---

## 15. Limitations

- Single-user desktop app (SQLite is not suited to many simultaneous users).
- No login or authentication.
- No update/edit feature yet.
- No pagination for very large datasets.
- Branch list is hardcoded in `config.py`.

---

## 16. Future Improvements

1. **Edit feature** — allow updating existing records.
2. **Login screen** — simple user/password with hashed storage.
3. **Pagination** — handle thousands of records.
4. **Multi-user database** — move to PostgreSQL.
5. **Backup button** — copy `student.db` to a dated file.
6. **Branch list from file** — load allowed branches from JSON.
7. **Search by roll number and branch** — currently only by name.
8. **Import from CSV** — the reverse of export.
9. **Packaging** — convert to `.exe` with PyInstaller.

---

## 17. Interview Notes

### Two-minute pitch

> "The Student Database System is a Tkinter + SQLite desktop application. I refactored it from a single script into modules: config, logger, validators, db, and exporter. I added email and contact validation with regex, enforced unique roll numbers at the database level, replaced string-formatted SQL with parameterised queries to prevent SQL injection, and added logging to a file so problems can be diagnosed after the fact. I also added a CSV export feature and unit tests for the validators."

### Common questions

**Q: Why SQLite?**
A: Lightweight, zero-configuration, embedded, and perfect for single-user desktop apps.

**Q: How do you prevent duplicate students?**
A: A `UNIQUE` constraint on `STU_ROLLNO`, plus `IntegrityError` handling in `db.py`.

**Q: How do you prevent SQL injection?**
A: All queries use parameterised `?` placeholders instead of string formatting.

**Q: How is data validated?**
A: Regex for email and contact; length check for name; alphanumeric check for roll number; branch must be in the allowed list.

**Q: What if the database is corrupted?**
A: Currently you would restore from a backup. A future improvement is a scheduled backup and an integrity check using `PRAGMA integrity_check`.

**Q: What was the biggest change you made?**
A: Splitting the single file into modules and adding validation. It made the app safer and testable.

---

## Author

Refactored and extended as a demonstration of modular Python desktop application design.