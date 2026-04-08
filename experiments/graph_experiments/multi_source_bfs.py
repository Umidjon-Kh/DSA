"""
Multi-Source BFS
================
Iterative BFS that finds, for every target cell, which source is closest
and what the shortest distance is — all in a *single* O(N×M) pass.

Why Multi-Source BFS?
---------------------
Imagine you have S sources (e.g. clinics, fire stations, chargers) and
T targets (e.g. patients, people, cars).  The naive approach runs one BFS
per target → O(T * N*M).  Multi-Source BFS loads ALL sources into one
queue at t=0 and lets their wavefronts expand simultaneously.  The first
wavefront to reach a target wins — that source is the closest one.
Total cost: O(N*M), regardless of how many sources or targets there are.

Cell legend during visualization:
    🔴  source  (start of a wavefront)
    🏁  target  (waiting to be claimed)
    🟢  target  (claimed — nearest source found)
    🟡  frontier cells currently in the queue
    🔵  visited / explored
    ⬛  wall
    ⬜  free cell

Functions:
    in_bound(x, y, matrix)                              -> bool
    multi_source_bfs(matrix, sources, targets, cb)      -> dict[target, (source, dist)]
    draw_matrix(matrix, state, sources, targets,
                claimed, in_queue, current)             -> None
    make_visual_callback(matrix, sources, targets,
                         delay)                         -> Callable
    add_random_walls(maze, min_walls, max_walls)        -> None
    pick_random_points(maze, count)                     -> list[tuple]
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


# ─────────────────────────────────────────────
#  Core Algorithm
# ─────────────────────────────────────────────


def multi_source_bfs(
    matrix: List[List[int]],
    sources: List[Tuple[int, int]],
    targets: List[Tuple[int, int]],
    visual_callback: Optional[Callable] = None,
) -> Dict[Tuple[int, int], Tuple[Tuple[int, int], int]]:
    """
    Multi-Source BFS: finds the nearest source for every reachable target.

    All sources are enqueued simultaneously at distance 0.  Their wavefronts
    expand in lock-step, so the first wavefront to touch a target is
    guaranteed to be the shortest path — no repeated searches needed.

    Args:
        matrix:          2D maze (0 = free, 1 = wall).
        sources:         List of (row, col) source cells.
        targets:         List of (row, col) target cells.
        visual_callback: Optional fn(current, visited, in_queue, claimed)
                         called after each cell is dequeued.

    Returns:
        result: {target: (nearest_source, distance), ...}
                Unreachable targets are omitted from the dict.
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0

    visited: List[List[bool]] = [[False] * cols for _ in range(rows)]
    owner: List[List[Optional[Tuple[int, int]]]] = [[None] * cols for _ in range(rows)]
    dist: List[List[int]] = [[0] * cols for _ in range(rows)]
    in_queue: Set[Tuple[int, int]] = set()

    queue: deque = deque()

    # ── Seed the queue with ALL sources at once ──────────────────────────
    for src in sources:
        sx, sy = src
        if not in_bound(sx, sy, matrix) or matrix[sx][sy] == 1:
            continue
        visited[sx][sy] = True
        owner[sx][sy] = src
        dist[sx][sy] = 0
        in_queue.add(src)
        queue.append((sx, sy))

    target_set = set(targets)
    remaining = len(
        target_set
        & {s for s in sources if in_bound(*s, matrix) and matrix[s[0]][s[1]] == 0}
        ^ target_set
    )
    remaining = len(target_set)
    result: Dict[Tuple[int, int], Tuple[Tuple[int, int], int]] = {}

    # ── Single BFS pass ──────────────────────────────────────────────────
    while queue and remaining > 0:
        x, y = queue.popleft()
        in_queue.discard((x, y))

        if visual_callback:
            visual_callback((x, y), visited, in_queue, result)

        if (x, y) in target_set and (x, y) not in result:
            result[(x, y)] = (owner[x][y], dist[x][y])
            remaining -= 1

        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if in_bound(nx, ny, matrix) and matrix[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                owner[nx][ny] = owner[x][y]
                dist[nx][ny] = dist[x][y] + 1
                in_queue.add((nx, ny))
                queue.append((nx, ny))

    # Drain remaining queue for full visualization even after all targets found
    if visual_callback:
        while queue:
            x, y = queue.popleft()
            in_queue.discard((x, y))
            visual_callback((x, y), visited, in_queue, result)
            for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (
                    in_bound(nx, ny, matrix)
                    and matrix[nx][ny] == 0
                    and not visited[nx][ny]
                ):
                    visited[nx][ny] = True
                    owner[nx][ny] = owner[x][y]
                    dist[nx][ny] = dist[x][y] + 1
                    in_queue.add((nx, ny))
                    queue.append((nx, ny))

    return result


# ─────────────────────────────────────────────
#  Visualization
# ─────────────────────────────────────────────

# Distinct emoji per source index (up to 8 sources)
SOURCE_EMOJIS = ["🔴", "🟠", "🟣", "🟤", "⚫", "🔵", "🟡", "🟢"]
CLAIMED_EMOJIS = ["❤️ ", "🧡", "💜", "🤎", "🖤", "💙", "💛", "💚"]


def draw_matrix(
    matrix: List[List[int]],
    visited: List[List[bool]],
    in_queue: Set[Tuple[int, int]],
    current: Tuple[int, int],
    sources: List[Tuple[int, int]],
    targets: Set[Tuple[int, int]],
    claimed: Dict[Tuple[int, int], Tuple[Tuple[int, int], int]],
) -> None:
    """
    Redraws the maze.  Each source gets its own color; claimed targets
    inherit that color so you can see which source 'owns' which target.
    """
    system("cls" if name == "nt" else "clear")
    source_index = {src: i for i, src in enumerate(sources)}

    for x, row in enumerate(matrix):
        parts = []
        for y in range(len(row)):
            cell = (x, y)
            if cell in source_index:
                parts.append(SOURCE_EMOJIS[source_index[cell] % len(SOURCE_EMOJIS)])
            elif cell in claimed:
                src, d = claimed[cell]
                idx = source_index.get(src, 0)
                parts.append(CLAIMED_EMOJIS[idx % len(CLAIMED_EMOJIS)])
            elif cell in targets:
                parts.append("🏁")
            elif cell == current:
                parts.append("🔘")
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
    sources: List[Tuple[int, int]],
    targets: List[Tuple[int, int]],
    delay: float = 0.04,
) -> Callable:
    """Returns a callback closure for live BFS visualization."""
    target_set = set(targets)

    def callback(
        current: Tuple[int, int],
        visited: List[List[bool]],
        in_queue: Set[Tuple[int, int]],
        claimed: Dict,
    ) -> None:
        draw_matrix(matrix, visited, in_queue, current, sources, target_set, claimed)
        sleep(delay * 4 if current in target_set and current in claimed else delay)

    return callback


# ─────────────────────────────────────────────
#  Maze & point generation
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


def pick_random_points(
    maze: List[List[int]],
    count: int,
) -> List[Tuple[int, int]]:
    """Returns `count` distinct free cells chosen at random."""
    free = [(r, c) for r, row in enumerate(maze) for c, v in enumerate(row) if v == 0]
    return sample(free, min(count, len(free)))


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    ROWS, COLS = 25, 55
    NUM_SOURCES = randint(2, 6)  # random number of sources
    NUM_TARGETS = randint(3, 10)  # random number of targets

    maze = [[0] * COLS for _ in range(ROWS)]
    add_random_walls(maze, min_walls=200, max_walls=550)

    # Pick sources + targets from free cells (no overlap)
    all_points = pick_random_points(maze, NUM_SOURCES + NUM_TARGETS)
    sources = all_points[:NUM_SOURCES]
    targets = all_points[NUM_SOURCES:]

    print(f"Sources : {NUM_SOURCES}  {' '.join(SOURCE_EMOJIS[:NUM_SOURCES])}")
    print(f"Targets : {NUM_TARGETS}  🏁")
    sleep(1.2)

    callback = make_visual_callback(maze, sources, targets, delay=0.03)

    start_time = perf_counter()
    result = multi_source_bfs(maze, sources, targets, visual_callback=callback)
    total = perf_counter() - start_time

    # ── Final summary ────────────────────────────────────────────────────
    source_index = {src: i for i, src in enumerate(sources)}
    print("=" * 48)
    print("  Multi-Source BFS  —  Results")
    print("=" * 48)
    for i, target in enumerate(targets):
        if target in result:
            src, d = result[target]
            idx = source_index.get(src, 0)
            s_emoji = SOURCE_EMOJIS[idx % len(SOURCE_EMOJIS)]
            c_emoji = CLAIMED_EMOJIS[idx % len(CLAIMED_EMOJIS)]
            print(
                f"  🏁 target {i + 1:>2}  →  {c_emoji} source {idx + 1}  ({s_emoji})  dist: {d}"
            )
        else:
            print(f"  🏁 target {i + 1:>2}  →  ✖  unreachable")
    print("─" * 48)
    found = sum(1 for t in targets if t in result)
    print(f"  Claimed   : {found} / {NUM_TARGETS}")
    print(f"  Time      : {total:.6f} seconds  (single BFS pass)")
    print("=" * 48)
