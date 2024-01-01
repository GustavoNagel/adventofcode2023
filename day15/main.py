from collections import defaultdict
from contextlib import suppress

def hash_me(code: str) -> int:
    current_value = 0
    for char in code:
        current_value += ord(char)
        current_value = (current_value * 17) % 256
    return current_value

def generate_boxes(line_as_list: list[str]):
    boxes: defaultdict[int, dict[str, int]] = defaultdict(dict)
    for code in line_as_list:
        label, _, focal_length = code.partition('=')
        if focal_length:
            boxes[hash_me(label)].update({label: int(focal_length)})
        else:
            label = label.strip('-')
            with suppress(KeyError):
                del boxes[hash_me(label)][label]
    return boxes

def count_total_focusing_power(boxes: defaultdict[int, dict[str, int]]) -> int:
    total = 0
    for box_number, box in boxes.items():
        for i, focal_length in enumerate(box.values()):
            total += (box_number + 1) * (i + 1) * focal_length
    return total

def get_total_focusing_power(line_as_list: list[str]) -> int:
    boxes = generate_boxes(line_as_list)
    return count_total_focusing_power(boxes)

def run(filename: str):
    with open(filename, 'r') as file:
        line_as_list = next(file).strip().split(',')
        sum_hashes = sum(hash_me(code) for code in line_as_list)
        return sum_hashes, get_total_focusing_power(line_as_list)
