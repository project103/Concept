import json
from tkinter import Label, Tk, Button, Text, messagebox, simpledialog
from tkinter.ttk import Combobox
from datetime import datetime
from typing import List, Dict, Any

# Define constants for TransactionType and Category
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


def load_data(file_path: str) -> List[Dict[str, Any]]:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_data(file_path: str, data: List[Dict[str, Any]]):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def add_transaction(
    category: str, amount: float, type: str, date: str, transactions: List[Dict[str, Any]], budgets: List[Dict[str, Any]]
) -> (List[Dict[str, Any]], List[Dict[str, Any]]):  # type: ignore
    new_transaction = {"category": category, "amount": amount, "type": type, "date": date}
    updated_transactions = transactions + [new_transaction]

    # Update budget dynamically
    if type == TransactionType["EXPENSE"]:
        updated_budgets = update_budget(category, amount, budgets)
    else:
        updated_budgets = budgets

    return updated_transactions, updated_budgets


def update_budget(category: str, amount: float, budgets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Update the budget for a specific category in a functional style."""
    def update_budget_item(budget_item: Dict[str, Any]) -> Dict[str, Any]:
        if budget_item["category"] == category:
            new_spent = budget_item["spent"] + amount
            if new_spent > budget_item["limit"]:
                messagebox.showwarning(
                    "Spending Limit Exceeded",
                    f"You have exceeded the spending limit for {category}. "
                    f"Your budget limit is {budget_item['limit']} and you are trying to spend {new_spent}."
                )
            # Return the updated budget item with the new 'spent' value
            return {**budget_item, "spent": new_spent}
        return budget_item

    # Create a new list by mapping the update function over the budgets
    return list(map(update_budget_item, budgets))
def update_budget_limit(category: str, amount: float, budgets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Update the budget for a specific category in a functional style."""
    def update_budget_item(budget_item: Dict[str, Any]) -> Dict[str, Any]:
        if budget_item["category"] == category:
            new_spent =  amount

            # Return the updated budget item with the new 'spent' value
            return {**budget_item, "limit": new_spent}
        return budget_item

    # Create a new list by mapping the update function over the budgets
    return list(map(update_budget_item, budgets))

# do date parsing
def parse_date(date_str, formats=None):
    if formats is None:
        formats = ["%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"]
    
    if not formats:
        return None
    
    try:
        return datetime.strptime(date_str, formats[0])
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return parse_date(date_str, formats[1:])

def format_transactions(transactions: List[Dict[str, Any]]) -> str:
    if not transactions:
        return ""
    
    transaction = transactions[0]
    formatted_transaction = f"{transaction['category']} | {transaction['amount']} | {transaction['type']} | {parse_date(transaction['date']).strftime('%d/%m/%Y')}"
    
    return formatted_transaction + "\n" + format_transactions(transactions[1:])

def format_budgets(budgets: List[Dict[str, Any]], result: str = "") -> str:
    if not budgets:
        return result.strip()
    
    budget = budgets[0]
    formatted_budget = f"Category: {budget['category']}, Month: {budget['month']}, Limit: {budget['limit']}, Spent: {budget['spent']}"
    
    return format_budgets(budgets[1:], result + formatted_budget + "\n")


# GUI interaction functions
def handle_add_transaction(transaction_file_path: str, budget_file_path: str, output_text: Text):
    category_window = Tk()
    category_window.title("Select Transaction Category")

    category_label = Label(category_window, text="Select a category:")
    category_label.pack(pady=5)

    category_combobox = Combobox(category_window, values=PREDEFINED_CATEGORIES)
    category_combobox.pack(pady=5)
    category_combobox.set("Select Category")

    def submit_category():
        category = category_combobox.get()
        if category not in PREDEFINED_CATEGORIES:
            messagebox.showwarning("Input Error", "Please select a valid category.")
            category_window.destroy()
            return

        try:
            amount = simpledialog.askfloat("Amount", "Enter the transaction amount:")
            if amount is None or amount <= 0:
                raise ValueError("Amount must be a positive number.")
        except ValueError as e:
            messagebox.showwarning("Input Error", str(e))
            category_window.destroy()
            return

        type = simpledialog.askstring("Transaction Type", "Enter the transaction type (Income/Expense):")
        if type not in [TransactionType["INCOME"], TransactionType["EXPENSE"]]:
            messagebox.showwarning("Input Error", "Invalid transaction type.")
            category_window.destroy()
            return

        date = simpledialog.askstring("Transaction Date", "Enter the transaction date (YYYY-MM-DD):")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid date format. Please enter in YYYY-MM-DD format.")
            category_window.destroy()
            return

        # Load existing data
        transaction_data = load_data(transaction_file_path)
        budget_data = load_data(budget_file_path)

        transactions = transaction_data
        budgets = budget_data

        # Add transaction and dynamically update budgets
        updated_transactions, updated_budgets = add_transaction(
            category, amount, type, date, transactions, budgets
        )

        # Save updated data
        save_data(transaction_file_path, updated_transactions)
        save_data(budget_file_path, updated_budgets)

        output_text.delete(1.0, "end")
        output_text.insert("end", "Transaction added and budget updated successfully.")
        category_window.destroy()

    submit_button = Button(category_window, text="Submit", command=submit_category)
    submit_button.pack(pady=5)
    category_window.mainloop()


def handle_view_all_transactions(transaction_file_path: str, output_text: Text):
    data = load_data(transaction_file_path)

    if not data:
        output_text.delete(1.0, "end")
        output_text.insert("end", "No transactions found.")
        return

    output_text.delete(1.0, "end")
    output_text.insert("end", format_transactions(data))


def handle_update_budget(budget_file_path: str, output_text: Text):
    category = simpledialog.askstring("Budget Category", "Enter the budget category to update:")
    if not category:
        messagebox.showwarning("Input Error", "Category cannot be empty.")
        return

    try:
        amount = simpledialog.askfloat("Amount", "Enter the spending amount:")
        if amount is None or amount <= 0:
            raise ValueError("Amount must be a positive number.")
    except ValueError as e:
        messagebox.showwarning("Input Error", str(e))
        return

    data = load_data(budget_file_path)
    updated_budgets = update_budget_limit(category, amount, data)
    save_data(budget_file_path, updated_budgets)

    output_text.delete(1.0, "end")
    output_text.insert("end", "Budget updated successfully.")


def handle_view_all_budgets(budget_file_path: str, output_text: Text):
    data = load_data(budget_file_path)

    if not data:
        output_text.delete(1.0, "end")
        output_text.insert("end", "No budgets found.")
        return

    output_text.delete(1.0, "end")
    output_text.insert("end", format_budgets(data))


