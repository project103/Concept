#imperative code
import json
from datetime import datetime

class FinancialTransaction:
    def __init__(self, transaction_date, transaction_amount, transaction_type, transaction_category):
        self.category = transaction_category
        self.amount = transaction_amount
        self.type = transaction_type
        self.date = transaction_date

# File path for the transactions database
database_file_path = r"F:study\level 4\Concept\FinancialApp2\FinancialApp2\transactions.json"

# Mutable collection for transactions
financial_database = []

def save_database_to_file():
    json_data = json.dumps([t.__dict__ for t in transaction_database])
    with open(database_file_path, 'w') as file:
        file.write(json_data)

def load_database_from_file():
    global transaction_database
    try:
        with open(database_file_path, 'r') as file:
            data = json.load(file)
            transaction_database = []
            for entry in data:
                transaction_database.append(
                    FinancialTransaction(
                        datetime.strptime(entry["date"], "%d-%m-%Y"),  # Parse date
                        entry["amount"],  # Amount
                        entry["type"].lower(),  # Normalize type (case-insensitive)
                        entry["category"]  # Category
                    )
                )
    except FileNotFoundError:
        print("No existing database file found. Starting fresh.")

def display_transactions():
    print("Current Transaction Database:")
    for transaction in transaction_database:
        formatted_date = transaction.date.strftime("%d/%m/%Y")
        print(f"Date: {formatted_date}, Amount: {transaction.amount}, Type: {transaction.type}, Category: {transaction.category}")

def parse_date(date_string, formats=None):
    if formats is None:
        formats = ["%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"]
    
    for format in formats:
        try:
            return datetime.strptime(date_string, format)
        except ValueError:
            continue
    return None

def calculate_string_length(s):
    length = 0
    for char in s:
        length += 1
    return length

def find_separator_position(s):
    for index, char in enumerate(s):
        if char in ['-', '/']:
            return index
    return -1

def try_parse_month_year(month_year_string):
    if month_year_string == "":
        return None 
    length = calculate_string_length(month_year_string)
    separator_position = find_separator_position(month_year_string)

    if separator_position == -1:
        return None  

    month = parse_int(month_year_string, 0, separator_position)
    year = parse_int(month_year_string, separator_position + 1, length)

    if month is not None and year is not None and 1 <= month <= 12:
        return datetime(year, month, 1)
    return None

def parse_int(input_string, start_pos, end_pos):
    current_sum = 0
    for i in range(start_pos, end_pos):
        char = input_string[i]
        if '0' <= char <= '9':
            current_sum = current_sum * 10 + int(char)
        else:
            return None
    return current_sum

from datetime import datetime

def is_date_within_range(date, start_date, end_date):
    # If date is a string, convert it to datetime
    if isinstance(date, str):
        date = datetime.strptime(date, "%d-%m-%Y")  

    if start_date and isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%d-%m-%Y")  
    
    if end_date and isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%d-%m-%Y")  

    # Check if date is within the range
    if start_date and end_date:
        return start_date <= date <= end_date
    if start_date:
        return start_date <= date
    if end_date:
        return date <= end_date
    return True


def is_in_month(date, month):
    return month == 0 or date.month == month

def is_in_category(category, head_category):
    return category == "" or head_category == category 

def category_exist(category, transactions):
    for transaction in transactions:
        if transaction.category == category:
            return True
    return False

def calculate_spending(transactions, category, start_date_str, end_date_str, month):
    parsed_start_date = parse_date(start_date_str)
    parsed_end_date = parse_date(end_date_str)
    total_spending = 0.0

    for transaction in transactions:
        date_within_range = is_date_within_range(transaction.date, parsed_start_date, parsed_end_date)
        in_month = is_in_month(transaction.date, month)
        in_category = is_in_category(category, transaction.category)

        if transaction.type == "expense" and in_category and date_within_range and in_month:
            total_spending += transaction.amount

    return total_spending

def sum_spending_for_year(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    total_spending = calculate_spending(transaction_database, "", start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"), 0)
    return f"Total spending for year {year}: {total_spending:.2f}"

def sum_spending_for_day(date_string):
    date = parse_date(date_string)
    if date:
        total_spending = calculate_spending(transaction_database, "", date.strftime("%d/%m/%Y"), date.strftime("%d/%m/%Y"), 0)
        return f"Total spending for day {date.day:02d}/{date.month:02d}/{date.year}: {total_spending:.2f}"
    else:
        return "Invalid date format. Please use one of the supported formats."

def sum_spending_in_date_range(start_date, end_date):
    total_spending = calculate_spending(transaction_database, "", start_date, end_date, 0)
    if start_date == "" and end_date == "":
        return f"Total spending (from beginning to now): {total_spending:.2f}"
    elif start_date == "":
        return f"Total Spending (from beginning to {end_date}): {total_spending:.2f}"
    elif end_date == "":
        return f"Total Spending (from {start_date} to now): {total_spending:.2f}"
    else:
        return f"Total Spending (from {start_date} to {end_date}): {total_spending:.2f}"

def sum_spending_for_month(month):
    total_spending = calculate_spending(transaction_database, "", "", "", month)
    return f"Total Spending in Month {month}: {total_spending:.2f}"

def sum_spending_in_category(category):
    if category_exist(category, transaction_database):
        total_spending = calculate_spending(transaction_database, category, "", "", 0)
        return f"Total Spending of {category}: {total_spending:.2f}"
    else:
        return f"Sorry, the category {category} does not exist."

def sum_spending_in_category_and_month(category, month_year_string, print_total):
    date = try_parse_month_year(month_year_string)
    if date:
        month = date.month
        year = date.year
        start_date = datetime(year, month, 1).strftime("%d/%m/%Y")
        end_date = datetime(year, month, 28).strftime("%d/%m/%Y")  
        total_spending = calculate_spending(transaction_database, category, start_date, end_date, month)

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

def sum_spending_in_category_and_date_range(category, start_date, end_date):
    if category_exist(category, transaction_database):
        total_spending = calculate_spending(transaction_database, category, start_date, end_date, 0)
        return f"Total Spending of {category} (from {start_date} to {end_date}): {total_spending:.2f}"
    else:
        return f"Sorry, the category {category} does not exist."

def get_categories(transactions):
    categories = []
    for transaction in transactions:
        category_exists = False
        for category in categories:
            if transaction.category == category:
                category_exists = True
                break
        if not category_exists:
            categories = categories + [transaction.category]  
    return categories

def print_total_spending(categories=None):
    if categories is None:
        categories = get_categories(transaction_database)

    output = []
    for category in categories:
        total_spending = calculate_spending(transaction_database, category, "", "", 0)
        if total_spending > 0.0:
            output = output + [f"Total Spending of {category}: {total_spending:.2f}"]  
    return output
# Calculate percentage change
def calculate_percentage_change(old_value, new_value):
    if old_value == 0.0:
        return None 
    return ((new_value - old_value) / old_value) * 100.0

# Print spending insights
def print_spending_insight(change, category, month_year=None):
    if change > 0.0:
        if month_year:
            return f"You spent {change:.2f}% more on {category} in {month_year} compared to the previous month."
        else:
            return f"You spent {change:.2f}% more on {category} this month compared to the previous month."
    elif change < 0.0:
        if month_year:
            return f"You spent {abs(change):.2f}% less on {category} in {month_year} compared to the previous month."
        else:
            return f"You spent {abs(change):.2f}% less on {category} this month compared to the previous month."
    else:
        if month_year:
            return f"Your spending on {category} remained the same in {month_year} compared to the previous month."
        else:
            return f"Your spending on {category} remained the same this month compared to the previous month."

# Generate spending insights for all categories
def generate_spending_insights_for_all_categories(categories=None, current_month=None, current_year=None, previous_month=None, previous_year=None):
    insights = []

    if categories is None:
        current_month = datetime.now().month
        current_year = datetime.now().year
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year if current_month > 1 else current_year - 1
        
        categories = get_categories(transaction_database)

    index = 0
    while index < len(categories):
        category = categories[index]
        current_spending = sum_spending_in_category_and_month(category, f"{current_month}-{current_year}", False)
        previous_spending = sum_spending_in_category_and_month(category, f"{previous_month}-{previous_year}", False)

        change = calculate_percentage_change(previous_spending, current_spending)
        if change is not None:
            insight_statement = print_spending_insight(change, category)
            insights = insights + [{'category': category, 'insight': insight_statement}]
        
        index += 1  # Move to the next category

    return insights

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
        if change is not None:
            return print_spending_insight(change, category, month_year)
        else:
            return f"No spending data available for {category} in the previous month."
    else:
        return "Invalid month-year format. Please use one of the right formats."


def save_output_to_file(output_data, filename=r'F:\study\level 4\Concept\project\imperative\JSON\report2.json'):
    with open(filename, 'w') as file:
        json.dump(output_data, file, indent=4)  

def display_summaries():
    output_data = {}
    output_data["Total spending"] = sum_spending_in_date_range("", "")
    output_data["Total spending by categories"] = print_total_spending()
    output_data["Total insigths"]= generate_spending_insights_for_all_categories()
    output_data["Total spending for year 2023"] = sum_spending_for_year(2023)
    output_data["Total spending for year 2024"] = sum_spending_for_year(2024)
    return output_data

load_database_from_file()
save_output_to_file(display_summaries())
