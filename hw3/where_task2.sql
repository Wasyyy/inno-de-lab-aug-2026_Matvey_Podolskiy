select 
o.order_id, 
o.item, 
o.amount,
o.customer_id 
from orders o
where o.amount > 1000;
