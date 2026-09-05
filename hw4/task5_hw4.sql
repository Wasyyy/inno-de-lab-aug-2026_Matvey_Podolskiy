CREATE OR REPLACE FUNCTION CalculateAnnualBonus(employee_id INT, salary NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    RETURN salary * 0.10;
END;
$$ LANGUAGE plpgsql;

SELECT EmployeeID, FirstName, LastName, Salary, CalculateAnnualBonus(EmployeeID, Salary) AS AnnualBonus
FROM Employees;

CREATE OR REPLACE VIEW IT_Department_View AS
SELECT EmployeeID, FirstName, LastName, Salary
FROM Employees
WHERE Department = 'Senior IT';

SELECT * FROM IT_Department_View;
