from client import Client

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
        show_menu()
        choice = input("Enter choice: ")

        if choice == '1':
            create_client()
        elif choice == '2':
            list_clients()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()