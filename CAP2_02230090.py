import os
import random
import hashlib

# Constants
ACCOUNTS_FILE = 'accounts.txt'

def hash_password(password):
    """
    Hashes a password using SHA-256.

    Parameters:
    password (str): The password to hash.

    Returns:
    str: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

class Account:
    def __init__(self, account_number, password, account_type, balance=0.0):
        """
        Initializes an account.

        Parameters:
        account_number (str): The account number.
        password (str): The plain text password.
        account_type (str): The type of the account (savings/current).
        balance (float): The initial balance (default is 0.0).
        """
        self.account_number = account_number
        self.password = hash_password(password)  # Store the hashed password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        """
        Deposits money into the account.

        Parameters:
        amount (float): The amount to deposit.
        """
        self.balance += amount

    def withdraw(self, amount):
        """
        Withdraws money from the account if sufficient balance exists.

        Parameters:
        amount (float): The amount to withdraw.

        Returns:
        bool: True if the withdrawal was successful, False if insufficient funds.
        """
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False

    def to_string(self):
        """
        Converts the account details to a string format suitable for file storage.

        Returns:
        str: The account details as a string.
        """
        return f"{self.account_number},{self.password},{self.account_type},{self.balance}\n"

class BankingApp:
    def __init__(self):
        """
        Initializes the banking application by loading existing accounts from file.
        """
        self.accounts = {}  # Dictionary to store accounts with account number as key
        self.load_accounts()

    def load_accounts(self):
        """
        Loads accounts from the accounts file.
        """
        if os.path.exists(ACCOUNTS_FILE):  # Check if accounts file exists
            with open(ACCOUNTS_FILE, 'r') as f:  # Open the file in read mode
                for line in f:
                    account_number, password, account_type, balance = line.strip().split(',')
                    # Create Account object and store it in the accounts dictionary
                    self.accounts[account_number] = Account(
                        account_number, password, account_type, float(balance))

    def save_accounts(self):
        """
        Saves all accounts to the accounts file.
        """
        with open(ACCOUNTS_FILE, 'w') as f:  # Open the file in write mode
            for account in self.accounts.values():
                f.write(account.to_string())  # Write each account's details to the file

    def create_account(self, account_type):
        """
        Creates a new account with a random account number and password.

        Parameters:
        account_type (str): The type of the account (savings/current).
        """
        account_number = str(random.randint(100000, 999999))  # Generate a random account number
        password = str(random.randint(1000, 9999))  # Generate a random 4-digit password
        account = Account(account_number, password, account_type)  # Create a new Account object
        self.accounts[account_number] = account  # Add the new account to the accounts dictionary
        self.save_accounts()  # Save all accounts to the file
        print(f"Account created. Account Number: {account_number}, Password: {password}")

    def login(self, account_number, password):
        """
        Logs in to an account if the account number and password match.

        Parameters:
        account_number (str): The account number.
        password (str): The password.

        Returns:
        Account: The account object if login is successful, None otherwise.
        """
        if account_number in self.accounts:  # Check if the account number exists
            account = self.accounts[account_number]
            if account.password == hash_password(password):  # Verify the password
                return account  # Return the account object if login is successful
        return None

    def delete_account(self, account_number):
        """
        Deletes an account by account number.

        Parameters:
        account_number (str): The account number to delete.

        Returns:
        bool: True if the account was successfully deleted, False otherwise.
        """
        if account_number in self.accounts:  # Check if the account number exists
            del self.accounts[account_number]  # Delete the account from the dictionary
            self.save_accounts()  # Save the updated accounts to the file
            return True
        return False

    def transfer_money(self, from_account, to_account_number, amount):
        """
        Transfers money from one account to another.

        Parameters:
        from_account (Account): The account to transfer money from.
        to_account_number (str): The account number to transfer money to.
        amount (float): The amount to transfer.

        Returns:
        bool: True if the transfer was successful, False otherwise.
        """
        if to_account_number in self.accounts:  # Check if the recipient account exists
            to_account = self.accounts[to_account_number]
            if from_account.withdraw(amount):  # Withdraw the amount from the sender's account
                to_account.deposit(amount)  # Deposit the amount into the recipient's account
                self.save_accounts()  # Save the updated accounts to the file
                return True
            else:
                print("Insufficient funds.")
        else:
            print("Receiving account does not exist.")
        return False

def main():
    """
    Main function to run the banking application.
    """
    app = BankingApp()  # Initialize the BankingApp

    while True:
        print("\n1. Create Account\n2. Login\n3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            account_type = input("Enter account type (savings/current): ")
            app.create_account(account_type)  # Create a new account

        elif choice == '2':
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = app.login(account_number, password)  # Attempt to login
            if account:
                print(f"Logged in as {account_number}. Balance: {account.balance}")

                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Transfer\n4. Delete Account\n5. Logout")
                    action = input("Choose an action: ")

                    if action == '1':
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)  # Deposit money
                        app.save_accounts()  # Save the updated account
                        print(f"Deposited {amount}. New balance: {account.balance}")

                    elif action == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):  # Attempt to withdraw money
                            app.save_accounts()  # Save the updated account
                            print(f"Withdrew {amount}. New balance: {account.balance}")
                        else:
                            print("Insufficient funds.")

                    elif action == '3':
                        to_account_number = input("Enter recipient account number: ")
                        amount = float(input("Enter amount to transfer: "))
                        if app.transfer_money(account, to_account_number, amount):  # Transfer money
                            print(f"Transferred {amount} to {to_account_number}. New balance: {account.balance}")

                    elif action == '4':
                        if app.delete_account(account.account_number):  # Delete the account
                            print("Account deleted successfully.")
                            break
                        else:
                            print("Failed to delete account.")

                    elif action == '5':
                        break  # Logout
                    else:
                        print("Invalid choice.")

            else:
                print("Invalid login credentials.")

        elif choice == '3':
            break  # Exit the application

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()