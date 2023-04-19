import numpy as np
import random


n_nurses = random.randint(5, 15)
n_shifts = random.randint(2, 5)
n_days = random.randint(5, 14)
n_ants = n_nurses
n_iterations = random.randint(50, 200)
alpha = random.uniform(0.5, 2)
beta = random.uniform(0.5, 2)
evaporation_rate = random.uniform(0.1, 0.9)

min_shifts = 1
max_shifts = random.randint(2, 5)
desired_shifts = np.random.choice(n_shifts, (n_nurses, n_days))

pheromones = np.ones((n_nurses, n_shifts, n_days))
best_schedule_cost = float('inf')
best_schedule = None


MAX_CONSECUTIVE_DAYS = 6
MIN_REST_DAYS_AFTER_SERIES = 1
CONSTRAINT_PENALTY = 100

def schedule_cost(schedule):
    cost = 0

    for nurse in range(n_nurses):
        total_shifts = np.sum(schedule[nurse, :, :])
        if total_shifts < min_shifts:
            cost += (min_shifts - total_shifts) * CONSTRAINT_PENALTY
        elif total_shifts > max_shifts:
            cost += (total_shifts - max_shifts) * CONSTRAINT_PENALTY

    for nurse in range(n_nurses):
        for day in range(n_days - MAX_CONSECUTIVE_DAYS):
            consecutive_days = np.sum(schedule[nurse, :, day:day+MAX_CONSECUTIVE_DAYS+1])
            if consecutive_days > MAX_CONSECUTIVE_DAYS:
                cost += CONSTRAINT_PENALTY

    for nurse in range(n_nurses):
        for day in range(n_days - MAX_CONSECUTIVE_DAYS - MIN_REST_DAYS_AFTER_SERIES):
            consecutive_days = np.sum(schedule[nurse, :, day:day+MAX_CONSECUTIVE_DAYS])
            rest_days = np.sum(schedule[nurse, :, day+MAX_CONSECUTIVE_DAYS:day+MAX_CONSECUTIVE_DAYS+MIN_REST_DAYS_AFTER_SERIES])
            if consecutive_days == MAX_CONSECUTIVE_DAYS and rest_days < MIN_REST_DAYS_AFTER_SERIES:
                cost += CONSTRAINT_PENALTY

    for nurse in range(n_nurses):
        for day in range(n_days - 1):
            shifts_today = np.sum(schedule[nurse, :, day])
            shifts_tomorrow = np.sum(schedule[nurse, :, day + 1])
            if shifts_today > 0 and shifts_tomorrow > 0:
                cost += CONSTRAINT_PENALTY

    return cost


for iteration in range(n_iterations):
    schedules = []
    costs = []

    for ant in range(n_ants):
        schedule = np.zeros((n_nurses, n_shifts, n_days), dtype=int)

        for day in range(n_days):
            for shift in range(n_shifts):
                available_nurses = list(range(n_nurses))  # Update with constraints
                probabilities = []

                for nurse in available_nurses:
                    pheromone = pheromones[nurse, shift, day] ** alpha
                    visibility = 1 / (1 + abs(desired_shifts[nurse, day] - shift)) ** beta
                    probability = pheromone * visibility
                    probabilities.append(probability)

                probabilities /= np.sum(probabilities)
                chosen_nurse = np.random.choice(available_nurses, p=probabilities)
                schedule[chosen_nurse, shift, day] = 1

        cost = schedule_cost(schedule)
        schedules.append(schedule)
        costs.append(cost)

        if cost < best_schedule_cost:
            best_schedule_cost = cost
            best_schedule = schedule

    # Update pheromones
    for nurse in range(n_nurses):
        for shift in range(n_shifts):
            for day in range(n_days):
                delta_pheromone = 0

                for schedule, cost in zip(schedules, costs):
                    if schedule[nurse, shift, day] == 1 and cost != 0:
                        delta_pheromone += 1 / cost

                pheromones[nurse, shift, day] = (1 - evaporation_rate) * pheromones[nurse, shift, day] + delta_pheromone


print("Best schedule cost:", best_schedule_cost)
print("\nShifts per day:")
for day in range(n_days):
    print(f"Day {day + 1}:")
    for shift in range(n_shifts):
        working_nurses = np.where(best_schedule[:, shift, day] == 1)[0]
        print(f"  Shift {shift + 1}: {len(working_nurses)} nurses")

print("\nNurse schedule:")
for nurse in range(n_nurses):
    print(f"Nurse {nurse + 1}:")
    for day in range(n_days):
        print(f"  Day {day + 1}:", end=" ")
        shifts = []
        for shift in range(n_shifts):
            if best_schedule[nurse, shift, day] == 1:
                shifts.append(shift + 1)
        print(", ".join(f"Shift {s}" for s in shifts) if shifts else "Off")


with open("../../nurse_schedule.txt", "w") as f:
    f.write(f"Best schedule cost: {best_schedule_cost}\n\n")

    f.write("Shifts per day:\n")
    for day in range(n_days):
        f.write(f"Day {day + 1}:\n")
        for shift in range(n_shifts):
            working_nurses = np.where(best_schedule[:, shift, day] == 1)[0]
            f.write(f"  Shift {shift + 1}: {len(working_nurses)} nurses\n")

    f.write("\nNurse schedule:\n")
    for nurse in range(n_nurses):
        f.write(f"Nurse {nurse + 1}:\n")
        for day in range(n_days):
            f.write(f"  Day {day + 1}:")
            shifts = []
            for shift in range(n_shifts):
                if best_schedule[nurse, shift, day] == 1:
                    shifts.append(shift + 1)
            f.write(" " + ", ".join(f"Shift {s}" for s in shifts) if shifts else " Off")
            f.write("\n")


