"""Tuition-fee calculation for the Student Services App (refactored legacy_fees.py)."""

from dataclasses import dataclass
from enum import Enum

PRICE_PER_CREDIT_HOUR = 350
LARGE_FEE_THRESHOLD = 6000
LARGE_FEE_REDUCTION = 200
SUMMER_SUPPLEMENT = 150


class StudentType(Enum):
    """Kinds of student, each with its own share of the full price."""

    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


# Share of the full course price each type of student pays.
PRICE_SHARE = {
    StudentType.REGULAR: 1.0,
    StudentType.STAFF_CHILD: 0.5,
    StudentType.SCHOLARSHIP: 0.0,
}

REPORT_LABELS = {
    StudentType.REGULAR: "Student fee",
    StudentType.STAFF_CHILD: "Staff child fee",
    StudentType.SCHOLARSHIP: "Scholarship fee",
}


@dataclass(frozen=True)
class Course:
    """A course the student is registered for."""

    hours: int


def tuition_fee(courses, kind, summer=False, discount=0, extras=()):
    """Return the total tuition fee for one student."""
    total = (
        sum(course.hours for course in courses)
        * PRICE_PER_CREDIT_HOUR
        * PRICE_SHARE[kind]
    )
    if total > LARGE_FEE_THRESHOLD:
        total -= LARGE_FEE_REDUCTION
    if summer:
        total += SUMMER_SUPPLEMENT
    return total - discount + sum(extras)


def fee_report(fee, kind):
    """Return the report lines for a fee (calculation and printing are now separate)."""
    lines = [f"{REPORT_LABELS[kind]}: {fee}"]
    if fee > LARGE_FEE_THRESHOLD:
        lines.append("High fee")
    return "\n".join(lines)


def process_all(students):
    """Return a {name: fee} dictionary with a fee for every student."""
    return {
        student["name"]: tuition_fee(
            student["courses"], student["type"], student["summer"]
        )
        for student in students
    }
