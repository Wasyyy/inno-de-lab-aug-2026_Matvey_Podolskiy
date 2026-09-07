num1 = float(input("Введите первое число: "))
operation = input("Введите операцию (+, -, *, /): ")
num2 = float(input("Введите второе число: "))

if operation == "+":
    result = num1 + num2
elif operation == "-":
    result = num1 - num2
elif operation == "*":
    result = num1 * num2
elif operation == "/":
    if num2 == 0:
        print("Ошибка: деление на ноль!")
        result = None
    else:
        result = num1 / num2
else:
    print("Ошибка: неизвестная операция.")
    result = None

if result is not None:
    print(f"Результат: {result}")