from utils import read_file
import numpy as np


def test_solution(x, y, x_mult, y_mult, expected):
    x_int = int(x)
    y_int = int(y)
    actual = (x_int * x_mult) + (y_int * y_mult)
    return actual == expected


def numpy_solve(x, y, p_xy):
    a = np.array([x, y])
    b = np.array(p_xy)
    button_presses = np.linalg.solve(a, b)
    button_presses[0] = button_presses[0].round()
    button_presses[1] = button_presses[1].round()
    return button_presses


def cramer_solve(a_x, a_y, b_x, b_y, p_x, p_y):
    A = (p_x * b_y - p_y * b_x) / (a_x * b_y - a_y * b_x)
    B = (a_x * p_y - a_y * p_x) / (a_x * b_y - a_y * b_x)
    return A, B


# Button A: X+77, Y+52
# Button B: X+14, Y+32
# Prize: X=5233, Y=14652
inputs = read_file("src/inputs/day13.txt")
ii = 0
x = []
y = []
ab = []
p1_ans = 0
p1_ans2 = 0
p2_tweak = 10000000000000
for input in inputs:
    if len(input) == 0:
        ii = 0
        x.clear()
        y.clear()
        continue

    if ii < 2:
        x.append(int(input[12:14]))
        y.append(int(input[18:]))
    else:
        x_idx = input.index("X=")
        y_idx = input.index("Y=")
        ab = [
            int(input[x_idx + 2 : y_idx - 2]) + p2_tweak,
            int(input[y_idx + 2 :]) + p2_tweak,
        ]

        button_presses_np = numpy_solve(x, y, ab)
        button_presses_cr = cramer_solve(x[0], y[0], x[1], y[1], ab[0], ab[1])

        if (
            test_solution(button_presses_np[0], button_presses_np[1], x[0], x[1], ab[0])
            and test_solution(
                button_presses_np[0], button_presses_np[1], y[0], y[1], ab[1]
            )
            and button_presses_cr[0] >= 0
            # and button_presses_cr[0] < 101
            and button_presses_cr[1] >= 0
            # and button_presses_cr[1] < 101
        ):
            cr_solution_works = test_solution(
                button_presses_cr[0], button_presses_cr[1], x[0], x[1], ab[0]
            )
            np_solution_works = test_solution(
                button_presses_np[0], button_presses_np[1], x[0], x[1], ab[0]
            )
            print(f"{cr_solution_works} - Button presses:     {button_presses_cr}")
            print(f"{np_solution_works} - Button presses OG:  {button_presses_np}")

            score = int(button_presses_cr[0]) * 3 + int(button_presses_cr[1])
            p1_ans += score

            score2 = int(button_presses_np[0].round()) * 3 + int(
                button_presses_np[1].round()
            )
            p1_ans2 += score2

            print(f"Score: {p1_ans} / {p1_ans2}")
            print("")
    ii += 1

print(f"answer: {p1_ans} / {p1_ans2}")
