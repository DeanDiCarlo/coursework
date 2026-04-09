import random
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Patch


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


def generate_random_state():
    return [random.randint(0, 7) for _ in range(8)]


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


def hill_climber_8queens(max_restarts=100):
    history = []
    total_steps = 0

    overall_best_state = None
    overall_best_fitness = float('inf')

    for restart in range(max_restarts + 1):
        current_state = generate_random_state()
        current_fitness = compute_fitness(current_state)

        history.append({
            'step': total_steps,
            'state': copy.copy(current_state),
            'fitness': current_fitness,
            'restart': restart,
            'is_restart_boundary': True,
        })

        if current_fitness < overall_best_fitness:
            overall_best_fitness = current_fitness
            overall_best_state = copy.copy(current_state)

        if current_fitness == 0:
            return {
                'solution': current_state,
                'fitness': 0,
                'history': history,
                'total_steps': total_steps,
                'restarts_used': restart,
                'solved': True,
            }

        while True:
            total_steps += 1
            neighbor, neighbor_fitness = get_best_neighbor(current_state)

            if neighbor_fitness >= current_fitness:
                break

            current_state = neighbor
            current_fitness = neighbor_fitness

            history.append({
                'step': total_steps,
                'state': copy.copy(current_state),
                'fitness': current_fitness,
                'restart': restart,
                'is_restart_boundary': False,
            })

            if current_fitness < overall_best_fitness:
                overall_best_fitness = current_fitness
                overall_best_state = copy.copy(current_state)

            if current_fitness == 0:
                return {
                    'solution': current_state,
                    'fitness': 0,
                    'history': history,
                    'total_steps': total_steps,
                    'restarts_used': restart,
                    'solved': True,
                }

    return {
        'solution': overall_best_state if overall_best_state is not None else [],
        'fitness': overall_best_fitness,
        'history': history,
        'total_steps': total_steps,
        'restarts_used': max_restarts,
        'solved': False,
    }


def draw_solution_board(result, save_path="solution_board.png"):
    state = result['solution']
    n = len(state)
    solved = result['solved']

    fig, ax = plt.subplots(figsize=(6, 6))

    for row in range(n):
        for col in range(n):
            color = '#DDDDDD' if (row + col) % 2 == 0 else '#AAAAAA'
            rect = patches.Rectangle(
                (col, n - 1 - row), 1, 1,
                linewidth=0.5,
                edgecolor='#888888',
                facecolor=color,
            )
            ax.add_patch(rect)

    for col, row in enumerate(state):
        ax.text(
            col + 0.5, n - 1 - row + 0.5,
            "*",
            fontsize=20,
            ha='center', va='center',
            color='black',
            fontweight='bold',
        )

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(range(n))
    ax.set_yticklabels(range(n - 1, -1, -1))
    ax.tick_params(length=0)
    ax.set_aspect('equal')

    status = "Solved" if solved else "Not Solved"
    ax.set_title(
        f"8 Queens — {status}\n"
        f"Restarts: {result['restarts_used']}  |  Steps: {result['total_steps']}  |  Fitness: {result['fitness']}"
    )

    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Board saved to {save_path}")
    plt.show()


def draw_convergence_plot(result, save_path="convergence.png"):
    history = result['history']

    if not history:
        return

    steps = [h['step'] for h in history]
    fitnesses = [h['fitness'] for h in history]
    restart_steps = [h['step'] for h in history if h.get('is_restart_boundary', False)]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(steps, fitnesses, color='steelblue', linewidth=1.5, label='Fitness (attacking pairs)')

    for i, rs in enumerate(restart_steps):
        ax.axvline(x=rs, color='red', linestyle='--', linewidth=0.8, alpha=0.6,
                   label='Restart' if i == 0 else None)

    ax.axhline(y=0, color='green', linestyle='-', linewidth=1.0, alpha=0.6, label='Goal (0)')

    ax.set_xlabel("Cumulative Step")
    ax.set_ylabel("Attacking Pairs")
    ax.set_title("Fitness Convergence Over Time")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Convergence plot saved to {save_path}")
    plt.show()


def draw_restart_performance(result, save_path="restart_performance.png"):
    history = result['history']

    if not history:
        return

    restart_best = {}
    for h in history:
        r = h['restart']
        f = h['fitness']
        if r not in restart_best or f < restart_best[r]:
            restart_best[r] = f

    restart_ids = sorted(restart_best.keys())
    best_fitnesses = [restart_best[r] for r in restart_ids]
    colors = ['green' if f == 0 else 'steelblue' for f in best_fitnesses]

    fig, ax = plt.subplots(figsize=(max(8, len(restart_ids) * 0.5), 5))

    bars = ax.bar(restart_ids, best_fitnesses, color=colors, edgecolor='black', linewidth=0.5)

    for bar, val in zip(bars, best_fitnesses):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(val),
            ha='center', va='bottom', fontsize=9
        )

    ax.set_xlabel("Restart #")
    ax.set_ylabel("Best Fitness Achieved")
    ax.set_title("Performance Per Restart Attempt")
    ax.set_xticks(restart_ids)
    ax.grid(True, axis='y', alpha=0.3)

    legend_elements = [
        Patch(facecolor='green', edgecolor='black', label='Solved (fitness=0)'),
        Patch(facecolor='steelblue', edgecolor='black', label='Not solved'),
    ]
    ax.legend(handles=legend_elements)

    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Restart performance chart saved to {save_path}")
    plt.show()


def visualize_all(result):
    draw_solution_board(result)
    draw_convergence_plot(result)
    draw_restart_performance(result)


if __name__ == "__main__":
    result = hill_climber_8queens(max_restarts=100)

    print()
    print("=" * 35)
    print("   8 Queens Hill Climber")
    print("=" * 35)
    print(f"  Solved:         {result['solved']}")
    print(f"  Solution:       {result['solution']}")
    print(f"  Restarts used:  {result['restarts_used']}")
    print(f"  Total steps:    {result['total_steps']}")
    print(f"  Final fitness:  {result['fitness']}")
    print("=" * 35)

    if not result['solved']:
        print("\n  WARNING: No perfect solution found.")
        print("  Try increasing max_restarts.\n")

    visualize_all(result)
