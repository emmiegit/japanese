#!/usr/bin/env python3

"""
Generate an HTML table which serves as a calendar for the month.

Each cell will be marked according to its reading, which will show on hover.
"""

import json
import os
from datetime import datetime
from enum import Enum, unique

import jinja2

@unique
class DayOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


def rotate_right(items, shift):
    if not items:
        return

    shift %= len(items)
    items.extend(items[:shift])
    del items[:shift]


class WeekBracket:
    """
    A data structure which writes left-to-right, top-down.

    Used to write day-by-day values and manage the internal
    lists without exposing the complexity to the outside.
    """

    def __init__(self):
        self.weeks = []
        self.new_row()
        self.week_index = 0
        self.day_index = 0

    def incr_day(self):
        self.day_index += 1

        if self.day_index >= 7:
            self.day_index = 0
            self.incr_week()

    def incr_week(self):
        self.week_index += 1

        if week_index > len(self.weeks):
            self.new_row()

    def day_of_week(self, start_day):
        return DayOfWeek(self.day_index + start_day.value)

    def get(self):
        return self.weeks[self.week_index][self.day_index]

    def set(self, data):
        self.weeks[self.week_index][self.day_index] = data

    def append(self, data):
        self.set(data)
        self.incr_day()

    def new_row(self):
        self.weeks.append([None] * 7)

    def done(self):
        return self.weeks


class CalendarGenerator:
    def __init__(self, start_date=None, week_start=SUNDAY, furigana=False, path="."):
        date = start_date or datetime.now()
        self.year = date.year
        self.month = date.month

        self.furigana = furigana

        with open(os.path.join(path, "..", "data", "days-of-the-month.json")) as file:
            data = json.load()
            self.month_days = data["days-of-the-month"]
            self.words = data["words"]

        with open(os.path.join(path, "..", "data", "days-of-the-week.json")) as file:
            data = json.load()
            self.week_days = data["days-of-the-week"]
            self.week_days_after = data["after"]

        self.loader = jinja2.FileSystemLoader(searchpath=path)
        self.env = jinja2.Environment(loader=self.loader)
        self.template = self.env.get_template("calendar.j2")

    def weekday_data(self, weekday_enum):
        return self.week_days[weekday_enum - 1]

    def generate_week_days(self):
        week_days = [self.weekday_data(enum) for enum in DayOfWeek]
        # (week_start.value - 1) gives us how many times we need to shift the list
        rotate_right(week_days, self.week_start.value - 1)
        return week_days

    def generate_month_days(self):
        weeks = WeekBracket()

        # Iterate until the correct day-of-week for the start of the month
        date = datetime(self.year, self.month, 1)
        while weeks.day_of_week(self.week_start) == DayOfWeek(date.isoweekday()):
            weeks.incr_day()

        for day in range(1, 32):
            try:
                date = datetime(self.year, self.month, day)
            except ValueError:
                # out of range
                break

            data = self.month_days[day - 1]
            weeks.append({
                "number": day,
                "data": data,
                "arabic": data["arabic"],
                "chinese": data["chinese"],
                "hiragana": data["hiragana"],
                "class": f"day-{data['type']}",
            })

        return weeks.done()

    def generate_context(self):
        return {
            "month": self.month,
            "year": self.year,
            "weeks": self.generate_month_days(),
            "week_days": self.generate_week_days(),
            "use_furigana": self.furigana,
        }

    def output(self, path):
        context = self.generate_context()
        html = self.template.render(context)

        with open(path, "w") as file:
            file.write(html)


if __name__ == "__main__":
    generator = CalendarGenerator()
    generator.output("month-calendar.html")
