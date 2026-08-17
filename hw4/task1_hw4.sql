insert into employees (firstname, lastname, department, salary) values 
('Mat', 'Robinson', 'HR', 72000.00),
('Tom', 'Barinson', 'Finance', 77000.00);

select * from employees e ;

select 
lastname,
firstname
from employees e 
where e.department = 'IT';

update employees e 
set salary = 65000.00
where e.employeeid = 1;

delete from employees 
where employeeid = 5;

select * from employees e ;
