# Smart Student Expense & Budget Analyzer

## Overview

The Smart Student Expense & Budget Analyzer is a Python-based command-line application designed to help students manage their personal finances.

The application allows users to record expenses, create budgets, analyze spending patterns, manage financial goals, record monthly income, and generate a financial report.

The project uses JSON files for local data storage and Python's built-in `unittest` framework for testing.

## Features

### Expense Management

- Add expenses
- View all expenses
- Search expenses
- Filter expenses by category
- Edit expenses
- Delete expenses

### Budget Management

- Set monthly budget
- Set category-wise budgets
- View budget status
- Check budget limits and warnings

### Spending Analytics

- Calculate total spending
- Calculate average expense
- Find highest expense
- Find lowest expense
- Analyze spending by category
- Find highest spending category
- Count transactions

### Financial Goals

- Create financial goals
- View financial goals
- Update saved amount
- Track goal progress
- Delete goals

### Income Management

- Set monthly income
- View monthly income

### Financial Reports

The application generates a combined financial report containing:

- Monthly income
- Total spending
- Remaining money
- Average expense
- Highest and lowest expenses
- Category-wise spending
- Highest spending category
- Transaction count
- Budget status
- Financial goal progress

## Technologies Used

- Python
- JSON
- Python `unittest`
- Command Line Interface (CLI)

No external Python packages are required.

## Project Structure

```text
Project Vityarthi/
│
├── main.py
├── README.md
├── statement.md
│
├── data/
│   ├── budget.json
│   ├── expenses.json
│   ├── goals.json
│   └── income.json
│
├── modules/
│   ├── __init__.py
│   ├── expense_manager.py
│   ├── budget_manager.py
│   ├── analytics.py
│   ├── goal_manager.py
│   ├── income_manager.py
│   └── report_generator.py
│
├── utils/
│   ├── __init__.py
│   ├── file_handler.py
│   ├── validation.py
│   └── helpers.py
│
└── tests/
    ├── __init__.py
    ├── test_expenses.py
    ├── test_budget.py
    ├── test_analytics.py
    ├── test_goals.py
    ├── test_income.py
    └── test_report.py