import itertools
import math
from functools import reduce


def gcd_list(numbers):
    return reduce(math.gcd, numbers)


def dist(arr, arr1):
    return sum(map(lambda i: (arr[i] - arr1[i]) ** 2, range(len(arr)))) ** (1 / len(arr))


def find_color_coefficients(colors, ratio):
    if any(c < 0 or c > 255 for c in ratio):
        return None
    elif len(colors) < 2:
        return None

    min_dist = float('inf')
    best_coefficients = None

    for coefficients in itertools.product(range(0, 10), repeat=len(colors)):
        if sum(coefficients) == 0:
            continue
        mixed_color = [sum(colors[j][i] * coefficients[j] for j in range(len(colors))) // sum(coefficients) for i in
                       range(3)]
        current_dist = dist(mixed_color, ratio)
        if current_dist < min_dist:
            min_dist = current_dist
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

# Example usage

A = [2575315, 2878223, 3605363, 4939579, 7286775, 7809975]  # decimal numbers
rgb_lst = convert_dec_to_rgb(A)

colors = rgb_lst

ratio = [145, 225, 254] # target color
coefficients = find_color_coefficients(colors, ratio)
if coefficients is not None:
    print("Коэффициенты для смешивания цветов:", " : ".join(map(str, coefficients)))
else:
    print("Не удалось найти коэффициенты для смешивания цветов")

