# lib/models/client.py
import bcrypt
import re
from models.account import Account
from typing import List, Union, Dict



class Client:
    all: Dict[int, "Client"] = {}

    def __init__(self, name: str, address: str, DOB: int, id_number: str, email: str, income: Union[int, float], credit_score: int, id: int = None):
        self.id = id
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
