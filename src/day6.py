from enum import Enum
from typing import Dict, List, Tuple
from utils import read_file


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class VisitTracker:
    def __init__(self, direction: Direction, row: int, col: int):
        self.tracker: Dict[Tuple[int, int], Direction] = {}
        self.tracker[(row, col)] = direction

    def add_visit(self, direction: Direction, row: int, col: int) -> bool:
        """Adds a location + direction.
        Returns:
            True - when new location + direction
            False - if location + direction already exist (loop detection)
        """
        if (row, col) in self.tracker and self.tracker[(row, col)] == direction:
            return False

        self.tracker[(row, col)] = direction
        return True

    def has_loop(self, direction: Direction, row: int, col: int) -> bool:
        return (row, col) in self.tracker.keys() and self.tracker[(row, col)] == direction


class Map:
    def __init__(self, inputs):
        self.grid = []
        self.row_idx = 0
        self.col_idx = 0
        self.direction = Direction.UP
        self.distinct_visit_count = 0
        self._visit_tracker: VisitTracker

        index = 0
        for input in inputs:
            if "^" in input:
                self.row_idx = index
                self.col_idx = input.find("^")
                self._visit_tracker = VisitTracker(Direction.UP, self.row_idx, self.col_idx)
            self.grid.append(list(input))
            index += 1

    @property
    def grid_max_row(self):
        return len(self.grid) - 1

    @property
    def grid_max_col(self):
        return len(self.grid[0]) - 1

    @property
    def visit_tracker(self) -> VisitTracker:
        return self._visit_tracker

    def __get_next_spot(self):
        next_spot = self.row_idx, self.col_idx
        match self.direction:
            case Direction.UP:
                next_spot = self.row_idx - 1, self.col_idx
            case Direction.DOWN:
                next_spot = self.row_idx + 1, self.col_idx
            case Direction.LEFT:
                next_spot = self.row_idx, self.col_idx - 1
            case Direction.RIGHT:
                next_spot = self.row_idx, self.col_idx + 1
        return next_spot

    def __rotate_90(self):
        match self.direction:
            case Direction.UP:
                self.direction = Direction.RIGHT
            case Direction.RIGHT:
                self.direction = Direction.DOWN
            case Direction.DOWN:
                self.direction = Direction.LEFT
            case Direction.LEFT:
                self.direction = Direction.UP

    def move_guard(self, check_for_loop=False) -> bool:
        next_row_idx, next_col_idx = self.__get_next_spot()

        # If the next spot is outside of the map limits, move the guard out
        # and don't do anything else
        if (
            next_row_idx < 0
            or next_row_idx > self.grid_max_row
            or next_col_idx < 0
            or next_col_idx > self.grid_max_col
        ):
            self.row_idx = next_row_idx
            self.col_idx = next_col_idx
            return True

        if check_for_loop and self._visit_tracker.has_loop(
            self.direction, next_row_idx, next_col_idx
        ):
            return False

        if self.grid[next_row_idx][next_col_idx] == "#":
            self.__rotate_90()
            if check_for_loop and self._visit_tracker.has_loop(
                self.direction, self.row_idx, self.col_idx
            ):
                return False
            next_row_idx, next_col_idx = self.__get_next_spot()

        if self.grid[next_row_idx][next_col_idx] in [".", "^"]:
            self.grid[next_row_idx][next_col_idx] = "X"
            self.distinct_visit_count += 1
            self.row_idx = next_row_idx
            self.col_idx = next_col_idx
            self._visit_tracker.add_visit(self.direction, next_row_idx, next_col_idx)
        elif self.grid[next_row_idx][next_col_idx] == "X":
            self.row_idx = next_row_idx
            self.col_idx = next_col_idx
            self._visit_tracker.add_visit(self.direction, next_row_idx, next_col_idx)

        return True

    def is_guard_gone(self):
        return (
            self.row_idx < 0
            or self.row_idx > self.grid_max_row
            or self.col_idx < 0
            or self.col_idx > self.grid_max_col
        )

    def add_obstacle(self, row: int, col: int):
        self.grid[row][col] = "#"


inputs = read_file("inputs/day6.txt")
map = Map(inputs)

while not map.is_guard_gone():
    map.move_guard()

print(f"p1 answer = {map.distinct_visit_count}")

# Part 2
# 1. Get places visited
p2_answer = 0
visit_tracker = map.visit_tracker
for key in visit_tracker.tracker.keys():
    # reset map
    map = Map(inputs)
    map.add_obstacle(key[0], key[1])
    # print(f"adding obstacle at ({key[0]},{key[1]})")
    # map.add_obstacle(11, 48)

    loop_found = False
    counter = 0
    while not map.is_guard_gone() and counter < 16900:
        counter += 1
        has_moved = map.move_guard(True)
        # print(f"    moved to adding obstacle at ({key[0]},{key[1]})")
        if not has_moved:
            loop_found = True
            break

    p2_answer += 1 if loop_found or counter == 16900 else 0

print(f"p2 answer = {p2_answer}")
