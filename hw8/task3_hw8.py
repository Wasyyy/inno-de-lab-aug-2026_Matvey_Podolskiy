from typing import Any

DEFAULT_RETURN_INDEX_BASE = 10.0


def calculate_overdue_fine(movie_title: str, days_overdue: Any, fine_rate: float) -> tuple[float, float] | None:
    """
    Функция принимает "сырые" данные о количестве дней просрочки,
    которые могут иметь некорректный тип или формат (например, строку
    с нечисловым значением, список вместо числа или ноль дней), и
    безопасно обрабатывает такие случаи без остановки программы.
    Обрабатываются следующие ошибки входных данных:
        - TypeError: days_overdue имеет тип, который невозможно
          преобразовать в float (например, список).
        - ValueError: days_overdue является строкой, которая не
          представляет собой корректное число (например, "пять").
        - ZeroDivisionError: days_overdue равно нулю, из-за чего
          невозможно рассчитать индекс оборачиваемости (деление на 0).

    Args:
        movie_title: Название фильма, по которому оформляется возврат.
        days_overdue: Количество дней просрочки возврата. Ожидается
            число или числовая строка, но может быть передано
            значение некорректного типа или формата.
        fine_rate: Ставка штрафа в долларах за один день просрочки.

    Returns:
        tuple[float, float] | None: кортеж (total_fine, return_index)
        при успешном расчете, где total_fine — итоговая сумма штрафа,
        а return_index — технический индекс оборачиваемости. Возвращает
        None, если во время расчета произошла одна из обрабатываемых
        ошибок (TypeError, ValueError или ZeroDivisionError).
    """
    try:
        numeric_days = float(days_overdue)
        total_fine = numeric_days * fine_rate
        return_index = DEFAULT_RETURN_INDEX_BASE / numeric_days
        print(f"Фильм: '{movie_title}' | Итоговый штраф: {total_fine}$ | Индекс: {return_index}")
        return total_fine, return_index
    except TypeError as error:
        print(f" TypeError Некорректный тип данных для '{movie_title}': {error}")
        return None
    except ValueError as error:
        print(f"ValueError Невозможно преобразовать дни в число для '{movie_title}': {error}")
        return None
    except ZeroDivisionError as error:
        print(f"ZeroDivisionError Возврат без просрочки для '{movie_title}': {error}")
        return None
    finally:
        print("--- Проверка транзакции возврата завершена ---")


# Тестовые вызовы функции

print("=== ПРОВЕРКА ВОЗВРАТОВ ===")

calculate_overdue_fine("Matrix", 5, 1.5)
calculate_overdue_fine("Inception", "пять", 2.0)
calculate_overdue_fine("Avatar", 0, 2.5)
calculate_overdue_fine("Interstellar", [3,], 3.0)