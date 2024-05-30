CREATE TABLE Accounts (
    account_number BIGINT PRIMARY KEY,
    routing_number BIGINT NOT NULL,
    account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('Saving', 'Checking', 'Business', 'Credit')),
    balance DECIMAL(15, 2) NOT NULL
    FOREIGN KEY (client) REFERENCES Clients (client)
);


INSERT INTO accounts (account_number, routing_number, account_type, balance, client)
VALUES 



-- CREATE TABLE PaymentHistory (
--     id SERIAL PRIMARY KEY,
--     account_number BIGINT NOT NULL,
--     payment_date DATE NOT NULL,
--     amount DECIMAL(15, 2) NOT NULL,
--     description TEXT,
--     FOREIGN KEY (account_number) REFERENCES Accounts (account_number)
-- );


