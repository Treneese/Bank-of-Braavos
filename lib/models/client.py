# lib/models/client.py
import bcrypt

class Client:

    all = {}

    def __init__(self, name, address, DOB, id_number, email, income, education, credit_score,  id=None):
        self.id = id
        self.name = name
        self.address = address
        self.DOB = DOB
        self.id_number = id_number
        self.email = email
        self.income = income
        # self.education = education
        self.credit_score = credit_score

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )
        
    @property
    def address(self):
        return self._address
    
    @staticmethod
    def is_valid_address(address):
        # Simple validation: contains at least one digit and some alphabetic characters
        return bool(re.search(r'\d', address)) and bool(re.search(r'[a-zA-Z]', address))
    
    @address.setter
    def address(self, address):
        if isinstance(address, str) and self.is_valid_address(address):
            self._address = address
        else:
            raise ValueError("Invalid street address")

    @property
    def DOB(self):
        return self._DOB
    
    @staticmethod
    def is_valid_DOB(DOB):
        if isinstance(DOB, int):
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
    def DOB(self, DOB):
        if self.is_valid_DOB(DOB):
            self._DOB = DOB
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
        if self.is_valid_id_number(id_number):
            self._id_number = id_number
        else:
            raise ValueError("ID Number must be a string of exactly 10 digits")
   
    @property
    def email(self):
        return self._email

    @staticmethod
    def is_valid_email(email):
    # Simple regex for email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @email.setter
    def email(self, email):
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
        if self.is_valid_income(income):
            self._income = income
        else:
            raise ValueError("Income must be a non-negative number")

    @property
    def credit_score(self):
        return self._credit_score
    
    @credit_score.setter
    def credit_score(self, value):
        # Assuming credit score should be within a certain range (for example, 300 to 850)
        if value < 300 or value > 850:
            raise ValueError("Credit score must be between 300 and 850")
        self._credit_score = value

    @property
    def last_four(self):
        if self._plain_ssn:
            return self._plain_ssn[-4:]
        return None
    
    @property
    def ssn(self):
        raise AttributeError("SSN is write-only")

    @ssn.setter
    def ssn(self, ssn):
        self._hashed_ssn = self.hash_ssn_with_bcrypt(ssn)
    
    def verify_ssn(self, ssn):
        return self.verify_ssn_with_bcrypt(ssn, self._hashed_ssn)

    @staticmethod
    def hash_ssn_with_bcrypt(ssn):
        salt = bcrypt.gensalt()  # Automatically generates a salt
        hashed = bcrypt.hashpw(ssn.encode(), salt)
        return hashed

    @staticmethod
    def verify_ssn_with_bcrypt(ssn, hashed_ssn):
        if bcrypt.checkpw(ssn.encode(), hashed_ssn):
            print("It Matches!")
        else:
            print("It Does not Match :(")
