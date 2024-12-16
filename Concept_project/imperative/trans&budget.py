import json
from tkinter import Label, Tk, Button, Text, messagebox, simpledialog
from tkinter.ttk import Combobox
from datetime import datetime

TransactionType = {"INCOME": "Income", "EXPENSE": "Expense"}
Category = {
    "FOOD": "Food",
    "RENT": "Rent",
    "ENTERTAINMENT": "Entertainment",
    "OTHER": "Other",
    "SALARY": "Salary"
}
PREDEFINED_CATEGORIES = [
    Category["FOOD"],
    Category["RENT"],
    Category["ENTERTAINMENT"],
    Category["OTHER"],
    Category["SALARY"],
]

transaction_file_path = "F:/study/level 4/Concept/project/functional/JSON/transactions.json"
budget_file_path = "F:/study/level 4/Concept/project/functional/JSON/budget_db.json"

try:
    with open(transaction_file_path, "r") as file:
        transactions = json.load(file)
except FileNotFoundError:
    transactions = []

try:
    with open(budget_file_path, "r") as file:
        budgets = json.load(file)
except FileNotFoundError:
    budgets = []


root = Tk()
root.title("Transaction and Budget Manager")

output_text = Text(root, width=70, height=15, wrap="word", font=("Arial", 10))
output_text.pack(padx=10, pady=10)

def view_all_transactions():
    if not transactions:
        output_text.delete(1.0, "end")
        output_text.insert("end", "No transactions found.")
        return

    output_text.delete(1.0, "end")
    for transaction in transactions:
        output_text.insert("end", f"{transaction['category']} | {transaction['amount']} | {transaction['type']} | {transaction['date']}\n")

def view_all_budgets():
    if not budgets:
        output_text.delete(1.0, "end")
        output_text.insert("end", "No budgets found.")
        return

    output_text.delete(1.0, "end")
    for budget in budgets:
        output_text.insert("end", f"Category: {budget['category']}, Month: {budget['month']}, Limit: {budget['limit']}, Spent: {budget['spent']}\n")

def add_transaction():
    transaction_type = simpledialog.askstring(
        "Transaction Type",
        "Select the transaction type:\n1. Income\n2. Expense",
    )

    if transaction_type == "1":
        transaction_type = TransactionType["INCOME"]
        category = "Salary"  
    elif transaction_type == "2":
        transaction_type = TransactionType["EXPENSE"]
        category = simpledialog.askstring(
            "Transaction Category",
            f"Select a category from the following:\n{', '.join(PREDEFINED_CATEGORIES)}",
        )
        if category not in PREDEFINED_CATEGORIES:
            messagebox.showwarning("Input Error", "Please select a valid category.")
            return
    else:
        messagebox.showwarning("Input Error", "Invalid selection. Please select 1 for Income or 2 for Expense.")
        return

    try:
        # Ask for the amount
        amount = simpledialog.askfloat("Amount", "Enter the transaction amount:")
        if amount is None or amount <= 0:
            raise ValueError("Amount must be a positive number.")
    except ValueError as e:
        messagebox.showwarning("Input Error", str(e))
        return

    # Ask for the transaction date
    date = simpledialog.askstring("Transaction Date", "Enter the transaction date (YYYY-MM-DD):")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid date format. Please enter in YYYY-MM-DD format.")
        return

    # Add the new transaction
    new_transaction = {"category": category, "amount": amount, "type": transaction_type, "date": date}
    transactions.append(new_transaction)

    # Update budgets for expenses
    if transaction_type == TransactionType["EXPENSE"]:
        for budget in budgets:
            if budget["category"] == category:
                new_spent = budget["spent"] + amount
                if new_spent > budget["limit"] * 80 / 100:
                    messagebox.showwarning(
                        "Spending Limit Exceeded",
                        f"You are nearing the spending limit for {category}. "
                        f"Your budget limit is {budget['limit']} and you are trying to spend {new_spent}."
                    )
                budget["spent"] = new_spent

    # Save updated data to file
    with open(transaction_file_path, "w") as file:
        json.dump(transactions, file, indent=4)
    with open(budget_file_path, "w") as file:
        json.dump(budgets, file, indent=4)

    # Provide feedback to the user
    output_text.delete(1.0, "end")
    output_text.insert("end", "Transaction added and budget updated successfully.")

# Update or add budget spending
def add_budget_spending():
    # Show existing categories to the user
    existing_categories = [budget["category"] for budget in budgets]
    categories_text = "Existing categories: " + ", ".join(existing_categories) if existing_categories else "No existing categories."

    category = simpledialog.askstring("Budget Category", f"{categories_text}\n\nEnter the category to add or update budget:")
    if not category:
        messagebox.showwarning("Input Error", "Category cannot be empty.")
        return

    try:
        amount = simpledialog.askfloat("Amount", "Enter the budget amount:")
        if amount is None or amount <= 0:
            raise ValueError("Amount must be a positive number.")
    except ValueError as e:
        messagebox.showwarning("Input Error", str(e))
        return

    # Check if the category exists in the budgets list
    category_found = False
    for budget in budgets:
        if budget["category"] == category:
            budget["limit"] = amount  # Update the budget limit for the existing category
            budget["spent"] = budget.get("spent", 0)  # Ensure "spent" is initialized
            category_found = True
            break

    # If the category does not exist, add a new budget entry
    if not category_found:
        new_budget = {
            "category": category,
            "limit": amount,
            "spent": 0
        }
        budgets.append(new_budget)

    # Save updated budgets to the file
    with open(budget_file_path, "w") as file:
        json.dump(budgets, file, indent=4)

    output_text.delete(1.0, "end")
    if category_found:
        output_text.insert("end", f"Budget for category '{category}' updated successfully.")
    else:
        output_text.insert("end", f"New budget for category '{category}' added successfully.")



# Create the main UI
Button(
    root, text="View All Transactions", command=view_all_transactions
).pack(padx=10, pady=5)

Button(
    root, text="View All Budgets", command=view_all_budgets
).pack(padx=10, pady=5)

Button(
    root, text="Add Transaction", command=add_transaction
).pack(padx=10, pady=5)

Button(
    root, text="Update or add Budget Spending", command=add_budget_spending
).pack(padx=10, pady=5)

root.mainloop()
