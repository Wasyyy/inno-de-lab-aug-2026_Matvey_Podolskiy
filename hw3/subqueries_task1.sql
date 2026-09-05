select 
c.first_name ,
c.last_name ,
o.amount
from customers c join orders o on 
c.customer_id= o.customer_id
where amount = (select MAX(amount)
from orders o);