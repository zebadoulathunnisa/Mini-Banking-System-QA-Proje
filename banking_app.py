import sqlite3
import logging
import os

# Create logs directory if not exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Connect to SQLite database
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        name TEXT PRIMARY KEY,
        balance REAL
    )
''')
conn.commit()

# Function: Create account
def create_account(name):
    cursor.execute('INSERT OR IGNORE INTO accounts (name, balance) VALUES (?, ?)', (name, 0))
    conn.commit()

# Function: Deposit
def deposit(name, amount):
    cursor.execute('UPDATE accounts SET balance = balance + ? WHERE name = ?', (amount, name))
    conn.commit()
    logging.info(f"{name} deposited ₹{amount}")

# Function: Withdraw
def withdraw(name, amount):
    cursor.execute('SELECT balance FROM accounts WHERE name = ?', (name,))
    row = cursor.fetchone()
    if row and row[0] >= amount:
        cursor.execute('UPDATE accounts SET balance = balance - ? WHERE name = ?', (amount, name))
        conn.commit()
        logging.info(f"{name} withdrew ₹{amount}")
    else:
        print("Insufficient funds.")
        logging.warning(f"{name} failed to withdraw ₹{amount} due to insufficient funds")

# Function: Check balance
def check_balance(name):
    cursor.execute('SELECT balance FROM accounts WHERE name = ?', (name,))
    row = cursor.fetchone()
    if row:
        print(f"{name}'s balance: ₹{row[0]}")
        logging.info(f"{name} checked balance: ₹{row[0]}")
    else:
        print("Account not found.")

# === Interactive Menu ===
name = input("Enter your name: ").capitalize()
create_account(name)

while True:
    print("\nChoose an option:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. Exit")

    choice = input("Your choice: ")

    if choice == '1':
        amt = float(input("Enter amount to deposit: ₹"))
        deposit(name, amt)

    elif choice == '2':
        amt = float(input("Enter amount to withdraw: ₹"))
        withdraw(name, amt)

    elif choice == '3':
        check_balance(name)

    elif choice == '4':
        print("Thank you for using the banking system.")
        break

    else:
        print("Invalid choice. Try again.")
