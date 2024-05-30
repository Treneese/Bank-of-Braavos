CREATE TABLE Clients (
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
);

INSERT INTO clients (name, address, DOB, id_numbe, email, income, credit_score, hashed_ssn, id_number,) VALUES
