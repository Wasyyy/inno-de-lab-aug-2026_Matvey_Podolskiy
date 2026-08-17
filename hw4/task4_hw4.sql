UPDATE Employees 
SET Salary = Salary * 1.10 
WHERE Department = 'HR';

UPDATE Employees 
SET Department = 'Senior IT' 
WHERE Salary > 70000.00;

DELETE FROM Employees e
WHERE NOT EXISTS (
    SELECT 1 
    FROM EmployeeProjects ep 
    WHERE ep.EmployeeID = e.EmployeeID
);

BEGIN;

INSERT INTO Projects (ProjectName, Budget, StartDate) 
VALUES ('New Automation Project', 50000.00, CURRENT_DATE);

INSERT INTO EmployeeProjects (EmployeeID, ProjectID, HoursWorked)
VALUES 
((SELECT EmployeeID FROM Employees LIMIT 1), currval('projects_projectid_seq'), 40.0),
((SELECT EmployeeID FROM Employees OFFSET 1 LIMIT 1), currval('projects_projectid_seq'), 25.5);

COMMIT;

SELECT * FROM Employees; 
SELECT * FROM EmployeeProjects;