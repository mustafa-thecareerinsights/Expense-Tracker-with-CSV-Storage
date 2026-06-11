import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
FIELDS = ["Expense ID", "Title", "Amount", "Date", "Category"]


def create_csv_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDS)


def get_next_expense_id():
    create_csv_file()
    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        ids = [int(row["Expense ID"]) for row in reader if row["Expense ID"].isdigit()]
        return max(ids) + 1 if ids else 1


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_expense():
    try:
        expense_id = get_next_expense_id()

        title = input("Enter expense title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return

        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        date = input("Enter date (YYYY-MM-DD): ").strip()
        if not validate_date(date):
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        category = input("Enter category: ").strip()
        if not category:
            print("Category cannot be empty.")
            return

        with open(FILE_NAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([expense_id, title, amount, date, category])

        print("Expense added successfully!")

    except ValueError:
        print("Invalid amount. Please enter a number.")
    except Exception as e:
        print("Error:", e)


def view_expenses():
    create_csv_file()

    try:
        with open(FILE_NAME, mode="r") as file:
            reader = csv.DictReader(file)
            expenses = list(reader)

            if not expenses:
                print("No expenses found.")
                return

            print("\nAll Expenses:")
            print("-" * 70)
            print(f"{'ID':<5}{'Title':<20}{'Amount':<10}{'Date':<15}{'Category':<15}")
            print("-" * 70)

            for row in expenses:
                print(f"{row['Expense ID']:<5}{row['Title']:<20}{row['Amount']:<10}{row['Date']:<15}{row['Category']:<15}")

    except Exception as e:
        print("Error:", e)


def filter_by_date():
    create_csv_file()

    date = input("Enter date to filter (YYYY-MM-DD): ").strip()

    if not validate_date(date):
        print("Invalid date format.")
        return

    found = False

    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Date"] == date:
                print(row)
                found = True

    if not found:
        print("No expenses found for this date.")


def filter_by_month():
    create_csv_file()

    month = input("Enter month to filter (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format. Please use YYYY-MM.")
        return

    found = False

    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Date"].startswith(month):
                print(row)
                found = True

    if not found:
        print("No expenses found for this month.")


def calculate_total():
    create_csv_file()

    total = 0

    try:
        with open(FILE_NAME, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                total += float(row["Amount"])

        print(f"Total Expenses: ${total:.2f}")

    except Exception as e:
        print("Error:", e)


def summary_report():
    create_csv_file()

    summary = {}

    try:
        with open(FILE_NAME, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                category = row["Category"]
                amount = float(row["Amount"])
                summary[category] = summary.get(category, 0) + amount

        if not summary:
            print("No expenses found.")
            return

        print("\nExpense Summary Report:")
        print("-" * 40)

        for category, total in summary.items():
            print(f"{category}: ${total:.2f}")

    except Exception as e:
        print("Error:", e)


def menu():
    create_csv_file()

    while True:
        print("\n========== Expense Tracker ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses by Date")
        print("4. Filter Expenses by Month")
        print("5. Calculate Total Expenses")
        print("6. Generate Summary Report")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_by_date()
        elif choice == "4":
            filter_by_month()
        elif choice == "5":
            calculate_total()
        elif choice == "6":
            summary_report()
        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1 to 7.")


if __name__ == "__main__":
    menu()