import importlib

if __name__ == "__main__":
    day_number = int(input('Which day do you wanna run?'))
    day_module = importlib.import_module(f'day{day_number:0>2}.main')
    print(day_module.run(filename=f'day{day_number:0>2}/input_file.txt'))
