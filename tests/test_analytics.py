import unittest

from modules.analytics import (
    calculate_total,
    calculate_average,
    find_highest_expense,
    find_lowest_expense,
    category_analysis,
    find_highest_category,
    count_transactions
)


class AnalyticsTests(unittest.TestCase):

    def setUp(self):
        self.expenses = [
            {
                "id": 1,
                "amount": 250,
                "category": "Food",
                "description": "Lunch",
                "date": "2026-09-20"
            },
            {
                "id": 2,
                "amount": 100,
                "category": "Transport",
                "description": "Bus",
                "date": "2026-09-20"
            },
            {
                "id": 3,
                "amount": 300,
                "category": "Food",
                "description": "Dinner",
                "date": "2026-09-21"
            },
            {
                "id": 4,
                "amount": 500,
                "category": "Entertainment",
                "description": "Movie",
                "date": "2026-09-22"
            }
        ]

    def test_total(self):
        self.assertEqual(calculate_total(self.expenses), 1150)

    def test_average(self):
        self.assertEqual(calculate_average(self.expenses), 287.5)

    def test_highest_expense(self):
        result = find_highest_expense(self.expenses)
        self.assertEqual(result["amount"], 500)

    def test_lowest_expense(self):
        result = find_lowest_expense(self.expenses)
        self.assertEqual(result["amount"], 100)

    def test_category_analysis(self):
        result = category_analysis(self.expenses)

        self.assertEqual(result["Food"], 550)
        self.assertEqual(result["Transport"], 100)
        self.assertEqual(result["Entertainment"], 500)

    def test_highest_category(self):
        categories = category_analysis(self.expenses)

        result = find_highest_category(categories)

        self.assertEqual(result, "Food")

    def test_transaction_count(self):
        self.assertEqual(count_transactions(self.expenses), 4)


if __name__ == "__main__":
    unittest.main()