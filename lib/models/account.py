# lib/models/account.py
from models.__init__ import CURSOR, CONN
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
        
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Account instances """
        sql = """
             account_number BIGINT PRIMARY KEY,
            routing_number BIGINT NOT NULL,
            account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('Saving', 'Checking', 'Business', 'Credit')),
            balance DECIMAL(15, 2) NOT NULL
            client TEXT NOT NULL,
            FOREIGN KEY (client) REFERENCES Clients (name)

       
       
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Account instances """
        sql = """
            DROP TABLE IF EXISTS accounts;
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """ Insert a new row with the values of the current account object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO departments (account_number, routing_number, account_type, balance, payment_history, client)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.account_number, self.routing_number, self.account_type, self.balance, self.payment_history, self.client))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    @classmethod
    def create(cls, account_number, routing_number, account_type, balance):
        """Create a new accountt instance and save it to the database."""
        account = cls(account_number, routing_number, account_type, balance)
        account.save()
        return account
    
    def update(self):
        """Update the table row corresponding to the current Account instance."""
        sql = """
            UPDATE accounts
            SET account_number = ?, routing_number = ?, account_type = ?, balance = ?, payment_history = ?, client = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.account_number, self.routing_number, self.account_type, self.balance, self.payment_history, self.client))
        CONN.commit()

        
    def delete(self):
        """Delete the table row corresponding to the current Account instance,
        delete the dictionary entry, and reassign id attribute"""
        sql = """
            DELETE FROM accounts
            WHERE id = ?
        """
    
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
    
        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the account to None
        self.account = None

    @classmethod
    @classmethod
    def instance_from_db(cls, row):
        """Return a Account object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        account = cls.all.get(row[0])
        if account:
            # ensure attributes match row values in case local instance was modified
            account.account_number = row[1]
            account.routing_number = row[2]
            account.account_type = row[3]
            account.balance = row[4]
            account.payment_history = row[5]
            account.client = row[6]
        else:
            # not in dictionary, create new instance and add to dictionary
            account = cls(row[1], row[2], row[3], row[4], row[5], row[6])
            account.id = row[0]
            cls.all[account.id] = account
        return account


    @classmethod
    def get_all(cls):
        """Return a list containing one Account object per table row"""
        sql = """
            SELECT *
            FROM accounts
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
        

    @classmethod
    def find_by_account_number(cls, account_number):
        """Return a Account object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM accounts
            WHERE account_number = ?
        """

        row = CURSOR.execute(sql, (account_number,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, id):
        """Return account object corresponding to the table row matching the key"""
        sql = """
            SELECT *
            FROM accounts
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_client(cls, client):
        """Return a Account object corresponding to first table row matching specified client"""
        sql = """
            SELECT *
            FROM accounts
            WHERE client is ?
        """

        row = CURSOR.execute(sql, (client,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def clients(self):
        """Return list of clients associated with current accounts"""
        from client import Client
        sql = """
            SELECT * FROM clients
            WHERE account_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Client.instance_from_db(row) for row in rows
        ]





    def __repr__(self):
        return f'<Account account_number={self.account_number} account_type={self.account_type} client={self.client}>'