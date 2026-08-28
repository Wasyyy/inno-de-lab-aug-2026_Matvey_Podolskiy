select 
first_name,
last_name,
age,
country
from customers c 
where age>25 
and country in ('USA');
