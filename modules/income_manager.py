"""Functions for managing monthly income."""

from pathlib import Path

from utils.file_handler import load_json, save_json
from utils.validation import validate_amount


INCOME_FILE = Path(__file__).resolve().parents[1] / "data" / "income.json"


def get_income(storage_path=INCOME_FILE):
    income = load_json(storage_path, {"amount": 0.0})

    if not isinstance(income, dict):
        raise ValueError("Income storage must contain a dictionary.")

    return income


def set_income(amount, storage_path=INCOME_FILE):
    amount = validate_amount(amount)

    income = {
        "amount": amount
    }

    save_json(storage_path, income)

    return income


def get_income_amount(storage_path=INCOME_FILE):
    income = get_income(storage_path)

    return income.get("amount", 0.0)