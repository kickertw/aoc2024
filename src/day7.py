from typing import List
from utils import binary_up_to_n_places, read_file, ternary_up_to_n_places


class Equation:
    def __init__(self, equation_inputs: str) -> None:
        input_parts = equation_inputs.split(":")
        self._answer = int(input_parts[0])
        self._parts = input_parts[1].strip().split(" ")

    @property
    def parts(self) -> List[str]:
        return self._parts

    @property
    def answer(self) -> int:
        return self._answer


inputs = read_file("src/inputs/day7.txt")
equations: List[Equation] = []
for input in inputs:
    equations.append(Equation(input))

p1_answer = 0
for equation in equations:
    permutations = 2 ** (len(equation.parts) - 1)
    for i in range(permutations):
        operation_list = binary_up_to_n_places(i, len(equation.parts) - 1)

        running_ans = int(equation.parts[0])
        for ii in range(1, len(equation.parts)):
            if operation_list[ii - 1] == "0":
                running_ans += int(equation.parts[ii])
            elif operation_list[ii - 1] == "1":
                running_ans *= int(equation.parts[ii])
            else:
                print("you should never get here")

        if running_ans == equation.answer:
            p1_answer += equation.answer
            break

print(f"p1 answer = {p1_answer}")

p2_answer = 0
for equation in equations:
    permutations = 3 ** (len(equation.parts) - 1)
    for i in range(permutations):
        operation_list = ternary_up_to_n_places(i, len(equation.parts) - 1)

        running_ans = int(equation.parts[0])
        for ii in range(1, len(equation.parts)):
            if operation_list[ii - 1] == "0":
                running_ans += int(equation.parts[ii])
            elif operation_list[ii - 1] == "1":
                running_ans *= int(equation.parts[ii])
            elif operation_list[ii - 1] == "2":
                running_ans = int(str(running_ans) + equation.parts[ii])
            else:
                print("you should never get here")

        if running_ans == equation.answer:
            p2_answer += equation.answer
            break

print(f"p2 answer = {p2_answer}")
