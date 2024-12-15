from enum import Enum
from typing import List

valid_numbers = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "zero",
]


def read_file(filename) -> list[str]:
    with open(filename, "r") as file:
        return file.read().splitlines()


def find_number_in_string(string, starting_index=0):
    index = starting_index
    for char in string[starting_index:]:
        if char.isdigit():
            return (char, index)
        index += 1
    return None, -1


def convert_string_to_int(value):
    match value:
        case "one":
            return 1
        case "two":
            return 2
        case "three":
            return 3
        case "four":
            return 4
        case "five":
            return 5
        case "six":
            return 6
        case "seven":
            return 7
        case "eight":
            return 8
        case "nine":
            return 9
        case "zero":
            return 0
        case _:
            return int(value)


# Finds numbers in a string and returns a list of them
# Numbers can be digits or words (e.g. - one, two, etc)
def find_number_in_string_v2(string):
    found_arr = {}
    for key in valid_numbers:
        index = 0
        while index > -1:
            index = string.find(key, index)
            if index > -1:
                found_arr[index] = convert_string_to_int(key)
                index += 1
    return found_arr


def create_number_from_string_using_first_and_last_digits(input_string, use_v1=True):
    if use_v1:
        (first_number, found_index) = find_number_in_string(input_string)
        (next_number, found_index) = find_number_in_string(
            input_string, found_index + 1
        )
        last_number = first_number if found_index == -1 else next_number

        while found_index != -1:
            last_number = next_number
            (next_number, found_index) = find_number_in_string(
                input_string, found_index + 1
            )

        return int(first_number + last_number)
    else:
        found_numbers = find_number_in_string_v2(input_string)
        sorted_numbers = sorted(found_numbers.items())
        _, val = sorted_numbers[0]
        _, val2 = sorted_numbers[-1]
        numbersLen = len(sorted_numbers)
        if numbersLen == 1:
            return val * 10 + val

        return val * 10 + val2


def binary_up_to_n_places(num, n) -> str:
    """Generates a binary string representation of a number up to n places."""

    binary_str = bin(num)[2:]  # Remove the '0b' prefix
    return binary_str.zfill(n)  # Pad with zeros to the left


def ternary_up_to_n_places(num, n):
    if num == 0:
        return "0".zfill(n)
    nums = []
    while num:
        num, r = divmod(num, 3)
        nums.append(str(r))
    return ("".join(reversed(nums))).zfill(n)


class Direction(Enum):
    UNKNOWN = "unknown"
    INCREASING = "increasing"
    DECREASING = "decreasing"
