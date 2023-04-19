import random
from math import sqrt
import matplotlib.pyplot as plt

def distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def tour_length(tour, points):
    return sum(distance(points[tour[i]], points[tour[i - 1]]) for i in range(len(points)))


def two_opt_swap(tour, i, k):
    new_tour = tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]
    return new_tour


def lin_kernighan(points):
    n = len(points)
    tour = list(range(n))
    min_tour_length = tour_length(tour, points)
    improved = True

    while improved:
        improved = False

        for i in range(n):
            for j in range(i + 2, n):
                new_tour = two_opt_swap(tour, i, j)
                new_tour_length = tour_length(new_tour, points)

                if new_tour_length < min_tour_length:
                    tour = new_tour
                    min_tour_length = new_tour_length
                    improved = True

    return min_tour_length, tour


points = [(random.randint(0, 100), random.randint(0, 100)) for i in range(100)]
min_tour_length, best_tour = lin_kernighan(points)

# Plot the solution
x = [point[0] for point in points]
y = [point[1] for point in points]
fig, ax = plt.subplots()
ax.scatter(x, y, color='blue')

best_tour.append(best_tour[0])  # add the first point to the end to complete the loop
x = [points[i][0] for i in best_tour]
y = [points[i][1] for i in best_tour]
ax.plot(x, y, marker='o', linestyle='dashed', color='red')

# Add edges with red color
for i in range(len(best_tour) - 1):
    start = best_tour[i]
    end = best_tour[i+1]
    ax.plot([points[start][0], points[end][0]], [points[start][1], points[end][1]], color='red')

print("Min tour length:", min_tour_length)
print("Best tour:", best_tour)

plt.show()

