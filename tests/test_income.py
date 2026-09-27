import tempfile
import unittest
from pathlib import Path

from modules.income_manager import (
    get_income,
    set_income,
    get_income_amount
)


class TestIncomeManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.income_file = Path(self.temp_dir.name) / "income.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_set_income(self):
        income = set_income(25000, self.income_file)

        self.assertEqual(income["amount"], 25000)

    def test_get_income(self):
        set_income(30000, self.income_file)

        income = get_income(self.income_file)

        self.assertEqual(income["amount"], 30000)

    def test_get_income_amount(self):
        set_income(18000, self.income_file)

        amount = get_income_amount(self.income_file)

        self.assertEqual(amount, 18000)


if __name__ == "__main__":
    unittest.main()