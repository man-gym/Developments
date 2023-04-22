import itertools
import math
from functools import reduce

def gcd_list(numbers):
    return reduce(math.gcd, numbers)

colors = []
while True:
    color = input("Введите цвет или нажмите Enter: ")
    if color == "":
        break
    color = color.split(",")
    color = [int(x) for x in color]
    if any(c < 0 or c > 255 for c in color):
        print("Ошибка: значение цвета должно быть от 0 до 255.")
    else:
        colors.append(color)

ratio = input("Введите желаемый цвет в формате RGB (например, 128,128,128): ").split(",")
ratio = [int(x) for x in ratio]

if any(c < 0 or c > 255 for c in ratio):
    print("Ошибка: значение цвета должно быть от 0 до 255.")
elif len(colors) < 2:
    print("Ошибка: для расчета коэффициентов смешивания необходимо как минимум два цвета.")
else:
    min_coeff_sum = float('inf')
    best_coefficients = None
    max_search_range = 30

    for coefficients in itertools.product(range(1, max_search_range), repeat=len(colors)):
        # if sum(coefficients) == 0:
        #     continue
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
        print("Не удалось найти коэффициенты для смешивания цветов.")
