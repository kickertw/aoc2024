from typing import List, Tuple

from utils import read_file


class Disk:
    def __init__(self, input: str):
        self.file_array = []
        id = 0
        is_file = True
        for val in list(input):
            fill_val = id if is_file else None
            self.file_array.extend([fill_val] * int(val))
            is_file = not is_file
            id += 1 if is_file else 0

    def compress_file_array(self) -> None:
        if None not in self.file_array:
            return

        left_cursor = self.file_array.index(None)
        right_cursor = len(self.file_array) - 1

        while left_cursor <= right_cursor:
            if self.file_array[right_cursor] != None:
                self.file_array[left_cursor] = self.file_array[right_cursor]
                self.file_array[right_cursor] = None
                right_cursor -= 1

            while self.file_array[right_cursor] == None and right_cursor > 0:
                right_cursor -= 1

            while self.file_array[left_cursor] != None and left_cursor < len(self.file_array):
                left_cursor += 1

    def __get_size(self, starting_idx, search_key) -> int:
        end_idx = starting_idx + 1
        size = 1
        while end_idx < len(self.file_array) and self.file_array[end_idx] == search_key:
            end_idx += 1
            size += 1

        return size

    def __find_next_empty_slot(self, min_size) -> Tuple[int, int]:
        if None not in self.file_array:
            return -1

        starting_idx = self.file_array.index(None)
        size = self.__get_size(starting_idx, None)

        while size < min_size:
            if starting_idx + size >= len(self.file_array):
                return -1

            if None not in self.file_array[starting_idx + size :]:
                return -1

            starting_idx = self.file_array.index(None, starting_idx + size)
            size = self.__get_size(starting_idx, None)

        return starting_idx

    def __find_file(self, id) -> Tuple[int, int]:
        starting_idx = self.file_array.index(id)
        size = self.__get_size(starting_idx, id)

        return starting_idx, size

    def compress_file_array_v2(self) -> None:
        highest_id = self.file_array[-1]
        current_id = highest_id

        while current_id > 0:
            right_cursor, file_size = self.__find_file(current_id)
            left_cursor = self.__find_next_empty_slot(file_size)

            if left_cursor == -1 or left_cursor >= right_cursor:
                current_id -= 1
                continue

            for ii in range(file_size):
                self.file_array[left_cursor + ii] = current_id
                self.file_array[right_cursor + ii] = None

            current_id -= 1

    def calculate_check_sum(self) -> int:
        check_sum = 0
        for index, val in enumerate(self.file_array):
            if val is None:
                continue

            check_sum += index * val

        return check_sum


# input = "3782118872134750622467835777254673636196562746855573185893741653571496603359914633393136809199145738934656846217147511147489654758495722127919572086248890763312491887551193634532769146333647596961952049941650367861312773944145132727181821933749652074618792583185519881985251922398345353546024213424945453295651222428293839898744345315636542296867459474777379362061985694193143329244455090609191811016873883378685722946994386914915813959174478873243927342572563171239857261737644249396722370762055158729431119998545233625127"
inputs = read_file("src/inputs/day9.txt")
input = inputs[0]

# Part 1
disk_map = Disk(input)
disk_map.compress_file_array()
p1_ans = disk_map.calculate_check_sum()
print(f"p1 answer = {p1_ans}")

# This is very non performant...
disk_map = Disk(input)
# print(disk_map.file_array)
disk_map.compress_file_array_v2()
p2_ans = disk_map.calculate_check_sum()
print(f"p2 answer = {p2_ans}")
