"""
DFS Path Finder with Live Console Visualization
================================================

This module implements a recursive Depth-First Search algorithm to determine
if a path exists from start cell to and end cell in grid-based maze.

Walls (blocked cells) are represented by 1, free cells by 0.
The algorithm marks visited cells and shows the exploration step by step.

Functions:
    in_bound(x, y, matrix) -> bool
    dfs_visual(x, y, end, used, matrix, visual_callback) -> bool
    has_path_visual(matrix, used, cur_x, cur_y) -> None
    make_visual_callback(matrix, delay) -> callable
"""

import os
import random
import time
from typing import Callable, List, Tuple


def in_bound(x: int, y: int, matrix: List[List[int]]) -> bool:
    """
    Checks if coordinates (x, y) are inside the matrix bounds.
    Returns:
        True if inside bounds, False otherwise.
    """
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[x])


def dfs_visual(
    x: int,
    y: int,
    target: Tuple[int, int],
    used: List[List[bool]],
    matrix: List[List[int]],
    visual_callback: Callable[[int, int, List[List[bool]]], None],
) -> bool:
    """
    Recursive DFS that marks visited cells and calls a visualization
    function after each step.

    Args:
        x: current row index
        y: current column index
        end: target coordinates (row, col)
        used: 2D boolean matrix marking already visited cells
        matrix: the maze (0 = free, 1 = wall)
        visual_callback: function called after each cell is visited.
                         It receives (x, y, used).

    Returns:
        True if a path from (x, y) to end is found, False otherwise.
    """
    # ---------------------------------------------------
    # Stop if out of bound, on a wall, or already visited
    if not in_bound(x, y, matrix):
        return False

    elif matrix[x][y] == 1:
        return False

    # Visualising
    visual_callback((x, y), target, used)

    if used[x][y] is True:
        return False
    # ---------------------------------------------------

    # Mark current cell as visited
    used[x][y] = True

    # Reached the target?
    if (x, y) == target:
        return True

    # Explore neighbors in order: up, right, down, left
    return (
        dfs_visual(x - 1, y, target, used, matrix, visual_callback)  # up
        or dfs_visual(x, y + 1, target, used, matrix, visual_callback)  # right
        or dfs_visual(x + 1, y, target, used, matrix, visual_callback)  # down
        or dfs_visual(x, y - 1, target, used, matrix, visual_callback)  # left
    )


def has_path_visual(
    matrix: List[List[int]],
    start: Tuple[int, int],
    target: Tuple[int, int],
    visual_callback: Callable[[int, int, List[List[bool]]], None],
) -> bool:
    """
    Initialise the used matrix and start the recursive DFS.

    Args:
        matrix: the maze (0 = free, 1 == wall)
        start: (row, col) of the starting cell
        end: (row, col) of the target cell
        visaul_callback: function called after each visited cell.

    Returns:
        True if a path exists, False otherwise.
    """
    # Create a matrix of the same size, filled with False (not visited)
    used = [[False for _ in range(len(row))] for row in matrix]
    return dfs_visual(start[0], start[1], target, used, matrix, visual_callback)


def draw_matrix(
    matrix: List[List[int]],
    used: List[List[bool]],
    current: Tuple[int, int],
    target: Tuple[int, int],
) -> None:
    """
    Clears the console and draw the current state of the maze.

    Emojis to render it more beatiful and user friendly:
        🔴, 🟠, 🟡, 🟢, 🔵, 🟣, 🟤, ⚫, ⚪
        🟥, 🟧, 🟨, 🟩, 🟦, 🟪, 🟫, ⬛, ⬜.
    You can use it to set icon for:
        walls, free cell, current position and already visited cells

    Args:
        matrix: the original maze ( 0 = free, 1 = wall)
        used: boolean matrix marking visited cells
        current: current position of step
        end: target posiotion
    """
    # Clear screen after each traverse step
    os.system("cls" if os.name == "nt" else "clear")

    for x in range(len(matrix)):
        row_parts = []
        for y in range(len(matrix[x])):
            if (x, y) == current:  # current position
                if used[x][y]:
                    row_parts.append("🟡")  # if current position in used
                else:
                    row_parts.append("🟢")  # otherwise
            elif (x, y) == target:  # target posiotion
                row_parts.append("🔴")
            elif used[x][y]:  # already visited
                row_parts.append("🔵")
            elif matrix[x][y] == 1:  # walls
                row_parts.append("⬛")
            else:  # free, not visited
                row_parts.append("⬜")
        print(" ".join(row_parts))
    print()


def make_visual_callback(
    matrix: List[List[int]],
    delay: float = 0.3,
) -> Callable[[int, int, List[List[bool]]], None]:
    """
    Create a callback function that draws the maze after each step.

    Args:
        matrix: the original maze (used to know wall positions)
        delay: time in seconds to puase after each redrew

    Returns:
        A callback function that accepts (x, y, used) and draws the maze.
    """

    def callback(current, target, used_state: List[List[bool]]) -> None:
        draw_matrix(matrix, used_state, current, target)
        time.sleep(delay)

    return callback


# Function that adds random walls in maze
def add_random_walls(maze, min_walls=1, max_walls=None):
    """
    Adds random number of walls in to the maze.

    Args:
        maze: nested list (0 = free, 1 = wall)
        min_walls: minimal number of walls that need to be in maze (optional)
        max_walls: max number of walls that need to be in maze (optional)
                    If None, 20% summary of all cells
    """
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0
    total_cells = rows * cols

    # Determining max number of walls
    if max_walls is None:
        max_walls = max(min_walls, int(total_cells * 0.2))

    free_cells = [(r, c) for r in range(rows) for c in range(cols) if maze[r][c] == 0]

    # Checking for free cells to put walls
    # if max possible is 0 that means we dont have free slots
    max_possible = len(free_cells)
    if max_possible == 0:
        return

    num_walls = random.randint(min_walls, min(max_walls, max_possible))

    # Putting walls in randomly cells (without retrying)
    walls_postions = random.sample(free_cells, num_walls)
    for r, c in walls_postions:
        maze[r][c] = 1


# ---------------- FINAL EXAMPLE USAGE ---------------------
if __name__ == "__main__":
    # Define a maze: o = free, 1 = wall
    maze = [[0] * 68 for _ in range(30)]
    # Adding walls
    add_random_walls(maze, min_walls=330, max_walls=800)
    # Collecting all free cells to get random start and end positions
    free_cells = [
        (x, y) for x, row in enumerate(maze) for y, cell in enumerate(row) if cell == 0
    ]

    if len(free_cells) < 2:
        print("Need more free space to start and an end positions")
    else:
        start_pos, target_pos = random.sample(free_cells, 2)
        # Creating a visualization callback with gived delay seconds
        visual = make_visual_callback(maze, delay=0.05)

        # Run the dfs search with live display
        path_exists = has_path_visual(maze, start_pos, target_pos, visual)

        # After search finishes, print the result
        print(f"Path found: {path_exists}")
