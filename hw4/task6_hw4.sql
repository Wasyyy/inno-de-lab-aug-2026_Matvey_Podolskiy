SELECT p.ProjectName 
FROM Projects p
JOIN EmployeeProjects ep ON p.ProjectID = ep.ProjectID
JOIN Employees e ON ep.EmployeeID = e.EmployeeID
WHERE e.FirstName = 'Bob' AND e.LastName = 'Johnson' AND ep.HoursWorked > 150;

UPDATE Projects p
SET Budget = Budget * 1.10
WHERE EXISTS (
    SELECT 1 
    FROM EmployeeProjects ep
    JOIN Employees e ON ep.EmployeeID = e.EmployeeID
    WHERE ep.ProjectID = p.ProjectID AND e.Department = 'Senior IT'
);

UPDATE Projects
SET EndDate = StartDate + INTERVAL '1 year'
WHERE EndDate IS NULL;

BEGIN;

DO $$
DECLARE
    new_emp_id INT;
    proj_id INT;
BEGIN
    SELECT ProjectID INTO proj_id FROM Projects WHERE ProjectName = 'Website Redesign' LIMIT 1;
    
    IF proj_id IS NULL THEN
        INSERT INTO Projects (ProjectName, Budget, StartDate) 
        VALUES ('Website Redesign', 30000.00, CURRENT_DATE)
        RETURNING ProjectID INTO proj_id;
    END IF;

    INSERT INTO Employees (FirstName, LastName, Department, Salary, Email)
    VALUES ('Alex', 'Muller', 'Senior IT', 60000.00, 'alex.muller@company.com')
    RETURNING EmployeeID INTO new_emp_id;

    INSERT INTO EmployeeProjects (EmployeeID, ProjectID, HoursWorked)
    VALUES (new_emp_id, proj_id, 80.0);
END $$;

COMMIT;

SELECT * FROM Projects;
SELECT * FROM EmployeeProjects;
