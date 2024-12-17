import json
from tkinter import Tk, Button, Text, messagebox, simpledialog
from datetime import datetime
from collections import namedtuple
from typing import List, Optional, Callable, Any

SavingsGoal = namedtuple("SavingsGoal", ["name", "target_amount", "target_date", "progress"])

def load_savings_goals(file_path: str) -> List[SavingsGoal]:
    def recursive_load(data):
        if not data:
            return []
        return [SavingsGoal(**data[0])] + recursive_load(data[1:])
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return recursive_load(data)
    except FileNotFoundError:
        return []


def save_data(file_path: str, data: List[SavingsGoal]):
    def convert(data):
        if isinstance(data, SavingsGoal):
            return data._asdict()
        elif isinstance(data, list):
            if not data:
                return []
            return [convert(data[0])] + convert(data[1:])

        return data
    data_dict = convert(data)
    with open(file_path, "w") as file:
        json.dump(data_dict, file, indent=4)

def calculate_monthly_savings(goal: SavingsGoal) -> float:
    target_date = datetime.strptime(goal.target_date, "%Y-%m-%d")
    current_date = datetime.now()
    months_remaining = (target_date.year - current_date.year) * 12 + target_date.month - current_date.month
    if months_remaining <= 0:
        return 0
    return (goal.target_amount - goal.progress) / months_remaining

def collect_savings_goal_input() -> Optional[SavingsGoal]:
    root = Tk()
    root.withdraw()

    name = simpledialog.askstring("Savings Goal Name", "Enter the savings goal name:")
    if not name:
        messagebox.showwarning("Input Error", "Goal name cannot be empty.")
        return None

    try:
        target_amount = simpledialog.askfloat("Target Amount", "Enter the target amount:")
        if target_amount is None or target_amount <= 0:
            raise ValueError("Target amount must be a positive number.")
    except ValueError as e:
        messagebox.showwarning("Input Error", str(e))
        return None

    target_date = simpledialog.askstring("Target Date", "Enter the target date (YYYY-MM-DD):")
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid date format. Please enter in YYYY-MM-DD format.")
        return None

    return SavingsGoal(name, target_amount, target_date, 0)

def add_savings_goal(file_path: str) -> List[SavingsGoal]:
    savings_goals = load_savings_goals(file_path)

    new_goal = collect_savings_goal_input()
    if new_goal is None:
        return savings_goals

    updated_goals = savings_goals + [new_goal]
    save_data(file_path, updated_goals)
    messagebox.showinfo("Success", f"Savings goal '{new_goal.name}' added successfully.")
    return updated_goals

def reset_goal_progress(goal: SavingsGoal) -> SavingsGoal:
    return goal._replace(progress=0)

def reset_all_goal_progress(file_path: str):
    savings_goals = load_savings_goals(file_path)

    def recursive_reset(goals, index=0, length=None):
        if length is None:
            length = get_length(goals)
        if index >= length:
            return goals
        goals[index] = reset_goal_progress(goals[index])
        return recursive_reset(goals, index + 1, length)

    def get_length(goals, index=0):
        try:
            goals[index]
            return get_length(goals, index + 1)
        except IndexError:
            return index

    updated_goals = recursive_reset(savings_goals)
    save_data(file_path, updated_goals)
    messagebox.showinfo("Success", "All savings goals have been reset to 0 progress.")



def update_goal_progress(goal: SavingsGoal, progress_update: float) -> Optional[SavingsGoal]:
    new_progress = goal.progress + progress_update
    if new_progress > goal.target_amount or progress_update < 0:
        return None

    return goal._replace(progress=new_progress)

def update_savings_goal_progress(file_path: str):
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

    def recursive_update(goals, index, length):
        if index >= length:
            return goals
        goal = goals[index]
        if goal.name == goal_name:
            updated_goal = update_goal_progress(goal, progress_update)
            if updated_goal is None:
                messagebox.showwarning("Update Error", "Invalid progress update. Check the target amount.")
                return None  # Exit if there's an error
            goals[index] = updated_goal
        return recursive_update(goals, index + 1, length)

    def get_length(goals, index=0):
        try:
            goals[index]
            return get_length(goals, index + 1)
        except IndexError:
            return index

    length = get_length(savings_goals)
    updated_savings_goals = recursive_update(savings_goals, 0, length)

    if updated_savings_goals is not None:
        save_data(file_path, updated_savings_goals)
        messagebox.showinfo("Success", f"Progress for '{goal_name}' updated successfully.")


def format_goal(goal: SavingsGoal) -> str:
    monthly_savings = calculate_monthly_savings(goal)
    return (
        f"🎯 {goal.name}: Save {goal.target_amount} by {goal.target_date}. "
        f"Progress: {goal.progress:.2f} (Monthly Savings: {monthly_savings:.2f})"
    )

def view_savings_goals(file_path: str, output_text: Text):
    savings_goals = load_savings_goals(file_path)
    
    def recursive_format(goals, index=0, result=""):
        # Base case: if index is out of range
        if not goals or index >= index_of_last_element(goals):
            return result
        goal_str = format_goal(goals[index])
        return recursive_format(goals, index + 1, result + goal_str + "\n")
    
    def index_of_last_element(goals):
        if not goals:
            return -1
        index = 0
        try:
            while True:
                goals[index]
                index += 1
        except IndexError:
            return index - 1

    if not savings_goals:
        formatted_goals = "No savings goals found."
    else:
        formatted_goals = recursive_format(savings_goals).strip()
    
    output_text.delete(1.0, 'end')
    output_text.insert('end', formatted_goals)


def main_app():
    file_path = "savings_goals.json"

    root = Tk()
    root.title("Savings Goal Tracker")

    output_text = Text(root, height=20, width=80)
    output_text.pack()

    Button(root, text="View All Goals", command=lambda: view_savings_goals(file_path, output_text)).pack()
    Button(root, text="Add Savings Goal", command=lambda: add_savings_goal(file_path)).pack()
    Button(root, text="Update Goal Progress", command=lambda: update_savings_goal_progress(file_path)).pack()
    Button(root, text="Reset All Progress", command=lambda: reset_all_goal_progress(file_path)).pack()

    root.mainloop()

if __name__ == "__main__":
    main_app()
