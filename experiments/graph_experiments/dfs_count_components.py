"""
DFS Components Counter
==================================
Iterative DFS that counts all connected components in a colored grid.
Each unique non-zero integer represents a color/component group.
Already-visited cells are marked as 0 (black) during traversal.

Color mapping:
    [1] [2] [3] [4] [5] [6] [7] [8] [0]
    🟥, 🟧, 🟨, 🟩, 🟦, 🟪, 🟫, ⬛, ⬜

Functions:
    in_bound(x, y, matrix) -> bool
    dfs_components_counter(matrix, callback) -> dict[int, int]
    draw_matrix(matrix) -> None
    make_visual_callback(matrix, delay) -> Callable
    add_random_components(maze, num_colors, density) -> None
"""

from os import name, system
from random import choice, randint
from time import perf_counter, sleep
from typing import Callable, Dict, List, Optional

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────

COLORS = {
    0: "⬜",
    1: "🟥",
    2: "🟧",
    3: "🟨",
    4: "🟩",
    5: "🟦",
    6: "🟪",
    7: "🟫",
    8: "⬛",
}
VISITED_MARK = 8  # cells turn ⬛ once fully explored
COLOR_IDS = [c for c in COLORS if c not in (0, VISITED_MARK)]

# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────


def in_bound(x: int, y: int, matrix: List[List[int]]) -> bool:
    """Returns True if (x, y) is inside the matrix bounds."""
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[x])


# ─────────────────────────────────────────────
#  Core Algorithm
# ─────────────────────────────────────────────


def dfs_components_counter(
    matrix: List[List[int]],
    visual_callback: Optional[Callable] = None,
) -> Dict[int, int]:
    """
    Iterative DFS that counts connected components per color.

    A component is a group of orthogonally adjacent cells sharing
    the same non-zero color value.  Visited cells are overwritten
    with VISITED_MARK (8 / ⬛) so the original matrix is mutated
    in-place — pass a deep-copy if you need to preserve it.

    Args:
        matrix:          2D grid of integers (0 = empty, 1-7 = colors).
        visual_callback: Optional fn(matrix) called after each cell pop.

    Returns:
        counts: {color_id: number_of_components, ...}
                Only colors that actually appear in the grid are included.
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    counts: Dict[int, int] = {}

    for start_x in range(rows):
        for start_y in range(cols):
            color = matrix[start_x][start_y]
            if color == 0 or color == VISITED_MARK:
                continue  # empty or already explored

            # Found an unvisited component of `color`
            counts[color] = counts.get(color, 0) + 1

            # Flood-fill this component with iterative DFS
            stack = [(start_x, start_y)]
            while stack:
                x, y = stack.pop()
                if matrix[x][y] != color:
                    # Already visited by this fill or different color
                    continue

                matrix[x][y] = VISITED_MARK  # mark as visited

                if visual_callback:
                    visual_callback(matrix)

                for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if in_bound(nx, ny, matrix) and matrix[nx][ny] == color:
                        stack.append((nx, ny))

    return counts


# ─────────────────────────────────────────────
#  Visualization
# ─────────────────────────────────────────────


def draw_matrix(matrix: List[List[int]]) -> None:
    """Clears the console and redraws the current grid state."""
    system("cls" if name == "nt" else "clear")
    for row in matrix:
        print(" ".join(COLORS.get(cell, "❓") for cell in row))
    print()


def make_visual_callback(
    delay: float = 0.05,
) -> Callable:
    """Returns a callback closure that redraws the grid after each step."""

    def callback(matrix: List[List[int]]) -> None:
        draw_matrix(matrix)
        sleep(delay)

    return callback


# ─────────────────────────────────────────────
#  Grid generation
# ─────────────────────────────────────────────


def add_random_components(
    maze: List[List[int]],
    num_colors: int = len(COLOR_IDS),
    density: float = 0.45,
) -> None:
    """
    Randomly fills cells with colored integers (in-place).

    Args:
        maze:       Pre-allocated grid filled with 0s.
        num_colors: How many distinct colors to use (max 7).
        density:    Fraction of cells to fill, between 0.0 and 1.0.
    """
    rows = len(maze)
    cols = len(maze[0]) if rows else 0
    num_colors = max(1, min(num_colors, len(COLOR_IDS)))
    active_colors = COLOR_IDS[:num_colors]

    for r in range(rows):
        for c in range(cols):
            if randint(0, 99) < int(density * 100):
                maze[r][c] = choice(active_colors)


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import copy

    ROWS, COLS = 30, 60

    maze = [[0] * COLS for _ in range(ROWS)]
    add_random_components(maze, num_colors=7, density=1)

    # Draw initial state before DFS
    draw_matrix(maze)
    sleep(0.8)

    # Keep a copy for the final summary (original colors)
    original = copy.deepcopy(maze)

    callback = make_visual_callback(delay=0.01)

    start = perf_counter()
    counts = dfs_components_counter(maze, visual_callback=callback)
    total_time = perf_counter() - start
    # Final results
    draw_matrix(maze)
    print("=" * 36)
    print("  Connected components per color")
    print("=" * 36)
    total = 0
    for color_id in sorted(counts):
        emoji = COLORS.get(color_id, "?")
        n = counts[color_id]
        total += n
        print(
            f"  {emoji}  color {color_id}  →  {n:>3} component{'s' if n != 1 else ''}"
        )
    print("─" * 36)
    print(f"  Total components : {total}.")
    print(f"Time: {total_time:.6f} seconds.")
    print("=" * 36)
