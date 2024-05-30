import bcrypt
import re
import ipdb

class Client:

    def __init__(self, name, address, DOB, id_number, email, income, credit_score, id=None):
        ipdb.set_trace()
        self.id = id
        self.name = name
        self.address = address
        self.DOB = DOB
        self.id_number = id_number
        self.email = email
        self.income = income
        self.credit_score = credit_score

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        ipdb.set_trace()
        if isinstance(name, str):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def address(self):
        return self._address

    @staticmethod
    def is_valid_address(address):
        ipdb.set_trace()
        # Simple validation: contains at least one digit and some alphabetic characters
        return bool(re.search(r'\d', address)) and bool(re.search(r'[a-zA-Z]', address))

    @address.setter
    def address(self, address):
        ipdb.set_trace()
        if isinstance(address, str) and self.is_valid_address(address):
            self._address = address
        else:
            raise ValueError("Invalid street address")

    @property
    def DOB(self):
        return self._DOB

    @DOB.setter
    def DOB(self, DOB):
        # Ensures DOB is an integer in the format YYYYMMDD
        DOB_str = str(DOB)
        if len(DOB_str) == 8:
            try:
                year = int(DOB_str[:4])
                month = int(DOB_str[4:6])
                day = int(DOB_str[6:])
                if 1 <= month <= 12 and 1 <= day <= 31:
                    self._DOB = DOB
                else:
                    raise ValueError("Invalid date of birth")
            except ValueError:
                raise ValueError("Invalid date of birth")
        else:
            raise ValueError("Date of Birth must be an integer in the format YYYYMMDD")

    @property
    def id_number(self):
        return self._id_number

    @staticmethod
    def is_valid_id_number(id_number):
        return isinstance(id_number, str) and id_number.isdigit() and len(id_number) == 10

    @id_number.setter
    def id_number(self, id_number):
        ipdb.set_trace()
        if self.is_valid_id_number(id_number):
            self._id_number = id_number
        else:
            raise ValueError("ID Number must be a string of exactly 10 digits")

    @property
    def email(self):
        return self._email

    @staticmethod
    def is_valid_email(email):
        ipdb.set_trace()
        # Simple regex for email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @email.setter
    def email(self, email):
        ipdb.set_trace()
        if isinstance(email, str) and self.is_valid_email(email):
            self._email = email
        else:
            raise ValueError("Invalid email address")

    @property
    def income(self):
        return self._income

    @staticmethod
    def is_valid_income(income):
        return isinstance(income, (int, float)) and income >= 0

    @income.setter
    def income(self, income):
        ipdb.set_trace()
        if self.is_valid_income(income):
            self._income = income
        else:
            raise ValueError("Income must be a non-negative number")

    @property
    def credit_score(self):
        return self._credit_score

    @credit_score.setter
    def credit_score(self, value):
        ipdb.set_trace()
        # Assuming credit score should be within a certain range (for example, 300 to 850)
        if value < 300 or value > 850:
            raise ValueError("Credit score must be between 300 and 850")
        self._credit_score = value

    @property
    def last_four(self):
        ipdb.set_trace()
        # Returning the last four digits of the ID number for simplicity
        if self._id_number:
            return self._id_number[-4:]
        return None

    @property
    def ssn(self):
        raise AttributeError("SSN is write-only")

    @ssn.setter
    def ssn(self, ssn):
        ipdb.set_trace()
        self._hashed_ssn = self.hash_ssn_with_bcrypt(ssn)

    def verify_ssn(self, ssn):
        ipdb.set_trace()
        return self.verify_ssn_with_bcrypt(ssn, self._hashed_ssn)

    @staticmethod
    def hash_ssn_with_bcrypt(ssn):
        ipdb.set_trace()
        salt = bcrypt.gensalt()  # Automatically generates a salt
        hashed = bcrypt.hashpw(ssn.encode(), salt)
        return hashed

    @staticmethod
    def verify_ssn_with_bcrypt(ssn, hashed_ssn):
        ipdb.set_trace()
        return bcrypt.checkpw(ssn.encode(), hashed_ssn)
