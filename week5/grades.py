"""Pair-programming kata: convert a numeric score to a letter grade."""

MIN_SCORE = 0
MAX_SCORE = 100

# Lowest score for each letter, checked from the highest down.
GRADE_THRESHOLDS = (
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
)
FAIL_GRADE = "F"


def letter_grade(score):
    """Return the letter grade (A-F) for a score between 0 and 100.

    Raises ValueError for scores outside 0-100.
    """
    if not MIN_SCORE <= score <= MAX_SCORE:
        raise ValueError(
            f"score must be between {MIN_SCORE} and {MAX_SCORE}, got {score}"
        )
    for threshold, letter in GRADE_THRESHOLDS:
        if score >= threshold:
            return letter
    return FAIL_GRADE
