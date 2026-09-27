"""Functions for generating financial reports."""

from modules.analytics import (
    calculate_total,
    calculate_average,
    find_highest_expense,
    find_lowest_expense,
    category_analysis,
    find_highest_category,
    count_transactions
)

from modules.income_manager import get_income_amount
from modules.expense_manager import view_expenses
from modules.budget_manager import get_budget_status
from modules.goal_manager import view_goals, calculate_goal_progress


def generate_report():
    expenses = view_expenses()

    income = get_income_amount()

    total_spending = calculate_total(expenses)
    average_expense = calculate_average(expenses)

    highest_expense = find_highest_expense(expenses)
    lowest_expense = find_lowest_expense(expenses)

    category_totals = category_analysis(expenses)
    highest_category = find_highest_category(category_totals)

    transaction_count = count_transactions(expenses)

    budget_status = get_budget_status()

    goals = view_goals()

    remaining_money = income - total_spending

    report = {
        "income": income,
        "total_spending": total_spending,
        "remaining_money": round(remaining_money, 2),
        "average_expense": average_expense,
        "highest_expense": highest_expense,
        "lowest_expense": lowest_expense,
        "category_totals": category_totals,
        "highest_category": highest_category,
        "transaction_count": transaction_count,
        "budget_status": budget_status,
        "goals": goals
    }

    return report


def display_report():
    report = generate_report()

    print("\n==============================================")
    print("             FINANCIAL REPORT")
    print("==============================================")

    print("\n===== INCOME & SPENDING =====")
    print("Monthly Income: ₹", report["income"])
    print("Total Spending: ₹", report["total_spending"])
    print("Remaining Money: ₹", report["remaining_money"])
    print("Average Expense: ₹", report["average_expense"])
    print("Transactions:", report["transaction_count"])

    print("\n===== EXPENSE DETAILS =====")

    highest = report["highest_expense"]

    if highest is None:
        print("No expenses available.")
    else:
        print("Highest Expense: ₹", highest["amount"])
        print("Category:", highest["category"])
        print("Description:", highest["description"])
        print("Date:", highest["date"])

    lowest = report["lowest_expense"]

    if lowest is not None:
        print("Lowest Expense: ₹", lowest["amount"])
        print("Category:", lowest["category"])
        print("Description:", lowest["description"])
        print("Date:", lowest["date"])

    print("\n===== CATEGORY ANALYSIS =====")

    if len(report["category_totals"]) == 0:
        print("No category data available.")
    else:
        for category in report["category_totals"]:
            print(
                category,
                ": ₹",
                round(report["category_totals"][category], 2)
            )

        print(
            "Highest Spending Category:",
            report["highest_category"]
        )

    print("\n===== BUDGET STATUS =====")

    budget = report["budget_status"]
    overall_budget = budget["overall"]

    print("Monthly Budget: ₹", overall_budget["budget"])
    print("Monthly Spent: ₹", overall_budget["spent"])
    print("Monthly Remaining: ₹", overall_budget["remaining"])
    print("Budget Status:", overall_budget["status"])

    print("\nCategory Budgets:")

    if len(budget["categories"]) == 0:
        print("No category budgets set.")
    else:
        for category in budget["categories"]:
            category_budget = budget["categories"][category]

            print(
                category,
                "| Budget: ₹", category_budget["budget"],
                "| Spent: ₹", category_budget["spent"],
                "| Remaining: ₹", category_budget["remaining"],
                "| Status:", category_budget["status"]
            )

    print("\n===== FINANCIAL GOALS =====")

    if len(report["goals"]) == 0:
        print("No financial goals available.")
    else:
        for goal in report["goals"]:
            progress = calculate_goal_progress(goal)

            print("Goal:", goal["name"])
            print("Target: ₹", goal["target"])
            print("Saved: ₹", goal["saved"])
            print("Progress:", progress, "%")

            if progress >= 100:
                print("Status: Completed")
            else:
                print("Status: In Progress")

            print()