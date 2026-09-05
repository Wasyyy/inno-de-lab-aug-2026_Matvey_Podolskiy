select 
item,
avg(amount) as avg_amount,
count(*)
from orders o 
group by item ;