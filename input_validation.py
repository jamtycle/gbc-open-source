import datetime

# categories for expenses
categories = ['food', 'clothing', 'entertainment', 'rent', 'transportation', 'others']


# category input validation
def validate_category(category):
    if category.lower() not in categories:
        print(f"Invalid category. Please choose one of the following: {', '.join(categories)}")
        return False
    return True


# date input validation
def validate_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%d-%m-%Y')
    except ValueError:
        print("Incorrect date format, should be dd-mm-yyyy")
        return False
    return True


# week number input validation
def validate_week(week_num):
    if not 0 <= week_num <= 52:
        print("Invalid week number. Please enter a number between 0 and 52")
        return False
    return True


# amount input validation
def validate_amount(amount):
    if isinstance(amount, str):
        try:
            float(amount)
            return True
        except ValueError:
            return False
    if not isinstance(amount, (int, float)):
        print("Invalid amount. Please enter a number")
        return False
    return True


# Ask user to input expenses
def input_expense():
    category = input("Enter expense category: ")
    while not validate_category(category):
        category = input("Enter expense category: ")

    date_string = input("Enter date (dd-mm-yyyy): ")
    while not validate_date(date_string):
        date_string = input("Enter date (dd-mm-yyyy): ")
    date = datetime.datetime.strptime(date_string, '%d-%m-%Y')

    week_num = input("Enter week number (0-52): ")
    while not validate_week(int(week_num)):
        week_num = input("Enter week number (0-52): ")
    week_num = int(week_num)

    amount = input("Enter expense amount in CAD: ")
    while not validate_amount(float(amount)):
        amount = input("Enter expense amount in CAD: ")
    amount = float(amount)

    return {'category': category, 'date': date, 'week_num': week_num, 'amount': amount}
