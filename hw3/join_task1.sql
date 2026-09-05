select 
o.item ,
o.amount ,
c.first_name ,
c.last_name 
from orders o join customers c 
on c.customer_id = o.customer_id ;