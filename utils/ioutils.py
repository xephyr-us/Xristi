from importlib.machinery import SourceFileLoader
import inspect
import csv
import os


_ASSIGN_SYM = "="

_WINDOWS_RELATIVE_START = ".\\"
_UNIX_RELATIVE_START = "./"

_cached_csv_writers = {}



def read_csv(path):
    """
    Yields each row of a csv file as a tuple.
    """
    with open(path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row):
                yield tuple(_infer_type(s) for s in row)


def write_csv(path, *row):
    """
    Appends all arguments as a new row to a csv file.
    """
    if path in _cached_csv_writers.keys():
        writer = _cached_csv_writers[path]
    else:
        with open(path, "a", newline="") as file:
            writer = csv.writer(file)
        _cached_csv_writers[path] = writer
    writer.writerow(row)


def read_config(path):
    """
    Returns a dictionary containing the contents of a config file.
    Keys are lowercased for casefolding.
    """
    path = os.path.abspath(path)
    contents = {}
    with open(path, "r") as file:
        for line in file.readlines():
            stripped = line.strip()
            if stripped:
                key, value = stripped.split(_ASSIGN_SYM)
                key = key.lower()
                context = os.path.split(path)[0]
                value = _extend_value_if_filepath(_infer_type(value), context)
                contents[key] = value
    return contents


def absolute_subdirectories(path):
    """
    Yields the absolute path of each subdirectory within a directory.
    """
    assert os.path.isdir(path)
    for file in os.listdir(path):
        subpath = os.path.join(path, file)
        if os.path.isdir(subpath):
            yield os.path.abspath(subpath)


def directory_contains(dir, filename):
    """
    Returns True if a file of the given name exists within the given directory.
    """
    assert os.path.isdir(dir)
    return filename in os.listdir(dir)


def import_module_from_source(path):
    """
    Returns a reference to a Python file as a module object.
    """
    name = os.path.basename(path).split(".")[0]
    module = SourceFileLoader(name, path).load_module()
    return module


def value_if_mapped(d, key):
    """
    Returns None if the given key does not exist within the given dictionary; returns the mapped value otherwise.
    """
    return d[key] if key in d.keys() else None


def get_cwd(depth=0):
    """
    Returns the current working directory of the Python file inwhich it's called.
    """
    caller = inspect.stack()[1 + depth][1]
    return os.path.split(os.path.abspath(caller))[0]


def _infer_type(string):
    """
    Attempts to convert a string into an appropriate datatype for its content.
    ie: "100" become int(100), "5.444" becomes float(5.444), "dog" remains "dog"
    """
    if string.isnumeric():
        if "." in string:
            return float(string)
        return int(string)
    return string


def _extend_value_if_filepath(value, context):
    """
    If the given value is a relative file path, convert it to its absolute path using the given context;
    otherwise return the value.
    """
    if value.startswith(_WINDOWS_RELATIVE_START) or value.startswith(_UNIX_RELATIVE_START):
        return context + value[1:]
    return value
