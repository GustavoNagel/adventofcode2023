import numpy as np

num_ref = {
    "O": 1,
    ".": 0,
}

cycles_options = (
    True,  # North
    True,  # West
    False,  # South
    False,  # East
)

def calculate_load(tilted_platform: np.ndarray):
    _, b = tilted_platform.shape
    weight_1 = np.array(range(b, 0, -1), np.int32)
    return (tilted_platform * weight_1).sum()

def tilt_platform(platform: np.ndarray, sort_reverse: bool, replace_for_num: bool = True):
    tilted_platform = []
    for column in platform:
        new_column, sub_column = [], []
        for piece in column:
            if piece != "#":
                sub_column.append(num_ref[piece] if replace_for_num else piece)
            else:
                new_column.extend(sorted(sub_column, reverse=sort_reverse))
                new_column.append(0 if replace_for_num else "#")
                sub_column = []
        if sub_column:
            new_column.extend(sorted(sub_column, reverse=sort_reverse))
        tilted_platform.append(new_column)
    return np.array(tilted_platform)

def is_platform_in_historical_records(
    platform: np.ndarray,
    historical_platform_records: dict[int, np.ndarray],
) -> int | None:
    for i, each_platform in historical_platform_records.items():
        if (each_platform == platform).all():
            return i

def apply_cycles(platform: np.ndarray, times: int):
    historical_platform_records = {}
    for index in range(times):
        for sort_reverse in cycles_options:
            platform = tilt_platform(platform.transpose(), sort_reverse=sort_reverse, replace_for_num=False)
        if i:= is_platform_in_historical_records(platform, historical_platform_records):
            return historical_platform_records[(i + (times - index) % (index - i)) - 1]
        else:
            historical_platform_records[index] = platform
    return platform

def get_platform_load(platform: np.ndarray, cycles: int = 0):
    """Get platform load.

    If cycles are not applied, we must tilt platform to north to calculate load over North,
    otherwise we tilt platform to east (cycle final position) and still calculate load over North.
    """
    platform = apply_cycles(platform, times=cycles)
    if not cycles:
        tilted_platform = tilt_platform(platform.transpose(), sort_reverse=True, replace_for_num=True)
        return calculate_load(tilted_platform)
    else:
        tilted_platform = tilt_platform(platform, sort_reverse=False, replace_for_num=True)
        return calculate_load(tilted_platform.transpose())

def run(filename: str, cycles: int = 0):
    with open(filename, 'r') as file:
        ref = [list(line) for line in map(lambda x: x.strip(), file) if line]
        load_sum = get_platform_load(np.array(ref), cycles)
    return load_sum

if __name__ == "__main__":
    print(run("input_file.txt"))
    print(run("input_file.txt", cycles=1_000_000_000))
