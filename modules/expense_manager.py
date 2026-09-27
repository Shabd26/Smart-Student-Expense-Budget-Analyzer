"""Expense storage and lookup operations."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from utils.file_handler import load_json, save_json
from utils.validation import validate_amount, validate_category, validate_date, validate_description

EXPENSES_FILE = Path(__file__).resolve().parents[1] / "data" / "expenses.json"


def _load_expenses(storage_path: str | Path = EXPENSES_FILE) -> list[dict]:
    expenses = load_json(storage_path, [])
    if not isinstance(expenses, list):
        raise ValueError("Expenses storage must contain a list.")
    return expenses


def _next_id(expenses: list[dict]) -> int:
    return max((expense.get("id", 0) for expense in expenses), default=0) + 1


def add_expense(amount: object, category: object, description: object = "", expense_date: object | None = None, storage_path: str | Path = EXPENSES_FILE) -> dict:
    """Validate, save, and return one new expense."""
    expenses = _load_expenses(storage_path)
    new_expense = {"id": _next_id(expenses), "amount": validate_amount(amount), "category": validate_category(category), "description": validate_description(description), "date": validate_date(expense_date or date.today().isoformat())}
    expenses.append(new_expense)
    save_json(storage_path, expenses)
    return new_expense


def view_expenses(storage_path: str | Path = EXPENSES_FILE) -> list[dict]:
    """Return every expense in storage."""
    return _load_expenses(storage_path)


def search_expenses(query: object, storage_path: str | Path = EXPENSES_FILE) -> list[dict]:
    """Find expenses by exact ID or category/description text."""
    term = str(query).strip().casefold()
    if not term:
        return []
    return [expense for expense in _load_expenses(storage_path) if term == str(expense.get("id", "")).casefold() or term in expense.get("category", "").casefold() or term in expense.get("description", "").casefold()]


def filter_by_category(category: object, storage_path: str | Path = EXPENSES_FILE) -> list[dict]:
    """Return expenses whose category matches case-insensitively."""
    target = validate_category(category).casefold()
    return [expense for expense in _load_expenses(storage_path) if expense.get("category", "").casefold() == target]


def edit_expense(expense_id: int, *, amount: object | None = None, category: object | None = None, description: object | None = None, expense_date: object | None = None, storage_path: str | Path = EXPENSES_FILE) -> dict | None:
    """Update supplied fields for an expense, or return None if absent."""
    expenses = _load_expenses(storage_path)
    for expense in expenses:
        if expense.get("id") == expense_id:
            if amount is not None:
                expense["amount"] = validate_amount(amount)
            if category is not None:
                expense["category"] = validate_category(category)
            if description is not None:
                expense["description"] = validate_description(description)
            if expense_date is not None:
                expense["date"] = validate_date(expense_date)
            save_json(storage_path, expenses)
            return expense
    return None


def delete_expense(expense_id: int, storage_path: str | Path = EXPENSES_FILE) -> bool:
    """Remove an expense by ID and report whether it existed."""
    expenses = _load_expenses(storage_path)
    remaining = [expense for expense in expenses if expense.get("id") != expense_id]
    if len(remaining) == len(expenses):
        return False
    save_json(storage_path, remaining)
    return True
