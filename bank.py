from datetime import datetime
import os

next_transaction_id = 2


class Account:
    def __init__(
        self,
        account_number,
        name,
        pin,
        balance=0.0,
        status="ACTIVE",
        failed_attempts=0,
        daily_withdrawal=0.0,
        daily_transfer=0.0,
        last_reset_date=None,
        transactions=None
    ):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = balance
        self.status = status
        self.failed_attempts = failed_attempts
        self.daily_withdrawal = daily_withdrawal
        self.daily_transfer = daily_transfer
        self.last_reset_date = (
            last_reset_date
            or datetime.now().strftime("%Y-%m-%d")
        )
        self.transactions = transactions if transactions else []

    def reset_daily_limits(self):
        today = datetime.now().strftime("%Y-%m-%d")

        if self.last_reset_date != today:
            self.daily_withdrawal = 0.0
            self.daily_transfer = 0.0
            self.last_reset_date = today

    def create_transaction_id(self):
        global next_transaction_id

        transaction_id = f"TXN{next_transaction_id:04d}"
        next_transaction_id += 1

        return transaction_id

    def add_transaction(self, description):
        transaction_id = self.create_transaction_id()
        date = datetime.now().strftime("%Y-%m-%d")

        transaction = f"{transaction_id} - {date} - {description}"

        self.transactions.append(transaction)

        return transaction_id, date

    def save_receipt(
        self,
        transaction_id,
        date,
        transaction_type,
        amount,
        balance_after
    ):
        os.makedirs("receipts", exist_ok=True)

        filename = f"receipts/{transaction_id}.txt"

        with open(filename, "w") as file:
            file.write("==============================\n")
            file.write("       MY PYTHON BANK\n")
            file.write("==============================\n")
            file.write("       TRANSACTION RECEIPT\n")
            file.write("==============================\n\n")

            file.write(f"Transaction ID: {transaction_id}\n")
            file.write(f"Date: {date}\n")
            file.write(f"Account Number: {self.account_number}\n")
            file.write(f"Customer: {self.name}\n")
            file.write(f"Transaction Type: {transaction_type}\n")
            file.write(f"Amount: {amount}\n")
            file.write(
                f"Balance After Transaction: "
                f"{balance_after}\n"
            )
            file.write("Status: SUCCESS\n")

            file.write("\n==============================\n")

        print(f"Receipt saved to: {filename}")

    def show_receipt(
        self,
        transaction_id,
        date,
        transaction_type,
        amount,
        balance_after
    ):
        print("\n===== TRANSACTION RECEIPT =====")
        print(f"Transaction ID: {transaction_id}")
        print(f"Date: {date}")
        print(f"Account Number: {self.account_number}")
        print(f"Customer: {self.name}")
        print(f"Transaction Type: {transaction_type}")
        print(f"Amount: {amount}")
        print(f"Balance After Transaction: {balance_after}")
        print("Status: SUCCESS")
        print("===============================")

        self.save_receipt(
            transaction_id,
            date,
            transaction_type,
            amount,
            balance_after
        )

    def deposit(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        self.balance += amount

        transaction_id, date = self.add_transaction(
            f"Deposited {amount}"
        )

        self.show_receipt(
            transaction_id,
            date,
            "Deposit",
            amount,
            self.balance
        )

    def withdraw(self, amount):
        self.reset_daily_limits()

        daily_limit = 100000.0

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if amount > self.balance:
            print("Insufficient balance.")
            return

        if self.daily_withdrawal + amount > daily_limit:
            print("Daily withdrawal limit exceeded.")
            return

        self.balance -= amount
        self.daily_withdrawal += amount

        transaction_id, date = self.add_transaction(
            f"Withdrew {amount}"
        )

        self.show_receipt(
            transaction_id,
            date,
            "Withdrawal",
            amount,
            self.balance
        )

    def check_balance(self):
        print(f"\nCurrent balance: {self.balance}")

    def transaction_history(self):
        print("\n===== TRANSACTION HISTORY =====")

        if not self.transactions:
            print("No transactions found.")
            print("===============================")
            return

        for transaction in self.transactions:
            parts = transaction.split(" - ", 2)

            if len(parts) == 3:
                transaction_id = parts[0]
                date = parts[1]
                description = parts[2]

                print(
                    f"{transaction_id} | "
                    f"{date} | "
                    f"{description}"
                )
            else:
                print(transaction)

        print("===============================")

    def transfer_money(self, receiver, amount):
        self.reset_daily_limits()
        receiver.reset_daily_limits()

        daily_limit = 200000.0

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if amount > self.balance:
            print("Insufficient balance.")
            return

        if self.daily_transfer + amount > daily_limit:
            print("Daily transfer limit exceeded.")
            return

        self.balance -= amount
        receiver.balance += amount

        self.daily_transfer += amount

        sender_transaction_id, date = self.add_transaction(
            f"Transferred {amount} to "
            f"{receiver.account_number}"
        )

        receiver.add_transaction(
            f"Received {amount} from "
            f"{self.account_number}"
        )

        self.show_receipt(
            sender_transaction_id,
            date,
            "Transfer",
            amount,
            self.balance
        )

        print(
            f"\nTransfer successful to "
            f"{receiver.name} "
            f"({receiver.account_number})"
        )

    def account_statement(self):
        self.reset_daily_limits()

        print("\n===== ACCOUNT STATEMENT =====")
        print(f"Account Number: {self.account_number}")
        print(f"Customer Name: {self.name}")
        print(f"Balance: {self.balance}")
        print(f"Status: {self.status}")
        print(
            f"Daily Withdrawal: "
            f"{self.daily_withdrawal}"
        )
        print(
            f"Daily Transfer: "
            f"{self.daily_transfer}"
        )
        print("Daily Withdrawal Limit: 100000.0")
        print("Daily Transfer Limit: 200000.0")

        print("\nTransactions:")

        if not self.transactions:
            print("No transactions found.")
        else:
            for transaction in self.transactions:
                print(transaction)

        print("=============================")

    def change_pin(self):
        old_pin = input("Enter current PIN: ")

        if old_pin != self.pin:
            print("Incorrect current PIN.")
            return

        new_pin = input("Enter new PIN: ")

        if len(new_pin) != 4 or not new_pin.isdigit():
            print("PIN must contain exactly 4 digits.")
            return

        confirm_pin = input("Confirm new PIN: ")

        if new_pin != confirm_pin:
            print("PINs do not match.")
            return

        self.pin = new_pin

        print("PIN changed successfully.")

    def edit_details(self):
        print("\n===== EDIT ACCOUNT DETAILS =====")

        new_name = input(
            f"Enter new name "
            f"(press Enter to keep {self.name}): "
        )

        if new_name.strip():
            self.name = new_name.strip()

        print("Account details updated successfully.")

    def close_account(self):
        confirmation = input(
            "Are you sure you want to close this account? "
            "(yes/no): "
        )

        if confirmation.lower() == "yes":
            self.status = "CLOSED"

            print("Account closed successfully.")

            return True

        print("Account closure cancelled.")

        return False


accounts = []


def save_accounts():
    with open("accounts.txt", "w") as file:
        for account in accounts:
            transactions = "||".join(
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
                f"{account.last_reset_date}|"
                f"{transactions}\n"
            )

        file.write(
            f"TRANSACTION_ID|{next_transaction_id}\n"
        )


def load_accounts():
    global next_transaction_id

    accounts.clear()

    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                if parts[0] == "TRANSACTION_ID":
                    next_transaction_id = int(parts[1])
                    continue

                if len(parts) < 10:
                    continue

                account_number = parts[0]
                name = parts[1]
                pin = parts[2]
                balance = float(parts[3])
                status = parts[4]
                failed_attempts = int(parts[5])
                daily_withdrawal = float(parts[6])
                daily_transfer = float(parts[7])
                last_reset_date = parts[8]

                transactions = []

                if parts[9]:
                    transactions = parts[9].split("||")

                account = Account(
                    account_number,
                    name,
                    pin,
                    balance,
                    status,
                    failed_attempts,
                    daily_withdrawal,
                    daily_transfer,
                    last_reset_date,
                    transactions
                )

                accounts.append(account)

    except FileNotFoundError:
        print(
            "accounts.txt not found. "
            "Starting with no accounts."
        )


def find_account(account_number):
    for account in accounts:
        if account.account_number == account_number:
            return account

    return None


def customer_login():
    print("\n===== CUSTOMER LOGIN =====")

    account_number = input(
        "Enter account number: "
    )

    pin = input("Enter PIN: ")

    account = find_account(account_number)

    if account is None:
        print("Account not found.")
        return

    if account.status == "BLOCKED":
        print("This account is blocked.")
        return

    if account.status == "CLOSED":
        print("This account is closed.")
        return

    if pin != account.pin:
        account.failed_attempts += 1

        print("Incorrect PIN.")

        if account.failed_attempts >= 3:
            account.status = "BLOCKED"

            print("Too many failed attempts.")
            print("Account has been blocked.")

        save_accounts()

        return

    account.failed_attempts = 0

    print("\nLogin successful!")
    print(f"Welcome, {account.name}!")

    customer_menu(account)


def customer_menu(account):
    while True:
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

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                amount = float(
                    input("Enter deposit amount: ")
                )

                account.deposit(amount)
                save_accounts()

            except ValueError:
                print("Please enter a valid amount.")

        elif choice == "2":
            try:
                amount = float(
                    input("Enter withdrawal amount: ")
                )

                account.withdraw(amount)
                save_accounts()

            except ValueError:
                print("Please enter a valid amount.")

        elif choice == "3":
            account.check_balance()

        elif choice == "4":
            account.transaction_history()

        elif choice == "5":
            receiver_number = input(
                "Enter receiver account number: "
            )

            receiver = find_account(receiver_number)

            if receiver is None:
                print("Receiver account not found.")
                continue

            if receiver.account_number == account.account_number:
                print(
                    "You cannot transfer money to yourself."
                )
                continue

            try:
                amount = float(
                    input("Enter transfer amount: ")
                )

                account.transfer_money(
                    receiver,
                    amount
                )

                save_accounts()

            except ValueError:
                print("Please enter a valid amount.")

        elif choice == "6":
            account.account_statement()

        elif choice == "7":
            account.change_pin()
            save_accounts()

        elif choice == "8":
            account.edit_details()
            save_accounts()

        elif choice == "9":
            closed = account.close_account()

            if closed:
                save_accounts()
                break

        elif choice == "10":
            save_accounts()

            print("Logged out successfully.")

            break

        elif choice == "11":
            save_accounts()

            print(
                "Thank you for using MY PYTHON BANK."
            )

            exit()

        elif choice == "12":
            search_transaction(account)

        else:
            print("Invalid option.")


def search_transaction(account):
    transaction_id = input(
        "Enter transaction ID: "
    ).strip().upper()

    found = False

    for transaction in account.transactions:

        if transaction.startswith(transaction_id):

            print("\n===== TRANSACTION DETAILS =====")

            parts = transaction.split(" - ", 2)

            if len(parts) == 3:

                txn_id = parts[0]
                date = parts[1]
                description = parts[2]

                print(
                    f"Transaction ID: {txn_id}"
                )

                print(
                    f"Account Number: "
                    f"{account.account_number}"
                )

                print(
                    f"Customer Name: "
                    f"{account.name}"
                )

                print(f"Date: {date}")

                if description.startswith("Deposited"):
                    transaction_type = "Deposit"

                elif description.startswith("Withdrew"):
                    transaction_type = "Withdrawal"

                elif description.startswith("Transferred"):
                    transaction_type = "Transfer"

                elif description.startswith("Received"):
                    transaction_type = "Transfer"

                else:
                    transaction_type = "Other"

                print(
                    f"Transaction Type: "
                    f"{transaction_type}"
                )

                if transaction_type in [
                    "Deposit",
                    "Withdrawal"
                ]:
                    amount = description.split()[-1]

                    print(
                        f"Amount/Details: {amount}"
                    )

                else:
                    print(
                        f"Amount/Details: "
                        f"{description}"
                    )

                print(
                    f"Description: "
                    f"{description}"
                )

            print("===============================")

            found = True

            break

    if not found:
        print("Transaction not found.")


def admin_login():
    print("\n===== ADMIN LOGIN =====")

    username = input(
        "Enter admin username: "
    )

    password = input(
        "Enter admin password: "
    )

    if username == "admin" and password == "admin123":

        print("Admin login successful.")

        admin_menu()

    else:
        print("Invalid admin credentials.")


def admin_menu():
    while True:

        print("\n===== ADMIN MENU =====")
        print("1. View all accounts")
        print("2. Search account")
        print("3. Block account")
        print("4. Unblock account")
        print("5. Exit admin menu")

        choice = input("Choose an option: ")

        if choice == "1":

            print("\n===== ALL ACCOUNTS =====")

            if not accounts:
                print("No accounts found.")

            for account in accounts:

                print(
                    f"{account.account_number} | "
                    f"{account.name} | "
                    f"{account.balance} | "
                    f"{account.status}"
                )

        elif choice == "2":

            number = input(
                "Enter account number: "
            )

            account = find_account(number)

            if account:

                print(
                    f"\nAccount Number: "
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

            else:
                print("Account not found.")

        elif choice == "3":

            number = input(
                "Enter account number to block: "
            )

            account = find_account(number)

            if account:

                account.status = "BLOCKED"

                save_accounts()

                print("Account blocked.")

            else:
                print("Account not found.")

        elif choice == "4":

            number = input(
                "Enter account number to unblock: "
            )

            account = find_account(number)

            if account:

                account.status = "ACTIVE"
                account.failed_attempts = 0

                save_accounts()

                print("Account unblocked.")

            else:
                print("Account not found.")

        elif choice == "5":
            break

        else:
            print("Invalid option.")


def create_account():
    print("\n===== CREATE ACCOUNT =====")

    account_number = input(
        "Enter account number: "
    )

    if find_account(account_number):

        print("Account number already exists.")

        return

    name = input(
        "Enter customer name: "
    )

    pin = input(
        "Create 4-digit PIN: "
    )

    if len(pin) != 4 or not pin.isdigit():

        print(
            "PIN must contain exactly 4 digits."
        )

        return

    account = Account(
        account_number,
        name,
        pin
    )

    accounts.append(account)

    save_accounts()

    print("\nAccount created successfully!")

    print(
        f"Your account number is "
        f"{account_number}"
    )


def main():
    load_accounts()

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
            customer_login()

        elif choice == "2":
            admin_login()

        elif choice == "3":
            create_account()

        elif choice == "4":

            save_accounts()

            print(
                "Thank you for using MY PYTHON BANK."
            )

            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()