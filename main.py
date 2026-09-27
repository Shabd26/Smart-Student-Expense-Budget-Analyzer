from modules.expense_manager import add_expense, view_expenses, search_expenses, filter_by_category, edit_expense, delete_expense
from modules.budget_manager import set_monthly_budget, set_category_budget, get_budget_status, check_budget_limits
from modules.analytics import calculate_total, calculate_average, find_highest_expense, find_lowest_expense, category_analysis, find_highest_category, count_transactions
from modules.goal_manager import create_goal, view_goals, update_saved_amount, delete_goal, calculate_goal_progress, get_goal_status
from modules.income_manager import get_income_amount, set_income
from modules.report_generator import display_report


def show_expenses(expenses):
    if len(expenses) == 0:
        print("\nNo expenses found.")
    else:
        for e in expenses:
            print("ID:", e["id"], "| Amount: ₹", e["amount"], "| Category:", e["category"], "| Description:", e["description"], "| Date:", e["date"])


def expense_menu():
    while True:
        print("\n===== EXPENSE MANAGEMENT =====")
        print("1. Add Expense\n2. View Expenses\n3. Search Expenses\n4. Filter by Category\n5. Edit Expense\n6. Delete Expense\n0. Back")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                amount = float(input("Enter amount: ₹"))
                e = add_expense(amount, input("Enter category: "), input("Enter description: "), input("Enter date (YYYY-MM-DD): "))
                print("\nExpense added successfully! ID:", e["id"])
            elif choice == "2":
                show_expenses(view_expenses())
            elif choice == "3":
                show_expenses(search_expenses(input("Enter search keyword: ")))
            elif choice == "4":
                show_expenses(filter_by_category(input("Enter category: ")))
            elif choice == "5":
                i = int(input("Enter expense ID: "))
                e = edit_expense(i, float(input("Enter new amount: ₹")), input("Enter new category: "), input("Enter new description: "), input("Enter new date (YYYY-MM-DD): "))
                print("\nExpense " + ("updated successfully!" if e else "not found."))
            elif choice == "6":
                e = delete_expense(int(input("Enter expense ID: ")))
                print("\nExpense " + ("deleted successfully." if e else "not found."))
            elif choice == "0":
                break
            else:
                print("\nInvalid choice.")
        except ValueError as error:
            print("\nError:", error)


def budget_menu():
    while True:
        print("\n===== BUDGET MANAGEMENT =====")
        print("1. Set Monthly Budget\n2. Set Category Budget\n3. View Budget Status\n4. Check Budget Limits\n0. Back")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                budget = set_monthly_budget(float(input("Enter monthly budget: ₹")))
                print("\nMonthly budget set: ₹", budget)
            elif choice == "2":
                category = input("Enter category: ")
                budget = set_category_budget(category, float(input("Enter category budget: ₹")))
                print("\nCategory budget set:", budget["category"], "₹", budget["amount"])
            elif choice == "3":
                s = get_budget_status()
                o = s["overall"]
                print("\n===== BUDGET STATUS =====")
                print("Monthly Budget: ₹", o["budget"], "\nMonthly Spent: ₹", o["spent"], "\nMonthly Remaining: ₹", o["remaining"])
                for category in s["categories"]:
                    d = s["categories"][category]
                    print(category, "| Budget: ₹", d["budget"], "| Spent: ₹", d["spent"], "| Remaining: ₹", d["remaining"], "| Status:", d["status"])
            elif choice == "4":
                warnings = check_budget_limits()
                if len(warnings) == 0:
                    print("\nNo budget limits exceeded.")
                else:
                    for warning in warnings:
                        print(warning)
            elif choice == "0":
                break
            else:
                print("\nInvalid choice.")
        except ValueError as error:
            print("\nError:", error)


def analytics_menu():
    while True:
        print("\n===== SPENDING ANALYTICS =====")
        print("1. Total Spending\n2. Average Expense\n3. Highest Expense\n4. Lowest Expense\n5. Category Analysis\n6. Highest Spending Category\n7. Number of Transactions\n0. Back")
        choice = input("Enter your choice: ")
        try:
            expenses = view_expenses()
            if choice == "1":
                print("\nTotal Spending: ₹", calculate_total(expenses))
            elif choice == "2":
                print("\nAverage Expense: ₹", calculate_average(expenses))
            elif choice == "3":
                e = find_highest_expense(expenses)
                if e is None:
                    print("\nNo expenses available.")
                else:
                    print("\nHighest Expense: ₹", e["amount"], "\nCategory:", e["category"], "\nDescription:", e["description"], "\nDate:", e["date"])
            elif choice == "4":
                e = find_lowest_expense(expenses)
                if e is None:
                    print("\nNo expenses available.")
                else:
                    print("\nLowest Expense: ₹", e["amount"], "\nCategory:", e["category"], "\nDescription:", e["description"], "\nDate:", e["date"])
            elif choice == "5":
                a = category_analysis(expenses)
                if len(a) == 0:
                    print("\nNo expenses available.")
                else:
                    for category in a:
                        print(category, ": ₹", round(a[category], 2))
            elif choice == "6":
                a = category_analysis(expenses)
                category = find_highest_category(a)
                if category is None:
                    print("\nNo expenses available.")
                else:
                    print("\nHighest Spending Category:", category, "₹", round(a[category], 2))
            elif choice == "7":
                print("\nNumber of Transactions:", count_transactions(expenses))
            elif choice == "0":
                break
            else:
                print("\nInvalid choice.")
        except ValueError as error:
            print("\nError:", error)


def goals_menu():
    while True:
        print("\n===== FINANCIAL GOALS =====")
        print("1. Create Goal\n2. View Goals\n3. Update Saved Amount\n4. Delete Goal\n0. Back")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                goal = create_goal(input("Enter goal name: "), float(input("Enter target amount: ₹")))
                print("\nGoal created successfully! ID:", goal["id"])
            elif choice == "2":
                goals = view_goals()
                if len(goals) == 0:
                    print("\nNo financial goals found.")
                else:
                    for g in goals:
                        print("\nID:", g["id"], "|", g["name"], "| Target: ₹", g["target"], "| Saved: ₹", g["saved"])
                        print("Progress:", calculate_goal_progress(g), "% | Status:", get_goal_status(g))
            elif choice == "3":
                goal = update_saved_amount(int(input("Enter goal ID: ")), float(input("Enter total saved amount: ₹")))
                if goal is None:
                    print("\nGoal not found.")
                else:
                    print("\nSaved amount updated! Progress:", calculate_goal_progress(goal), "%")
            elif choice == "4":
                deleted = delete_goal(int(input("Enter goal ID: ")))
                print("\nGoal " + ("deleted successfully." if deleted else "not found."))
            elif choice == "0":
                break
            else:
                print("\nInvalid choice.")
        except ValueError as error:
            print("\nError:", error)


def income_menu():
    while True:
        print("\n===== INCOME MANAGEMENT =====")
        print("1. Set Monthly Income\n2. View Monthly Income\n0. Back")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                income = set_income(float(input("Enter monthly income: ₹")))
                print("\nMonthly income: ₹", income["amount"])
            elif choice == "2":
                print("\nMonthly Income: ₹", get_income_amount())
            elif choice == "0":
                break
            else:
                print("\nInvalid choice.")
        except ValueError as error:
            print("\nError:", error)


def main():
    while True:
        print("\n==============================================")
        print("SMART STUDENT EXPENSE & BUDGET ANALYZER")
        print("==============================================")
        print("1. Manage Expenses\n2. Manage Budget\n3. Spending Analytics\n4. Financial Goals\n5. Income Management\n6. Financial Report\n7. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            expense_menu()
        elif choice == "2":
            budget_menu()
        elif choice == "3":
            analytics_menu()
        elif choice == "4":
            goals_menu()
        elif choice == "5":
            income_menu()
        elif choice == "6":
            display_report()
        elif choice == "7":
            print("\nThank you for using the Smart Student Expense & Budget Analyzer!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram stopped.")
