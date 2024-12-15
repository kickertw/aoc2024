import os
from typing import List
from utils import read_file, Direction


def check_level_is_safe(level_vals: List[str]) -> bool:
    last_val = None
    direction = Direction.UNKNOWN
    for level_val in level_vals:
        new_val = int(level_val)
        # Initialize the last value
        if last_val == None:
            last_val = new_val
            continue

        # Initialize the direction
        if direction == Direction.UNKNOWN:
            if new_val > last_val:
                direction = Direction.INCREASING
            elif new_val < last_val:
                direction = Direction.DECREASING

        diff = abs(new_val - last_val)

        if diff < 1 or diff > 3:
            return False

        if direction == Direction.INCREASING and new_val < last_val:
            return False

        if direction == Direction.DECREASING and new_val > last_val:
            return False

        last_val = new_val

    return True


def check_level_is_safe_v2(level: str) -> bool:
    level_vals = level.split(" ")

    is_safe = check_level_is_safe(level_vals)
    if is_safe:
        return True
    else:
        for ii in range(len(level_vals)):
            new_level_vals = level_vals[:ii] + level_vals[ii + 1 :]
            # print(f"  [Bad Level] - Now checking {new_level_vals}")
            is_safe = check_level_is_safe(new_level_vals)
            if is_safe:
                return True

    return False


inputs = read_file("inputs/day2.txt")
p1_answer = 0
p2_answer = 0
for level in inputs:
    level_vals = level.split(" ")

    # Part 1
    is_level_safe = check_level_is_safe(level_vals)
    # print(f"checking {level} = {is_level_safe}")
    p1_answer += 1 if is_level_safe else 0

    # Part 2
    # print(f"Checking {level}")
    is_level_safe = check_level_is_safe_v2(level)
    p2_answer += 1 if is_level_safe else 0


print(f"P1 answer - {p1_answer}")
print(f"P2 answer - {p2_answer}")
