import os
from typing import List, Tuple
from utils import read_file


def init_grid(inputs: List[str]) -> List[List[str]]:
    grid = []

    for input in inputs:
        grid.append(list(input))

    return grid


def word_search(grid: List[List[str]], starting_point: Tuple[int, int], key: str = "XMAS") -> int:
    row_index = starting_point[0]
    col_index = starting_point[1]
    found_count = 0

    if grid[row_index][col_index] != key[0]:
        return 0

    # Search up
    if row_index >= 3:
        word = (
            grid[row_index][col_index]
            + grid[row_index - 1][col_index]
            + grid[row_index - 2][col_index]
            + grid[row_index - 3][col_index]
        )
        if word == key:
            found_count += 1

    # Search down
    if row_index <= len(grid) - 4:
        word = (
            grid[row_index][col_index]
            + grid[row_index + 1][col_index]
            + grid[row_index + 2][col_index]
            + grid[row_index + 3][col_index]
        )
        if word == key:
            found_count += 1

    # Search left
    if col_index >= 3:
        word = (
            grid[row_index][col_index]
            + grid[row_index][col_index - 1]
            + grid[row_index][col_index - 2]
            + grid[row_index][col_index - 3]
        )
        if word == key:
            found_count += 1

    # Search right
    if col_index <= len(grid[0]) - 4:
        word = (
            grid[row_index][col_index]
            + grid[row_index][col_index + 1]
            + grid[row_index][col_index + 2]
            + grid[row_index][col_index + 3]
        )
        if word == key:
            found_count += 1

    # Search diagonal (up-left)
    if row_index >= 3 and col_index >= 3:
        word = (
            grid[row_index][col_index]
            + grid[row_index - 1][col_index - 1]
            + grid[row_index - 2][col_index - 2]
            + grid[row_index - 3][col_index - 3]
        )
        if word == key:
            found_count += 1

    # Search diagonal (up-right)
    if row_index >= 3 and col_index <= len(grid[0]) - 4:
        word = (
            grid[row_index][col_index]
            + grid[row_index - 1][col_index + 1]
            + grid[row_index - 2][col_index + 2]
            + grid[row_index - 3][col_index + 3]
        )
        if word == key:
            found_count += 1

    # Search diagonal (down-right)
    if row_index <= len(grid) - 4 and col_index <= len(grid[0]) - 4:
        word = (
            grid[row_index][col_index]
            + grid[row_index + 1][col_index + 1]
            + grid[row_index + 2][col_index + 2]
            + grid[row_index + 3][col_index + 3]
        )
        if word == key:
            found_count += 1

    # Search diagonal (down-left)
    if row_index <= len(grid) - 4 and col_index >= 3:
        word = (
            grid[row_index][col_index]
            + grid[row_index + 1][col_index - 1]
            + grid[row_index + 2][col_index - 2]
            + grid[row_index + 3][col_index - 3]
        )
        if word == key:
            found_count += 1

    return found_count


def word_search_v2(grid: List[List[str]], starting_point: Tuple[int, int]) -> bool:
    row_index = starting_point[0]
    col_index = starting_point[1]

    key = "MAS"
    reverse_key = key[::-1]

    # We can't start searching on the edge of the grid
    if row_index in [0, len(grid) - 1] or col_index in [0, len(grid[0]) - 1]:
        return False

    # If we aren't on an "A", return
    if grid[row_index][col_index] != key[1]:
        return False

    # upper_left = (row_index - 1, col_index - 1)
    # lower_left = (row_index + 1, col_index - 1)

    # Search diagonal (up-right)
    word = (
        grid[row_index + 1][col_index - 1]
        + grid[row_index][col_index]
        + grid[row_index - 1][col_index + 1]
    )
    if word != key and word != reverse_key:
        return False

    # Search diagonal (down-right)
    word = (
        grid[row_index - 1][col_index - 1]
        + grid[row_index][col_index]
        + grid[row_index + 1][col_index + 1]
    )
    if word != key and word != reverse_key:
        return False

    return True


# Program start
inputs = read_file("inputs/day4.txt")
grid = init_grid(inputs)

p1_answer = 0
p2_answer = 0

# loop through the grid and check for the pattern "XMAS"
# This is up, down, left, right, and diagonals
for row_idx in range(len(grid)):
    for col_index in range(len(grid[0])):
        found_count = word_search(grid, (row_idx, col_index))
        p1_answer += found_count

        is_found_p2 = word_search_v2(grid, (row_idx, col_index))
        if is_found_p2:
            # print(f"found 'xmas' on {row_idx},{col_index}")
            p2_answer += 1

print(f"P1 answer - {p1_answer}")
print(f"P2 answer - {p2_answer}")
