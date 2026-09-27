"""Tests for budget-management operations."""

import tempfile
import unittest
from pathlib import Path

from modules.budget_manager import check_budget_limits, get_budget_status, set_category_budget, set_monthly_budget
from modules.expense_manager import add_expense


class BudgetManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        root = Path(self.temporary_directory.name)
        self.budget_path = root / "budget.json"
        self.expenses_path = root / "expenses.json"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_status_tracks_overall_and_category_spending(self) -> None:
        set_monthly_budget(500, self.budget_path)
        set_category_budget("Food", 200, self.budget_path)
        add_expense(180, "Food", expense_date="2026-09-05", storage_path=self.expenses_path)
        report = get_budget_status(self.budget_path, self.expenses_path, "2026-09")
        self.assertEqual(report["overall"]["remaining"], 320.0)
        self.assertEqual(report["categories"]["Food"]["status"], "warning")

    def test_limit_checker_reports_exceeded_budget(self) -> None:
        set_monthly_budget(100, self.budget_path)
        add_expense(125, "Food", expense_date="2026-09-05", storage_path=self.expenses_path)
        messages = check_budget_limits(budget_path=self.budget_path, expenses_path=self.expenses_path, month="2026-09")
        self.assertEqual(len(messages), 1)
        self.assertIn("exceeded", messages[0])
