import math

def calculate_shot_parameters(target_x, target_y, canvas_width, canvas_height, gravity=9.8):
    # Вычисляем центр холста
    center_x = canvas_width / 2
    center_y = canvas_height / 2

    # Расстояние между центром холста и целевой точкой
    distance_x = target_x - center_x
    distance_y = target_y - center_y

    # Вычисляем углы выстрела
    angle_horizontal = math.atan2(distance_y, distance_x)
    angle_vertical = math.pi / 4

    # Вычисляем мощность выстрела
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
    power = math.sqrt((2 * gravity * distance) / (math.sin(2 * angle_vertical)))

    return angle_horizontal, angle_vertical, power

def calculate_trajectory(angle_horizontal, angle_vertical, power, gravity=9.8, time_step=0.01):
    trajectory_points = []

    t = 0
    while True:
        x = power * t * math.cos(angle_horizontal) * math.cos(angle_vertical)
        y = power * t * math.sin(angle_horizontal) * math.cos(angle_vertical) - 0.5 * gravity * t**2

        trajectory_points.append((x, y))

        if y < 0:
            break

        t += time_step

    return trajectory_points

# Пример использования функций
target_x = 150
target_y = 100
canvas_width = 250
canvas_height = 250

angle_horizontal, angle_vertical, power = calculate_shot_parameters(target_x, target_y, canvas_width, canvas_height)
trajectory_points = calculate_trajectory(angle_horizontal, angle_vertical, power)

for point in trajectory_points:
    print(point)
