import re

number_list = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
inverted_number_list = [word[::-1] for word in number_list]
# pattern = pattern2 = re.compile(r"(?=(\d))")
pattern = re.compile(rf"(?=(\d|{'|'.join(number_list)}))")
pattern2 = re.compile(rf"(?=(\d|{'|'.join(inverted_number_list)}))")


def get_digit(line, inverted: bool = False) -> str:
    if not inverted:
        result = pattern.search(line)
        base_list = number_list
    else:
        result = pattern2.search(line[::-1])
        base_list = inverted_number_list
    return result.group(1) if result.group(1).isdigit() else str(base_list.index(result.group(1)))

def run(line: str) -> int:
    first_digit = get_digit(line)
    second_digit = get_digit(line, inverted=True)
    return int(first_digit + second_digit)

def run_and_sum() -> int:
    with open("input_file.txt", 'r') as file:
        return sum(run(line) for line in file)

if __name__ == "__main__":
    print(run_and_sum())