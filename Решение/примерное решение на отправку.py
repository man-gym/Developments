import math
import requests
from io import BytesIO
from PIL import Image

# Константы
GRAVITY = 9.80665
PI = 3.1415926535898
MASS_REDUCTION = 0.001
CANVAS_WIDTH = 250
CANVAS_HEIGHT = 250
CATAPULT_Y = -300
API_URL = 'http://api.datsart.dats.team/'

# Функция для выполнения POST запроса к API
def post_request(endpoint, data, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(API_URL + endpoint, data=data, headers=headers)
    return response.json()

# Функция для получения попадания снаряда на холст
def get_projectile_landing(power, angle_horizontal, angle_vertical):
    angle_horizontal_rad = math.radians(angle_horizontal)
    angle_vertical_rad = math.radians(angle_vertical)
    Vx = power * math.cos(angle_horizontal_rad) * math.sin(angle_vertical_rad)
    Vy = power * math.cos(angle_vertical_rad)
    T = (2 * Vy) / (GRAVITY * MASS_REDUCTION)
    x = Vx * T
    y = Vy * T
    return x, y

token = '64383981e22a364383981e22a5'

# Получение исходного изображения
image_url = 'http://s.datsart.dats.team/game/image/shared/1.png'
response = requests.get(image_url)
source_image = Image.open(BytesIO(response.content))

# Функция для определения цвета пикселя
def get_pixel_color(x, y):
    return source_image.getpixel((x, y))

# Расчет углов и мощности выстрела
def calculate_shots():
    shots = []

    for x in range(CANVAS_WIDTH):
        for y in range(CANVAS_HEIGHT):
            color = get_pixel_color(x, y)
            if color != (255, 255, 255):  # Пропускаем белые пиксели
                # Расчет угла горизонтального и вертикального и мощности здесь (это сложная часть)
                angle_horizontal, angle_vertical, power = calculate_angles_and_power(x, y, color)
                shot_data = {
                    'x': x,
                    'y': y,
                    'color': color,
                    'angle_horizontal': angle_horizontal,
                    'angle_vertical': angle_vertical,
                    'power': power
                }
                shots.append(shot_data)

    return shots

def calculate_angles_and_power(x, y, color):
    # Фиксированная мощность выстрела
    power = 50

    # Расчет угла между точкой выстрела и целевой точкой
    delta_x = x - CANVAS_WIDTH / 2
    delta_y = y - CANVAS_HEIGHT
    distance = np.sqrt(delta_x ** 2 + delta_y ** 2)

    # Расчет вертикального угла выстрела (усредненное значение)
    angle_vertical = np.arctan(delta_y / delta_x) * 180 / np.pi

    # Расчет горизонтального угла выстрела, основанного на предположении о фиксированной мощности
    optimal_angle_horizontal = 2 * np.arcsin(distance * GRAVITY / (power**2)) * 180 / (2 * np.pi)

    # Изменение знака горизонтального угла, если точка находится слева от точки выстрела
    if delta_x < 0:
        optimal_angle_horizontal = -optimal_angle_horizontal

    return optimal_angle_horizontal, angle_vertical, power

shots = calculate_shots()


# Выполнение выстрелов
for shot in shots:
    data = {
        'angleHorizontal': shot['angle_horizontal'],
        'angleVertical': shot['angle_vertical'],
        'colorPot': shot['color'],
        'power': shot['power']
    }
    shot_result = post_request('/art/state/shot', data, token)
    if not shot_result['success']:
        print(f"Error executing shot at ({shot['x']}, {shot['y']}): {shot_result}")

# Выполнение выстрелов
for shot in shots:
    data = {
        'angleHorizontal': shot['angle_horizontal'],
        'angleVertical': shot['angle_vertical'],
        'colorPot': shot['color'],
        'power': shot['power']
    }
    response = post_request('/art/state/shot', data, token)
    if not response['success']:
        print(f"Error executing shot at ({shot['x']}, {shot['y']}): {response}")

# Проверка результата
result = post_request('/art/state/result', {}, token)
print(f"Final score: {result['response']['grade']}")


