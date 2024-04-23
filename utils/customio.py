import csv


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


def _infer_type(string):
    if string.isnumeric():
        if "." in string:
            return float(string)
        return int(string)
    return string

