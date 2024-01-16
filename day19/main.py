import operator
import re
from copy import deepcopy
from functools import reduce

workflow_internal_pattern = re.compile(r'([xmas]{1})([\<\>]{1})(\d+)\:(\w+)')
workflow_pattern = re.compile(r'^(\w+)\{([\<\>\:\w\,]+)\,(\w+)\}$')
rating_pattern = re.compile(r'^\{([xmas\=\d\,]+)+\}$')


class Ratings:

    def __init__(self, ratings_str: str):
        for rating in ratings_str.split(','):
            key, value = rating.split('=')
            setattr(self, key, int(value))

    def sum(self):
        return sum(getattr(self, k) for k in 'xmas')


class Workflow:

    def __init__(self, name: str, conditions: str, otherwise: str):
        self.name = name
        self.conditions = conditions
        self.otherwise = otherwise

    def _iter_over_conditions(self):
        for condition in workflow_internal_pattern.finditer(self.conditions):
            key, sign, value, go_to = condition.groups()
            yield key, sign, value, go_to

    def evaluate_ratings(self, ratings: Ratings):
        for key, sign, value, go_to in self._iter_over_conditions():
            actual_value = getattr(ratings, key)
            if eval(f'{actual_value}{sign}{value}'):
                return go_to
        return self.otherwise

    def get_possible_approval_ranges(self, initial_ranges: dict[str, set]):
        negative_ranges = initial_ranges
        for key, sign, value, go_to in self._iter_over_conditions():
            positive_ranges = deepcopy(negative_ranges)
            range_1 = set(range(1, int(value)) if sign == '<' else range(int(value) + 1, 4001))
            negative_ranges = deepcopy(positive_ranges)
            positive_ranges[key].intersection_update(range_1)
            negative_ranges[key].difference_update(range_1)
            if go_to != 'R':
                yield go_to, positive_ranges
        if self.otherwise != 'R':
            yield self.otherwise, negative_ranges


def is_ratings_approved(ratings: Ratings, workflow_dict: dict[str, Workflow]) -> bool:
    is_approved = 'in'
    while is_approved not in ('A', 'R'):
        current_workflow = workflow_dict[is_approved]
        is_approved = current_workflow.evaluate_ratings(ratings)
    return is_approved == 'A'


def get_probability(ranges: dict[str, set]):
    return reduce(operator.mul, (len(x) for x in ranges.values()))


def get_nested_workflows(
    workflow_name: str,
    workflow_dict: dict[str, Workflow],
    ranges: dict[str, set],
):
    _sum = 0
    workflow = workflow_dict[workflow_name]
    for go_to, new_ranges in workflow.get_possible_approval_ranges(ranges):
        # print(go_to, [len(x) for x in new_ranges.values()])
        if go_to == 'A':
            _sum += get_probability(new_ranges)
        else:
            _sum += get_nested_workflows(go_to, workflow_dict, new_ranges)
    return _sum

def get_sum_approved_probability(workflow_dict: dict[str, Workflow]):
    initial_ranges = {k: set(range(1,4001)) for k in 'xmas'}
    return get_nested_workflows('in', workflow_dict, initial_ranges)


def run(filename: str):
    with open(filename, 'r') as file:
        sum_approved_ratings = 0
        workflow_dict = {}
        workflow_flag = True
        for line in file:
            if workflow_flag:
                match_object = workflow_pattern.match(line)
                if match_object is not None:
                    workflow = Workflow(*match_object.groups())
                    workflow_dict[workflow.name] = workflow
                else:
                    workflow_flag = False
                    continue
            else:
                match_object = rating_pattern.match(line)
                ratings = Ratings(match_object.group(1))
                if is_ratings_approved(ratings, workflow_dict):
                    sum_approved_ratings += ratings.sum()
        return sum_approved_ratings, get_sum_approved_probability(workflow_dict)

if __name__ == "__main__":
    print(run("input_file.txt"))
