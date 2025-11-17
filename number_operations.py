"""
Простая программа для работы с числами
Выполняет различные операции: проверка на простое число, факториал, сумма цифр
"""

def is_prime(n: int) -> bool:
    """Проверяет, является ли число простым"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def factorial(n: int) -> int | None:
    """Вычисляет факториал числа"""
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def sum_of_digits(n: int) -> int:
    """Вычисляет сумму цифр числа"""
    if n < 0:
        n = abs(n)

    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total

def get_primes_in_range(start: int, end: int) -> list[int]:
    """Возвращает список простых чисел в заданном диапазоне"""
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def main():
    """Главная функция программы"""
    print("=== Операции с числами ===\n")

    while True:
        print("Выберите операцию:")
        print("1. Проверить, является ли число простым")
        print("2. Вычислить факториал")
        print("3. Вычислить сумму цифр числа")
        print("4. Найти простые числа в диапазоне")
        print("5. Выход")

        choice = input("\nВаш выбор: ")

        if choice == "1":
            try:
                num = int(input("Введите число: "))
                if is_prime(num):
                    print(f"{num} - простое число")
                else:
                    print(f"{num} - не простое число")
            except ValueError:
                print("Ошибка: введите целое число")

        elif choice == "2":
            try:
                num = int(input("Введите число: "))
                result = factorial(num)
                if result is not None:
                    print(f"Факториал {num} = {result}")
                else:
                    print("Факториал определен только для неотрицательных чисел")
            except ValueError:
                print("Ошибка: введите целое число")

        elif choice == "3":
            try:
                num = int(input("Введите число: "))
                result = sum_of_digits(num)
                print(f"Сумма цифр числа {num} = {result}")
            except ValueError:
                print("Ошибка: введите целое число")

        elif choice == "4":
            try:
                start = int(input("Введите начало диапазона: "))
                end = int(input("Введите конец диапазона: "))
                if start > end:
                    print("Ошибка: начало диапазона должно быть меньше или равно концу")
                else:
                    primes = get_primes_in_range(start, end)
                    if primes:
                        print(f"Простые числа в диапазоне [{start}, {end}]: {primes}")
                    else:
                        print(f"В диапазоне [{start}, {end}] нет простых чисел")
            except ValueError:
                print("Ошибка: введите целые числа")

        elif choice == "5":
            print("До свидания!")
            break

        else:
            print("Неверный выбор")

        print()

if __name__ == "__main__":
    main()

