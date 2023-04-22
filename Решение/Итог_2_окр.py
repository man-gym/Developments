import cv2
import numpy as np
from sklearn.cluster import DBSCAN

def process_image(image_path, circle_radius=5, circle_margin=2):
    def generate_circle_grid(image, radius, margin=0):
        circles = []
        y_step = int(radius * np.sqrt(3))
        x_step = 2 * radius + margin

        for y in range(radius, image.shape[0], y_step):
            offset = 0 if y % (2 * y_step) == 0 else radius
            for x in range(offset + radius, image.shape[1], x_step):
                circles.append((y, x))

        return circles

    image = cv2.imread(image_path)

    color_coords = np.argwhere(np.any(image != [255, 255, 255], axis=-1))

    dbscan = DBSCAN(eps=5, min_samples=20)
    dbscan.fit(color_coords)

    clusters = dbscan.labels_

    circles_image = image.copy()

    circle_count = 0
    circle_data = []
    for y, x in generate_circle_grid(circles_image, circle_radius, circle_margin):
        indices = np.where((color_coords == [y, x]).all(axis=1))[0]
        if indices.size > 0 and clusters[indices[0]] != -1:
            cv2.circle(circles_image, (x, y), circle_radius, (0, 0, 0), 1)

            mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            cv2.circle(mask, (x, y), circle_radius, (255, 255, 255), -1)

            pixel_colors = image[np.where(mask == 255)]

            circle_color = np.mean(pixel_colors, axis=0)

            print(f"Circle {circle_count + 1} ({x}, {y}): {circle_color}")

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1
            text = str(circle_count + 1)
            text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
            text_x = x - text_size[0] // 2
            text_y = y + text_size[1] // 2
            cv2.putText(circles_image, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)

            circle_data.append({"id": circle_count + 1, "coordinates": (x, y), "color": circle_color})

            circle_count += 1

    gray_image = cv2.cvtColor(circles_image, cv2.COLOR_BGR2GRAY)

    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    edges = cv2.Canny(blurred_image, 100, 200)

    bordered_image = circles_image.copy()

    border_color = (0, 0, 0)
    border_thickness = 1
    for y in range(edges.shape[0]):
        for x in range(edges.shape[1]):
            if edges[y, x] != 0:
                cv2.rectangle(bordered_image, (x, y), (x, y), border_color, border_thickness)

    cv2.imshow('Bordered Image', bordered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return circle_data

    # Пример использования функции

"""
image_path = 'image.png'
circle_data = process_image(image_path)
print(circle_data)
"""