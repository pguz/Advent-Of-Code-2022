# Day 20: Grove Positioning System


def parse_file(fd):
    return (fd.readlines(),)


def sum_grove_coordinates(numbers):
    j = 0
    while j < len(numbers):
        if isinstance(numbers[j], str):
            number = int(numbers.pop(j))
            new_index = (j + number) % len(numbers)
            numbers[new_index:new_index] = [number]
        else:
            j += 1

    return sum(
        numbers[(numbers.index(0) + 1000 * i) % len(numbers)] for i in range(1, 4)
    )


def sum_grove_coordinates_expanded(mixed_numbers):
    numbers = [int(n) * 811589153 for n in mixed_numbers]
    indexes = list(range(len(numbers)))

    for _ in range(10):
        for i, n in enumerate(numbers):
            num_index = indexes.index(i)
            indexes.pop(num_index)
            new_index = (num_index + n) % len(indexes)
            indexes.insert(new_index, i)

    sorted_numbers = [numbers[i] for i in indexes]
    return sum(
        sorted_numbers[(sorted_numbers.index(0) + 1000 * i) % len(sorted_numbers)] for i in range(1, 4)
    )


solution_function_01 = sum_grove_coordinates
solution_function_02 = sum_grove_coordinates_expanded
