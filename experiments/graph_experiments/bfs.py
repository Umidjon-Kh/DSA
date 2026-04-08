"""
BFS Path Finder (Breadth-First Search)
=======================================
Iterative BFS that finds the *shortest* path from start to target
in a grid-based maze.  Walls are represented by 1, free cells by 0.

Cell legend during visualization:
    🟢  current cell being processed
    🟣  target cell
    🟡  cells waiting in the queue (frontier)
    🔵  cells already visited
    ⬛  wall
    ⬜  free cell
    🔴   final path (shown after target is found)

Functions:
    in_bound(x, y, matrix) -> bool
    reconstruct_path(parent, end) -> tuple[list, str]
    bfs_path_finder(matrix, start, target, callback) -> tuple[bool, list, str]
    draw_matrix(matrix, visited, in_queue, current, target, path) -> None
    make_visual_callback(matrix, delay) -> Callable
    add_random_walls(maze, min_walls, max_walls) -> None
"""

from collections import deque
from os import name, system
from random import randint, sample
from time import perf_counter, sleep
from typing import Callable, Dict, List, Optional, Set, Tuple

# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────


def in_bound(x: int, y: int, matrix: List[List[int]]) -> bool:
    """Returns True if (x, y) is inside the matrix bounds."""
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[x])


def reconstruct_path(
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]],
    end: Tuple[int, int],
) -> Tuple[List[Tuple[int, int]], str]:
    """
    Walks the parent dict from end back to start.

    Returns:
        path_list : [(r0,c0), (r1,c1), ..., (rN,cN)]
        path_str  : "r0,c0 -> r1,c1 -> ... -> rN,cN"
    """
    path, node = [], end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    path_str = " -> ".join(f"{r},{c}" for r, c in path)
    return path, path_str


# ─────────────────────────────────────────────
#  Core Algorithm
# ─────────────────────────────────────────────


def bfs_path_finder(
    matrix: List[List[int]],
    start: Tuple[int, int],
    target: Tuple[int, int],
    visual_callback: Optional[Callable] = None,
) -> Tuple[bool, List[Tuple[int, int]], str]:
    """
    Iterative BFS with parent-dict path reconstruction.

    Unlike DFS, BFS always finds the *shortest* path (fewest steps).

    Args:
        matrix:          2D maze (0 = free, 1 = wall).
        start:           (row, col) starting cell.
        target:          (row, col) target cell.
        visual_callback: Optional fn(current, target, visited, in_queue, path)
                         called after each cell is dequeued.

    Returns:
        found:      True if a path exists.
        path_list:  List of (row, col) from start to target (empty if not found).
        path_str:   Human-readable path string.
    """
    visited: List[List[bool]] = [[False] * len(row) for row in matrix]
    in_queue: Set[Tuple[int, int]] = set()
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}

    visited[start[0]][start[1]] = True
    in_queue.add(start)
    queue: deque = deque([start])

    while queue:
        x, y = queue.popleft()
        in_queue.discard((x, y))

        if visual_callback:
            visual_callback((x, y), target, visited, in_queue, [])

        if (x, y) == target:
            path_list, path_str = reconstruct_path(parent, target)
            # Final frame — highlight the path
            if visual_callback:
                visual_callback((x, y), target, visited, in_queue, path_list)
            return True, path_list, path_str

        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:  # up down right left
            nx, ny = x + dx, y + dy
            if in_bound(nx, ny, matrix) and matrix[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                in_queue.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return False, [], ""


# ─────────────────────────────────────────────
#  Visualization
# ─────────────────────────────────────────────


def draw_matrix(
    matrix: List[List[int]],
    visited: List[List[bool]],
    in_queue: Set[Tuple[int, int]],
    current: Tuple[int, int],
    target: Tuple[int, int],
    path: List[Tuple[int, int]],
) -> None:
    """
    Clears the console and redraws the maze state.

    Priority (highest → lowest):
        🟢  current
        🟣  target
        🔴   path cell (shown on final frame)
        🟡  in queue / frontier
        🔵  visited
        ⬛  wall
        ⬜  free
    """
    system("cls" if name == "nt" else "clear")
    path_set = set(path)
    for x, row in enumerate(matrix):
        parts = []
        for y in range(len(row)):
            cell = (x, y)
            if cell == current:
                parts.append("🟢")
            elif cell == target:
                parts.append("🟣")
            elif cell in path_set:
                parts.append("🔴")
            elif cell in in_queue:
                parts.append("🟡")
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
    """Returns a callback closure that draws the maze after each BFS step."""

    def callback(
        current: Tuple[int, int],
        target: Tuple[int, int],
        visited: List[List[bool]],
        in_queue: Set[Tuple[int, int]],
        path: List[Tuple[int, int]],
    ) -> None:
        draw_matrix(matrix, visited, in_queue, current, target, path)
        # Pause longer on the final path reveal
        sleep(delay * 6 if path else delay)

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
        callback = make_visual_callback(maze, delay=0.01)

        start_time = perf_counter()
        found, path_list, path_str = bfs_path_finder(
            maze, start_pos, target_pos, callback
        )
        total = perf_counter() - start_time

        print(f"Path found : {found}.")
        if found:
            print(f"Length     : {len(path_list)} steps  (shortest possible)")
        print(f"Time       : {total:.6f} seconds.")
        # print(f"Path       : {path_str}")
