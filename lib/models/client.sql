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
('John Doe', '123 Main St', 19800101, 'ID123456', 'john.doe@example.com', 75000.00, 720, 'hashed_ssn_value'),
('Jane Smith', '456 Elm St', 19900202, 'ID654321', 'jane.smith@example.com', 82000.00, 680, 'hashed_ssn_value'),
('Emily Johnson', '789 Maple St', 19750315, 'ID789012', 'emily.johnson@example.com', 90000.00, 750, 'hashed_ssn_value');
