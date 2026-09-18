from datetime import date


MIN_DEPOSIT = 100
MAX_DEPOSIT = 100000

MIN_WITHDRAWAL = 100
MAX_WITHDRAWAL = 50000

MIN_TRANSFER = 100
MAX_TRANSFER = 100000

DAILY_WITHDRAWAL_LIMIT = 100000
DAILY_TRANSFER_LIMIT = 200000


class Account:

    def __init__(self, account_number, name, pin):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = 0.0
        self.transactions = []
        self.status = "ACTIVE"
        self.failed_attempts = 0

        self.daily_withdrawal = 0.0
        self.daily_transfer = 0.0
        self.last_transaction_date = str(date.today())

    def reset_daily_limits(self):
        today = str(date.today())

        if self.last_transaction_date != today:
            self.daily_withdrawal = 0.0
            self.daily_transfer = 0.0
            self.last_transaction_date = today

    def add_transaction(self, transaction_id, description):
        today = str(date.today())

        transaction = (
            f"{transaction_id} - {today} - {description}"
        )

        self.transactions.append(transaction)

    def deposit(self, amount):

        if amount < MIN_DEPOSIT:
            print(f"Minimum deposit is {MIN_DEPOSIT}.")
            return False

        if amount > MAX_DEPOSIT:
            print(f"Maximum deposit is {MAX_DEPOSIT}.")
            return False

        transaction_id = generate_transaction_id()

        self.balance += amount

        self.add_transaction(
            transaction_id,
            f"Deposited {amount}"
        )

        print("Deposit successful!")
        print(f"Transaction ID: {transaction_id}")

        return True

    def withdraw(self, amount):

        self.reset_daily_limits()

        if amount < MIN_WITHDRAWAL:
            print(f"Minimum withdrawal is {MIN_WITHDRAWAL}.")
            return False

        if amount > MAX_WITHDRAWAL:
            print(f"Maximum withdrawal is {MAX_WITHDRAWAL}.")
            return False

        if amount > self.balance:
            print("Insufficient balance.")
            return False

        if self.daily_withdrawal + amount > DAILY_WITHDRAWAL_LIMIT:
            print("Daily withdrawal limit exceeded.")
            return False

        transaction_id = generate_transaction_id()

        self.balance -= amount
        self.daily_withdrawal += amount

        self.add_transaction(
            transaction_id,
            f"Withdrew {amount}"
        )

        print("Withdrawal successful!")
        print(f"Transaction ID: {transaction_id}")

        return True

    def check_balance(self):
        return self.balance

    def show_transactions(self):

        print("\n===== TRANSACTION HISTORY =====")

        if not self.transactions:
            print("No transactions found.")
            return

        for transaction in self.transactions:
            print("-", transaction)

    def verify_pin(self, pin):
        return self.pin == pin

    def change_pin(self):

        print("\n===== CHANGE PIN =====")

        current_pin = input("Enter current PIN: ")

        if current_pin != self.pin:
            print("Incorrect current PIN.")
            return False

        new_pin = input("Enter new 4-digit PIN: ")

        if not new_pin.isdigit() or len(new_pin) != 4:
            print("PIN must contain exactly 4 digits.")
            return False

        confirm_pin = input("Confirm new PIN: ")

        if new_pin != confirm_pin:
            print("PINs do not match.")
            return False

        self.pin = new_pin

        transaction_id = generate_transaction_id()

        self.add_transaction(
            transaction_id,
            "PIN changed"
        )

        print("PIN changed successfully!")

        return True

    def account_statement(self):

        self.reset_daily_limits()

        print("\n===== ACCOUNT STATEMENT =====")
        print(f"Account Number: {self.account_number}")
        print(f"Customer Name: {self.name}")
        print(f"Account Status: {self.status}")
        print(f"Balance: {self.balance}")

        print()
        print(f"Today's Withdrawals: {self.daily_withdrawal}")
        print(
            f"Daily Withdrawal Limit: "
            f"{DAILY_WITHDRAWAL_LIMIT}"
        )

        print()
        print(f"Today's Transfers: {self.daily_transfer}")
        print(
            f"Daily Transfer Limit: "
            f"{DAILY_TRANSFER_LIMIT}"
        )

        print("\nTransactions:")

        if not self.transactions:
            print("No transactions found.")
        else:
            for transaction in self.transactions:
                print("-", transaction)

    def transfer_money(self):

        self.reset_daily_limits()

        print("\n===== TRANSFER MONEY =====")

        receiver_number = input(
            "Enter receiver account number: "
        )

        receiver = find_account(receiver_number)

        if receiver is None:
            print("Receiver account not found.")
            return False

        if receiver.account_number == self.account_number:
            print("You cannot transfer money to yourself.")
            return False

        if receiver.status != "ACTIVE":
            print("Receiver account is not active.")
            return False

        try:
            amount = float(
                input("Enter transfer amount: ")
            )
        except ValueError:
            print("Please enter a valid amount.")
            return False

        if amount < MIN_TRANSFER:
            print(f"Minimum transfer is {MIN_TRANSFER}.")
            return False

        if amount > MAX_TRANSFER:
            print(f"Maximum transfer is {MAX_TRANSFER}.")
            return False

        if amount > self.balance:
            print("Insufficient balance.")
            return False

        if self.daily_transfer + amount > DAILY_TRANSFER_LIMIT:
            print("Daily transfer limit exceeded.")
            return False

        transaction_id = generate_transaction_id()

        self.balance -= amount
        receiver.balance += amount

        self.daily_transfer += amount

        self.add_transaction(
            transaction_id,
            f"Transferred {amount} to {receiver.account_number}"
        )

        receiver.add_transaction(
            transaction_id,
            f"Received {amount} from {self.account_number}"
        )

        print("Transfer successful!")
        print(f"Transaction ID: {transaction_id}")

        return True

    def search_transaction(self):

        print("\n===== SEARCH TRANSACTION =====")

        transaction_id = input(
            "Enter transaction ID: "
        ).strip().upper()

        for transaction in self.transactions:

            if transaction.startswith(transaction_id):

                print("\nTransaction found:")
                print("-", transaction)

                print("\n===== TRANSACTION DETAILS =====")

                parts = transaction.split(" - ", 2)

                if len(parts) == 3:

                    found_id = parts[0]
                    transaction_date = parts[1]
                    description = parts[2]

                else:

                    found_id = parts[0]
                    transaction_date = "Unknown"
                    description = parts[1]

                print(f"Transaction ID: {found_id}")
                print(f"Account Number: {self.account_number}")
                print(f"Customer Name: {self.name}")
                print(f"Date: {transaction_date}")

                if description.startswith("Deposited"):

                    transaction_type = "Deposit"

                    amount_text = (
                        description
                        .replace("Deposited", "")
                        .strip()
                    )

                elif description.startswith("Withdrew"):

                    transaction_type = "Withdrawal"

                    amount_text = (
                        description
                        .replace("Withdrew", "")
                        .strip()
                    )

                elif description.startswith("Transferred"):

                    transaction_type = "Transfer"

                    amount_text = (
                        description
                        .replace("Transferred", "")
                        .strip()
                    )

                elif description.startswith("Received"):

                    transaction_type = "Transfer Received"

                    amount_text = (
                        description
                        .replace("Received", "")
                        .strip()
                    )

                elif description.startswith("PIN changed"):

                    transaction_type = "PIN Change"
                    amount_text = "N/A"

                else:

                    transaction_type = "Other"
                    amount_text = "N/A"

                print(
                    f"Transaction Type: "
                    f"{transaction_type}"
                )

                print(f"Amount/Details: {amount_text}")

                print(
                    f"Description: "
                    f"{description}"
                )

                return True

        print("\nTransaction not found.")

        if self.transactions:

            print("\nAvailable transaction IDs:")

            for transaction in self.transactions:

                transaction_parts = transaction.split(
                    " - ",
                    1
                )

                print("-", transaction_parts[0])

        return False

    def close_account(self):

        print("\n===== CLOSE ACCOUNT =====")

        if self.balance != 0:

            print(
                "You cannot close an account "
                "with money in it."
            )

            print(
                f"Current balance: {self.balance}"
            )

            return False

        confirmation = input(
            "Are you sure you want to close "
            "your account? (yes/no): "
        ).lower()

        if confirmation != "yes":

            print("Account closing cancelled.")

            return False

        self.status = "CLOSED"

        print("Account closed successfully.")

        return True


accounts = []

next_transaction_id = 2


def generate_transaction_id():

    global next_transaction_id

    transaction_id = (
        f"TXN{next_transaction_id:04d}"
    )

    next_transaction_id += 1

    return transaction_id


def reset_all_daily_limits():

    for account in accounts:
        account.reset_daily_limits()


def find_account(account_number):

    for account in accounts:

        if account.account_number == account_number:
            return account

    return None


def create_account():

    print("\n===== CREATE ACCOUNT =====")

    account_number = input(
        "Enter account number: "
    )

    if find_account(account_number):

        print("Account number already exists.")

        return

    name = input("Enter customer name: ")

    pin = input("Create a 4-digit PIN: ")

    if not pin.isdigit() or len(pin) != 4:

        print("PIN must contain exactly 4 digits.")

        return

    account = Account(
        account_number,
        name,
        pin
    )

    accounts.append(account)

    print("\nAccount created successfully!")

    print(
        f"Account Number: {account_number}"
    )

    print(
        f"Customer Name: {name}"
    )


def edit_account_details(account):

    print("\n===== EDIT ACCOUNT DETAILS =====")

    new_name = input(
        f"Enter new name or press Enter "
        f"to keep '{account.name}': "
    )

    if new_name:
        account.name = new_name

    print(
        "Account details updated successfully."
    )


def login():

    print("\n===== CUSTOMER LOGIN =====")

    account_number = input(
        "Enter account number: "
    )

    account = find_account(account_number)

    if account is None:

        print("Account not found.")

        return None

    if account.status == "BLOCKED":

        print("This account is blocked.")

        return None

    if account.status == "CLOSED":

        print("This account is closed.")

        return None

    pin = input("Enter PIN: ")

    if account.verify_pin(pin):

        account.failed_attempts = 0

        print("\nLogin successful!")

        print(
            f"Welcome, {account.name}!"
        )

        return account

    account.failed_attempts += 1

    print("Incorrect PIN.")

    remaining = 3 - account.failed_attempts

    if account.failed_attempts >= 3:

        account.status = "BLOCKED"

        print("Too many failed attempts.")

        print(
            "Your account has been blocked."
        )

    else:

        print(
            f"Attempts remaining: {remaining}"
        )

    return None


def admin_login():

    print("\n===== ADMIN LOGIN =====")

    username = input("Admin username: ")

    password = input("Admin password: ")

    if username == "admin" and password == "admin123":

        print("Admin login successful!")

        return True

    print("Invalid admin login.")

    return False


def view_all_accounts():

    print("\n===== ALL ACCOUNTS =====")

    if not accounts:

        print("No accounts found.")

        return

    for account in accounts:

        print("----------------------------")

        print(
            f"Account Number: "
            f"{account.account_number}"
        )

        print(
            f"Name: {account.name}"
        )

        print(
            f"Balance: {account.balance}"
        )

        print(
            f"Status: {account.status}"
        )

        print(
            f"Failed Attempts: "
            f"{account.failed_attempts}"
        )


def count_accounts():

    print("\n===== ACCOUNT COUNT =====")

    print(
        f"Total accounts: {len(accounts)}"
    )


def block_account():

    print("\n===== BLOCK ACCOUNT =====")

    account_number = input(
        "Enter account number: "
    )

    account = find_account(account_number)

    if account is None:

        print("Account not found.")

        return

    account.status = "BLOCKED"

    print("Account blocked successfully.")


def activate_account():

    print("\n===== ACTIVATE ACCOUNT =====")

    account_number = input(
        "Enter account number: "
    )

    account = find_account(account_number)

    if account is None:

        print("Account not found.")

        return

    account.status = "ACTIVE"

    account.failed_attempts = 0

    print("Account activated successfully.")


def admin_menu():

    while True:

        print("\n===== ADMIN MENU =====")

        print("1. View all accounts")
        print("2. Count accounts")
        print("3. Block account")
        print("4. Activate account")
        print("5. Logout")

        choice = input(
            "Choose an option: "
        )

        if choice == "1":

            view_all_accounts()

        elif choice == "2":

            count_accounts()

        elif choice == "3":

            block_account()

        elif choice == "4":

            activate_account()

        elif choice == "5":

            print("Admin logged out.")

            break

        else:

            print("Invalid option.")


def customer_menu(account):

    while True:

        reset_all_daily_limits()

        print("\n===== CUSTOMER MENU =====")

        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check balance")
        print("4. Transaction history")
        print("5. Transfer money")
        print("6. Account statement")
        print("7. Change PIN")
        print("8. Edit account details")
        print("9. Close account")
        print("10. Logout")
        print("11. Exit")
        print("12. Search transaction")

        choice = input(
            "Choose an option: "
        )

        if choice == "1":

            try:

                amount = float(
                    input("Enter deposit amount: ")
                )

                account.deposit(amount)

            except ValueError:

                print(
                    "Please enter a valid amount."
                )

        elif choice == "2":

            try:

                amount = float(
                    input(
                        "Enter withdrawal amount: "
                    )
                )

                account.withdraw(amount)

            except ValueError:

                print(
                    "Please enter a valid amount."
                )

        elif choice == "3":

            print(
                f"Current balance: "
                f"{account.check_balance()}"
            )

        elif choice == "4":

            account.show_transactions()

        elif choice == "5":

            account.transfer_money()

        elif choice == "6":

            account.account_statement()

        elif choice == "7":

            account.change_pin()

        elif choice == "8":

            edit_account_details(account)

        elif choice == "9":

            if account.close_account():

                break

        elif choice == "10":

            print("Logged out successfully.")

            break

        elif choice == "11":

            print(
                "Thank you for using "
                "the banking system."
            )

            save_accounts()

            exit()

        elif choice == "12":

            account.search_transaction()

            input(
                "\nPress Enter to continue..."
            )

        else:

            print("Invalid option.")


def save_accounts():

    try:

        with open(
            "accounts.txt",
            "w"
        ) as file:

            for account in accounts:

                transactions = ";".join(
                    account.transactions
                )

                file.write(
                    f"{account.account_number}|"
                    f"{account.name}|"
                    f"{account.pin}|"
                    f"{account.balance}|"
                    f"{account.status}|"
                    f"{account.failed_attempts}|"
                    f"{account.daily_withdrawal}|"
                    f"{account.daily_transfer}|"
                    f"{account.last_transaction_date}|"
                    f"{transactions}\n"
                )

            file.write(
                f"TRANSACTION_ID|"
                f"{next_transaction_id}\n"
            )

    except Exception as error:

        print(
            f"Error saving accounts: {error}"
        )


def load_accounts():

    global next_transaction_id

    try:

        with open(
            "accounts.txt",
            "r"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                if parts[0] == "TRANSACTION_ID":

                    next_transaction_id = int(
                        parts[1]
                    )

                    continue

                if len(parts) < 10:
                    continue

                account_number = parts[0]
                name = parts[1]
                pin = parts[2]

                account = Account(
                    account_number,
                    name,
                    pin
                )

                account.balance = float(parts[3])

                account.status = parts[4]

                account.failed_attempts = int(
                    parts[5]
                )

                account.daily_withdrawal = float(
                    parts[6]
                )

                account.daily_transfer = float(
                    parts[7]
                )

                account.last_transaction_date = (
                    parts[8]
                )

                if parts[9]:

                    old_transactions = (
                        parts[9].split(";")
                    )

                    for transaction in old_transactions:

                        if not transaction:
                            continue

                        if transaction.startswith("TXN"):

                            account.transactions.append(
                                transaction
                            )

                        else:

                            transaction_id = (
                                generate_transaction_id()
                            )

                            account.transactions.append(
                                f"{transaction_id} - "
                                f"{account.last_transaction_date} - "
                                f"{transaction}"
                            )

                accounts.append(account)

    except FileNotFoundError:

        print(
            "No accounts file found. "
            "Starting with empty bank."
        )

    except Exception as error:

        print(
            f"Error loading accounts: {error}"
        )


def start_bank():

    while True:

        print("\n==============================")
        print("        MY PYTHON BANK")
        print("==============================")

        print("1. Customer Login")
        print("2. Admin Login")
        print("3. Create Account")
        print("4. Exit")

        choice = input(
            "Choose an option: "
        )

        if choice == "1":

            account = login()

            if account:

                customer_menu(account)

        elif choice == "2":

            if admin_login():

                admin_menu()

        elif choice == "3":

            create_account()

            save_accounts()

        elif choice == "4":

            save_accounts()

            print(
                "Thank you for using "
                "My Python Bank."
            )

            break

        else:

            print("Invalid option.")


load_accounts()
start_bank()