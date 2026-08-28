select
c.country ,
count(*)
from customers c 
group by c.country 