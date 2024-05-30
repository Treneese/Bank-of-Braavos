from db import CONN, initialize_db, close_db
from models.client import Client
from models.account import Account


initialize_db()


clients_data = [
    {
        "name": "John Doe",
        "address": "123 Main St",
        "DOB": 19850101,
        "id_number": "1234567890",
        "email": "john.doe@example.com",
        "ssn": "123-45-6789",
        "income": 55000,
        "credit_score": 700
    },
    {
        "name": "Jane Smith",
        "address": "456 Elm St",
        "DOB": 19900202,
        "id_number": "0987654321",
        "email": "jane.smith@example.com",
        "ssn": "987-65-4321",
        "income": 62000,
        "credit_score": 720
    },
    {
        "name": "Alice Johnson",
        "address": "789 Oak St",
        "DOB": 19751215,
        "id_number": "1122334455",
        "email": "alice.johnson@example.com",
        "ssn": "112-23-3445",
        "income": 75000,
        "credit_score": 680
    }
]


for data in clients_data:
    client = Client(**data)
    client.save()
    print(f"Inserted {client}")


    accounts_data = [
        {
            "account_number": 123456789012,
            "routing_number": 111000025,
            "account_type": "Checking",
            "balance": 1000.0,
            "payment_history": [],
            "client": client
        },
        {
            "account_number": 123456789013,
            "routing_number": 111000025,
            "account_type": "Saving",
            "balance": 5000.0,
            "payment_history": [],
            "client": client
        }
    ]

    for acc_data in accounts_data:
        account = Account(**acc_data)
        account.save()
        print(f"Inserted {account}")


close_db()
