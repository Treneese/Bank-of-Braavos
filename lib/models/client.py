# lib/models/client.py
from .__init__ import CURSOR, CONN
import bcrypt
import re
from .account import Account

class Client:

    all = {}

    def __init__(self, name, address, DOB, id_number, email, income, credit_score,  id=None):
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


    # Saves an client to the database
    def save(self):
        """ Insert a new row with the name of the client object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        
        sql = """
                INSERT INTO clients (name, address, DOB, id_number, email, income, credit_score, id)
                VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.address, self.DOB, self. id_number, self.email, self.income, self.cred_score, self.id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    #? Creates and saves client to the database
    @classmethod
    def create(cls, name, address, DOB, id_number, email, income, credit_score,  id=None):
        """ Initialize a new Client instance and save the object to the database """
        client = cls(name, address, DOB, id_number, email, income, credit_score,  id=None)
        client.save()
        return client

    #? Deletes client from database
    def delete(self):
        """Delete the table row corresponding to the current client instance,
        delete the client entry, and reassign id attribute"""

        sql = """
            DELETE FROM clients
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None
    

    #? Checks to see if a client exists in database
    @classmethod
    def instance_from_db(cls, row):
        """Return an client object having the attribute values from the table row."""

        #Check the dictionary for an existing instance using the row's primary key
        client = cls.all.get(row[0])
        if client:
            # ensure attributes match row values in case local instance was modified
            client.name = row[1]
            client.address = row[2]
            client.DOB = row[3]
            client.id_number = row[4]
            client.email = row[5]
            client.income = row[6]
            client.credit_score = row[7]
            name, address, DOB, id_number, email, income, credit_score,  id=None
        else:
            # not in dictionary, create new instance and add to dictionary
            client = cls(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            client.id = row[4]
            cls.all[client.id] = client
        return client

    #? Returns list of all clients from database
    @classmethod 
    def get_all(cls):
        """Return a list containing a client object per row in the table"""
        sql = """
            SELECT *
            FROM client
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    #? Finds a client from database by their id
    @classmethod 
    def find_by_id(cls, id):
        """Return a client object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM clients
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    #? Finds client from database by their name
    @classmethod
    def find_by_name(cls, name):
        """Return a client object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM clients
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    #? Finds all accounts of clients instance from database
    def find_all_accs(self):
        """Return a list of account objects associated with this client"""
        try:
            return [account for account in Account.get_all() if account.client_id == self.id]
        except: Exception("No accounts found by client")