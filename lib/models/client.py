# lib/models/client.py
import bcrypt
import re
import ipdb
from models.account import Account
from typing import List, Union, Dict
from db import CURSOR, CONN 

class Client:
    all: Dict[int, "Client"] = {}
    _id_counter = 1 

    def __init__(self, name: str, address: str, DOB: int, id_number: str, email: str, ssn: int, income: Union[int, float], credit_score: int, id: int = None):
        self.id = id or Client._id_counter
        if id is None:
            Client._id_counter += 1
        self.name = name
        self.address = address
        self.DOB = DOB
        self.id_number = id_number
        self.email = email
        self.income = income
        self.credit_score = credit_score
        self._hashed_ssn = None
        Client.all[id_number] = self

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if isinstance(name, str) and name.strip():
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def address(self) -> str:
        return self._address

    @staticmethod
    def is_valid_address(address: str) -> bool:
        return bool(re.search(r'\d', address)) and bool(re.search(r'[a-zA-Z]', address))

    @address.setter
    def address(self, address: str) -> None:
        if isinstance(address, str) and self.is_valid_address(address):
            self._address = address
        else:
            raise ValueError("Invalid street address")

    @property
    def DOB(self) -> int:
        return self._DOB

    @staticmethod
    def is_valid_DOB(DOB: int) -> bool:
        DOB_str = str(DOB)
        if len(DOB_str) == 8:
            try:
                year = int(DOB_str[:4])
                month = int(DOB_str[4:6])
                day = int(DOB_str[6:])
                if 1 <= month <= 12 and 1 <= day <= 31:
                    return True
            except ValueError:
                pass
        return False

    @DOB.setter
    def DOB(self, DOB: int) -> None:
        if self.is_valid_DOB(DOB):
            self._DOB = DOB
        else:
            raise ValueError("Date of Birth must be an integer in the format YYYYMMDD")

    @property
    def id_number(self) -> str:
        return self._id_number

    @staticmethod
    def is_valid_id_number(id_number: str) -> bool:
        return isinstance(id_number, str) and id_number.isdigit() and len(id_number) == 10

    @id_number.setter
    def id_number(self, id_number: str) -> None:
        if self.is_valid_id_number(id_number):
            self._id_number = id_number
        else:
            raise ValueError("ID Number must be a string of exactly 10 digits")

    @property
    def email(self) -> str:
        return self._email

    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @email.setter
    def email(self, email: str) -> None:
        if isinstance(email, str) and self.is_valid_email(email):
            self._email = email
        else:
            raise ValueError("Invalid email address")

    @property
    def income(self) -> Union[int, float]:
        return self._income

    @staticmethod
    def is_valid_income(income: Union[int, float]) -> bool:
        return isinstance(income, (int, float)) and income >= 0

    @income.setter
    def income(self, income: Union[int, float]) -> None:
        if self.is_valid_income(income):
            self._income = income
        else:
            raise ValueError("Income must be a non-negative number")

    @property
    def credit_score(self) -> int:
        return self._credit_score

    @credit_score.setter
    def credit_score(self, value: int) -> None:
        if 300 <= value <= 850:
            self._credit_score = value
        else:
            raise ValueError("Credit score must be between 300 and 850")

    @property
    def last_four(self) -> str:
        if self._hashed_ssn:
            return self._hashed_ssn[-4:]
        return None

    @property
    def ssn(self) -> str:
        raise AttributeError("SSN is write-only")

    @ssn.setter
    def ssn(self, ssn: str) -> None:
        self._hashed_ssn = self.hash_ssn_with_bcrypt(ssn)

    def verify_ssn(self, ssn: str) -> bool:
        return self.verify_ssn_with_bcrypt(ssn, self._hashed_ssn)

    @staticmethod
    def hash_ssn_with_bcrypt(ssn: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(ssn.encode(), salt)
        return hashed

    @staticmethod
    def verify_ssn_with_bcrypt(ssn: str, hashed_ssn: str) -> bool:
        return bcrypt.checkpw(ssn.encode(), hashed_ssn)

    @property
    def accounts(self) -> List["Account"]:
        return [account for account in Account.all.values() if account.client == self]

    def __repr__(self) -> str:
        return f'<Client name={self.name}>'


    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Client instances """
        sql = """
              CREATE TABLE IF NOT EXISTS clients (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              address TEXT NOT NULL,
              DOB INTEGER NOT NULL,
              id_number TEXT NOT NULL,
              email TEXT NOT NULL,
              income REAL NOT NULL,
              credit_score INTEGER NOT NULL,
              hashed_ssn TEXT,
              UNIQUE (id_number),
              CHECK (credit_score BETWEEN 300 AND 850)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Client instances """
        sql = """
            DROP TABLE IF EXISTS clients;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, address, DOB, id_number, email, income, credit_score, and ssn values of the current Client object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO clients ( name, address, DOB, id_number, email, income, credit_score, ssn)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.address, self.DOB, self.id_number, self.email, self.income, self.credit_score, self.ssn))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Client instance."""
        sql = """
            UPDATE clients
            SET name = ?, address = ?, DOB = ?, id_number = ?, email = ?, income = ?, credit_score = ?, ssn = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.address, self.DOB, self.id_number, self.email, self.income, self.credit_score, self.ssn))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Client instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM clients
            WHERE id = ?
        """

        CURSOR.execute
