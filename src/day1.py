from typing import List
from utils import read_file

split_key = "   "
input = read_file("src/inputs/day1.txt")

first_list = []
second_list = []
for entry in input:
    entry_values = entry.split(split_key)
    first_list.append(int(entry_values[0]))
    second_list.append(int(entry_values[1]))

first_list.sort()
second_list.sort()


def get_part1_answer(first_list: List[int], second_list: List[int]):
    p1_answer = 0
    for ii in range(len(first_list)):
        diff = abs(second_list[ii] - first_list[ii])
        # print(f"{ii} - distance between {second_list[ii]} and {first_list[ii]} = {diff}")
        p1_answer += diff

    print(f"Part 1 = {p1_answer}")


def get_part2_answer(first_list: List[int], second_list: List[int]):
    p2_answer = 0
    for ii in range(len(first_list)):
        p2_answer += first_list[ii] * second_list.count(first_list[ii])

    print(f"Part 2 = {p2_answer}")


get_part1_answer(first_list, second_list)
get_part2_answer(first_list, second_list)
