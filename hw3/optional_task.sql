select 
CONCAT(first_name, ' ', last_name) AS full_name,
country, 
count(*) as total_orders,
SUM(amount) as total_amount
from orders o 
join customers c on c.customer_id = o.customer_id 
join shippings s on o.customer_id = s.customer 
where s.status = 'Delivered'
group by 
c.first_name ,
c.last_name ,
c.country ,
o.customer_id
having count(*) >= 2 ;

