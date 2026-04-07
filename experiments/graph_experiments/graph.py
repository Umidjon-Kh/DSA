from typing import List, Tuple

# ================================================================================
# --------------------------------------------------------------------------------
# Algorithm DFS (Deep First Search)
# --------------------------------------------------------------------------------
# The meaning of depth-first traversal is not to find the shortest path,
# but to go around the field in a certain order and
# find out whether there is a path at all or not


# ---------------------- HOW IT PRESENTS IN CODE -----------------------
# Internal function that checks it has gone a broad or not.
def in_bound(x: int, y: int, matrix: List[List[int]]) -> bool:
    return 0 <= x < len(matrix) and 0 <= y < len(matrix)


# Algorithm that recursively traverses all fileds in a matrix
#  and marks them after checking
def dfs(
    x: int,
    y: int,
    end: Tuple[int, int],
    used: List[List[bool]],
    matrix: List[List[int]],
) -> bool:
    # If we are out of border or this block is marked as used or its blocked
    # Returns False
    if not in_bound(x, y, matrix) or matrix[x][y] == 1 or used[x][y]:
        return False

    used[x][y] = True
    if (x, y) == end:
        return True

    # Recursively marking all fields and
    # if field is in the end on of them returns True
    return (
        dfs(x - 1, y, end, used, matrix)  # go up
        or dfs(x, y + 1, end, used, matrix)  # go right
        or dfs(x + 1, y, end, used, matrix)  # go down
        or dfs(x, y - 1, end, used, matrix)  # go left
    )


# Main function has path that runs
# all recursion algorithm that traverses all fields
def has_path(
    matrix: List[List[int]],
    start: Tuple[int, int],
    end: Tuple[int, int],
) -> bool:
    # Used to mark all fields that traversed
    used = [[False for _ in range(len(row))] for row in matrix]
    # Returns True if path is found to end, otherwise returns False
    return dfs(start[0], start[1], end, used, matrix)


# ================================================================================
