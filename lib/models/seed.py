from db import CONN, initialize_db, close_db
from models.client import Client
from models.account import Account


initialize_db()

Arya = Client( name="arya stark", address= "123 main", DOB= 19981915, email="arya.stark@gmail.com", ssn= "123452232", income=84039, credit_score= "770")


clients_data = [
    {
        "name": "Arya Stark",
        "address": "123 Main St",
        "DOB": 19850101,
        "id_number": "1234567890",
        "email": "arya.stark@example.com",
        "ssn": "123-45-6789",
        "income": 55000,
        "credit_score": 700
    },
    {
        "name": "John Snow",
        "address": "456 Elm St",
        "DOB": 19900202,
        "id_number": "0987654321",
        "email": "john.snow@example.com",
        "ssn": "987-65-4321",
        "income": 62000,
        "credit_score": 720
    },
    {
        "name": "Tyrion Lannister",
        "address": "789 Oak St",
        "DOB": 19751215,
        "id_number": "1122334455",
        "email": "tyrion.lannister@example.com",
        "ssn": "112-23-3445",
        "income": 175000,
        "credit_score": 680
    }
]


for data in clients_data:
    client = Client(**data)
    Arya.save()
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