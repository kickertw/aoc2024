# from collections import defaultdict
from typing import List, Tuple
from utils import read_file


class Map:
    def __init__(self, inputs: List[str], is_p1=True):
        self.grid: List[List[str]] = []
        self.trailheads: List[Tuple[int, int]] = []
        self.is_p1 = is_p1

        row = 0
        for line in inputs:
            line_list = list(
                map(lambda x: int(x) if str.isnumeric(x) else -1, list(line))
            )

            col = 0
            for val in line_list:
                if val == 0:
                    self.trailheads.append((row, col))
                col += 1

            self.grid.append(line_list)
            row += 1

    def __find_next_node(
        self, row: int, col: int, id: int, visited: List[Tuple[int, int]]
    ) -> Tuple[int, int]:
        top = row - 1, col
        right = row, col + 1
        bottom = row + 1, col
        left = row, col - 1

        adjacent = [top, right, bottom, left]
        valid_nodes = []

        for node in adjacent:
            node_row = node[0]
            node_col = node[1]
            if (
                node_row >= 0
                and node_col >= 0
                and node_row < len(self.grid)
                and node_col < len(self.grid[0])
                and node not in visited
                and id == self.grid[node_row][node_col]
            ):
                valid_nodes.append(node)

        return valid_nodes

    def __calc_node_score(self, row, col, id: int = 0, visited=None) -> int:
        if visited is None:
            visited = []

        if self.is_p1:
            visited.append((row, col))

        next_nodes = self.__find_next_node(row, col, id + 1, visited)
        if id + 1 == 9:
            if self.is_p1:
                for node in next_nodes:
                    visited.append((node[0], node[1]))

            # print(f"          End Node Found - score = {len(next_nodes)}")
            return len(next_nodes)

        if len(next_nodes) == 0:
            return 0

        score = 0
        for node in next_nodes:
            # print(" " * id + f"Currently @ {id} ({node}). Getting score for {id + 1}")
            score += self.__calc_node_score(node[0], node[1], id + 1, visited)

        # print(" " * id + f"Returning score {score}")
        return score

    def calc_total_score(self) -> int:
        score = 0
        for node in self.trailheads:
            # print(f"Searching for root node score @ {node}")
            node_score = self.__calc_node_score(node[0], node[1])
            score += node_score
            # print(f"Node ({node[0]},{node[1]}) has score = {node_score}")

        return score


inputs = read_file("src/inputs/day10.txt")
map = Map(inputs)
p1_ans = map.calc_total_score()
print(f"p1 = {p1_ans}")

map.is_p1 = False
p2_ans = map.calc_total_score()
print(f"p2 = {p2_ans}")
