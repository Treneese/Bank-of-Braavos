# lib/models/account.py

class Account:

    ALLOWED_ACCOUNT_TYPES = ["Saving", "Checking", "Business", "Credit"]

    all = {}

    def __init__(self, account_number, routing_number, account_type, balance, payment_history):
        self.account_number = account_number
        self.routing_number = routing_number
        self.account_type = account_type
        self.balance = balance
        self.payment_history = payment_history
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
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        if isinstance(balance, (int, float)):
            self._balance = balance
        else:
            raise ValueError("Balance must be a number")

    @property
    def payment_history(self):
        return self._payment_history

    @payment_history.setter
    def payment_history(self, payment_history):
        if isinstance(payment_history, list):
            self._payment_history = payment_history
        else:
            raise ValueError("Payment History must be a list")