from collections import defaultdict
from typing import List, Tuple
from utils import read_file
from PIL import Image


class Robot:
    def __init__(self, input: str, max_width: int, max_height: int):
        self.location: Tuple[int, int] = None
        self.velocity: Tuple[int, int] = None
        self.max_width = max_width
        self.max_height = max_height
        self.__parse_input(input)

    def __parse_input(self, input: str):
        idx = input.index(" v=")
        position = input[2:idx].split(",")
        velo = input[idx + 3 :].split(",")
        self.location = int(position[0]), int(position[1])
        self.velocity = int(velo[0]), int(velo[1])

    def move(self):
        new_x = (self.location[0] + self.velocity[0]) % max_width
        new_y = (self.location[1] + self.velocity[1]) % max_height

        self.location = new_x, new_y

    def get_quadrant(self):
        x = self.location[0]
        y = self.location[1]
        x_midpoint = (self.max_width - 1) / 2
        y_midpoint = (self.max_height - 1) / 2

        if x < x_midpoint and y < y_midpoint:
            return 1

        if x > x_midpoint and y < y_midpoint:
            return 2

        if x < x_midpoint and y > y_midpoint:
            return 3

        if x > x_midpoint and y > y_midpoint:
            return 4

        return -1

    def to_string(self, show_location_only=False):
        output = (
            f"I'm at {self.location} and move {self.velocity}"
            if not show_location_only
            else f"I'm at {self.location}"
        )
        print(output)


robots: List[Robot] = []
max_width = 101
max_height = 103
inputs = read_file("src/inputs/day14.txt")
for input in inputs:
    robot = Robot(input, max_width, max_height)
    robots.append(robot)

# Part 1
seconds_elapsed = 100
quadrants = defaultdict(int)
for robot in robots:
    for _ in range(seconds_elapsed):
        robot.move()
    quadrant = robot.get_quadrant()
    quadrants[quadrant] += 1
    # robot.to_string(True)

p1_ans = quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4]
print(f"p1 = {p1_ans}")

# Part 2
# The X-Mas tree was found on 7623s
# Generate images based on robot locations and drop a pixel in the image
for s in range(10000):
    img = Image.new("RGB", (max_width, max_height), "black")
    pixels = img.load()
    for robot in robots:
        robot.move()
        pixels[robot.location[0], robot.location[1]] = (255, 255, 255)
    if s > 7000:
        filename = "images/day14/" + str(s + 1) + ".png"
        img.save(filename)
