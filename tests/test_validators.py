import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from validators import (
    validate_name,
    validate_contact,
    validate_email,
    validate_rollno,
    validate_branch,
    validate_all,
)


def test_name_empty():
    assert validate_name("")[0] is False


def test_name_valid():
    assert validate_name("Lalanthika")[0] is True


def test_email_invalid():
    assert validate_email("not-an-email")[0] is False


def test_email_valid():
    assert validate_email("test@example.com")[0] is True


def test_contact_invalid():
    assert validate_contact("abc")[0] is False


def test_contact_valid():
    assert validate_contact("+91 9876543210")[0] is True


def test_rollno_invalid():
    assert validate_rollno("12 34")[0] is False


def test_branch_invalid():
    assert validate_branch("XYZ")[0] is False


def test_branch_valid():
    assert validate_branch("CSE")[0] is True


def test_validate_all_collects_errors():
    ok, errors = validate_all("", "abc", "nope", "", "XYZ")
    assert ok is False
    assert len(errors) >= 3