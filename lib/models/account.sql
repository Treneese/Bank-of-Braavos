CREATE TABLE Accounts (
    account_number BIGINT PRIMARY KEY,
    routing_number BIGINT NOT NULL,
    account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('Saving', 'Checking', 'Business', 'Credit')),
    balance DECIMAL(15, 2) NOT NULL,
    client_id INTEGER NOT NULL, -- Renamed to client_id for consistency
    FOREIGN KEY (client_id) REFERENCES Clients (id)
);

INSERT INTO Accounts (account_number, routing_number, account_type, balance, client_id)
VALUES 
    -- Add your values here, for example:
    (1234567890123456, 987654321, 'Saving', 1000.00, 1),
    (1234567890123457, 987654322, 'Checking', 2000.00, 2);

-- If you need to uncomment and use the PaymentHistory table, here is the corrected version
-- CREATE TABLE PaymentHistory (
--     id SERIAL PRIMARY KEY,
--     account_number BIGINT NOT NULL,
--     payment_date DATE NOT NULL,
--     amount DECIMAL(15, 2) NOT NULL,
--     description TEXT,
--     FOREIGN KEY (account_number) REFERENCES Accounts (account_number)
-- );