import itertools
import math
from functools import reduce


def gcd_list(numbers):
    return reduce(math.gcd, numbers)


def find_color_coefficients(colors, ratio):
    if any(c < 0 or c > 255 for c in ratio):
        return None
    elif len(colors) < 2:
        return None

    min_coeff_sum = float('inf')
    best_coefficients = None
    max_search_range = 30

    for coefficients in itertools.product(range(0, 10), repeat=len(colors)):
        if sum(coefficients) == 0:
            continue
        mixed_color = [sum(colors[j][i] * coefficients[j] for j in range(len(colors))) // sum(coefficients) for i in
                       range(3)]
        if (abs(mixed_color[0] - ratio[0]) <= 10 or abs(ratio[0] - mixed_color[0]) <= 10) and (
                abs(mixed_color[1] - ratio[1]) <= 10 or abs(ratio[1] - mixed_color[1]) <= 10) and (
                abs(mixed_color[2] - ratio[2]) <= 10 or abs(ratio[2] - mixed_color[2]) <= 10):
            coeff_sum = sum(coefficients)
            if coeff_sum < min_coeff_sum:
                min_coeff_sum = coeff_sum
                best_coefficients = coefficients

    if best_coefficients is not None:
        gcd = gcd_list(best_coefficients)
        simplified_coefficients = [c // gcd for c in best_coefficients]
        return simplified_coefficients
    else:
        return None


def convert_dec_to_rgb(A):
    D = []
    for i in A:
        binary_str = bin(i)[2:].zfill(24)
        octets = [binary_str[j:j+8] for j in range(0, 24, 8)]
        r = int(octets[0], 2)
        g = int(octets[1], 2)
        b = int(octets[2], 2)
        D.append(r)
        D.append(g)
        D.append(b)
    new_lst = []
    for i in range(0, len(D), 3):
        new_lst.append(D[i:i + 3])
    return new_lst


# Пример использования
"""
A = [16711680, 65280, 255]  # decimal numbers
rgb_lst = convert_dec_to_rgb(A)

colors = rgb_lst

ratio = [128, 128, 128] # конечный
coefficients = find_color_coefficients(colors, ratio)
if coefficients is not None:
    print("Коэффициенты для смешивания цветов:", " : ".join(map(str, coefficients)))
else:
    print("Не удалось найти коэффициенты для смешивания цветов")
"""
