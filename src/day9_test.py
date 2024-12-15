# import pytest
# from day9 import Disk


# def test_calculate_check_sum():
#     disk = Disk("2333133121414131402")
#     disk.file_array = list("00992111777.44.333....5555.6666.....8888..")
#     for idx, val in enumerate(disk.file_array):
#         if val == ".":
#             disk.file_array[idx] = None
#         else:
#             disk.file_array[idx] = int(val)

#     check_sum = disk.calculate_check_sum()
#     assert check_sum == 2858


# @pytest.mark.parametrize(
#     "input,expected",
#     [
#         ("2333133121414131499", 6204),
#         ("714892711", 813),
#         ("12101", 4),
#         ("1313165", 169),
#         ("12345", 132),
#         ("12143", 31),
#         ("14113", 16),
#         ("121", 1),
#     ],
# )
# def test_calculate_check_sum_v2(input, expected):
#     disk = Disk(input)
#     disk.compress_file_array_v2()
#     check_sum = disk.calculate_check_sum()
#     assert check_sum == expected
