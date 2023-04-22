#!/usr/bin/env python3

"""
Generate an HTML table which displays the day of the week association table.
"""

import argparse
import json
import os

import jinja2


class TableGenerator:
    def __init__(self, *, week_start="Sunday", furigana=True, path="."):
        self.furigana = furigana

        with open(os.path.join(path, "..", "data", "days-of-the-week.json")) as file:
            data = json.load(file)
            self.week_days = rotate_week_days(data["days-of-the-week"], week_start)
            self.after = data["after"]
            self.words = data["words"]

        self.loader = jinja2.FileSystemLoader(searchpath=path)
        self.env = jinja2.Environment(loader=self.loader)
        self.env.globals.update(
            is_string=lambda s: isinstance(s, str),
            zip=zip,
        )
        self.template = self.env.get_template("table.j2")

    def generate_context(self):
        return {
            "week_days": self.week_days,
            "after": self.after,
            "words": self.words,
            "use_furigana": self.furigana,
        }

    def output(self, path):
        context = self.generate_context()
        html = self.template.render(context)

        with open(path, "w") as file:
            file.write(html)


def rotate_week_days(week_days, week_start):
    week_start = week_start.lower()

    while week_days[0]["english"].lower() != week_start:
        item = week_days.pop(0)
        week_days.append(item)

    return week_days


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Japanese day-of-week association table renderer")
    argparser.add_argument(
        "-s",
        "--start-day",
        dest="start_day",
        default="Sunday",
        help="Day of week to begin a week on.",
    )
    argparser.add_argument(
        "-F",
        "--furigana",
        "--use-furigana",
        action="store_true",
        dest="use_furigana",
        help="Whether to add furigana to the days of the week."
    )
    argparser.add_argument(
        "-p",
        "--path",
        dest="path",
        default=".",
        help="What path to read data from. Assumed to be the week_days directory of the repository by default.",
    )
    argparser.add_argument(
        "-o",
        "--output",
        dest="output",
        default="table.html",
        help="What path to output the final HTML to.",
    )
    args = argparser.parse_args()

    generator = TableGenerator(
        week_start=args.start_day,
        path=args.path,
    )
    generator.output(args.output)
