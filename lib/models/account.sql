CREATE TABLE Accounts (
    account_number BIGINT PRIMARY KEY,
    routing_number BIGINT NOT NULL,
    account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('Saving', 'Checking', 'Business', 'Credit')),
    balance DECIMAL(15, 2) NOT NULL
    client TEXT NOT NULL,
    FOREIGN KEY (client) REFERENCES Clients (name)
);


INSERT INTO accounts (account_number, routing_number, account_type, balance, client)
VALUES 

(1234567890123456, 111000025, 'Saving', 1500.75, Jane Smith),
(1234567890123457, 111000026, 'Checking', 2500.00, John Doe),
(1234567890123458, 111000027, 'Business', 10000.00, Emily Johnson);

-- CREATE TABLE PaymentHistory (
--     id SERIAL PRIMARY KEY,
--     account_number BIGINT NOT NULL,
--     payment_date DATE NOT NULL,
--     amount DECIMAL(15, 2) NOT NULL,
--     description TEXT,
--     FOREIGN KEY (account_number) REFERENCES Accounts (account_number)
-- );