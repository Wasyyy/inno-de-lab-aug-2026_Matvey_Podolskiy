CREATE TABLE Departments (
    DepartmentID SERIAL PRIMARY KEY,
    DepartmentName VARCHAR(50) UNIQUE NOT NULL,
    Location VARCHAR(50)
);

ALTER TABLE Employees
ADD COLUMN Email VARCHAR(100);


UPDATE Employees
SET Email = 'smith+alice@gmail.com'
WHERE EmployeeID = 1;


UPDATE Employees
SET Email = 'johnson+bob@gmail.com'
WHERE EmployeeID = 2;


UPDATE Employees
SET Email = 'brown+charlie@gmail.com'
WHERE EmployeeID = 3;


UPDATE Employees
SET Email = 'prince+diana@gmail.com'
WHERE EmployeeID = 4;

UPDATE Employees
SET Email = 'robinson+mat@gmail.com'
WHERE EmployeeID = 6;


UPDATE Employees
SET Email = 'barinson+tom@gmail.com'
WHERE EmployeeID = 7;


ALTER TABLE Employees
ADD CONSTRAINT employees_email_unique UNIQUE (Email);


ALTER TABLE Departments
RENAME COLUMN Location TO OfficeLocation;
