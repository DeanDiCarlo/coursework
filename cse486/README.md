# CW2 N-Queens (CSE486)

This folder contains a single coursework notebook:

- `CW2_NQueens.ipynb`

## What is implemented

The notebook implements and compares three search strategies for N-Queens:

1. **DFS with backtracking** (`dfs_n_queens`)
2. **BFS** (`bfs_n_queens`)
3. **IDS** (`ids_n_queens`) with a real depth-limited search subroutine (`dls`)

It also includes:

- Shared state representation: `state[row] = col`
- Safety check: `isSafe(state, row, col)`
- Solution validator: `is_valid_solution(sol, n)`
- Performance measurement decorator for runtime and RSS memory delta (KB)
- Benchmarks for `N = [4, 5, 6, 7, 8]` with 3-run averages
- Time and memory plots for all three algorithms

## Running in Colab

1. Upload/open `CW2_NQueens.ipynb` in Google Colab.
2. If needed, install missing dependencies in a cell:

```python
!pip -q install psutil matplotlib
```

3. Run all cells.

## Notes

- The notebook is intentionally self-contained and avoids local-only dependencies.
- RSS memory deltas can be noisy due to Python allocator/GC behavior.
