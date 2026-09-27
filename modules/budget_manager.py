"""Budget configuration and spending-limit checks."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from modules.expense_manager import EXPENSES_FILE, view_expenses
from utils.file_handler import load_json, save_json
from utils.validation import validate_amount, validate_category

BUDGET_FILE = Path(__file__).resolve().parents[1] / "data" / "budget.json"


def _load_budget(storage_path: str | Path = BUDGET_FILE) -> dict:
    """Load a budget file, supplying its standard shape when needed."""
    budget = load_json(storage_path, {"monthly_budget": 0.0, "category_budgets": {}})
    if not isinstance(budget, dict) or not isinstance(budget.get("category_budgets", {}), dict):
        raise ValueError("Budget storage has an invalid format.")
    budget.setdefault("monthly_budget", 0.0)
    budget.setdefault("category_budgets", {})
    return budget


def set_monthly_budget(amount: object, storage_path: str | Path = BUDGET_FILE) -> float:
    """Set and return the overall monthly spending limit."""
    budget = _load_budget(storage_path)
    budget["monthly_budget"] = validate_amount(amount)
    save_json(storage_path, budget)
    return budget["monthly_budget"]


def set_category_budget(category: object, amount: object, storage_path: str | Path = BUDGET_FILE) -> dict:
    """Set and return a category-specific monthly spending limit."""
    budget = _load_budget(storage_path)
    clean_category = validate_category(category)
    budget["category_budgets"][clean_category] = validate_amount(amount)
    save_json(storage_path, budget)
    return {"category": clean_category, "amount": budget["category_budgets"][clean_category]}


def _current_month_expenses(expenses: list[dict], month: str) -> list[dict]:
    return [expense for expense in expenses if str(expense.get("date", "")).startswith(month)]


def _status(spent: float, limit: float) -> dict:
    if limit <= 0:
        return {"spent": spent, "budget": limit, "remaining": None, "utilization": None, "status": "not set"}
    utilization = round((spent / limit) * 100, 2)
    return {
        "spent": spent,
        "budget": limit,
        "remaining": round(limit - spent, 2),
        "utilization": utilization,
        "status": "exceeded" if spent > limit else "warning" if utilization >= 80 else "within limit",
    }


def get_budget_status(
    budget_path: str | Path = BUDGET_FILE,
    expenses_path: str | Path = EXPENSES_FILE,
    month: str | None = None,
) -> dict:
    """Return overall and category budget status for a YYYY-MM month."""
    selected_month = month or date.today().strftime("%Y-%m")
    if len(selected_month) != 7 or selected_month[4] != "-":
        raise ValueError("Month must use YYYY-MM format.")
    budget = _load_budget(budget_path)
    expenses = _current_month_expenses(view_expenses(expenses_path), selected_month)
    total_spent = round(sum(float(expense.get("amount", 0)) for expense in expenses), 2)
    categories = {}
    for category, limit in budget["category_budgets"].items():
        spent = round(sum(float(expense.get("amount", 0)) for expense in expenses if expense.get("category", "").casefold() == category.casefold()), 2)
        categories[category] = _status(spent, float(limit))
    return {"month": selected_month, "overall": _status(total_spent, float(budget["monthly_budget"])), "categories": categories}


def check_budget_limits(**kwargs: object) -> list[str]:
    """Return human-readable warnings for budgets at 80% or more."""
    report = get_budget_status(**kwargs)
    messages = []
    for label, details in [("Overall", report["overall"]), *report["categories"].items()]:
        if details["status"] == "warning":
            messages.append(f"{label} budget is at {details['utilization']:.2f}%.")
        elif details["status"] == "exceeded":
            messages.append(f"{label} budget exceeded by ₹{abs(details['remaining']):.2f}.")
    return messages
