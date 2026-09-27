"""Validation routines for user-provided expense data."""

from __future__ import annotations

from datetime import date


def validate_amount(value: object) -> float:
    """Convert a positive numeric amount to a float."""
    try:
        amount = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError("Amount must be a number.") from error
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


def validate_category(value: object) -> str:
    """Return a non-empty expense category."""
    category = str(value).strip() if value is not None else ""
    if not category:
        raise ValueError("Category cannot be empty.")
    return category


def validate_description(value: object) -> str:
    """Return a trimmed expense description (which may be empty)."""
    return str(value).strip() if value is not None else ""


def validate_date(value: object) -> str:
    """Return a date in ISO (YYYY-MM-DD) format."""
    try:
        return date.fromisoformat(str(value)).isoformat()
    except (TypeError, ValueError) as error:
        raise ValueError("Date must use YYYY-MM-DD format.") from error
