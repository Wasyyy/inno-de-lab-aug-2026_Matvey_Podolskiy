select 
s.status,
c.first_name, 
c.last_name 
from shippings s join customers c 
on c.customer_id = s.customer  ;
