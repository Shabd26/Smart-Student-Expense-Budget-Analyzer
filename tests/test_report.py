import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from modules.report_generator import generate_report


class TestReportGenerator(unittest.TestCase):

    def test_generate_report(self):
        expenses = [
            {
                "id": 1,
                "amount": 500,
                "category": "Food",
                "description": "Lunch",
                "date": "2026-09-20"
            },
            {
                "id": 2,
                "amount": 1000,
                "category": "Travel",
                "description": "Bus",
                "date": "2026-09-21"
            }
        ]

        budget_status = {
            "monthly_budget": 5000,
            "monthly_spent": 1500,
            "monthly_remaining": 3500,
            "categories": {}
        }

        goals = [
            {
                "id": 1,
                "name": "Laptop",
                "target": 50000,
                "saved": 10000
            }
        ]

        with patch(
            "modules.report_generator.view_expenses",
            return_value=expenses
        ), patch(
            "modules.report_generator.get_income_amount",
            return_value=10000
        ), patch(
            "modules.report_generator.get_budget_status",
            return_value=budget_status
        ), patch(
            "modules.report_generator.view_goals",
            return_value=goals
        ):

            report = generate_report()

        self.assertEqual(report["income"], 10000)
        self.assertEqual(report["total_spending"], 1500)
        self.assertEqual(report["remaining_money"], 8500)
        self.assertEqual(report["average_expense"], 750)
        self.assertEqual(report["transaction_count"], 2)
        self.assertEqual(report["highest_category"], "Travel")
        self.assertEqual(len(report["goals"]), 1)


if __name__ == "__main__":
    unittest.main()