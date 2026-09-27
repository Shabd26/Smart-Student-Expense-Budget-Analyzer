"""Functions for managing financial goals."""

from pathlib import Path

from utils.file_handler import load_json, save_json
from utils.validation import validate_amount


GOALS_FILE = Path(__file__).resolve().parents[1] / "data" / "goals.json"


def load_goals(storage_path=GOALS_FILE):
    goals = load_json(storage_path, [])

    if not isinstance(goals, list):
        raise ValueError("Goals storage must contain a list.")

    return goals


def get_next_id(goals):
    highest_id = 0

    for goal in goals:
        if goal.get("id", 0) > highest_id:
            highest_id = goal.get("id", 0)

    return highest_id + 1


def create_goal(name, target, storage_path=GOALS_FILE):
    name = str(name).strip()

    if not name:
        raise ValueError("Goal name cannot be empty.")

    target = validate_amount(target)

    goals = load_goals(storage_path)

    new_goal = {
        "id": get_next_id(goals),
        "name": name,
        "target": target,
        "saved": 0.0
    }

    goals.append(new_goal)

    save_json(storage_path, goals)

    return new_goal


def view_goals(storage_path=GOALS_FILE):
    return load_goals(storage_path)


def update_saved_amount(goal_id, saved_amount, storage_path=GOALS_FILE):
    saved_amount = validate_amount(saved_amount)

    goals = load_goals(storage_path)

    for goal in goals:
        if goal.get("id") == goal_id:
            goal["saved"] = saved_amount

            save_json(storage_path, goals)

            return goal

    return None


def delete_goal(goal_id, storage_path=GOALS_FILE):
    goals = load_goals(storage_path)

    remaining_goals = []

    found = False

    for goal in goals:
        if goal.get("id") == goal_id:
            found = True
        else:
            remaining_goals.append(goal)

    if not found:
        return False

    save_json(storage_path, remaining_goals)

    return True


def calculate_goal_progress(goal):
    target = goal["target"]
    saved = goal["saved"]

    if target <= 0:
        return 0

    progress = (saved / target) * 100

    if progress > 100:
        progress = 100

    return round(progress, 2)


def get_goal_status(goal):
    progress = calculate_goal_progress(goal)

    if progress >= 100:
        return "Completed"

    return "In Progress"