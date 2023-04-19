import numpy as np
import random
import math
import matplotlib.pyplot as plt

points = [(random.randint(0, 100), random.randint(0, 100)) for i in range(100)]


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


class AntColonyOptimizer:
    def __init__(self, points, ants, evaporation_rate, alpha, beta, iterations):
        self.points = points
        self.distances = self.calculate_distances(points)
        self.ants = ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations

    def calculate_distances(self, points):
        n = len(points)
        distances = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                dist = distance(points[i], points[j])
                distances[i, j] = dist
                distances[j, i] = dist
        return distances

    def optimize(self):
        n = len(self.points)
        pheromone_matrix = np.ones((n, n))
        best_distance = float('inf')
        best_path = None

        for _ in range(self.iterations):
            all_paths = []
            all_distances = []

            for _ in range(self.ants):
                path = self.construct_solution(pheromone_matrix)
                distance = self.calculate_path_distance(path)
                all_paths.append(path)
                all_distances.append(distance)

                if distance < best_distance:
                    best_distance = distance
                    best_path = path

            pheromone_matrix = self.update_pheromones(pheromone_matrix, all_paths, all_distances)

        return best_path, best_distance

    def construct_solution(self, pheromone_matrix):
        n = len(self.points)
        start = random.randint(0, n - 1)
        path = [start]
        available_nodes = list(range(n))
        available_nodes.remove(start)

        for _ in range(n - 1):
            last_node = path[-1]
            probabilities = self.compute_probabilities(last_node, available_nodes, pheromone_matrix)
            next_node = self.select_next_node(available_nodes, probabilities)
            available_nodes.remove(next_node)
            path.append(next_node)

        return path

    def compute_probabilities(self, last_node, available_nodes, pheromone_matrix):
        pheromones = [pheromone_matrix[last_node, node] for node in available_nodes]
        distances = [self.distances[last_node, node] for node in available_nodes]
        sum_probs = sum(p ** self.alpha * (1 / d) ** self.beta for p, d in zip(pheromones, distances))
        return [(p ** self.alpha * (1 / d) ** self.beta) / sum_probs for p, d in zip(pheromones, distances)]

    def select_next_node(self, available_nodes, probabilities):
        return np.random.choice(available_nodes, p=probabilities)

    def calculate_path_distance(self, path):
        distance = 0
        for i in range(len(path) - 1):
            distance += self.distances[path[i], path[i + 1]]
        distance += self.distances[path[-1], path[0]]
        return distance

    def update_pheromones(self, pheromone_matrix, all_paths, all_distances):
            n = len(self.points)
            new_pheromone_matrix = (1 - self.evaporation_rate) * pheromone_matrix

            for path, distance in zip(all_paths, all_distances):
                pheromone_update = 1 / distance
                for i in range(n - 1):
                    new_pheromone_matrix[path[i], path[i + 1]] += pheromone_update
                    new_pheromone_matrix[path[i + 1], path[i]] += pheromone_update
                new_pheromone_matrix[path[-1], path[0]] += pheromone_update
                new_pheromone_matrix[path[0], path[-1]] += pheromone_update

            return new_pheromone_matrix

def plot_solution(points, best_path):
    plt.figure(figsize=(12, 6))

    for point in points:
        plt.scatter(point[0], point[1], c="blue")

    for i in range(len(best_path) - 1):
        point1 = points[best_path[i]]
        point2 = points[best_path[i + 1]]
        plt.plot([point1[0], point2[0]], [point1[1], point2[1]], "r-")

    point1 = points[best_path[-1]]
    point2 = points[best_path[0]]
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], "r-")

    plt.title("Best path found by Ant Colony Optimization")
    plt.show()

def main():
    ants = 10
    evaporation_rate = 0.1
    alpha = 1
    beta = 5
    iterations = 100

    optimizer = AntColonyOptimizer(points, ants, evaporation_rate, alpha, beta, iterations)
    best_path, best_distance = optimizer.optimize()

    print("Best path:", best_path)
    print("Best distance:", best_distance)

    plot_solution(points, best_path)

if __name__ == "__main__":
    main()





