#!/usr/bin/env python3

import csv
import os
import sys
from collections import namedtuple

import jinja2

KanaOriginEntry = namedtuple("KanaOriginEntry", ("kana", "kanji", "definition", "ruby"))


class KanaOriginGenerator:
    def __init__(self):
        self.cache = {}

    def ingest_csv(self, path):
        with open(path) as file:
            reader = csv.reader(file)

            # Skip the first row (has the column names)
            row = next(reader)
            assert row[0] == "kana"

            # Ingest each row
            entries = []
            for row in reader:
                entries.append(self.ingest_row(row))

        return entries

    def ingest_row(self, row):
        kana, kanji, word, furigana, definition = row

        # If this character doesn't have an example word, then return None.
        # Intentionally missing rows are marked with '~'
        if word == "~":
            self.cache[kanji] = None
            return None

        # Check if it's a kanji we've already seen, then just copy
        # Duplicate rows are marked with '-'
        if kanji in self.cache:
            assert word == "-", f"Identical kanji {kanji}, but specified twice for {kana}"
            entry = self.cache[kanji]

            if entry is None:
                # No example word
                return KanaOriginEntry(
                    kana=kana,
                    kanji=kanji,
                    definition=None,
                    ruby=None,
                )
            else:
                # Otherwise, build as normal
                ruby_word, definition = self.cache[kanji]
        else:
            assert word != "-", f"Unique kanji {kanji} marked as duplicate for {kana}"
            ruby_word = tuple(zip(word, furigana.split(".")))
            self.cache[kanji] = ruby_word, definition

        return KanaOriginEntry(
            kana=kana,
            kanji=kanji,
            definition=definition,
            ruby=ruby_word,
        )


if __name__ == "__main__":
    # Ingest CSV files
    generator = KanaOriginGenerator()
    hiragana = generator.ingest_csv("hiragana.csv")
    katakana = generator.ingest_csv("katakana.csv")

    # Set up Jinja environment
    loader = jinja2.FileSystemLoader(searchpath=".")
    env = jinja2.Environment(loader=loader)
    template = env.get_template("document.j2")

    # Output markdown
    with open("README.md", "w") as file:
        markdown = template.render(hiragana=hiragana, katakana=katakana)
        file.write(markdown)
