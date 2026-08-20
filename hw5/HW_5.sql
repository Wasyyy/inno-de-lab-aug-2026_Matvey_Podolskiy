CREATE TABLE Dim_Venue (
    venue_key     INTEGER PRIMARY KEY,      -- суррогатный ключ
    venue_id      INTEGER NOT NULL,         -- бизнес-ключ (из OLTP)
    venue_name    VARCHAR(200) NOT NULL,
    address       VARCHAR(300),
    city          VARCHAR(100) NOT NULL
);
 
CREATE TABLE Dim_Zone (
    zone_key      INTEGER PRIMARY KEY,
    zone_id       INTEGER NOT NULL,
    venue_key     INTEGER NOT NULL REFERENCES Dim_Venue(venue_key),
    zone_name     VARCHAR(100) NOT NULL,
    capacity      INTEGER,
    base_price    NUMERIC(10,2)
);
 
CREATE TABLE Dim_Event (
    event_key       INTEGER PRIMARY KEY,
    event_id        INTEGER NOT NULL,
    venue_key       INTEGER NOT NULL REFERENCES Dim_Venue(venue_key),
    event_name      VARCHAR(200) NOT NULL,
    event_date      DATE NOT NULL,
    event_category  VARCHAR(100),           -- концерт / спорт / театр и т.д.
    organizer       VARCHAR(200)
);
 
CREATE TABLE Dim_Visitor (
    visitor_key   INTEGER PRIMARY KEY,
    visitor_id    INTEGER NOT NULL,
    first_name    VARCHAR(100),
    last_name     VARCHAR(100),
    email         VARCHAR(255),
    phone         VARCHAR(20)
);
 
CREATE TABLE Dim_Date (
    date_key      INTEGER PRIMARY KEY,      
    full_date     DATE NOT NULL,
    day           INTEGER NOT NULL,
    month         INTEGER NOT NULL,
    month_name    VARCHAR(20) NOT NULL,
    quarter       INTEGER NOT NULL,
    year          INTEGER NOT NULL,
    day_of_week   VARCHAR(20) NOT NULL,
    is_weekend    BOOLEAN NOT NULL
);
 
CREATE TABLE Fact_Ticket_Sales (
    ticket_sales_key  BIGINT PRIMARY KEY,
    date_key          INTEGER NOT NULL REFERENCES Dim_Date(date_key),
    event_key         INTEGER NOT NULL REFERENCES Dim_Event(event_key),
    zone_key          INTEGER NOT NULL REFERENCES Dim_Zone(zone_key),
    visitor_key       INTEGER NOT NULL REFERENCES Dim_Visitor(visitor_key),
    ticket_id         INTEGER NOT NULL,     
    seat_number       VARCHAR(20) NOT NULL, 
    ticket_price      NUMERIC(10,2) NOT NULL,
    discount_amount   NUMERIC(10,2) DEFAULT 0,
    net_revenue       NUMERIC(10,2) NOT NULL,   -- цена билета - скидка
    ticket_qty        INTEGER NOT NULL DEFAULT 1
);
 
-- Аналитические запросы
 
-- Запрос 1. Выручка и число проданных билетов по каждому мероприятию.
-- Бизнес-вопрос: "Какие мероприятия принесли больше всего выручки?"
SELECT
    e.event_name,
    e.event_date,
    v.venue_name,
    v.city,
    SUM(f.ticket_qty)          AS tickets_sold,
    SUM(f.net_revenue)         AS total_revenue
FROM Fact_Ticket_Sales f
JOIN Dim_Event  e ON f.event_key = e.event_key
JOIN Dim_Venue  v ON e.venue_key = v.venue_key
GROUP BY e.event_name, e.event_date, v.venue_name, v.city
ORDER BY total_revenue DESC;
 
 
-- Запрос 2. Выручка по типам зон (VIP, партер, балкон и т.д.) с разбивкой по площадкам.
-- Бизнес-вопрос: "Какие зоны/категории мест наиболее прибыльны и как это различается между площадками?"
SELECT
    vn.venue_name,
    z.zone_name,
    COUNT(*)                         AS tickets_sold,
    SUM(f.net_revenue)               AS total_revenue,
    ROUND(AVG(f.net_revenue), 2)     AS avg_ticket_price
FROM Fact_Ticket_Sales f
JOIN Dim_Zone  z  ON f.zone_key = z.zone_key
JOIN Dim_Venue vn ON z.venue_key = vn.venue_key
GROUP BY vn.venue_name, z.zone_name
ORDER BY vn.venue_name, total_revenue DESC;
 
 
-- Запрос 3. Динамика выручки по месяцам и кварталам.
-- Бизнес-вопрос: "Как меняются продажи билетов во времени (сезонность, рост/падение по кварталам)?"
SELECT
    d.year,
    d.quarter,
    d.month_name,
    SUM(f.ticket_qty)     AS tickets_sold,
    SUM(f.net_revenue)    AS total_revenue
FROM Fact_Ticket_Sales f
JOIN Dim_Date d ON f.date_key = d.date_key
GROUP BY d.year, d.quarter, d.month, d.month_name
ORDER BY d.year, d.quarter, d.month;
 
 
-- Запрос 4. Топ-5 мероприятий по выручке в конкретном городе.
-- Бизнес-вопрос: "Какие мероприятия были самыми успешными в заданном городе (например, для планирования будущих событий там же)?"
SELECT
    e.event_name,
    e.event_date,
    vn.venue_name,
    SUM(f.net_revenue) AS total_revenue
FROM Fact_Ticket_Sales f
JOIN Dim_Event e  ON f.event_key = e.event_key
JOIN Dim_Venue vn ON e.venue_key = vn.venue_key
WHERE vn.city = 'Гомель'                
GROUP BY e.event_name, e.event_date, vn.venue_name
ORDER BY total_revenue DESC;
 
 
-- Запрос 5 Самые активные посетители (по числу и сумме покупок)
-- Бизнес-вопрос: "Кто наши самые ценные клиенты и стоит ли делать программу лояльности для постоянных посетителей?"
SELECT
    vis.visitor_id,
    vis.first_name,
    vis.last_name,
    vis.email,
    COUNT(DISTINCT f.event_key)  AS distinct_events_attended,
    SUM(f.ticket_qty)            AS total_tickets_bought,
    SUM(f.net_revenue)           AS total_spent
FROM Fact_Ticket_Sales f
JOIN Dim_Visitor vis ON f.visitor_key = vis.visitor_key
GROUP BY vis.visitor_id, vis.first_name, vis.last_name, vis.email
HAVING SUM(f.net_revenue) > 0
ORDER BY total_spent DESC;
