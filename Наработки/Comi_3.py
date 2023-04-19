import random
import math
import matplotlib.pyplot as plt


def generate_points(num_points, min_coord, max_coord):
    return [(random.randint(min_coord, max_coord), random.randint(min_coord, max_coord)) for _ in range(num_points)]


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def path_distance(path):
    return sum(distance(path[i], path[i - 1]) for i in range(len(path)))


def two_opt(path, i, k):
    return path[:i] + path[i:k+1][::-1] + path[k+1:]


def plot_tsp_solution(points, solution, title="TSP Solution"):
    plt.figure(figsize=(10, 6))
    plt.scatter([point[0] for point in points], [point[1] for point in points], c="b", marker="o")
    plt.title(title)

    for i in range(len(solution)):
        start = solution[i]
        end = solution[i - 1]
        plt.plot([start[0], end[0]], [start[1], end[1]], "r")

    for point in points:
        plt.text(point[0] + 1, point[1] + 1, f"{point[0]}, {point[1]}", fontsize=10)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()


def two_opt_algorithm(path, max_iterations, stop_threshold):
    best_path = path
    best_distance = path_distance(path)
    no_improvement_count = 0

    for iteration in range(max_iterations):
        improved = False
        for i in range(1, len(path) - 2):
            for k in range(i + 1, len(path) - 1):
                new_path = two_opt(path, i, k)
                new_distance = path_distance(new_path)

                if new_distance < best_distance:
                    best_path = new_path
                    best_distance = new_distance
                    improved = True

        if not improved:
            no_improvement_count += 1
            if no_improvement_count >= stop_threshold:
                break
        else:
            no_improvement_count = 0

    return best_path

def main():
    num_points = 100
    min_coord = 0
    max_coord = 100
    max_iterations = 10000
    stop_threshold = 200

    points = generate_points(num_points, min_coord, max_coord)
    initial_solution = random.sample(points, len(points))
    tsp_solution = two_opt_algorithm(initial_solution, max_iterations, stop_threshold)

    print("\nОбщая дистанция:", path_distance(tsp_solution))

    plot_tsp_solution(points, tsp_solution, title=f"TSP Solution (Total Distance: {path_distance(tsp_solution):.2f}))")

if __name__ == "__main__":
    main()

