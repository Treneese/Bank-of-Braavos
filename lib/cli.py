# lib/cli.py
from models.client import Client
from helpers import (
    exit_program,
    add_client,
    add_account,
    view_accounts,
    find_account_by_acc_number,
    find_client_by_id,
    view_client_accounts,
    delete_account,
    delete_client,

)
def create_client():
    name = input("Enter name: ")
    address = input("Enter address: ")
    DOB = input("Enter DOB (YYYYMMDD): ")
    id_number = input("Enter ID number: ")
    email = input("Enter email: ")
    income = input("Enter income: ")
    education = input("Enter education: ")
    credit_score = input("Enter credit score: ")

    try:
        client = Client(
            name=name,
            address=address,
            DOB=int(DOB),
            id_number=id_number,
            email=email,
            income=float(income),
            education=education,
            credit_score=int(credit_score)
        )
        print(f"Client created: {client}")
    except ValueError as e:
        print(f"Error creating client: {e}")

def list_clients():
    for client_id, client in Client.all_clients.items():
        print(client)

def show_menu():
    print("Welcome to Bank of Braavos")
    print("1. Create an account")
    print("2. List clients")
    print("3. Exit")

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            add_menu()
        elif choice == "2":
            view_menu()
        elif choice == "3":
            deposit_menu()
        elif choice == "4":
            delete_menu()
        else:
            print("\nInvalid choice")

def menu():
    print("\nWelcome, weary travaler, to The Iron Bank of Braavos!")
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Add/register an account")
    print("2. View your accounts")
    print("3. Withdraw/deposit funds")
    print("4. Delete account/ End your business with us")

def add_menu():
    while True:
        create_menu_options()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            main()
        elif choice == "2":
            add_client()
            add_menu()
        elif choice == "3":
            add_account()
            add_menu()
        else:
            print("Invalid choice")

def create_menu_options():
    print("\n-Now in Register Menu-")
    print("Please select an option:")
    print("0. Exit Program")
    print("1. Return to Main Menu")
    print("2. Register as a new Client")
    print("3. Add an account")

def view_menu():
    while True:
        view_menu_options()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            main()
        elif choice == "2":
            find_client_by_id()
        elif choice == "3":
            view_client_accounts()
        elif choice == "4":
            find_account_by_acc_number()
        else:
            print("Invalid choice")
        view_menu()

def view_menu_options():
    print("\n-Now in Viewing Menu-")
    print("Please select an option:")
    print("0. Exit Program")
    print("1. Return to Main Menu")
    print("2. Find account by id")
    print("3. View your accounts")
    print("4. Find account by Account #")
    
def deposit_menu():
    while True:
        deposit_menu_options()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            main()
        elif choice == "2":
            deposit_account()     
        elif choice == "3":
            withdraw_account()
        else :
            print("Invalid choice")

def deposit_menu_options():
    print("\n-Now in Deposit/Withdraw Menu-")
    print("Please select an option:")
    print("0. Exit Program")
    print("1. Return to Main Menu")
    print("2. Deposit into Account")
    print("3. Withdraw from Account")

def delete_menu():
    while True:
        delete_menu_options()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            main()    
        elif choice == "2":
            delete_account()
        elif choice == "3":
            delete_client()
        else :
            print("Invalid choice")


def delete_menu_options():
    print("\n-Now in Delete Menu-")
    print("Please select an option:")
    print("0. Exit Program")
    print("1. Return to Main Menu")
    print("2. Delete an account")
    print("3. Close all accounts")
    



if __name__ == '__main__':
    main()