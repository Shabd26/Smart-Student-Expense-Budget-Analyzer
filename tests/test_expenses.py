"""Tests for expense-management operations."""

import tempfile
import unittest
from pathlib import Path

from modules.expense_manager import add_expense, delete_expense, edit_expense, filter_by_category, search_expenses, view_expenses


class ExpenseManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temporary_directory.name) / "expenses.json"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_add_assigns_ids_and_saves_expense(self) -> None:
        first = add_expense(120, "Food", "Lunch", "2026-09-24", self.storage_path)
        second = add_expense("80.5", "Travel", "Bus", "2026-09-25", self.storage_path)
        self.assertEqual((first["id"], second["id"]), (1, 2))
        self.assertEqual(len(view_expenses(self.storage_path)), 2)

    def test_search_and_category_filter_are_case_insensitive(self) -> None:
        add_expense(120, "Food", "Lunch", "2026-09-24", self.storage_path)
        add_expense(50, "Travel", "Bus", "2026-09-25", self.storage_path)
        self.assertEqual(len(search_expenses("lunch", self.storage_path)), 1)
        self.assertEqual(len(filter_by_category("FOOD", self.storage_path)), 1)

    def test_edit_and_delete(self) -> None:
        add_expense(120, "Food", "Lunch", "2026-09-24", self.storage_path)
        updated = edit_expense(1, amount=150, storage_path=self.storage_path)
        self.assertEqual(updated["amount"], 150.0)
        self.assertTrue(delete_expense(1, self.storage_path))
        self.assertFalse(delete_expense(1, self.storage_path))

    def test_rejects_invalid_amount_and_date(self) -> None:
        with self.assertRaises(ValueError):
            add_expense(0, "Food", storage_path=self.storage_path)
        with self.assertRaises(ValueError):
            add_expense(100, "Food", expense_date="24-09-2026", storage_path=self.storage_path)
