import sys
from tkinter import filedialog, messagebox
import json
import csv
from typing import List, Dict, Union, Callable
sys.path.append(r"..\..\Concept_project\functional")

# Import the necessary functions
from financial_analysis import get_length

TRANSACTION_FIELDS = ["amount", "category", "type", "date"]
DATABASE_FILE = r"F:\study\level 4\Concept\Concept_project (2)\Concept_project\functional\JSON\transactions.json"
financial_file = r"F:\study\level 4\Concept\Concept_project (2)\Concept_project\functional\JSON\report2.json"

def check_fields(fields: List[str], transaction: Dict[str, Union[str, float]]) -> bool:
    if not fields:
        return True
    head, *tail = fields
    return head in transaction and check_fields(tail, transaction)

def validate_transaction(transaction: Dict[str, Union[str, float]]) -> bool:
    try:
        return (
            check_fields(TRANSACTION_FIELDS, transaction) and
            isinstance(float(transaction["amount"]), float) and
            transaction["type"] in {"Income", "Expense"} and
            isinstance(transaction["category"], str) and
            isinstance(transaction["date"], str)
        )
    except (ValueError, KeyError):
        return False

def load_database(file_path: str) -> List[Dict[str, Union[str, float]]]:
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_database(data: List[Dict[str, Union[str, float]]], file_path: str) -> None:
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

import json
from typing import Callable, List, Dict, Union

def import_from_json(
    file_path: str,
    validate: Callable,
    index: int = 0,
    data: List[Dict[str, Union[str, float]]] = None
) -> List[Dict[str, Union[str, float]]]:
    if data is None:
        data = []

    with open(file_path, "r") as f:
        json_data = json.load(f)

    if index < get_length(json_data):
        entry = json_data[index]
        if validate(entry):
            return import_from_json(file_path, validate, index + 1, data + [entry])
        return import_from_json(file_path, validate, index + 1, data)
    
    return data



def import_from_csv(
    file_path: str,
    validate: Callable,
    index: int = 0,
    data: List[Dict[str, Union[str, float]]] = None
) -> List[Dict[str, Union[str, float]]]:
    if data is None:
        data = []

    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if index < get_length(rows):
        row = rows[index]
        if validate(row):
            return import_from_csv(file_path, validate, index + 1, data + [row])
        return import_from_csv(file_path, validate, index + 1, data)            

    return data



def import_transactions():
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")]
    )
    if not file_path:
        return

    try:
        if file_path.endswith(".json"):
            imported_transactions = import_from_json(file_path, validate_transaction)
        elif file_path.endswith(".csv"):
            imported_transactions = import_from_csv(file_path, validate_transaction)
        else:
            raise ValueError("Unsupported file format.")

        current_transactions = load_database(DATABASE_FILE)
        updated_transactions = current_transactions + imported_transactions
        save_database(updated_transactions, DATABASE_FILE)

        messagebox.showinfo("Import Success", f"Imported {get_length(imported_transactions)} transactions successfully.")
    except Exception as e:
        messagebox.showerror("Import Error", str(e))

def export_transactions():
    transactions = load_database(DATABASE_FILE)
    if not transactions:
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
            save_database(transactions, file_path)
        elif file_path.endswith(".csv"):
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDS)
                writer.writeheader()

                def write_transaction(index: int):
                    if index < get_length(transactions):
                        writer.writerow(transactions[index])
                        write_transaction(index + 1)

                write_transaction(0)
        else:
            raise ValueError("Unsupported file format.")

        messagebox.showinfo("Export Success", f"Exported transactions successfully to {file_path}.")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))

def export_financial():
    transactions = load_database(financial_file)
    if not transactions:
        messagebox.showinfo("Export Error", "No transactions to export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json")]
    )
    if not file_path:
        return

    try:
        if file_path.endswith(".json"):
            save_database(transactions, file_path)
        elif file_path.endswith(".csv"):
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDS)
                writer.writeheader()

                def write_transaction(index: int):
                    if index < get_length(transactions):
                        writer.writerow(transactions[index])
                        write_transaction(index + 1)

                write_transaction(0)
        else:
            raise ValueError("Unsupported file format.")

        messagebox.showinfo("Export Success", f"Exported financial file successfully to {file_path}.")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))
