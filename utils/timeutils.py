import datetime as dt


DATE_FMT = "%m/%d"
TIME_FMT = "%I:%M%p"
YEAR_FMT = "/%y"

DATETIME_FMT = f"{TIME_FMT} {DATE_FMT}{YEAR_FMT}"

READABLE_DATE_FMT = "%-m/%d"
READABLE_TIME_FMT = "%-I:%M%p"
READABLE_YEAR_FMT = ", '%y"

MINUTE = 60
HOUR = 60 * 60
DAY = 60 * 60 * 24


def validate_datetime(datetime):
    if isinstance(datetime, int):
        return timestamp_to_datetime(datetime)
    return datetime


def str_to_datetime(string):
    return dt.datetime.strptime(string, DATETIME_FMT).replace(tzinfo=dt.timezone.utc)


def date_as_str(datetime, *args, include_year=True):
    valid = validate_datetime(datetime)
    year_fmt = YEAR_FMT if include_year else ""
    fmt = DATE_FMT + year_fmt
    return dt.datetime.strftime(valid, fmt)


def time_as_str(datetime):
    valid = validate_datetime(datetime)
    return dt.datetime.strftime(valid, TIME_FMT)


def datetime_as_str(datetime, *args, include_year=True):
    return f"{time_as_str(datetime)} {date_as_str(datetime, include_year=include_year)}"


def timestamp_to_datetime(timestamp):
    return dt.datetime.fromtimestamp(timestamp, dt.timezone.utc)


def datetime_to_timestamp(datetime):
    valid = validate_datetime(datetime)
    return int(dt.datetime.timestamp(valid))


def date_as_readable_str(datetime, *args, include_year=True):
    valid = validate_datetime(datetime)
    year_fmt = READABLE_YEAR_FMT if include_year else ""
    fmt = READABLE_DATE_FMT + year_fmt
    return dt.datetime.strftime(valid, fmt)


def time_as_readable_str(datetime):
    valid = validate_datetime(datetime)
    return dt.datetime.strftime(valid, READABLE_TIME_FMT)


def datetime_as_readable_str(datetime, *args, include_year=True):
    return f"{time_as_readable_str(datetime)} {date_as_readable_str(datetime, include_year=include_year)}"


def mins_from_midnight(timestamp):
    nearest_day = timestamp // DAY
    remainder = timestamp - (nearest_day * DAY)
    return remainder / MINUTE


def mins_to_midnight(timestamp):
    return (DAY / MINUTE) - mins_from_midnight(timestamp)


def minute_of_day(timestamp):
    return (timestamp % DAY) // MINUTE


def are_matching_dates(first, second):
    return date_as_str(first) == date_as_str(second)


def are_matching_times(first, second):
    return time_as_str(first) == time_as_str(second)
