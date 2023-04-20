import random
import math
import copy

points = [(random.randint(0, 100), random.randint(0, 100)) for i in range(100)]

def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def tour_length(tour, points):
    return sum(distance(points[tour[i]], points[tour[i-1]]) for i in range(len(tour)))

def random_tour(points):
    tour = list(range(len(points)))
    random.shuffle(tour)
    return tour

def local_search(tour, points):
    improved = True
    while improved:
        improved = False
        for i in range(len(tour)):
            for j in range(i+2, len(tour)):
                new_tour = copy.copy(tour)
                new_tour[i:j] = reversed(new_tour[i:j])
                if tour_length(new_tour, points) < tour_length(tour, points):
                    tour = new_tour
                    improved = True
    return tour

def bee_colony_algorithm(points, num_bees, num_iterations):
    best_tour = random_tour(points)
    best_tour_length = tour_length(best_tour, points)

    for _ in range(num_iterations):
        new_tours = [local_search(random_tour(points), points) for _ in range(num_bees)]
        new_tours_lengths = [tour_length(t, points) for t in new_tours]
        min_length = min(new_tours_lengths)
        if min_length < best_tour_length:
            best_tour = new_tours[new_tours_lengths.index(min_length)]
            best_tour_length = min_length

    return best_tour, best_tour_length

result_tour, result_length = bee_colony_algorithm(points, num_bees=10, num_iterations=100)

print("Лучший маршрут:", result_tour)
print("Длина маршрута:", result_length)
