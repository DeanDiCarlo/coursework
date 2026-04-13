import random
import copy
import time

def compute_fitness(state):
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:
                conflicts += 1
            elif abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def generate_random_state(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def get_best_neighbor(state):
    n = len(state)
    best_fitness = compute_fitness(state)
    best_neighbors = []
    for col in range(n):
        for row in range(n):
            if state[col] == row:
                continue
            neighbor = copy.copy(state)
            neighbor[col] = row
            fitness = compute_fitness(neighbor)
            if fitness < best_fitness:
                best_fitness = fitness
                best_neighbors = [neighbor]
            elif fitness == best_fitness:
                best_neighbors.append(neighbor)
    if best_neighbors:
        return random.choice(best_neighbors), best_fitness
    else:
        return copy.copy(state), best_fitness

def hill_climber(n, max_restarts=200):
    total_steps = 0
    for restart in range(max_restarts + 1):
        current_state = generate_random_state(n)
        current_fitness = compute_fitness(current_state)
        if current_fitness == 0:
            return True, restart, total_steps
        while True:
            total_steps += 1
            neighbor, neighbor_fitness = get_best_neighbor(current_state)
            if neighbor_fitness >= current_fitness:
                break
            current_state = neighbor
            current_fitness = neighbor_fitness
            if current_fitness == 0:
                return True, restart, total_steps
    return False, max_restarts, total_steps

RUNS = 30
board_sizes = [4, 6, 8, 10, 12, 16, 20]

print(f"{'N':>4} | {'Solved%':>8} | {'Avg Time(s)':>12} | {'Avg Steps':>10} | {'Avg Restarts':>13}")
print("-" * 65)

for n in board_sizes:
    successes = 0
    times = []
    steps_list = []
    restarts_list = []
    for _ in range(RUNS):
        t0 = time.time()
        solved, restarts, steps = hill_climber(n, max_restarts=200)
        elapsed = time.time() - t0
        if solved:
            successes += 1
        times.append(elapsed)
        steps_list.append(steps)
        restarts_list.append(restarts)
    pct = (successes / RUNS) * 100
    avg_t = sum(times) / RUNS
    avg_s = sum(steps_list) / RUNS
    avg_r = sum(restarts_list) / RUNS
    print(f"{n:>4} | {pct:>7.1f}% | {avg_t:>12.4f} | {avg_s:>10.1f} | {avg_r:>13.1f}")
