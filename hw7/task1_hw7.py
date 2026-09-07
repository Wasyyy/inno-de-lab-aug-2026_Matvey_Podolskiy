# Исходная необработанная строка из источника данных
raw_user_record = " 10827 ; aLeXanDer_vLaDimiRov ; mInSk ; ACTIVE "

# Разбиение строки через ;
parts = raw_user_record.split(";")

# Очистка каждого элемента от пробелов по краям по номеру в массиве данных
user_id = parts[0].strip()
username = parts[1].strip()
city = parts[2].strip()
status = parts[3].strip()

# Добавление префикса "UID-" к идентификатору через f-строку
user_id = f"UID-{user_id}"

# Замена _ на пробел и установка к правильного регистра
username = username.replace("_", " ")
username = username.title()

# Установка верхнего регистра(Капса) для города
city = city.upper()

# Установка статуса в прописной регистр
status = status.lower()

# 7. Собирка итоговой строки
result = " | ".join([user_id, username, city, status])

print(f"Нормализованная запись:{result}")