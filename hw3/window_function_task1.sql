select 
o.amount ,
o.customer_id, 
o.item ,
o.order_id ,
sum(amount) over(partition by o.customer_id ) as total_by_customer
from orders o;