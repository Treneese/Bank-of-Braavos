# lib/models/account.py
from typing import List, Union, Dict
from .client import Client

class Account:

    ALLOWED_ACCOUNT_TYPES = ["Saving", "Checking", "Business", "Credit"]

    all: Dict[int, "Account"] = {}

    def __init__(self, account_number: int, routing_number: int, account_type: str, balance: Union[int, float], payment_history: List[Dict], client: Client):
        self.account_number = account_number
        self.routing_number = routing_number
        self.account_type = account_type
        self.balance = balance
        self.payment_history = payment_history
        self.client = client
        Account.all[account_number] = self

    @property
    def account_number(self):
        return self._account_number

    @account_number.setter
    def account_number(self, account_number):
        if isinstance(account_number, int) and 12 <= len(str(account_number)) <= 17:
            self._account_number = account_number
        else:
            raise ValueError("Account Number must be an integer between 12 and 17 digits")

    @property
    def routing_number(self):
        return self._routing_number

    @routing_number.setter
    def routing_number(self, routing_number):
        if isinstance(routing_number, int) and len(str(routing_number)) == 9:
            self._routing_number = routing_number
        else:
            raise ValueError("Routing Number must be an integer of 9 digits")

    @property
    def account_type(self):
        return self._account_type

    @account_type.setter
    def account_type(self, account_type):
        if isinstance(account_type, str) and account_type in self.ALLOWED_ACCOUNT_TYPES:
            self._account_type = account_type
        else:
            raise ValueError("Account Type must be one of: 'Saving', 'Checking', 'Business', or 'Credit'")

    @property
    def balance(self) -> Union[int, float]:
        return self._balance

    @balance.setter
    def balance(self, balance: Union[int, float]) -> None:
        if isinstance(balance, (int, float)):
            self._balance = balance
        else:
            raise ValueError("Balance must be a number")

    @property
    def payment_history(self) -> List[Dict]:
        return self._payment_history

    @payment_history.setter
    def payment_history(self, payment_history: List[Dict]) -> None:
        if isinstance(payment_history, list):
            self._payment_history = payment_history
        else:
            raise ValueError("Payment History must be a list")

    @property
    def client(self) -> Client:
        return self._client

    @client.setter
    def client(self, client: Client) -> None:
        if isinstance(client, Client):
            self._client = client
        else:
            raise ValueError("Client must be an instance of the Client class")

        
    def __repr__(self):
        return f'<Account account_number={self.account_number} account_type={self.account_type} client={self.client}>'