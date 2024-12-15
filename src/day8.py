from typing import List
from utils import read_file


class Grid:
    def __init__(self, inputs: List[str]):
        self.antenna_locations = {}
        self.grid: List[str] = []
        self.max_row = len(inputs) - 1
        self.max_col = len(inputs[0]) - 1

        self.antinodes = set()

        # recording the antenna locations
        # e.g. { "a": [(1,1), (2,3)] }
        row_idx = 0
        for input in inputs:
            row = list(input)
            self.grid.append(list(input))

            col_idx = 0
            for val in row:
                if val != ".":
                    if val not in self.antenna_locations.keys():
                        self.antenna_locations[val] = []

                    self.antenna_locations[val].append((row_idx, col_idx))

                col_idx += 1
            row_idx += 1

    def __is_in_bounds(self, row, col) -> bool:
        return row >= 0 and col >= 0 and row <= self.max_row and col <= self.max_col

    def __add_antinode(self, row, col):
        if not self.__is_in_bounds(row, col):
            return

        self.antinodes.add((row, col))

        # Not needed but will help for debugging
        if self.grid[row][col] == ".":
            self.grid[row][col] = "#"

    def find_antinodes(self, is_p2: bool = False):
        for freq in self.antenna_locations.keys():
            locations = self.antenna_locations[freq]
            for ii in range(len(locations)):
                for jj in range(len(locations)):
                    if ii != jj:
                        row_diff = locations[jj][0] - locations[ii][0]
                        col_diff = locations[jj][1] - locations[ii][1]

                        if not is_p2:
                            antinode1_row = locations[ii][0] + (2 * row_diff)
                            antinode1_col = locations[ii][1] + (2 * col_diff)
                            self.__add_antinode(antinode1_row, antinode1_col)

                            antinode2_row = locations[ii][0] - row_diff
                            antinode2_col = locations[ii][1] - col_diff
                            self.__add_antinode(antinode2_row, antinode2_col)
                        else:
                            self.__add_antinode(locations[ii][0], locations[ii][1])
                            self.__add_antinode(locations[jj][0], locations[jj][1])

                            antinode1_row = 0
                            antinode1_col = 0
                            multiplier = 0
                            while self.__is_in_bounds(antinode1_row, antinode1_col):
                                multiplier += 1
                                antinode1_row = locations[jj][0] + (row_diff * multiplier)
                                antinode1_col = locations[jj][1] + (col_diff * multiplier)
                                self.__add_antinode(antinode1_row, antinode1_col)

                            antinode2_row = 0
                            antinode2_col = 0
                            multiplier = 0
                            while self.__is_in_bounds(antinode2_row, antinode2_col):
                                multiplier += 1
                                antinode2_row = locations[ii][0] - (row_diff * multiplier)
                                antinode2_col = locations[ii][1] - (col_diff * multiplier)
                                self.__add_antinode(antinode2_row, antinode2_col)

    def get_antinode_count(self) -> int:
        return len(self.antinodes)

    def print_grid(self):
        for row in self.grid:
            print(row)


inputs = read_file("src/inputs/day8.txt")
grid = Grid(inputs)
grid.find_antinodes()

p1_answer = grid.get_antinode_count()
print(f"p1 = {p1_answer}")

grid = Grid(inputs)
grid.find_antinodes(True)

p2_answer = grid.get_antinode_count()
print(f"p2 = {p2_answer}")

# for key in grid.antinodes.keys():
#     print(f"{key} has {len(grid.antinodes[key])} antinodes")
#     for node in grid.antinodes[key]:
#         print(f"    {node[0]},{node[1]}")

# grid.print_grid()
