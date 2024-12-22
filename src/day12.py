from collections import defaultdict
from typing import List, Set, Tuple

from utils import convert_strings_to_grid, read_file


class Plant:
    def __init__(
        self,
        location: Tuple[int, int],
        type: str,
        grid: List[List[str]],
        visit_tracker: Set["Plant"],
    ):
        self.location = location
        self.type = type
        self.grid = grid
        self.visit_tracker = visit_tracker
        self.up: Plant = None
        self.right: Plant = None
        self.down: Plant = None
        self.left: Plant = None

    def __hash__(self):
        return hash(self.location)

    def __eq__(self, other):
        return self.location == other.location

    def __is_in_bounds(self, row: int, col: int):
        return (
            row >= 0 and col >= 0 and row < len(self.grid) and col < len(self.grid[0])
        )

    def __is_same_plant_type(self, row: int, col: int):
        return self.grid[row][col] == self.type

    # Function to find a plant with a specific location in the set
    def __find_plant(
        self, plant_set: Set["Plant"], location: Tuple[int, int]
    ) -> "Plant":
        temp_plant = Plant(location, "", None, set())
        for plant in plant_set:
            if plant == temp_plant:
                return plant
        return None

    def build_region(self):
        row, col = self.location
        if not self.__is_in_bounds(row, col):  # or (row, col) in self.visit_tracker:
            return

        self.visit_tracker.add(self)

        # Up check
        if (
            self.up is None
            and self.__is_in_bounds(row - 1, col)
            and self.__is_same_plant_type(row - 1, col)
        ):
            found_plant = self.__find_plant(self.visit_tracker, (row - 1, col))
            if found_plant:
                self.up = found_plant
            else:
                self.up = Plant(
                    (row - 1, col), self.type, self.grid, self.visit_tracker
                )
                self.up.down = self
                self.up.build_region()

        # Down check
        if (
            self.down is None
            and self.__is_in_bounds(row + 1, col)
            and self.__is_same_plant_type(row + 1, col)
        ):
            found_plant = self.__find_plant(self.visit_tracker, (row + 1, col))
            if found_plant:
                self.down = found_plant
            else:
                self.down = Plant(
                    (row + 1, col), self.type, self.grid, self.visit_tracker
                )
                self.down.up = self
                self.down.build_region()

        # Right check
        if (
            self.right is None
            and self.__is_in_bounds(row, col + 1)
            and self.__is_same_plant_type(row, col + 1)
        ):
            found_plant = self.__find_plant(self.visit_tracker, (row, col + 1))
            if found_plant:
                self.right = found_plant
            else:
                self.right = Plant(
                    (row, col + 1), self.type, self.grid, self.visit_tracker
                )
                self.right.left = self
                self.right.build_region()

        # Left check
        if (
            self.left is None
            and self.__is_in_bounds(row, col - 1)
            and self.__is_same_plant_type(row, col - 1)
        ):
            found_plant = self.__find_plant(self.visit_tracker, (row, col - 1))
            if found_plant:
                self.left = found_plant
            else:
                self.left = Plant(
                    (row, col - 1), self.type, self.grid, self.visit_tracker
                )
                self.left.right = self
                self.left.build_region()

    def calculate_area(self, visited=None):
        area = 1

        if visited is None:
            visited = set()

        if self.location in visited:
            return 0

        visited.add(self.location)

        if self.up is not None and self.up.location not in visited:
            area += self.up.calculate_area(visited)

        if self.down is not None and self.down.location not in visited:
            area += self.down.calculate_area(visited)

        if self.right is not None and self.right.location not in visited:
            area += self.right.calculate_area(visited)

        if self.left is not None and self.left.location not in visited:
            area += self.left.calculate_area(visited)

        return area

    def calculate_perimeter(self, visited=None):
        permeter = (
            4
            - (self.up is not None)
            - (self.down is not None)
            - (self.right is not None)
            - (self.left is not None)
        )

        if visited is None:
            visited = set()

        if self.location in visited:
            return 0

        visited.add(self.location)

        if self.up is not None and self.up.location not in visited:
            permeter += self.up.calculate_perimeter(visited)

        if self.down is not None and self.down.location not in visited:
            permeter += self.down.calculate_perimeter(visited)

        if self.right is not None and self.right.location not in visited:
            permeter += self.right.calculate_perimeter(visited)

        if self.left is not None and self.left.location not in visited:
            permeter += self.left.calculate_perimeter(visited)

        return permeter

    def __get_plant_type(self, row: int, col: int):
        if self.__is_in_bounds(row, col):
            return self.grid[row][col]
        return "oob"

    def calculate_sides(self, visited: Set[Tuple[int, int]] = None) -> int:
        """
        This function will calculate the number of sides of the region by counting the number
        of "corners" in the region. A corner is defined as a point where the region changes direction.

        A corner is found when:
            - The diagonal grid value type != self.type or outside the current region AND
            - The adjacent cells are the same type
        """
        corners = 0

        if visited is None:
            visited = set()

        row, col = self.location

        ul_type = self.__get_plant_type(row - 1, col - 1)
        u_type = self.__get_plant_type(row - 1, col)
        l_type = self.__get_plant_type(row, col - 1)
        ur_type = self.__get_plant_type(row - 1, col + 1)
        r_type = self.__get_plant_type(row, col + 1)
        ll_type = self.__get_plant_type(row + 1, col - 1)
        d_type = self.__get_plant_type(row + 1, col)
        lr_type = self.__get_plant_type(row + 1, col + 1)

        # Check if upper left is corner
        if (self.type not in [u_type, l_type]) or (
            self.type != ul_type and self.type == u_type == l_type
        ):
            corners += 1

        # Check if upper right is corner
        if self.type not in [u_type, r_type] or (
            self.type != ur_type and self.type == u_type == r_type
        ):
            corners += 1

        # Check if lower left is corner
        if self.type not in [l_type, d_type] or (
            self.type != ll_type and self.type == l_type == d_type
        ):
            corners += 1

        # Check if lower right is corner
        if self.type not in [r_type, d_type] or (
            self.type != lr_type and self.type == r_type == d_type
        ):
            corners += 1

        visited.add(self.location)

        # Now check the adjacent cells
        if self.up is not None and self.up.location not in visited:
            corners += self.up.calculate_sides(visited)

        if self.down is not None and self.down.location not in visited:
            corners += self.down.calculate_sides(visited)

        if self.right is not None and self.right.location not in visited:
            corners += self.right.calculate_sides(visited)

        if self.left is not None and self.left.location not in visited:
            corners += self.left.calculate_sides(visited)

        return corners


class PlantRegion:
    def __init__(
        self,
        type: str,
        location: Tuple[int, int],
        visit_tracker: set,
        grid: List[List[str]],
    ):
        self.type = type
        self.grid = grid
        self.visit_tracker = visit_tracker
        self.head_plant = Plant(location, type, grid, visit_tracker)

    def build_region(self):
        self.head_plant.build_region()

    @property
    def area(self):
        return self.head_plant.calculate_area()

    @property
    def perimeter(self):
        return self.head_plant.calculate_perimeter()

    @property
    def sides(self):
        if (
            self.head_plant.up is None
            and self.head_plant.right is None
            and self.head_plant.down is None
            and self.head_plant.left is None
        ):
            return 4

        return self.head_plant.calculate_sides()


class Garden:
    def __init__(self, grid: List[List[str]], visit_tracker: set):
        self.grid = grid
        self.regions: List[PlantRegion] = []
        self.visit_tracker = visit_tracker


inputs = read_file("src/inputs/day12.txt")
grid = convert_strings_to_grid(inputs)
visit_tracker = set()
garden = Garden(grid, visit_tracker)

for row in range(len(grid)):
    for col in range(len(grid[0])):
        plant_location = Plant((row, col), "", grid, set())
        if plant_location in visit_tracker:
            continue

        plant_type = grid[row][col]
        new_region = PlantRegion(plant_type, (row, col), visit_tracker, grid)
        new_region.build_region()
        garden.regions.append(new_region)

p1_score = 0
p2_score = 0
for region in garden.regions:
    p1_score += region.area * region.perimeter
    p2_score += region.area * region.sides
    # print(
    #     f"Region {region.type} - area = {region.area}, perimeter = {region.perimeter}, sides = {region.sides}"
    # )

print(f"p1 answer = {p1_score}")
print(f"p2 answer = {p2_score}")
