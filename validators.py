import re

from config import MIN_NAME_LEN, MAX_NAME_LEN, ALLOWED_BRANCHES

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
CONTACT_RE = re.compile(r"^[0-9+\-\s]{7,15}$")


def validate_name(name: str):
    if not name or not name.strip():
        return False, "Name cannot be empty."
    if len(name.strip()) < MIN_NAME_LEN:
        return False, f"Name must be at least {MIN_NAME_LEN} characters."
    if len(name.strip()) > MAX_NAME_LEN:
        return False, f"Name must be under {MAX_NAME_LEN} characters."
    return True, ""


def validate_contact(contact: str):
    if not contact or not CONTACT_RE.match(contact.strip()):
        return False, "Contact must be 7-15 digits (with optional + and -)."
    return True, ""


def validate_email(email: str):
    if not email or not EMAIL_RE.match(email.strip()):
        return False, "Please enter a valid email address."
    return True, ""


def validate_rollno(rollno: str):
    if not rollno or not rollno.strip():
        return False, "Roll number cannot be empty."
    if not rollno.strip().isalnum():
        return False, "Roll number must be alphanumeric."
    return True, ""


def validate_branch(branch: str):
    if not branch or branch.strip().upper() not in ALLOWED_BRANCHES:
        return False, f"Branch must be one of: {', '.join(ALLOWED_BRANCHES)}"
    return True, ""


def validate_all(name, contact, email, rollno, branch):
    """Run every validator. Return (is_valid, list_of_errors)."""
    errors = []
    for ok, msg in (
        validate_name(name),
        validate_contact(contact),
        validate_email(email),
        validate_rollno(rollno),
        validate_branch(branch),
    ):
        if not ok:
            errors.append(msg)
    return (len(errors) == 0), errors