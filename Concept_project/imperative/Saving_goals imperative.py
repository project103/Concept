import json
from tkinter import Tk, Button, Text, messagebox, simpledialog
from datetime import datetime
from typing import List, Dict

def load_savings_goals(file_path: str) -> List[Dict]:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(file_path: str, data: List[Dict]):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def calculate_monthly_savings(goal: Dict) -> float:
    try:
        target_date = datetime.strptime(goal["target_date"], "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please enter in YYYY-MM-DD format.")
    
    current_date = datetime.now()

    if target_date <= current_date:
        raise ValueError("Target date must be in the future.")
    
    remaining_amount = goal["target_amount"] - goal["progress"]
    
    if remaining_amount <= 0:
        return 0
    
    months_remaining = (target_date.year - current_date.year) * 12 + target_date.month - current_date.month

    if months_remaining <= 0:
        return 0

    monthly_savings = remaining_amount / months_remaining

    return monthly_savings

def add_savings_goal(file_path: str):
    name = simpledialog.askstring("Savings Goal Name", "Enter the savings goal name:")
    if not name:
        messagebox.showwarning("Input Error", "Goal name cannot be empty.")
        return

    try:
        target_amount = simpledialog.askfloat("Target Amount", "Enter the target amount:")
        if target_amount is None or target_amount <= 0:
            raise ValueError("Target amount must be a positive number.")
    except ValueError as e:
        messagebox.showwarning("Input Error", str(e))
        return

    target_date = simpledialog.askstring("Target Date", "Enter the target date (YYYY-MM-DD):")
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid date format. Please enter in YYYY-MM-DD format.")
        return

    try:
        goal = {"name": name, "target_amount": target_amount, "target_date": target_date, "progress": 0}
        monthly_savings = calculate_monthly_savings(goal)
        
        if monthly_savings == 0:
            messagebox.showinfo("Information", "You do not have enough time to save for this goal or the goal is already complete.")
            return

        monthly_savings_message = f"To achieve this goal, you need to save {monthly_savings:.2f} per month."
        proceed = messagebox.askyesno("Monthly Savings", monthly_savings_message + "\nDo you want to proceed with adding this goal?")
        
        if not proceed:
            return

    except ValueError as e:
        messagebox.showwarning("Error", str(e))
        return

    savings_goals = load_savings_goals(file_path)
    savings_goals.append(goal)
    save_data(file_path, savings_goals)
    messagebox.showinfo("Success", f"Savings goal '{goal['name']}' added successfully.")

def view_savings_goal(file_path: str, output_text: Text):
    goal_name = simpledialog.askstring("View Savings Goal", "Enter the name of the goal to view:")
    if not goal_name:
        messagebox.showwarning("Input Error", "Goal name cannot be empty.")
        return

    savings_goals = load_savings_goals(file_path)
    goal_data = None
    for goal in savings_goals:
        if goal["name"] == goal_name:
            goal_data = goal
            break

    if goal_data:
        monthly_savings = calculate_monthly_savings(goal_data)
        goal_output = (
            f"Goal: {goal_data['name']} | Target: {goal_data['target_amount']} | "
            f"Progress: {goal_data['progress']} | Monthly Savings Required: {monthly_savings:.2f} | "
            f"Target Date: {goal_data['target_date']}\n"
        )
        output_text.delete(1.0, 'end')
        output_text.insert('end', goal_output)
    else:
        messagebox.showwarning("Goal Not Found", f"No goal found with the name '{goal_name}'.")

def update_goal_progress(file_path: str):
    goal_name = simpledialog.askstring("Update Progress", "Enter the name of the goal to update progress:")
    if not goal_name:
        messagebox.showwarning("Input Error", "Goal name cannot be empty.")
        return

    try:
        progress_update = simpledialog.askfloat("Progress Update", "Enter the amount to add to the progress:")
        if progress_update is None or progress_update < 0:
            raise ValueError("Progress update must be a positive number.")
    except ValueError as e:
        messagebox.showwarning("Input Error", str(e))
        return

    savings_goals = load_savings_goals(file_path)
    updated_goals = []
    goal_found = False

    for goal in savings_goals:
        if goal["name"] == goal_name:
            new_progress = goal["progress"] + progress_update
            if new_progress > goal["target_amount"] or progress_update < 0:
                messagebox.showwarning("Update Error", "Invalid progress update. Check the target amount.")
                return
            goal["progress"] = new_progress
            goal_found = True
        updated_goals.append(goal)

    if goal_found:
        save_data(file_path, updated_goals)
        messagebox.showinfo("Success", f"Progress for '{goal_name}' updated successfully.")
    else:
        messagebox.showwarning("Goal Not Found", f"No goal found with the name '{goal_name}'.")

def format_single_goal(goal: Dict) -> str:
    monthly_savings = calculate_monthly_savings(goal)
    return (
        f"Goal: {goal['name']} | Target: {goal['target_amount']} | "
        f"Progress: {goal['progress']} | Monthly Savings Required: {monthly_savings:.2f} | "
        f"Target Date: {goal['target_date']}"
    )

def view_all_savings_goals(file_path: str, output_text: Text):
    savings_goals = load_savings_goals(file_path)

    if not savings_goals:
        output_text.delete(1.0, 'end')
        output_text.insert('end', "No savings goals found.")
        return

    all_goals_output = ""
    for goal in savings_goals:
        all_goals_output += format_single_goal(goal) + "\n"

    output_text.delete(1.0, 'end')
    output_text.insert('end', all_goals_output)

root = Tk()
root.title("Savings Goals Viewer")

output_text = Text(root, width=70, height=15, wrap="word", font=("Arial", 10))
output_text.pack(padx=10, pady=10)

view_all_button = Button(root, text="View All Goals", command=lambda: view_all_savings_goals("F:/study/level 4/Concept/project/functional/JSON/savings_goal.json", output_text))
view_all_button.pack(padx=10, pady=10)

update_Goal = Button(root, text="Update Goal", command=lambda: update_goal_progress("F:/study/level 4/Concept/project/functional/JSON/savings_goal.json"))
update_Goal.pack(padx=15, pady=20)

add_Goal = Button(root, text="Add Goal", command=lambda: add_savings_goal("F:/study/level 4/Concept/project/functional/JSON/savings_goal.json"))
add_Goal.pack(padx=20, pady=20)

root.mainloop()
