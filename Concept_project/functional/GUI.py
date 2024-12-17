import tkinter as tk
from tkinter import ttk, messagebox
from financial_analysis import (
    load_database_from_file, save_database_to_file, display_transactions,
    sum_spending_for_year, sum_spending_for_day, sum_spending_in_date_range,
    sum_spending_for_month, sum_spending_in_category,
    sum_spending_in_category_and_date_range, generate_spending_insights,
    capture_display_transactions, save_output_to_file
)
from trans_budget import (
    handle_add_transaction, handle_view_all_transactions, handle_view_all_budgets, handle_update_budget
)
from import_export import (
    import_transactions, export_transactions ,export_financial
)
from Saving_goals import (
    add_savings_goal, update_savings_goal_progress, view_savings_goals ,reset_all_goal_progress
)

class FinancialAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Management Tool")

        
        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=("Arial", 10, "bold"),  
                             padding=10,
                             relief="flat",
                             width=25)  

        
        self.style.configure("TNotebook.Tab",
                             font=("Arial", 12, "bold"),
                             padding=[10, 5])  # 
        self.style.map("TNotebook.Tab", 
                       background=[("selected", "#5e81ac")],  
                       foreground=[("selected", "black")],    
                       focuscolor=[("selected", "#5e81ac")])  

        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.transaction_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.transaction_tab, text="Transactions")
        self.setup_transaction_tab()

        self.analysis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_tab, text="Spending Analysis")
        self.setup_analysis_tab()

        self.savings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.savings_tab, text="Savings Goals")
        self.setup_savings_tab()

        self.import_export_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.import_export_tab, text="Import/Export")
        self.setup_import_export_tab()

        self.analysis_output_text = tk.Text(self.analysis_tab, width=100, height=30, wrap="word", font=("Arial", 12))
        self.analysis_output_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.transaction_output_text = tk.Text(self.transaction_tab, width=100, height=20, wrap="word", font=("Arial", 12))
        self.transaction_output_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.savings_output_text = tk.Text(self.savings_tab, width=100, height=20, wrap="word", font=("Arial", 12))
        self.savings_output_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.trans_path = r"F:\study\level 4\Concept\Concept_project (2)\Concept_project\functional\JSON\transactions.json"
        self.budget_path = r"F:\study\level 4\Concept\Concept_project (2)\Concept_project\functional\JSON\budget_db.json"
        self.saving_goal_path = r"F:\study\level 4\Concept\Concept_project (2)\Concept_project\functional\JSON\savings_goal.json"

    def setup_transaction_tab(self):
        ttk.Button(self.transaction_tab, text="View All Transactions", command=lambda: handle_view_all_transactions(self.trans_path, self.transaction_output_text)).pack(pady=15)
        ttk.Button(self.transaction_tab, text="Add Transaction", command=lambda: handle_add_transaction(self.trans_path,self.budget_path, self.transaction_output_text)).pack(pady=15)
        ttk.Button(self.transaction_tab, text="View All Budgets", command=lambda: handle_view_all_budgets(self.budget_path, self.transaction_output_text)).pack(pady=15)
        ttk.Button(self.transaction_tab, text="Update Budget Limit", command=lambda: handle_update_budget(self.budget_path, self.transaction_output_text)).pack(pady=15)

    def setup_analysis_tab(self):
        ttk.Label(self.analysis_tab, text="Enter Year:").pack(pady=10)
        self.year_entry = ttk.Entry(self.analysis_tab, width=30, font=("Arial", 10))  # Larger input field, smaller font
        self.year_entry.pack(pady=10)
        ttk.Button(self.analysis_tab, text="Calculate Yearly Spending", command=self.calculate_yearly_spending).pack(pady=20)

        ttk.Label(self.analysis_tab, text="Enter Date (dd/mm/yyyy):").pack(pady=10)
        self.date_entry = ttk.Entry(self.analysis_tab, width=30, font=("Arial", 10))  # Larger input field, smaller font
        self.date_entry.pack(pady=10)
        ttk.Button(self.analysis_tab, text="Calculate Daily Spending", command=self.calculate_daily_spending).pack(pady=20)

        ttk.Label(self.analysis_tab, text="Enter Month (mm/yyyy):").pack(pady=10)
        self.month_entry = ttk.Entry(self.analysis_tab, width=30, font=("Arial", 10))  # Larger input field, smaller font
        self.month_entry.pack(pady=10)
        ttk.Button(self.analysis_tab, text="Calculate Monthly Spending", command=self.calculate_monthly_spending).pack(pady=20)

        ttk.Label(self.analysis_tab, text="Enter Category and Month (Category, mm/yyyy):").pack(pady=10)
        self.category_month_entry = ttk.Entry(self.analysis_tab, width=30, font=("Arial", 10))  # Larger input field, smaller font
        self.category_month_entry.pack(pady=10)
        ttk.Button(self.analysis_tab, text="Generate Insights", command=self.generate_insights).pack(pady=20)

    def setup_savings_tab(self):
        ttk.Button(self.savings_tab, text="View All Savings Goals", command=lambda: view_savings_goals(self.saving_goal_path, self.savings_output_text)).pack(pady=15)
        ttk.Button(self.savings_tab, text="Add Savings Goal", command=lambda: add_savings_goal(self.saving_goal_path)).pack(pady=15)
        ttk.Button(self.savings_tab, text="Update Savings Goal Progress", command=lambda: update_savings_goal_progress(self.saving_goal_path)).pack(pady=15)
        ttk.Button(self.savings_tab, text="Reset Savings Goal Progress", command=lambda: reset_all_goal_progress(self.saving_goal_path)).pack(pady=15)

    def setup_import_export_tab(self):
        ttk.Button(self.import_export_tab, text="Import Transactions", command=import_transactions).pack(pady=15)
        ttk.Button(self.import_export_tab, text="Export Transactions", command=export_transactions).pack(pady=15)
        ttk.Button(self.import_export_tab, text="Export financial_file", command=export_financial).pack(pady=15)

    def clear_text(self):
        self.analysis_output_text.delete("1.0", tk.END)
        self.transaction_output_text.delete("1.0", tk.END)
        self.savings_output_text.delete("1.0", tk.END)

    def append_text(self, text, output_text):
        output_text.insert(tk.END, text + "\n")

    def calculate_yearly_spending(self):
        year = self.year_entry.get()
        try:
            result = sum_spending_for_year(int(year))
            self.append_text(result, self.analysis_output_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate yearly spending: {e}")

    def calculate_daily_spending(self):
        date = self.date_entry.get()
        try:
            result = sum_spending_for_day(date)
            self.append_text(result, self.analysis_output_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate daily spending: {e}")

    def calculate_monthly_spending(self):
        month = self.month_entry.get()
        try:
            month, year = map(int, month.split("/"))
            result = sum_spending_for_month(month)
            self.append_text(result, self.analysis_output_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate monthly spending: {e}")

    def generate_insights(self):
        category_month = self.category_month_entry.get()
        try:
            category, month_year = category_month.split(",")
            result = generate_spending_insights(category.strip(), month_year.strip())
            self.append_text(result, self.analysis_output_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate insights: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialAnalysisApp(root)
    root.mainloop()
