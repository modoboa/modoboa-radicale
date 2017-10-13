"""Calendar tools."""

import datetime


def week_range(year, weeknumber):
    """Return start and end dates of a given week."""
    fmt = "%Y-%W-%w"
    start_week = datetime.datetime.strptime(
        "{}-{}-{}".format(year, weeknumber, 1), fmt)
    end_week = datetime.datetime.strptime(
        "{}-{}-{}".format(year, weeknumber, 0), fmt)
    return start_week, end_week
