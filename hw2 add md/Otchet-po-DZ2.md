# Отчет по ДЗ2

## Part 1: Выбор сценария

Для данной работы выбран сценарий: система продажи билетов на мероприятия. Эта система будет управлять площадками, зонами площадок, мероприятиями, посетителями и купленными билетами. Система позволяет учитывать разные зоны на площадке (VIP, партер, балкон и др.) с различной стоимостью билетов.

## Part 2: Проектирование базы данных и документация

### Идентификация сущностей и атрибутов

1. Площадки (Venues) — информация о местах проведения мероприятий.
2. Зоны площадки (Zones) — различные зоны внутри площадки с вместимостью и базовой ценой.
3. Мероприятия (Events) — информация о проводимых мероприятиях.
4. Посетители (Visitors) — информация о покупателях билетов.
5. Билеты (Tickets) — информация о приобретённых билетах.

### Проектирование таблиц

#### 1. Table Name: Venues

Description: Хранит информацию о площадках проведения мероприятий.

Attributes:
- venue_id: INTEGER, PK, NOT NULL, UNIQUE
- venue_name: VARCHAR(200), NOT NULL
- address: VARCHAR(300), NOT NULL
- city: VARCHAR(100), NOT NULL

Constraints:
- PK_Venues: PRIMARY KEY (venue_id)

#### 2. Table Name: Zones

Description: Хранит информацию о зонах внутри площадки.

Attributes:
- zone_id: INTEGER, PK, NOT NULL, UNIQUE
- venue_id: INTEGER, FK (REFERENCES Venues), NOT NULL
- zone_name: VARCHAR(100), NOT NULL
- capacity: INTEGER, NOT NULL
- base_price: NUMERIC(10,2), NOT NULL

Constraints:
- PK_Zones: PRIMARY KEY (zone_id)
- FK_Zones_Venues: FOREIGN KEY (venue_id) REFERENCES Venues(venue_id)
- CHK_Capacity: CHECK (capacity > 0)
- CHK_BasePrice: CHECK (base_price > 0)
- UQ_ZoneName: UNIQUE (venue_id, zone_name)

#### 3. Table Name: Events

Description: Содержит информацию о мероприятиях.

Attributes:
- event_id: INTEGER, PK, NOT NULL, UNIQUE
- venue_id: INTEGER, FK (REFERENCES Venues), NOT NULL
- event_name: VARCHAR(200), NOT NULL
- event_date: TIMESTAMP, NOT NULL
- organizer: VARCHAR(200)

Constraints:
- PK_Events: PRIMARY KEY (event_id)
- FK_Events_Venues: FOREIGN KEY (venue_id) REFERENCES Venues(venue_id)

#### 4. Table Name: Visitors

Description: Хранит данные о посетителях.

Attributes:
- visitor_id: INTEGER, PK, NOT NULL, UNIQUE
- first_name: VARCHAR(100), NOT NULL
- last_name: VARCHAR(100), NOT NULL
- email: VARCHAR(255), NOT NULL, UNIQUE
- phone: VARCHAR(20)

Constraints:
- PK_Visitors: PRIMARY KEY (visitor_id)
- UQ_Email: UNIQUE (email)

#### 5. Table Name: Tickets

Description: Таблица для реализации связи многие-ко-многим между посетителями и мероприятиями. Хранит информацию о приобретённых билетах.

Attributes:
- ticket_id: INTEGER, PK, NOT NULL, UNIQUE
- event_id: INTEGER, FK (REFERENCES Events), NOT NULL
- zone_id: INTEGER, FK (REFERENCES Zones), NOT NULL
- visitor_id: INTEGER, FK (REFERENCES Visitors), NOT NULL
- seat_number: VARCHAR(20), NOT NULL
- purchase_date: TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP
- ticket_price: NUMERIC(10,2), NOT NULL

Constraints:
- PK_Tickets: PRIMARY KEY (ticket_id)
- FK_Tickets_Events: FOREIGN KEY (event_id) REFERENCES Events(event_id)
- FK_Tickets_Zones: FOREIGN KEY (zone_id) REFERENCES Zones(zone_id)
- FK_Tickets_Visitors: FOREIGN KEY (visitor_id) REFERENCES Visitors(visitor_id)
- CHK_TicketPrice: CHECK (ticket_price > 0)
- UQ_EventSeat: UNIQUE (event_id, zone_id, seat_number)

### Взаимосвязи

#### Venues и Zones (Один-ко-Многим)
Одна площадка может содержать множество зон, но каждая зона принадлежит только одной площадке.

- Zones.venue_id является внешним ключом, ссылающимся на Venues.venue_id.

#### Venues и Events (Один-ко-Многим)
На одной площадке может проводиться множество мероприятий, но каждое мероприятие проходит только на одной площадке.

- Events.venue_id является внешним ключом, ссылающимся на Venues.venue_id.

#### Events и Tickets (Один-ко-Многим)
Одно мероприятие может иметь множество проданных билетов, но каждый билет относится к одному конкретному мероприятию.

- Tickets.event_id является внешним ключом, ссылающимся на Events.event_id.

#### Zones и Tickets (Один-ко-Многим)
Одна зона может содержать множество билетов, но каждый билет относится к одной конкретной зоне.

- Tickets.zone_id является внешним ключом, ссылающимся на Zones.zone_id.

#### Visitors и Tickets (Один-ко-Многим)
Один посетитель может приобрести множество билетов, но каждый билет принадлежит одному посетителю.

- Tickets.visitor_id является внешним ключом, ссылающимся на Visitors.visitor_id.

#### Visitors и Events (Многие-ко-Многим)
Посетитель может посещать множество мероприятий, а каждое мероприятие может посещаться множеством посетителей.

- Связь реализуется через таблицу Tickets, содержащую внешние ключи event_id и visitor_id.

## Part 3: ER-диаграмма

![](./media/image1.png)
