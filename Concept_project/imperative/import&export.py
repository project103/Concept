import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv

TRANSACTION_FIELDS = ["amount", "category", "type", "date"]
DATABASE_FILE = "F:/study/level 4/Concept/project/imperative/JSON/transactions.json"

current_transactions = []

def load_database():
    global current_transactions
    try:
        with open(DATABASE_FILE, "r") as f:
            current_transactions = json.load(f)
    except FileNotFoundError:
        current_transactions = []

def save_database():
    global current_transactions
    with open(DATABASE_FILE, "w") as f:
        json.dump(current_transactions, f, indent=4)

def check_fields_with_loop(fields, transaction):
    for field in fields:
        if field not in transaction:
            return False
    return True

def validate_transaction(transaction):
    try:
        if not check_fields_with_loop(TRANSACTION_FIELDS, transaction):
            return False

        try:
            amount = float(transaction["amount"])
        except ValueError:
            return False

        if transaction["type"] not in {"Income", "Expense"}:
            return False

        if not isinstance(transaction["category"], str):
            return False

        if not isinstance(transaction["date"], str):
            return False

        return True
    except KeyError:
        return False

def import_from_json(file_path):
    valid_entries = []
    with open(file_path, "r") as f:
        data = json.load(f)
        for entry in data:
            if validate_transaction(entry):
                valid_entries.append(entry)
    return valid_entries

def import_from_csv(file_path):
    valid_entries = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["amount"] = float(row["amount"])
            except (ValueError, KeyError):
                continue

            if validate_transaction(row):
                valid_entries.append(row)
    return valid_entries

def import_transactions():
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")]
    )
    if not file_path:
        return

    try:
        if file_path.endswith(".json"):
            imported_transactions = import_from_json(file_path)
        elif file_path.endswith(".csv"):
            imported_transactions = import_from_csv(file_path)
        else:
            raise ValueError("Unsupported file format.")

        global current_transactions
        current_transactions.extend(imported_transactions)

        save_database()

        messagebox.showinfo("Import Success", f"Imported {len(imported_transactions)} transactions successfully.")
    except Exception as e:
        messagebox.showerror("Import Error", str(e))

def export_transactions():
    global current_transactions
    if not current_transactions:
        messagebox.showinfo("Export Error", "No transactions to export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")]
    )
    if not file_path:
        return

    try:
        if file_path.endswith(".json"):
            with open(file_path, "w") as f:
                json.dump(current_transactions, f, indent=4)
            messagebox.showinfo("Export Success", f"Exported transactions successfully to {file_path}.")
        elif file_path.endswith(".csv"):
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDS)
                writer.writeheader()
                for transaction in current_transactions:
                    row = {field: transaction.get(field, "") for field in TRANSACTION_FIELDS}
                    writer.writerow(row)

            messagebox.showinfo("Export Success", f"Exported transactions successfully to {file_path}.")
        else:
            raise ValueError("Unsupported file format.")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))

def create_gui():
    load_database()

    root = tk.Tk()
    root.title("Transaction Manager")

    tk.Label(root, text="Manage Transactions with JSON Database").pack(pady=10)

    tk.Button(root, text="Import Transactions", command=import_transactions).pack(pady=5)
    tk.Button(root, text="Export Transactions", command=export_transactions).pack(pady=5)
    tk.Button(root, text="Quit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
