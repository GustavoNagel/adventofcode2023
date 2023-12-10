import math

def solve_quadratic_equation(a, b, c):
    delta = (b ** 2 - 4 * a * c)
    x1 = (-b - delta ** 0.5) / (2 * a)
    x2 = (-b + delta ** 0.5) / (2 * a)
    return x1, x2

class Race:

    def __init__(self, total_time: int, record_distance: int) -> None:
        self.total_time = total_time
        self.record_distance = record_distance

    def count_winning_possibilities(self):
        """Count ways to win.

        n * (total_time - n) > record_distance
        - n ** 2 + total_time * n - record_distance > 0 
        """
        solution = solve_quadratic_equation(-1, self.total_time, -self.record_distance)
        min_x = math.floor(min(solution)) + 1
        max_x = math.ceil(max(solution)) - 1
        return max_x - min_x + 1

def run(filename: str, ignore_spaces: bool = False):
    with open(filename, 'r') as file:
        if ignore_spaces:
            first_line = [int(next(file)[9:].replace(" ", ""))]
            second_line = [int(next(file)[9:].replace(" ", ""))]
        else:
            first_line = list(map(int, next(file)[9:].split()))
            second_line = list(map(int, next(file)[9:].split()))
    number_ways_to_win = 1
    for _time, _distance in zip(first_line, second_line):
        race = Race(_time, _distance)
        number_ways_to_win *= race.count_winning_possibilities()
    return number_ways_to_win

if __name__ == "__main__":
    print(run("input_file.txt"))
    print(run("input_file.txt", ignore_spaces=True))