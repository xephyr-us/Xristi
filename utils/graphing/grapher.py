
import matplotlib.pyplot as plt

from utils import timekeeper as timeutil
from utils import customio as ioutil

from .entry import SleepEntry


class Grapher:

    def __init__(self, csv_filepath, output_filepath):
        self._csv = csv_filepath
        self._output = output_filepath
        self._axes = None

    def __call__(self, *args, **kwargs):
        self.graph()

    def graph(self):
        ranges = self._read_csv()
        entries = self._build_entries(ranges)
        self._init_graph()
        self._graph_entries(entries)

    def _read_csv(self):
        ranges = []
        for start, end in ioutil.read_csv(self._csv):
            ranges.append((start, end))
        return ranges

    def _build_entries(self, ranges):
        entries = []
        for start, end in ranges:
            if timeutil.are_matching_dates(start, end):
                entries.append(self._build_same_day_entry(start, end))
            else:
                entries.append(self._build_first_entry(start))
                entries.extend(self._build_middle_entries(start, end))
                entries.append(self._build_last_entry(end))
        return entries

    def _init_graph(self):
        _, self._axes = plt.subplots()
        plt.title("Sleep by Date")
        plt.xlabel("Date")
        plt.ylabel("Time of day")
        plt.grid(axis="y", zorder=0)
        plt.ylim(-1440, 0)
        plt.xticks(fontsize=8)
        self._axes.set_yticks(range(0, -1441, -120))
        self._axes.set_yticklabels(
            ["{}:00".format(h) for h in range(0, 24, 2)] + ["00:00"]
        )

    def _graph_entries(self, entries):
        if self._axes is None:
            return
        self._axes.bar(
            x=[e.title for e in entries],
            height=[-e.length for e in entries],
            bottom=[-e.start for e in entries],
            color="#7e27a3",
            zorder=3
        )
        plt.show()

    def _build_same_day_entry(self, start, end):
        first_minute = timeutil.minute_of_day(start)
        last_minute = timeutil.minute_of_day(end)
        return SleepEntry(
            timeutil.date_as_readable_str(start, include_year=False),
            first_minute,
            last_minute - first_minute
        )

    def _build_first_entry(self, start):
        return SleepEntry(
            timeutil.date_as_readable_str(timeutil.timestamp_to_datetime(start), include_year=False),
            timeutil.minute_of_day(start),
            timeutil.mins_to_midnight(start)
        )

    def _build_middle_entries(self, start, end):
        output = []
        end_date = timeutil.date_as_str(end)
        current = start + timeutil.DAY
        while timeutil.date_as_str(current) != end_date:
            entry = SleepEntry(
                timeutil.date_as_readable_str(current, include_year=False),
                0,
                timeutil.DAY / timeutil.MINUTE
            )
            output.append(entry)
            current += timeutil.DAY
        return output

    def _build_last_entry(self, end):
        return SleepEntry(
            timeutil.date_as_readable_str(timeutil.timestamp_to_datetime(end), include_year=False),
            0,
            timeutil.mins_from_midnight(end)
        )
