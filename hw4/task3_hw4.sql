CREATE ROLE hr_user WITH LOGIN PASSWORD 'secure_password123';
GRANT SELECT ON Employees TO hr_user;
GRANT INSERT, UPDATE ON Employees TO hr_user;

SELECT * FROM Employees;

INSERT INTO Employees (FirstName, LastName, Department, Salary) 
VALUES ('Test', 'User', 'HR', 40000.00);

GRANT INSERT, UPDATE ON Employees TO hr_user;

INSERT INTO Employees (FirstName, LastName, Department, Salary) 
VALUES ('Janson', 'Button', 'HR', 48000.00);

UPDATE Employees 
SET Salary = 52000.00 
WHERE FirstName = 'Janson' AND LastName = 'Button';