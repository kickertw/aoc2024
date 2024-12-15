from typing import List, Tuple
from utils import read_file


def get_inputs(inputs: List[str]):
    ordering_rules = {}
    pages_to_produce = []
    on_ordering_rules = True
    for input in inputs:
        if on_ordering_rules and len(input) == 0:
            on_ordering_rules = False
            continue

        if on_ordering_rules:
            rule = input.split("|")

            if rule[0] in ordering_rules:
                ordering_rules[rule[0]].append(rule[1])
            else:
                ordering_rules[rule[0]] = [rule[1]]
        else:
            # read pages to produce
            pages_to_produce.append(input.split(","))

    return ordering_rules, pages_to_produce


def get_middle_index_val(row) -> int:
    middle_index = int((len(row) - 1) / 2)
    return int(row[middle_index])


def is_row_valid(rules, page_to_produce) -> Tuple[bool, str, str]:
    index = 0
    is_valid_row = True

    while is_valid_row and index < len(page_to_produce) - 1:
        current_page = page_to_produce[index]
        running_index = index + 1
        while running_index < len(page_to_produce):
            next_page = page_to_produce[running_index]
            if next_page in rules:
                # if the current page is found, we know this should be after the next page
                # and therefore have an invalid ordering
                if current_page in rules[next_page]:
                    is_valid_row = False
                    break
            running_index += 1

        if is_valid_row:
            index += 1

    return is_valid_row, index, running_index


def get_p1_total(rules, pages_to_produce) -> int:
    p1_answer = 0
    for page_to_produce in pages_to_produce:
        is_valid, _, _ = is_row_valid(rules, page_to_produce)

        if is_valid:
            p1_answer += get_middle_index_val(page_to_produce)
    return p1_answer


def list_value_swap(values, index_a, index_b) -> List[str]:
    new_values = values.copy()
    temp_val = new_values[index_a]
    new_values[index_a] = new_values[index_b]
    new_values[index_b] = temp_val
    return new_values


def get_p2_total(rules, pages_to_produce) -> int:
    p2_answer = 0
    for page_to_produce in pages_to_produce:
        is_valid, index_a, index_b = is_row_valid(rules, page_to_produce)
        if is_valid:
            continue

        fixed_list = page_to_produce.copy()
        while not is_valid:
            fixed_list = list_value_swap(fixed_list, index_a, index_b)
            is_valid, index_a, index_b = is_row_valid(rules, fixed_list)

        p2_answer += get_middle_index_val(fixed_list)

    return p2_answer


inputs = read_file("src/inputs/day5.txt")
rules, pages_to_produce = get_inputs(inputs)

p1_answer = get_p1_total(rules, pages_to_produce)
p2_answer = get_p2_total(rules, pages_to_produce)

print(f"p1 sum = {p1_answer}")
print(f"p2 sum = {p2_answer}")
