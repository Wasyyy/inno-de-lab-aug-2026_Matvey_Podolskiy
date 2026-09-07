MAX_RENTAL_BATCH_LIMIT = 150.0

def  calculate_rental_batch(quantity: int, rental_rate: float, discount: float = 0.0) -> tuple(float, bool):
    """
    Функция вычисляет итоговую сумму за партию с применением жанровой
    скидки и проверяет, превышает ли эта сумма лимит автоматического
    одобрения заказа, заданный константой MAX_RENTAL_BATCH_LIMIT.

    Args:
        quantity: Количество дисков в партии.
        rental_rate: Стоимость аренды одного диска в долларах.
        discount: Скидка в долях единицы (например, 0.1 — это 10%).
        По умолчанию скидка отсутствует (0.0).

    Returns:
       Кортеж из двух элементов:
            - final_sum (float): итоговая сумма партии, округленная
            до двух знаков после запятой.
            - is_limit_exceeded (bool): True, если сумма превышает
            MAX_RENTAL_BATCH_LIMIT, иначе False.
    """
    final_sum = round(quantity * rental_rate * (1 - discount), 2)
    is_limit_exceeded = final_sum > MAX_RENTAL_BATCH_LIMIT
    return final_sum, is_limit_exceeded

print("=== ОТЧЕТ ПО ПАРТИЯМ АРЕНДЫ ===")

# Партия 1: вызов с позиционными аргументами
sum_1, exceeded_1 = calculate_rental_batch(30, 2.99)
print(f"Партия 1 (Academy Dinosaur): Сумма {sum_1}$. Превышение лимита: {exceeded_1}")

# Партия 2: вызов с именованными аргументами
sum_2, exceeded_2 = calculate_rental_batch(quantity=40, rental_rate=4.99, discount=0.1)
print(f"Партия 2 (Affair Prejudice): Сумма {sum_2}$. Превышение лимита: {exceeded_2}")

# Партия 3: вызов с позиционными аргументами (без скидки)
sum_3, exceeded_3 = calculate_rental_batch(10, 1.99)
print(f"Партия 3 (Agent Truman): Сумма {sum_3}$. Превышение лимита: {exceeded_3}")

# Партия 4: вызов с именованными аргументами
sum_4, exceeded_4 = calculate_rental_batch(quantity=50, rental_rate=3.50, discount=0.2)
print(f"Партия 4 (African Egg): Сумма {sum_4}$. Превышение лимита: {exceeded_4}")