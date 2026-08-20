# Проектирование Data Warehouse

**Бизнес-область:** Продажа билетов на мероприятия

## 1. Бизнес-процесс

Для проектирования хранилища данных выбран бизнес-процесс «Продажа билетов на мероприятия» — тот же сценарий, что использовался в ДЗ2 (OLTP-модель с сущностями Venues, Zones, Events, Visitors, Tickets). Этот процесс отражает транзакции покупки билетов посетителями на конкретные мероприятия, проходящие в конкретных зонах конкретных площадок.

Выбор обоснован тем, что процесс продажи билетов — классический пример измеримого, повторяющегося транзакционного процесса с чёткими количественными показателями (цена, количество, выручка) и естественным набором контекстных измерений (кто купил, что за мероприятие, где, когда, в какой зоне) — то есть идеально подходит для мультиизмеримого анализа в DW.

## 2. Уровень детализации (Grain)

Grain определён как: одна строка таблицы фактов = один проданный билет (одна позиция ticket в таблице Tickets из OLTP-модели).

Это самый низкий разумный уровень детализации, который сохраняет максимальную гибкость анализа: он позволяет агрегировать данные на любом более высоком уровне (по мероприятию, по площадке, по зоне, по посетителю, по дню/месяцу/году), не теряя возможности "провалиться" (drill-down) до конкретного билета и места.

## 3. Таблицы измерений (Dimension Tables)

Определены 5 измерений, из них 4 подключены напрямую к таблице фактов, а Dim_Venue является измерением-"снежинкой" (outrigger), на которое ссылаются Dim_Event и Dim_Zone — так как и мероприятие, и зона логически принадлежат конкретной площадке.

### 3.1 Dim_Venue (площадка)

| Атрибут | Тип | Описание |
|---|---|---|
| venue_key | integer, PK | Суррогатный ключ |
| venue_id | integer | Бизнес-ключ из OLTP (Venues.venue_id) |
| venue_name | varchar(200) | Название площадки |
| address | varchar(300) | Адрес |
| city | varchar(100) | Город (для географического анализа) |

### 3.2 Dim_Zone (зона площадки)

| Атрибут | Тип | Описание |
|---|---|---|
| zone_key | integer, PK | Суррогатный ключ |
| zone_id | integer | Бизнес-ключ (Zones.zone_id) |
| venue_key | integer, FK | Ссылка на Dim_Venue (снежинка) |
| zone_name | varchar(100) | Название зоны (VIP, партер, балкон…) |
| capacity | integer | Вместимость зоны |
| base_price | numeric(10,2) | Базовая цена зоны |

### 3.3 Dim_Event (мероприятие)

| Атрибут | Тип | Описание |
|---|---|---|
| event_key | integer, PK | Суррогатный ключ |
| event_id | integer | Бизнес-ключ (Events.event_id) |
| venue_key | integer, FK | Ссылка на Dim_Venue (снежинка) |
| event_name | varchar(200) | Название мероприятия |
| event_date | date | Дата проведения |
| event_category | varchar(100) | Категория (концерт/спорт/театр) — расширение для аналитики |
| organizer | varchar(200) | Организатор |

### 3.4 Dim_Visitor (посетитель)

| Атрибут | Тип | Описание |
|---|---|---|
| visitor_key | integer, PK | Суррогатный ключ |
| visitor_id | integer | Бизнес-ключ (Visitors.visitor_id) |
| first_name | varchar(100) | Имя |
| last_name | varchar(100) | Фамилия |
| email | varchar(255) | Email |
| phone | varchar(20) | Телефон |

### 3.5 Dim_Date (дата)

| Атрибут | Тип | Описание |
|---|---|---|
| date_key | integer, PK | Формат YYYYMMDD |
| full_date | date | Календарная дата |
| day / month / year | integer | Компоненты даты |
| month_name | varchar(20) | Название месяца |
| quarter | integer | Квартал (1–4) |
| day_of_week | varchar(20) | День недели |
| is_weekend | boolean | Признак выходного дня |

## 4. Таблица фактов (Fact Table)

Fact_Ticket_Sales — таблица фактов транзакционного типа (transaction fact table) на уровне гранулярности "один билет".

| Атрибут | Тип | Описание |
|---|---|---|
| ticket_sales_key | bigint, PK | Суррогатный ключ строки факта |
| date_key | integer, FK | Ссылка на Dim_Date (дата покупки билета) |
| event_key | integer, FK | Ссылка на Dim_Event |
| zone_key | integer, FK | Ссылка на Dim_Zone |
| visitor_key | integer, FK | Ссылка на Dim_Visitor |
| ticket_id | integer | Degenerate dimension — номер билета из OLTP |
| seat_number | varchar(20) | Degenerate dimension — номер места |
| ticket_price | numeric(10,2) | Мера: цена билета (аддитивная) |
| discount_amount | numeric(10,2) | Мера: скидка (аддитивная) |
| net_revenue | numeric(10,2) | Мера: чистая выручка = ticket_price − discount_amount |
| ticket_qty | integer | Мера: количество (всегда 1 на строку — для удобства SUM/COUNT) |

**Метрики (measures):**

- ticket_price — цена билета на момент продажи (аддитивная мера).
- discount_amount — сумма скидки, если применялась (аддитивная).
- net_revenue — чистая выручка по билету; главная мера для анализа доходов (аддитивная).
- ticket_qty — количество (константа = 1 на строку), удобна для подсчёта числа проданных билетов через SUM.

Degenerate dimensions: ticket_id и seat_number хранятся прямо в таблице фактов, так как не имеют собственных описательных атрибутов и не образуют полноценное измерение — только идентифицируют конкретную транзакцию/место.

## 5. Физическая модель схемы

Выбрана Snowflake-схема (схема "снежинка"). Основная причина выбора: в исходной OLTP-модели зона (Zone) и мероприятие (Event) естественным образом связаны с площадкой (Venue) через отношение "один-ко-многим" (одна площадка → много зон, одна площадка → много мероприятий). Нормализация Dim_Venue в отдельную таблицу и подключение к ней Dim_Zone и Dim_Event устраняет дублирование атрибутов площадки (venue_name, address, city), которые иначе пришлось бы хранить избыточно в каждой строке Dim_Zone и Dim_Event при звёздной схеме.

Компромисс: снежинка требует на 1 JOIN больше в запросах, где нужны атрибуты площадки, но это оправдано за счёт экономии места и упрощения обновления данных о площадке (обновление в одном месте вместо каскадного обновления во всех связанных зонах/мероприятиях).

![Схема хранилища данных](./images/schema.png)

Диаграмма: fact_ticket_sales — таблица фактов; dim_date и dim_visitor подключены к ней напрямую; dim_event и dim_zone также подключены к факту напрямую, но дополнительно ссылаются на dim_venue (это и делает схему snowflake, а не star). Метка (bk) обозначает бизнес-ключ, унаследованный из исходной OLTP-системы.

## 6. Аналитические запросы (SQL)

Ниже приведён полный SQL-скрипт: DDL для создания таблиц и 5 аналитических запросов с комментариями, объясняющими, на какой бизнес-вопрос отвечает каждый запрос. Кратко:

- Запрос 1 — выручка и число билетов по каждому мероприятию (рейтинг мероприятий по доходу).
- Запрос 2 — выручка по типам зон в разрезе площадок (какие зоны/категории мест прибыльнее).
- Запрос 3 — динамика выручки по месяцам/кварталам (сезонность и тренды продаж).
- Запрос 4 — топ мероприятий по выручке в конкретном городе (для планирования будущих событий).
- Запрос 5 — самые ценные посетители по числу и сумме покупок (основа для программы лояльности).

```sql
-- =====================================================================
-- DDL: таблицы измерений и таблица фактов
-- =====================================================================

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

-- =====================================================================
-- Аналитические запросы
-- =====================================================================

-- Запрос 1. Выручка и число проданных билетов по каждому мероприятию.
-- Бизнес-вопрос: "Какие мероприятия принесли больше всего выручки?"
SELECT
    e.event_name,
    e.event_date,
    v.venue_name,
    v.city,
    SUM(f.ticket_qty)  AS tickets_sold,
    SUM(f.net_revenue) AS total_revenue
FROM Fact_Ticket_Sales f
JOIN Dim_Event e ON f.event_key = e.event_key
JOIN Dim_Venue v ON e.venue_key = v.venue_key
GROUP BY e.event_name, e.event_date, v.venue_name, v.city
ORDER BY total_revenue DESC;

-- Запрос 2. Выручка по типам зон (VIP, партер, балкон и т.д.) с разбивкой по площадкам.
-- Бизнес-вопрос: "Какие зоны/категории мест наиболее прибыльны и как это различается между площадками?"
SELECT
    vn.venue_name,
    z.zone_name,
    COUNT(*)                     AS tickets_sold,
    SUM(f.net_revenue)           AS total_revenue,
    ROUND(AVG(f.net_revenue), 2) AS avg_ticket_price
FROM Fact_Ticket_Sales f
JOIN Dim_Zone z   ON f.zone_key = z.zone_key
JOIN Dim_Venue vn ON z.venue_key = vn.venue_key
GROUP BY vn.venue_name, z.zone_name
ORDER BY vn.venue_name, total_revenue DESC;

-- Запрос 3. Динамика выручки по месяцам и кварталам.
-- Бизнес-вопрос: "Как меняются продажи билетов во времени (сезонность, рост/падение по кварталам)?"
SELECT
    d.year,
    d.quarter,
    d.month_name,
    SUM(f.ticket_qty)  AS tickets_sold,
    SUM(f.net_revenue) AS total_revenue
FROM Fact_Ticket_Sales f
JOIN Dim_Date d ON f.date_key = d.date_key
GROUP BY d.year, d.quarter, d.month, d.month_name
ORDER BY d.year, d.quarter, d.month;

-- Запрос 4. Топ мероприятий по выручке в конкретном городе.
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

-- Запрос 5. Самые активные посетители (по числу и сумме покупок).
-- Бизнес-вопрос: "Кто наши самые ценные клиенты и стоит ли делать программу лояльности для постоянных посетителей?"
SELECT
    vis.visitor_id,
    vis.first_name,
    vis.last_name,
    vis.email,
    COUNT(DISTINCT f.event_key) AS distinct_events_attended,
    SUM(f.ticket_qty)           AS total_tickets_bought,
    SUM(f.net_revenue)          AS total_spent
FROM Fact_Ticket_Sales f
JOIN Dim_Visitor vis ON f.visitor_key = vis.visitor_key
GROUP BY vis.visitor_id, vis.first_name, vis.last_name, vis.email
HAVING SUM(f.net_revenue) > 0
ORDER BY total_spent DESC;
```
