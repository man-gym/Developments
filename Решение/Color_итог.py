import itertools
import math
from functools import reduce

def gcd_list(numbers):
    return reduce(math.gcd, numbers)

colors = []
while True:
    color = input("Tsvet or enter: ")
    if color == "":
        break
    color = color.split(",")
    color = [int(x) for x in color]
    if any(c < 0 or c > 255 for c in color):
        print("no")
    else:
        colors.append(color)

ratio = input("Final tsvet: ").split(",")
ratio = [int(x) for x in ratio]

if any(c < 0 or c > 255 for c in ratio):
    print("no")
elif len(colors) < 2:
    print("no")
else:
    min_coeff_sum = float('inf')
    best_coefficients = None
    max_search_range = 30

    for coefficients in itertools.product(range(1, max_search_range), repeat=len(colors)):
        if sum(coefficients) == 0:
            continue
        mixed_color = [sum(colors[j][i] * coefficients[j] for j in range(len(colors))) // sum(coefficients) for i in range(3)]
        if mixed_color == ratio:
            coeff_sum = sum(coefficients)
            if coeff_sum < min_coeff_sum:
                min_coeff_sum = coeff_sum
                best_coefficients = coefficients

    if best_coefficients is not None:
        gcd = gcd_list(best_coefficients)
        simplified_coefficients = [c // gcd for c in best_coefficients]
        print("Коэффициенты для смешивания цветов:", " : ".join(map(str, simplified_coefficients)))
    else:
        print("Не удалось найти коэффициенты для смешивания цветов")
