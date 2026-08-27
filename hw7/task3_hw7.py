# Конфигурационный словарь, полученный от сервиса инициализации
db_config = {
    "connection": {
        "host": "production-db.internal",
        "port": 5432,
        "user": "postgres"
    }
}

# Извлечение host и port из вложенного словаря connection
connection = db_config["connection"]
host = connection.get("host")
port = connection.get("port")

# Проверка наличия ssl_settings и вложенного ssl_mode
ssl_mode = db_config.get("ssl_settings", {}).get("ssl_mode", "verify-full")

# Замена значения user на "admin"
connection["user"] = "admin"

# Добавление нового параметра max_connections
connection["max_connections"] = 100

print(f"SSL Mode: {ssl_mode}")
print("Параметры соединения:")
for key, value in connection.items():
    print(f"* {key}: {value}")