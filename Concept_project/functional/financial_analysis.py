import json
from datetime import datetime
import sys

# Add the path to sys.path
sys.path.append(r"..\..\Concept_project\functional")

# Import the necessary functions
from trans_budget import load_data, save_data, format_transactions, parse_date



transaction_file_path=r"F:\study\level 4\Concept\Concept_project (2)\Concept_project\functional\JSON\transactions.json"

def save_database_to_file():
    save_data(transaction_file_path, transaction_database)

def load_database_from_file():
    global transaction_database
    transaction_database = load_data(transaction_file_path)

def display_transactions():
    print("Current Transaction Database:")
    format_transactions(transaction_database)


############

# calculate string length
def calculate_string_length(s, count=0):
    if count < 0: 
        return 0
    if s[count:]:
        return calculate_string_length(s, count + 1)
    return count

# find the position of the separator 
def find_separator_position(s, index=0):
    if index >= calculate_string_length(s): 
        return -1 
    if s[index] in ['-', '/']:
        return index
    return find_separator_position(s, index + 1)

# parse month-year strings
def try_parse_month_year(month_year_str):
    if month_year_str == "":
        return None 
    length = calculate_string_length(month_year_str)
    separator_position = find_separator_position(month_year_str)

    if separator_position == -1:
        return None  

    month = parse_int(month_year_str, 0, separator_position)
    year = parse_int(month_year_str, separator_position + 1, length)

    if month is not None and year is not None and 1 <= month <= 12:
        return datetime(year, month, 1)
    return None
    
#convert char to int
def parse_int(s, start_pos, end_pos, current_sum=0):
    if start_pos >= end_pos:
        return current_sum

    # get the current character
    char = s[start_pos]
    # check if the character is a digit
    if '0' <= char <= '9':
        digit = int(char)  
    else:
        return None  

    return parse_int(s, start_pos + 1, end_pos, current_sum * 10 + digit)

# check date within range
def is_date_within_range(date, start_date, end_date):
    if start_date and end_date:
        return start_date <= date <= end_date
    if start_date:
        return start_date <= date
    if end_date:
        return date <= end_date
    return True

# check month
def is_in_month(date, month):
    return month == 0 or date.month == month

# check category
def is_in_category(category, head_category):
    return category == "" or head_category == category 

# check if category exists
def category_exist(category, transactions):
    if not transactions:
        return False
    if transactions[0]["category"] == category:
        return True
    return category_exist(category, transactions[1:])

# calculate total spending
def calc_spending(transactions, category, start_date_str, end_date_str, month, current_sum=0.0, index=0):
    parsed_start_d = parse_date(start_date_str)
    parsed_end_d = parse_date(end_date_str)

    if transactions is None or transactions[index:] == []:
        return current_sum

    transaction = transactions[index]
    date_within_range = is_date_within_range(parse_date(transaction['date']), parsed_start_d, parsed_end_d)
    in_month = is_in_month(parse_date(transaction['date']), month)
    in_category = is_in_category(category, transaction['category'])

    if transaction['type'] == "Expense" and in_category and date_within_range and in_month:
        current_sum += transaction['amount']

    return calc_spending(transactions, category, start_date_str, end_date_str, month, current_sum, index+1)


# sum spending for a specific year 
def sum_spending_for_year(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    total_spending = calc_spending(transaction_database, "", start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"), 0)
    return f"Total spending for year {year}: {total_spending:.2f}"

# sum spending for a specific day 
def sum_spending_for_day(date_str):
    date = parse_date(date_str)
    if date:
        total_spending = calc_spending(transaction_database, "", date.strftime("%d/%m/%Y"), date.strftime("%d/%m/%Y"), 0)
        return f"Total spending for day {date.day:02d}/{date.month:02d}/{date.year}: {total_spending:.2f}"
    else:
        return "Invalid date format. Please use one of the supported formats."

# sum spending in a date range 
def sum_spending_in_date_range(start_date, end_date):
    total_spending = calc_spending(transaction_database, "", start_date, end_date, 0)
    if start_date == "" and end_date == "":
        return f"Total spending (from beginning to now): {total_spending:.2f}"
    elif start_date == "":
        return f"Total Spending (from beginning to {end_date}): {total_spending:.2f}"
    elif end_date == "":
        return f"Total Spending (from {start_date} to now): {total_spending:.2f}"
    else:
        return f"Total Spending (from {start_date} to {end_date}): {total_spending:.2f}"

# sum spending in a specific month 
def sum_spending_for_month(month):
    total_spending = calc_spending(transaction_database, "", "", "", month)
    return f"Total Spending in Month {month}: {total_spending:.2f}"

# sum spending in a specific category 
def sum_spending_in_category(category):
    if category_exist(category, transaction_database):
        total_spending = calc_spending(transaction_database, category, "", "", 0)
        return f"Total Spending of {category}: {total_spending:.2f}"
    else:
        return f"Sorry, the category {category} does not exist."

# sum spending in a specific category and month 
def sum_spending_in_category_and_month(category, month_year_str, print_total):
    date = try_parse_month_year(month_year_str)
    if date:
        month = date.month
        year = date.year
        start_date = datetime(year, month, 1).strftime("%d/%m/%Y")
        end_date = datetime(year, month, 28).strftime("%d/%m/%Y")  # Assume max 28 days for simplicity
        total_spending = calc_spending(transaction_database, category, start_date, end_date, month)

        if category_exist(category, transaction_database):
            if print_total:
                return f"Total Spending of {category} in {month:02d}/{year}: {total_spending:.2f}"
            return total_spending    
        else:
            if print_total:
                return f"Sorry, the category {category} does not exist."
            return 0.0       
    else:
        return "Invalid month-year format. Please use one of the supported formats."
        return 0.0

# calculate total spending in a specific category and date range 
def sum_spending_in_category_and_date_range(category, start_date, end_date):
    if category_exist(category, transaction_database):
        total_spending = calc_spending(transaction_database, category, start_date, end_date, 0)
        return f"Total Spending of {category} (from {start_date} to {end_date}): {total_spending:.2f}"
    else:
        return f"Sorry, the category {category} does not exist."


# add an element to a list 
def add_to_list(listt, element):
    if listt == []:
        return [element]  
    elif listt[0] == element:
        return listt 
    else:
        return [listt[0]] + add_to_list(listt[1:], element)  

# get categories
def get_categories(transactions, x=None):
    if x is None:
        x = []
    if not transactions:
        return x  

    x = add_to_list(x, transactions[0]['category'])
    return get_categories(transactions[1:], x)
    

# get length of list 
def get_length(list):
    if list == []:  
        return 0
    else:
        return 1 + get_length(list[1:])  

def print_total_spending(categories=None, index=0):
    if categories is None:
        categories = get_categories(transaction_database)

    if index >= get_length(categories):
        return []  

    category = categories[index]
    total_spending = calc_spending(transaction_database, category, "", "", 0)

    current_output = []
    if total_spending > 0.0:
        current_output = [f"Total Spending of {category}: {total_spending:.2f}"]

    return current_output + print_total_spending(categories, index + 1)

# Calculate percentage change 
def calculate_percentage_change(old_value, new_value):
    if old_value == 0.0:
        return None 
    return ((new_value - old_value) / old_value) * 100.0

# get categories with spending in the current month
def get_current_month_categories(transaction_database, current_month, current_year, categories=None, index=0, current_month_categories=None):
    if categories is None:
        categories = get_categories(transaction_database)
        current_month_categories = []

    # Base case: If we've checked all categories
    if index >= get_length(categories):
        return current_month_categories

    # Get the current category
    category = categories[index]
    current_spending = sum_spending_in_category_and_month(category, f"{current_month}-{current_year}", False)

    # Create a new list for current_month_categories
    if current_spending > 0:
        current_month_categories = current_month_categories + [category]  

    # Recursive call for the next category
    return get_current_month_categories(transaction_database, current_month, current_year, categories, index + 1, current_month_categories)

# Print spending insights
def print_spending_insight(change, category, month_year=None):
    if change is None:
        if month_year:    
            return f"No spending data available for {category} in the previous month of {month_year}."
        else:
            return f"No spending data available for {category} in the previous month."
    elif change==0.0:    
        if month_year:
            return f"Your spending on {category} remained the same in {month_year} compared to the previous month."
        else:
            return f"Your spending on {category} remained the same this month compared to the previous month."
    elif change > 0.0:
        if month_year:
            return f"You spent {change:.2f}% more on {category} in {month_year} compared to the previous month."
        else:
            return f"You spent {change:.2f}% more on {category} this month compared to the previous month."
    else:
        if month_year:
            return f"You spent {abs(change):.2f}% less on {category} in {month_year} compared to the previous month."
        else:
            return f"You spent {abs(change):.2f}% less on {category} this month compared to the previous month."
        
# generate spending insights for all categories
def generate_spending_insights_for_all_categories(current_month=None, current_year=None, index=0, insights=None):
    if insights is None:
        insights = []

    # Get current month and year
    if current_month is None or current_year is None:
        current_month = datetime.now().month
        current_year = datetime.now().year

    # Get categories for the current month only 
    categories = get_current_month_categories(transaction_database, current_month, current_year)

    # Base case: If we've processed all categories
    if index >= get_length(categories):
        return insights

    # Get the current category
    category = categories[index]
    current_spending = sum_spending_in_category_and_month(category, f"{current_month}-{current_year}", False)
    previous_month = current_month - 1 if current_month > 1 else 12
    previous_year = current_year if current_month > 1 else current_year - 1
    previous_spending = sum_spending_in_category_and_month(category, f"{previous_month}-{previous_year}", False)

    # Calculate change
    change = calculate_percentage_change(previous_spending, current_spending)

    # Generate insight statement 
    insight_statement = print_spending_insight(change, category)

    # Create the current insight
    current_insights = insights +[{'category': category, 'insight': insight_statement}]

    # Recursive call for the next category
    return generate_spending_insights_for_all_categories(current_month, current_year, index + 1, current_insights)


# Generate spending trends insights 
def generate_spending_insights(category, month_year):
    date = try_parse_month_year(month_year)
    if date:
        current_month = date.month
        current_year = date.year
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year if current_month > 1 else current_year - 1

        current_spending = sum_spending_in_category_and_month(category, f"{current_month}-{current_year}", False)
        previous_spending = sum_spending_in_category_and_month(category, f"{previous_month}-{previous_year}", False)

        change = calculate_percentage_change(previous_spending, current_spending)
        
        return print_spending_insight(change, category, month_year)
    else:
        return "Invalid month-year format. Please use one of the right formats."



def save_output_to_file(output_data, filename=r'F:\study\level 4\Concept\Concept_project (2)\Concept_project\functional\JSON\report2.json'):
    with open(filename, 'w') as f:
        json.dump(output_data, f, indent=4)  

def capture_display_transactions():
    output_data = {}

    output_data["Total spending"] = sum_spending_in_date_range("","")

    output_data["Total spending by categories"] = print_total_spending()

    output_data["Total spending insights"] = generate_spending_insights_for_all_categories()

    output_data["Total_spending_for_year_2023"] = sum_spending_for_year(2023)
    output_data["Total_spending_for_year_2024"] = sum_spending_for_year(2024)
    output_data["For day"]= sum_spending_for_day("7/12/2024")
    output_data["For 2 days"]= sum_spending_in_date_range("7/11/2024","7/12/2024")
    output_data['for month']=sum_spending_for_month(12)
    output_data['for minth and category']=sum_spending_in_category_and_month("Food","12-2024",True)
    output_data["for 1 insugths"]=generate_spending_insights("Food","12-2024")
    output_data["for another insigths"]=generate_spending_insights("Entertainment","12/2024")


    return output_data

load_database_from_file()

save_output_to_file(capture_display_transactions())
###########################
display_transactions()
# ------------------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
from financial_analysis import (
    load_database_from_file, save_database_to_file, display_transactions,
    sum_spending_for_year, sum_spending_for_day, sum_spending_in_date_range,
    sum_spending_for_month, sum_spending_in_category,
    sum_spending_in_category_and_date_range, generate_spending_insights,
    capture_display_transactions, save_output_to_file
)

# GUI Application
class FinancialAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Analysis Tool")

        # Tabs for organizing features
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Transaction Tab
        self.transaction_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.transaction_tab, text="Transactions")
        self.setup_transaction_tab()

        # Analysis Tab
        self.analysis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_tab, text="Spending Analysis")
        self.setup_analysis_tab()

        # Report Tab
        self.report_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.report_tab, text="Reports")
        self.setup_report_tab()

    def setup_transaction_tab(self):
        # Buttons to load/save database
        ttk.Button(self.transaction_tab, text="Load Transactions", command=self.load_transactions).pack(pady=10)
        ttk.Button(self.transaction_tab, text="Save Transactions", command=self.save_transactions).pack(pady=10)

        # Display transactions area
        self.transaction_display = tk.Text(self.transaction_tab, height=20, width=80)
        self.transaction_display.pack(pady=10)

        ttk.Button(self.transaction_tab, text="Display Transactions", command=self.show_transactions).pack(pady=10)

    def setup_analysis_tab(self):
        # Yearly Spending
        ttk.Label(self.analysis_tab, text="Enter Year:").pack(pady=5)
        self.year_entry = ttk.Entry(self.analysis_tab)
        self.year_entry.pack(pady=5)
        ttk.Button(self.analysis_tab, text="Calculate Yearly Spending", command=self.calculate_yearly_spending).pack(pady=10)

        # Daily Spending
        ttk.Label(self.analysis_tab, text="Enter Date (dd/mm/yyyy):").pack(pady=5)
        self.date_entry = ttk.Entry(self.analysis_tab)
        self.date_entry.pack(pady=5)
        ttk.Button(self.analysis_tab, text="Calculate Daily Spending", command=self.calculate_daily_spending).pack(pady=10)

        # Monthly Spending
        ttk.Label(self.analysis_tab, text="Enter Month (mm/yyyy):").pack(pady=5)
        self.month_entry = ttk.Entry(self.analysis_tab)
        self.month_entry.pack(pady=5)
        ttk.Button(self.analysis_tab, text="Calculate Monthly Spending", command=self.calculate_monthly_spending).pack(pady=10)

        # Spending Insights
        ttk.Label(self.analysis_tab, text="Enter Category and Month (Category, mm/yyyy):").pack(pady=5)
        self.category_month_entry = ttk.Entry(self.analysis_tab)
        self.category_month_entry.pack(pady=5)
        ttk.Button(self.analysis_tab, text="Generate Insights", command=self.generate_insights).pack(pady=10)

        # Output area
        self.analysis_output = tk.Text(self.analysis_tab, height=15, width=80)
        self.analysis_output.pack(pady=10)

    def setup_report_tab(self):
        ttk.Button(self.report_tab, text="Generate and Save Report", command=self.generate_and_save_report).pack(pady=20)
        ttk.Label(self.report_tab, text="Report saved as JSON file.").pack(pady=10)

    def load_transactions(self):
        try:
            load_database_from_file()
            messagebox.showinfo("Success", "Transactions loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transactions: {e}")

    def save_transactions(self):
        try:
            save_database_to_file()
            messagebox.showinfo("Success", "Transactions saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save transactions: {e}")

    def show_transactions(self):
        try:
            self.transaction_display.delete("1.0", tk.END)
            display_transactions()
            self.transaction_display.insert(tk.END, "Transactions displayed in console.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display transactions: {e}")

    def calculate_yearly_spending(self):
        year = self.year_entry.get()
        try:
            result = sum_spending_for_year(int(year))
            self.analysis_output.insert(tk.END, result + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate yearly spending: {e}")

    def calculate_daily_spending(self):
        date = self.date_entry.get()
        try:
            result = sum_spending_for_day(date)
            self.analysis_output.insert(tk.END, result + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate daily spending: {e}")

    def calculate_monthly_spending(self):
        month = self.month_entry.get()
        try:
            month, year = map(int, month.split("/"))
            result = sum_spending_for_month(month)
            self.analysis_output.insert(tk.END, result + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate monthly spending: {e}")

    def generate_insights(self):
        category_month = self.category_month_entry.get()
        try:
            category, month_year = category_month.split(",")
            result = generate_spending_insights(category.strip(), month_year.strip())
            self.analysis_output.insert(tk.END, result + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate insights: {e}")

    def generate_and_save_report(self):
        try:
            data = capture_display_transactions()
            save_output_to_file(data)
            messagebox.showinfo("Success", "Report generated and saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialAnalysisApp(root)
    root.mainloop()
