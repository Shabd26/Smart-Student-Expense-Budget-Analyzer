import tempfile
import unittest

from pathlib import Path

from modules.goal_manager import (
    create_goal,
    view_goals,
    update_saved_amount,
    delete_goal,
    calculate_goal_progress,
    get_goal_status
)


class GoalManagerTests(unittest.TestCase):

    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.goals_path = Path(
            self.temporary_directory.name
        ) / "goals.json"

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_create_goal(self):
        goal = create_goal(
            "New Laptop",
            70000,
            self.goals_path
        )

        self.assertEqual(goal["id"], 1)
        self.assertEqual(goal["name"], "New Laptop")
        self.assertEqual(goal["target"], 70000)
        self.assertEqual(goal["saved"], 0)

    def test_view_goals(self):
        create_goal(
            "New Laptop",
            70000,
            self.goals_path
        )

        goals = view_goals(self.goals_path)

        self.assertEqual(len(goals), 1)

    def test_update_saved_amount(self):
        goal = create_goal(
            "New Laptop",
            70000,
            self.goals_path
        )

        updated_goal = update_saved_amount(
            goal["id"],
            28000,
            self.goals_path
        )

        self.assertEqual(
            updated_goal["saved"],
            28000
        )

    def test_goal_progress(self):
        goal = {
            "target": 70000,
            "saved": 28000
        }

        progress = calculate_goal_progress(goal)

        self.assertEqual(progress, 40)

    def test_completed_goal(self):
        goal = {
            "target": 50000,
            "saved": 50000
        }

        self.assertEqual(
            get_goal_status(goal),
            "Completed"
        )

    def test_delete_goal(self):
        goal = create_goal(
            "New Laptop",
            70000,
            self.goals_path
        )

        result = delete_goal(
            goal["id"],
            self.goals_path
        )

        self.assertTrue(result)

        goals = view_goals(self.goals_path)

        self.assertEqual(len(goals), 0)


if __name__ == "__main__":
    unittest.main()