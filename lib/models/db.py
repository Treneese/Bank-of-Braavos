import sqlite3


CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()

def initialize_db():
    """Initialize the database by creating the necessary tables."""
    try:
        with CONN:
            CURSOR.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    DOB INTEGER NOT NULL,
                    id_number TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL,
                    income REAL NOT NULL,
                    credit_score INTEGER NOT NULL,
                    hashed_ssn TEXT,
                    CHECK (credit_score BETWEEN 300 AND 850)
                )
            """)
            CURSOR.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_number BIGINT PRIMARY KEY,
                    routing_number BIGINT NOT NULL,
                    account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('Saving', 'Checking', 'Business', 'Credit')),
                    balance DECIMAL(15, 2) NOT NULL,
                    client_id INTEGER NOT NULL,
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                )
            """)
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")

def close_db():
    """Close the database connection."""
    try:
        CURSOR.close()
        CONN.close()
    except sqlite3.Error as e:
        print(f"An error occurred while closing the database: {e}")