import re
import itertools

class Record:

    def __init__(self, condition_records: str, damaged_count: str | list[int], scale: int = 1):
        self.condition_records = '?'.join([condition_records] * scale)
        if isinstance(damaged_count, str):
            self.damaged_count = list(map(int, damaged_count.split(','))) * scale
        else:
            self.damaged_count = damaged_count * scale
        self.missing_damaged_count = sum(self.damaged_count) - self.condition_records.count('#')
        self.missing_info = [i.start() for i in re.finditer(r'\?', self.condition_records)]
        # print(self.condition_records, self.damaged_count, self.missing_damaged_count, self.missing_info)

    def count_possibilities(self):
        """Trying recursive approach."""
        temp_condition_records: str = f"{self.condition_records.lstrip('.')}."
        temp_damaged_count: list[int] = self.damaged_count.copy()
        
        count = 0
        for char in temp_condition_records:
            if char == '?':
                if self.missing_damaged_count > len(self.missing_info):
                    return 0
                return sum(self.__class__(temp_condition_records.lstrip('.').replace('?', j, 1), temp_damaged_count).count_possibilities() for j in ('.', '#'))
            elif char == '#':
                count += 1
            elif not count:
                pass
            else:
                try:
                    if temp_damaged_count.pop(0) != count:
                        return 0
                except IndexError:
                    return 0
                else:
                    temp_condition_records = temp_condition_records.lstrip('.').lstrip('#')
                    count = 0
        return 1 if not temp_damaged_count else 0

    def generate_possibilities(self):
        for possibility in itertools.combinations(self.missing_info, self.missing_damaged_count):
            new_string = ''
            for i, char in enumerate(self.condition_records):
                if char == '?':
                    new_string += '#' if i in possibility else '.'
                else:
                    new_string += char
            yield new_string

    def count_possibilities_v1(self):
        """First version considering all possibilities."""
        possibilities = 0
        for possibility in self.generate_possibilities():
            count = index_num = 0
            for char in f'{possibility}.':
                if char == '#':
                    count += 1
                elif not count:
                    pass
                else:
                    try:
                        if self.damaged_count[index_num] == count:
                            index_num += 1
                        else:
                            break
                    except IndexError:
                        break
                    else:
                        count = 0
            else:
                possibilities += 1

        return possibilities

def run(filename: str):
    with open(filename, 'r') as file:
        return sum(Record(*line.split()).count_possibilities() for line in file)
    #     counter = i = 0
    #     for line in file:
    #         counter += Record(*line.split(), scale=5).count_possibilities()
    #         i += 1
    #         print(i)
    # return counter