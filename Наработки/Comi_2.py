import random
import math
import itertools
import matplotlib.pyplot as plt

def generate_points(num_points, min_coord, max_coord):
    return [(random.randint(min_coord, max_coord), random.randint(min_coord, max_coord)) for _ in range(num_points)]

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def path_distance(path):
    return sum(distance(path[i], path[i - 1]) for i in range(len(path)))

def create_initial_population(points, population_size):
    return [random.sample(points, len(points)) for _ in range(population_size)]

def fitness_function(path):
    return -path_distance(path)

def selection(population, num_parents):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[:num_parents]

def crossover(parent1, parent2):
    child = [None] * len(parent1)

    start, end = sorted(random.sample(range(len(parent1)), 2))

    for i in range(start, end + 1):
        child[i] = parent1[i]

    child = list(itertools.chain(*([x] if x in child else [x, None] for x in parent2), child))
    child = [x for x in child if x is not None]

    return child

def mutation(individual, mutation_probability):
    for i in range(len(individual)):
        if random.random() < mutation_probability:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

def genetic_algorithm_tsp(points, population_size, num_generations, num_parents, mutation_probability):
    population = create_initial_population(points, population_size)

    for generation in range(num_generations):
        parents = selection(population, num_parents)
        offspring = [crossover(parents[i % num_parents], parents[(i + 1) % num_parents]) for i in range(len(population) - num_parents)]
        offspring = [mutation(child, mutation_probability) for child in offspring]
        population = parents + offspring

    return max(population, key=fitness_function)

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

def print_shortest_path(solution):
    print("Кратчайший путь:")
    for i, point in enumerate(solution):
        print(f"{i + 1}: {point}")
    print(f"1: {solution[0]} (возврат в начальную точку)")
    print(f"Длина пути: {path_distance(solution)}")


def main():
    num_points = 100
    min_coord = 0
    max_coord = 100
    population_size = 1000  # увеличение размера популяции
    num_generations = 2000  # увеличение количества поколений
    num_parents = 200  # увеличение количества родителей
    mutation_probability = 0.01

    points = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(100)]
    print("Сгенерированные точки:")
    for point in points:
        print(point)

    tsp_solution = genetic_algorithm_tsp(points, population_size, num_generations, num_parents, mutation_probability)
    print_shortest_path(tsp_solution)

    plot_tsp_solution(points, tsp_solution, title=f"TSP Solution (Total Distance: {path_distance(tsp_solution):.2f})")

if __name__ == "__main__":
    main()



