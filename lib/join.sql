SELECT * FROM accounts
JOIN clients ON accounts.client.id = client.id
WHERE client.id = 1;