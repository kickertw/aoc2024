from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple
import functools


@functools.cache
def split_rock(rock_id: str) -> Tuple[str, str]:
    left_rock = rock_id[0 : len(rock_id) // 2]
    right_rock = rock_id[len(rock_id) // 2 :]

    while left_rock[0] == "0" and len(left_rock) > 1:
        left_rock = left_rock[1:]

    while right_rock[0] == "0" and len(right_rock) > 1:
        right_rock = right_rock[1:]

    return left_rock, right_rock


def blink(rocks: List[str]) -> List[str]:
    """
    Works fine for part 1, but def not part 2 with 75 blinks.
    This is a very nieve approach
    """
    temp_rocks: List[int] = []
    for rock in rocks:
        if rock == "0":
            temp_rocks.append("1")
        elif len(rock) % 2 == 0:
            left, right = split_rock(rock)
            temp_rocks.extend([left, right])
        else:
            temp_rocks.append(str(int(rock) * 2024))

    return temp_rocks


def blink_v2(rocks: defaultdict[str, int]) -> DefaultDict[str, int]:
    temp_rocks = defaultdict(int)

    for key in rocks:
        if key == "0":
            temp_rocks["1"] += rocks["0"]
        elif len(key) % 2 == 0:
            left, right = split_rock(key)
            temp_rocks[left] += rocks[key]
            temp_rocks[right] += rocks[key]
        else:
            new_key = str(int(key) * 2024)
            temp_rocks[new_key] += rocks[key]

    return temp_rocks


def list_to_dict(list: List[str]) -> DefaultDict[str, int]:
    ret_val = defaultdict(int)
    for val in list:
        ret_val[val] += ret_val[val] if ret_val[val] > 0 else 1

    return ret_val


def count_rocks(rocks: DefaultDict[str, int]) -> int:
    ret_val = 0
    for key in rocks:
        ret_val += rocks[key]

    return ret_val


input = "5910927 0 1 47 261223 94788 545 7771"
rocks = input.split()

blinks = 75
rocks_v2 = list_to_dict(rocks)
for ii in range(blinks):
    # rocks = blink(rocks)
    # print(f"blinked {ii} time(s) - total rocks = {len(rocks)}")

    rocks_v2 = blink_v2(rocks_v2)
    # print(f"blink_v2 {ii} time(s) - total rocks = {count_rocks(rocks_v2)}")

print(f"{count_rocks(rocks_v2)}")

# p1_ans = count_rocks(rocks_v2)
# print(f"p1 = {p1_ans}")
