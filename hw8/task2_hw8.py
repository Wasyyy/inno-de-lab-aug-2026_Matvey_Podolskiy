import time
from functools import wraps
from typing import Callable, Any

# Константы уровня модуля
PERFORMANCE_LOG_PREFIX = "[PERF_LOG]"
TIME_DECIMALS = 8


def performance_logger(func: Callable(..., Any)) -> Callable(..., Any):
    """
    Оборачивает целевую функцию, засекая время до и после её вызова
    с помощью time.perf_counter(). После выполнения выводит в консоль
    сообщение с именем функции и затраченным временем

    Args:
        func: Целевая функция, время выполнения которой нужно замерить.

    Returns:
        Callable(..., Any): функция-обертка (wrapper), которая при
        вызове выполняет func, логирует время его работы и возвращает
        результат func без изменений.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = round(time.perf_counter() - start_time, TIME_DECIMALS)
        print(f"{PERFORMANCE_LOG_PREFIX} Функция '{func.__name__}' выполнена за {elapsed_time} сек.")
        return result
    return wrapper


@performance_logger
def get_sorted_report(genre_revenue: list(dict(str, str | float))) -> list(dict(str, str | float)):
    """
    Сортирует отчет по выручке жанров в порядке убывания.

    Принимает список словарей с данными о выручке по категориям
    фильмов и возвращает новый список, отсортированный по ключу
    total_sales от наибольшего значения к наименьшему.

    Args:
        genre_revenue: Список словарей, где каждый словарь содержит
            ключ "category" (str) с названием жанра и ключ
            "total_sales" (float) с суммой выручки по этому жанру.

    Returns:
        list[dict[str, str | float]]: список словарей, отсортированный
        по убыванию значения "total_sales".
    """
    return sorted(genre_revenue, key=lambda item: item["total_sales"], reverse=True)


# Тестовые данные

# Набор 1 (Стандартный)
dataset_1 = [
    {"category": "Action", "total_sales": 4311.85},
    {"category": "Animation", "total_sales": 4656.30},
    {"category": "Children", "total_sales": 3655.55}
]

# Набор 2 (С одинаковой выручкой)
dataset_2 = [
    {"category": "Classics", "total_sales": 1200.10},
    {"category": "Comedy", "total_sales": 4000.00},
    {"category": "Documentary", "total_sales": 4000.00}
]

# Набор 3 (Единичный элемент)
dataset_3 = [
    {"category": "Drama", "total_sales": 500.00}
]


def print_report(title: str, dataset: list[dict[str, str | float]]) -> None:
    """Выводит заголовок теста и отсортированный топ категорий по выручке.

    Args:
        title: Заголовок теста, отображаемый перед результатом.
        dataset: Список словарей с данными по выручке жанров,
            который будет передан в get_sorted_report.

    Returns:
        None
    """
    print(f"\n--- {title} ---")
    sorted_report = get_sorted_report(dataset)
    print("Топ категорий по выручке:")
    for index, item in enumerate(sorted_report, start=1):
        print(f"{index}. {item['category']}: {item['total_sales']}")


print("=== ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===")
print_report("ТЕСТ 1", dataset_1)
print_report("ТЕСТ 2", dataset_2)
print_report("ТЕСТ 3", dataset_3)