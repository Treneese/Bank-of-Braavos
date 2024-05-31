from models.account import Account
from models.client import Client
from random import randint

def exit_program():
    print("Thank you for Banking with us. Goodbye!")
    exit()

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def add_client():
    try:
        client = input("User name: ")
        address = input("Place of residence: ")
        dob = input("Enter date of birth in the format YYYYMMDD: ")
        id_number = str(random_with_N_digits(10))
        email = input("Enter email address: ")
        income = input("Enter yearly gross income: ")
        credit_score = input("Enter your credit score: ")
        ssn = input("Enter social security number: ")
        
        Client.create(client, address, dob, id_number, email, ssn, income, credit_score)
        print(f"\nClient {Client} added sucessfully.")
    except Exception as exc:
        print(f"\nError: {exc}")

def add_account():
    try:
        account_type = input(f"Choose which account type you would like to open {Account.ALLOWED_ACCOUNT_TYPES}")
        while account_type not in Account.ALLOWED_ACCOUNT_TYPES:
            print("Invalid Category")
            account_type = input(f"Choose which account type you would like to open {Account.ALLOWED_ACCOUNT_TYPES}")
        acc_num = random_with_N_digits(12)
        routing_num = random_with_N_digits(9)
        id_ = input("Verify account number: ")
        Account.create(acc_num, routing_num, account_type, balance= 0, client = id_)
        print(f"\n{account_type} account created sucessfully.")
    except Exception as exc:
        print(f"\nError: {exc}")


def view_accounts():
    accounts = Account.get_all()
    if accounts:
        for account in accounts:
            print(f"\n-{account.account_type} account- Routing number: {account.routing_number}  Balance: {account.balance}")
        else:
            print("\nNo Accounts found.")

def find_account_by_acc_number():
    id_ = input("Enter the account number: ")
    account = Account.find_by_id_number(id_)
    if account:
        print(f"\nAccount Found: -{account.account_number}- Type: {account.account_type}")
    else: 
        print(f"\nAccount {id_} not found")

def log_in():
    id_ = input("Enter the Client ID number: ")
    password = input("Enter client password")
    client = Client.find_by_id_number(id_)
    if client:
        print(f"\nWelcome, back {Client.name}!")
              


def deposit_account():
    id_ = input("Enter the account number: ")
    account = Account.find_by_id_number(id_)
    if account:
        amount = float(input("Enter amount to be deposited: "))
        account.balance += amount
        print("\n Amount Deposited:", amount)
        print(f"\n Current balance: {account.balance}")
    else: 
        print(f"\nError: Invalid entry- account not found")

def withdraw_account():
    id_ = input("Enter the account number: ")
    account = Account.find_by_id_number(id_)
    if account:
        print(f"\n Current balance: {account.balance}")
        amount = float(input("Enter amount to be withdrawn: "))
        if account.balance >= amount:
            account.balance -= amount
            print("\n You Withdrew:", amount)
        else:
            print("\n Insufficient balance  ")
    else: 
        print("\nError: account not found")

def find_client_by_id():
    id_ = input("Enter the Client ID number: ")
    client = Client.find_by_id_number(id_)
    if client:
        print(f"\nAccount Found: -{client.name}- DOB: {client.DOB}")
    else: 
        print(f"\nAccount {id_} not found")

def view_client_accounts():
    client_id = input("Enter your client id: ")
    client_object = Client.find_by_id_number(client_id)
    if client_object:
        accounts = client_object.find_all_accs()
        if not accounts: print(f"\nClient {client_object.name} has no accounts yet")
        try:
            for account in accounts:
                print(f"\nType: {account.account_type} || Balance: {account.balance} || {account.payment_history}")
        except Exception as exc:
            print("Error finding Account: ", exc)
    else :
        print(f"\nClient id of {client_id} not found")






        

def delete_account():
    account_ids = [account.account_number for account in Account.get_all()]
    account_number = input(f"Enter the account number you'd like to delete from this list {account_ids}: ")
    account = account.find_by_acc(account_number)
    if account:
        account.delete()
        print(f"\naccount -{account_number}- has been deleted")
    else :
        print(f"\nclient -{account_number}- not found")


def delete_client():
    client_ids = [f"{object.name}: {object.id_number}" for object in Client.get_all()]
    if len(client_ids) > 0:
        client_id = input(f"To delete a client, select a client id from this list {client_ids}: ")
        while client_id not in [str(object.id) for object in Client.get_all()]:
            print("Client id is not in list")
            client_id = input(f"To delete a client, select a client id from this list {client_ids}: ")
        selected_client = Client.find_by_id_number(client_id)
        print(f"\nYou deleted {selected_client.name} and all their accounts")
        client_accounts = [account for account in Account.get_all()]
        for account in client_accounts:
            if str(account.client_id) == client_id:
                account.delete()
            else:
                continue
        selected_client.delete()
    else:
        print("\nThere are no clients to delete")