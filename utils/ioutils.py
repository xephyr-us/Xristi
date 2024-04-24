import csv


ASSIGN_SYM = "="


def read_csv(path):
    with open(path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if not len(row):
                continue
            yield tuple(_infer_type(s) for s in row)


def write_csv(path, *row):
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)


def read_key_value_file(path):
    contents = {}
    with open(path, "r") as file:
        for line in file.readlines():
            stripped = line.strip()
            key, value = stripped.split(ASSIGN_SYM)
            contents[key] = _infer_type(value)
    return contents


def _infer_type(string):
    if string.isnumeric():
        if "." in string:
            return float(string)
        return int(string)
    return string

