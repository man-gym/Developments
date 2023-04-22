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


def convert_24bit_to_rgb(A):
    D = []
    for i in A:
        r = int(i[0:2], 16)
        g = int(i[2:4], 16)
        b = int(i[4:6], 16)
        D.append(r)
        D.append(g)
        D.append(b)
    new_lst = []
    for i in range(0, len(D), 3):
        new_lst.append(D[i:i + 3])
    return new_lst


# Пример использования
'''
A = ["FF0000", "00FF00", "0000FF"]
rgb_lst = convert_24bit_to_rgb(A)

colors = rgb_lst

ratio = [128, 128, 128] # конечный
coefficients = find_color_coefficients(colors, ratio)
if coefficients is not None:
    print("Коэффициенты для смешивания цветов:", " : ".join(map(str, coefficients)))
else:
    print("Не удалось найти коэффициенты для смешивания цветов")'''
