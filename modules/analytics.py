"""Functions used for spending analysis."""


def calculate_total(expenses):
    total = 0

    for expense in expenses:
        total = total + expense["amount"]

    return round(total, 2)


def calculate_average(expenses):
    if len(expenses) == 0:
        return 0

    total = calculate_total(expenses)
    average = total / len(expenses)

    return round(average, 2)


def find_highest_expense(expenses):
    if len(expenses) == 0:
        return None

    highest = expenses[0]

    for expense in expenses:
        if expense["amount"] > highest["amount"]:
            highest = expense

    return highest


def find_lowest_expense(expenses):
    if len(expenses) == 0:
        return None

    lowest = expenses[0]

    for expense in expenses:
        if expense["amount"] < lowest["amount"]:
            lowest = expense

    return lowest


def category_analysis(expenses):
    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category in category_totals:
            category_totals[category] = category_totals[category] + amount
        else:
            category_totals[category] = amount

    return category_totals


def find_highest_category(category_totals):
    if len(category_totals) == 0:
        return None

    highest_category = None
    highest_amount = 0

    for category in category_totals:
        if category_totals[category] > highest_amount:
            highest_amount = category_totals[category]
            highest_category = category

    return highest_category


def count_transactions(expenses):
    return len(expenses)