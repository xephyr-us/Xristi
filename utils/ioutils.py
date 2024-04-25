from importlib.machinery import SourceFileLoader
import csv
import os


_ASSIGN_SYM = "="

_WINDOWS_RELATIVE_START = ".\\"
_UNIX_RELATIVE_START = "./"


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


def read_key_value_file(path, casefold_keys=False, extend_filepaths=False):
    contents = {}
    with open(path, "r") as file:
        for line in file.readlines():
            stripped = line.strip()
            key, value = stripped.split(_ASSIGN_SYM)
            key = key.lower() if casefold_keys else key
            value = _infer_type(value)
            if extend_filepaths and isinstance(value, str):
                context = os.path.split(path)[0]
                value = _extend_value_if_filepath(value, context)
            contents[key] = value
    return contents


def absolute_subdirectories(path):
    assert os.path.isdir(path)
    for file in os.listdir(path):
        subpath = os.path.join(path, file)
        if os.path.isdir(subpath):
            yield os.path.abspath(subpath)


def is_in_directory(filename, path):
    assert os.path.isdir(path)
    return filename in os.listdir(path)


def import_module_from_source(path):
    name = os.path.basename(path).split(".")[0]
    module = SourceFileLoader(name, path).load_module()
    return module


def _infer_type(string):
    if string.isnumeric():
        if "." in string:
            return float(string)
        return int(string)
    return string


def _extend_value_if_filepath(value, context):
    if value.startswith(_WINDOWS_RELATIVE_START) or value.startswith(_UNIX_RELATIVE_START):
        return context + value[1:]
    return value
