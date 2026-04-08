"""
DFS Path Finder (Depth-Finder Search)
=====================================
Iterative DFS that finds a path from start to target in a grid-based maze.
Walls are represented by 1, free cells by 0.

Functions:
    in_bound(x, y, matrix) -> bool
    reconstruct_path(parent, end) -> tuple[list, str]
    dfs_path_finder(matrix, start, target, callback) -> tuple[bool, list, str]
    draw_matrix(matrix, visited, current, target) -> None
    make_visual_callback(matrix, delay) -> Callable
    add_random_walls(maze, min_walls, max_walls) -> None
"""

from os import name, system
from random import randint, sample
from time import perf_counter, sleep
from typing import Callable, List, Optional, Tuple

# ---------------------------------------------
#  Helpers
# ---------------------------------------------


def in_bound(x: int, y: int, matrix: List[List[int]]) -> bool:
    """Returns True if (x, y) is inside the matrix bounds."""
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[x])


def reconstruct_path(
    parent: dict,
    end: Tuple[int, int],
) -> Tuple[List[Tuple[int, int]], str]:
    """
    Walks the parent dict from end back to start.

    Returns:
        path_list: [(r0, c0), (r1, c1), ... (rN, cN)]
        path_str: "(r0, c0) -> (r1, c1) -> ... -> (rN, cN)"
    """
    path, node = [], end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    path_str = " -> ".join(f"{r},{c}" for r, c in path)
    return path, path_str


# ----------------------------------------------------
#  Core Algorithms
# ----------------------------------------------------


def dfs_path_finder(
    matrix: List[List[int]],
    start: Tuple[int, int],
    target: Tuple[int, int],
    visual_callback: Optional[Callable] = None,
) -> Tuple[bool, List[Tuple[int, int]], str]:
    """
    Iterative DFS with parent-dict path reconstruction.

    Args:
        matrix: 2D maze (0 = free, 1 = wall)
        start: (row, col) starting cell
        target: (row, col) target cell
        visual_callback: Optional fn(current, target, visited) for live display

    Returns:
        found: True if path exists
        path_list: list of (row, col) from start to target (empty if not found)
        path_str: human-readable string, e.g. "(0, 0) -> (0, 1) -> ..."
    """

    def _cb(current):
        if visual_callback:
            visual_callback(current, target, visited)

    visited = [[False] * len(row) for row in matrix]
    parent: dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}

    stack = [start]

    while stack:
        x, y = stack.pop()
        visited[x][y] = True
        _cb((x, y))

        if (x, y) == target:
            path_list, path_str = reconstruct_path(parent, target)
            return True, path_list, path_str

        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:  # up down right left
            nx, ny = x + dx, y + dy
            if in_bound(nx, ny, matrix) and matrix[nx][ny] == 0 and not visited[nx][ny]:
                parent[(nx, ny)] = (x, y)
                stack.append((nx, ny))

    return False, [], ""


# ─────────────────────────────────────────────
#  Visualization
# ─────────────────────────────────────────────


def draw_matrix(
    matrix: List[List[int]],
    visited: List[List[bool]],
    current: Tuple[int, int],
    target: Tuple[int, int],
) -> None:
    """
    Clears the console and redraws tha maze state.
    Emojis to use:
        🔴, 🟠, 🟡, 🟢, 🔵, 🟣, 🟤, ⚫, ⚪
        🟥, 🟧, 🟨, 🟩, 🟦, 🟪, 🟫, ⬛, ⬜.
    """
    system("cls" if name == "nt" else "clear")
    for x, row in enumerate(matrix):
        parts = []
        for y in range(len(row)):
            if (x, y) == current:
                parts.append("🟢")
            elif (x, y) == target:
                parts.append("🔴")
            elif visited[x][y]:
                parts.append("🔵")
            elif matrix[x][y] == 1:
                parts.append("⬛")
            else:
                parts.append("⬜")
        print(" ".join(parts))
    print()


def make_visual_callback(
    matrix: List[List[int]],
    delay: float = 0.05,
) -> Callable:
    """Returns a callback closure that draws the maze after each step."""

    def callback(
        current: Tuple[int, int],
        target: Tuple[int, int],
        visited: List[List[bool]],
    ) -> None:
        draw_matrix(matrix, visited, current, target)
        sleep(delay)

    return callback


# ─────────────────────────────────────────────
#  Maze generation
# ─────────────────────────────────────────────


def add_random_walls(
    maze: List[List[int]],
    min_walls: int = 1,
    max_walls: Optional[int] = None,
) -> None:
    """Randomly converts free cells to walls (in-place)."""
    rows, cols = len(maze), len(maze[0]) if maze else 0
    if max_walls is None:
        max_walls = max(min_walls, int(rows * cols * 0.2))

    free = [(r, c) for r in range(rows) for c in range(cols) if maze[r][c] == 0]
    if not free:
        return

    count = randint(min_walls, min(max_walls, len(free)))
    for r, c in sample(free, count):
        maze[r][c] = 1


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    maze = [[0] * 68 for _ in range(30)]
    add_random_walls(maze, min_walls=330, max_walls=800)

    free_cells = [
        (x, y) for x, row in enumerate(maze) for y, cell in enumerate(row) if cell == 0
    ]

    if len(free_cells) < 2:
        print("Not enough free cells for start and target.")
    else:
        start_pos, target_pos = sample(free_cells, 2)
        callback = make_visual_callback(maze, delay=0.08)

        start = perf_counter()
        found, path_list, path_str = dfs_path_finder(
            maze, start_pos, target_pos, callback
        )
        total = perf_counter() - start

        print(f"Path found: {found}.")
        print(f"Time: {total:.6f} seconds.")
        # if found:
        #     print(f"Length    : {len(path_list)} steps")
        #     print(f"Path      : {path_str}")
