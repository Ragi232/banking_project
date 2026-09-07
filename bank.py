class Account:
    def __init__(self, account_number, name, pin):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be greater than 0.")
            return

        self.balance += amount
        self.transactions.append(f"Deposited {amount}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
            return

        if amount > self.balance:
            print("Insufficient balance.")
            return

        self.balance -= amount
        self.transactions.append(f"Withdrew {amount}")

    def check_balance(self):
        return self.balance

    def show_transactions(self):
        return self.transactions

    def verify_pin(self, pin):
        return self.pin == pin


accounts = []


def save_accounts():
    with open("accounts.txt", "w") as file:
        for account in accounts:
            transactions = "|".join(account.transactions)

            file.write(
                f"{account.account_number},"
                f"{account.name},"
                f"{account.pin},"
                f"{account.balance},"
                f"{transactions}\n"
            )


def create_account():
    if accounts:
        account_number = max(
            account.account_number for account in accounts
        ) + 1
    else:
        account_number = 1001

    name = input("Enter your name: ")
    pin = input("Create a PIN: ")

    account = Account(account_number, name, pin)
    accounts.append(account)

    save_accounts()

    print("Account created successfully!")
    print("Your account number is:", account_number)


def load_accounts():
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")

                account_number = int(parts[0])
                name = parts[1]
                pin = parts[2]
                balance = float(parts[3])

                account = Account(account_number, name, pin)
                account.balance = balance

                if len(parts) > 4 and parts[4]:
                    account.transactions = parts[4].split("|")

                accounts.append(account)

    except FileNotFoundError:
        pass


def login(account_number, pin):
    for account in accounts:
        if account.account_number == account_number:
            if account.verify_pin(pin):
                return account

    return None


def bank_menu(account):
    print("\nLogin successful!")
    print("Welcome", account.name)
    print("Account number:", account.account_number)

    while True:
        print("\n--- BANK MENU ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check balance")
        print("4. Transaction history")
        print("5. Create account")
        print("6. Logout")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            amount = float(input("Enter deposit amount: "))
            account.deposit(amount)

        elif choice == "2":
            amount = float(input("Enter withdrawal amount: "))
            account.withdraw(amount)

        elif choice == "3":
            print("Balance:", account.check_balance())

        elif choice == "4":
            print("Transaction history:")

            if account.transactions:
                for transaction in account.show_transactions():
                    print("-", transaction)
            else:
                print("No transactions yet.")

        elif choice == "5":
            create_account()

        elif choice == "6":
            save_accounts()
            print("Logged out successfully.")
            break

        elif choice == "7":
            save_accounts()
            print("Accounts saved successfully.")
            print("Thank you for using the bank.")
            exit()

        else:
            print("Invalid option.")


def start_bank():
    while True:
        print("\n--- LOGIN ---")

        try:
            account_number = int(
                input("Enter your account number: ")
            )
        except ValueError:
            print("Account number must be a number.")
            continue

        logged_in = None

        for attempt in range(3):
            pin = input("Enter your PIN: ")

            logged_in = login(account_number, pin)

            if logged_in:
                break

            attempts_left = 2 - attempt

            if attempts_left > 0:
                print("Wrong PIN. Attempts left:", attempts_left)
            else:
                print("Too many incorrect attempts.")

        if logged_in:
            bank_menu(logged_in)


load_accounts()
start_bank()