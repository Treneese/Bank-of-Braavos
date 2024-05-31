SELECT * 
FROM Accounts
JOIN Clients ON Accounts.client = Clients.id
WHERE Clients.id = 1;