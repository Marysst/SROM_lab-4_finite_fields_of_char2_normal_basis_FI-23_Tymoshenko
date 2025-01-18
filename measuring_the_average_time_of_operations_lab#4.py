# Основний код (программа)
import sys
import numpy as np

class GF2ONBField:
    def __init__(self, m):
        self.m = m
        self.p = 2*m + 1
        if not self.is_onb(self.p, self.m):
            print("У цьому полі не існує ОНБ")
            sys.exit(-1)  # Завершення програми
        else:
            print("У цьому полі існує ОНБ")
        self.mult_matrix = self._compute_multiplicative_matrix()

    # Перевірка числа на простоту
    def isPrime(self, n):
        d = 2
        while d * d <= n and n % d != 0:
            d += 1
        if d * d > n:
            return True
        else:
            return False

    # Перевірка існування ОНБ
    def is_onb(self, p, m):
        if not self.isPrime(p):
            return False
        for k in range(1, p):
            if ((1 << k) - 1) % p == 0:
                if k == 2*m or ((p - 3) % 4 == 0 and k == m):
                    return True
        return False

    # Обчислення мультиплікативної матриці Λ для ОНБ
    def _compute_multiplicative_matrix(self):
        matrix = np.zeros((self.m, self.m), dtype=int)
        for i in range(self.m):
            for j in range(self.m):
                # Виконуємо перевірку умов на основі формули:
                if (
                    ((2 ** i) + (2 ** j)) % self.p == 1
                    or ((2 ** i) - (2 ** j)) % self.p == 1
                    or (-(2 ** i) + (2 ** j)) % self.p == 1
                    or (-(2 ** i) - (2 ** j)) % self.p == 1
                ):
                    matrix[i, j] = 1
        return matrix

    # Друк мультиплікативної матриці Λ
    def print_multiplicative_matrix(self):
        for row in self.mult_matrix:
            print(" ".join(map(str, row)))

    # Додавання двох елементів у полі
    def add(self, a, b):
        result = [0] * max(len(a), len(b))
        for i in range(max(len(a), len(b))):
            result[i] = 1 if (a[i] ^ b[i]) else 0
        return result

    # Піднесення елемента поля до квадрату
    def square(self, a):
        resault = a[:]
        temp = resault.pop()
        return [temp] + resault

    # Множення двох елементів у полі
    def multiply(self, a, b):
        result = np.zeros(self.m, dtype=int)
        for i in range(self.m):
            a_shifted = a[i:] + a[:i]
            b_shifted = b[i:] + b[:i]
            a_shifted = np.array(a_shifted, dtype=int)
            b_shifted = np.array(b_shifted, dtype=int).reshape(-1, 1)
            result[i] = (a_shifted @ self.mult_matrix @ b_shifted) % 2
        return list(result)

    # Піднесення елемента поля до довільного степеня
    def power(self, a, n):
        result = [1] * (self.m)
        base = a[:]
        deg = n[:]
        while len(deg) > 0:
            temp = deg.pop()
            if temp == 1:
                result = self.multiply(result, base)
            base = self.square(base)
        return result

    # Знаходження оберненого елемента за множенням
    def inverse(self, a):
        # Використовуємо те, що a^(2^m - 2) = a^{-1} у GF(2^m)
        temp = (1 << self.m) - 2
        temp = list(map(int, bin(temp)[2:]))
        return self.power(a, temp)

# Визначення середнього часу виконання операцій у полі
import random, time

# Генерація випадкових елементів у полі
def random_element(m):
    element = random.randint(1, (1 << m) - 1)
    element = [int(bit) for bit in bin(element)[2:]]
    element = element + [0] * (m - len(element))
    return element

# Вимірювання часу виконання операцій
def benchmark_operations(field, m, iterations):
    times = {"add": 0, "multiply": 0, "square": 0, "inverse": 0, "power": 0}

    for _ in range(iterations):
        a = random_element(m)
        b = random_element(m)
        n = random_element(m)

        # Час для додавання
        start = time.perf_counter()
        field.add(a, b)
        times["add"] += time.perf_counter() - start

        # Час для множення
        start = time.perf_counter()
        field.multiply(a, b)
        times["multiply"] += time.perf_counter() - start

        # Час для зведення до квадрату
        start = time.perf_counter()
        field.square(a)
        times["square"] += time.perf_counter() - start

        # Час для знаходження оберненого
        if a != 0:
            start = time.perf_counter()
            field.inverse(a)
            times["inverse"] += time.perf_counter() - start

        # Час для зведення до довільного степеня
        start = time.perf_counter()
        field.power(a, n)
        times["power"] += time.perf_counter() - start

    # Середній час для кожної операції
    for op in times:
        times[op] /= iterations

    return times

# Основна функція тестування
if __name__ == "__main__":
    # Поле GF(2^491)
    m = 491

    field = GF2ONBField(m)

    # Тестування часу виконання
    operation_times = benchmark_operations(field, m, 5)

    # Вивід результатів
    print("\nСередній час виконання операцій у полі GF(2^491):")
    for op, avg_time in operation_times.items():
        print(f"Операція {op}: {avg_time:.10f} секунд")
