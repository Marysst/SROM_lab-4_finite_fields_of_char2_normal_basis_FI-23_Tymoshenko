import sys

class GF2ONBField:
    def __init__(self, m):
        """
        Ініціалізує поле GF(2^m) з оптимальним нормальним базисом та обчислює мультиплікативну матрицю Λ.
        :param m: Розмірність поля (m > 0)
        """
        self.m = m
        self.p = 2*m + 1
        if not self.is_onb(self.p, self.m):
            print("У цьому полі не існує ОНБ")
            sys.exit(-1)  # Завершення програми
        else:
            print("У цьому полі існує ОНБ")
        self.mult_matrix = self._compute_multiplicative_matrix()
    
    def isPrime(self, n):
        d = 2
        while d * d <= n and n % d != 0:
            d += 1
        if d * d > n:
            return True
        else:
            return False

    def is_onb(self, p, m):
        if not self.isPrime(p):
            return False
        for k in range(1, p):
            if ((1 << k) - 1) % p == 0:
                if k == 2*m or (p - 3) % 4 == 0:
                    return True
        return False

    def _compute_multiplicative_matrix(self):
        """
        Обчислює мультиплікативну матрицю Λ для ОНБ.
        :return: Матриця Λ (m x m)
        """
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

    def print_multiplicative_matrix(self):
        """
        Друкує обчислену мультиплікативну матрицю Λ.
        """
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

# Приклад використання
if __name__ == "__main__":
    # Поле GF(2^491)
    m = 491

    field = GF2ONBField(m)

    # Елементи поля
    a = "11000111001111100000010110001110011001100110110001000100010101101001101101101100010111100000110111100010100110010001010011111010111000011110110010110010010101101111110001100010000010110001100000111101001000000000111100001010010100111011101011001001000100100000110001011111000011111111010011001100011111011110101000100001000000111000011000111011010100100101101110000101010111100100101000000001101011110000001110001000001010111110010000110111110010011000101000100010000001110010010100110110000"
    b = "10011111000011010100100100101001010101000010001110111001111110100101010101001110111010001101001110010111111011010000111111101100110111000010110110111101111000011000110010000011100111011001001011110001011111001100011010100100000001111111010011011000100110110010000100101001011110111101101000010001110011110000110100111101100001000000010111000001000100000101100101011111110111110000101001001100100111100101001001100000010010010001000000001010111100110100101100010000001011110100100100110001110"
    n = "00001101110101110100101000011011001001000000000101111101110100000000001111110111011101010101000101010100001010110000010001011010010001110100000100101111010010100001110001100001000010001101000100001001000011111000110011111101010001010101001101011111100010111000111100110000101101111011011010010010100000000001110110001001111100010111011110100111101011101101100111001110101110101110110101011001000001100101111011011110101100100100100101001111111100000000000000111101011011110001110110101011111"

    a = list(map(int, a))
    b = list(map(int, b))
    n = list(map(int, n))

    # Операції
    result_add = field.add(a, b)
    result_mult = field.multiply(a, b)
    result_square = field.square(a)
    result_power = field.power(a, n)
    result_inverse = field.inverse(a)

    # Вивід результатів
    print(f"Addition result (A+B): {''.join(map(str, result_add))}")
    print(f"Multiplication result (A*B): {''.join(map(str, result_mult))}")
    print(f"Square result (A^2): {''.join(map(str, result_square))}")
    print(f"Inverse result (A^(-1)): {''.join(map(str, result_inverse))}")
    print(f"Power result (A^N): {''.join(map(str, result_power))}")
