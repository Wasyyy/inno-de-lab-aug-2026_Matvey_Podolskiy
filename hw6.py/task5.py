from random import randint

secret_number = randint(1, 20)
attempts = 5

print("Я загадал число от 1 до 20. Угадайте за 5 попыток!")

while attempts > 0:
    guess = int(input("Введите число: "))
    if 1 <= guess <= 20:

        if guess == secret_number:
            print(f"Вы угадали число {secret_number}!")
            break
        elif guess > secret_number:
            print("Слишком много!")
        else:
            print("Слишком мало!")

        attempts -= 1
        if attempts > 0:
            print(f"Осталось попыток: {attempts}")
        else:
            print(f"Попытки закончились. Загаданное число было: {secret_number}")

    else:
        print("Ошибка. число не попадает в нужный промежуток")