"""
Python library for loading the Heisig kanji index.
"""

import json
import gzip
import sys
import os
from collections import namedtuple
from functools import cache

Kanji = namedtuple("Kanji", ("number", "kanji", "keyword", "strokes", "lesson"))

@cache
def read_kanji(limit=None):
    limit = limit or 100000
    current_directory = os.path.dirname(sys.argv[0])
    heisig_path = os.path.join(current_directory, "data", "heisig.json.gz")

    with gzip.open(heisig_path, "rt") as file:
        heisig_data = json.load(file)

    kanji = []
    for entry in heisig_data:
        if entry["number"] < limit:
            kanji.append(
                Kanji(
                    number=entry["number"],
                    kanji=entry["kanji"],
                    keyword=entry["keyword"],
                    strokes=entry["strokes"],
                    lesson=entry["lesson"],
                )
            )

    return kanji

@cache
def read_newspaper_kanji():
    current_directory = os.path.dirname(sys.argv[0])
    newspaper_path = os.path.join(current_directory, "data", "kanji-frequency-in-newspapers.txt.gz")

    with gzip.open(newspaper_path, "rt") as file:
        newspaper_data = file.read()

    kanji_list = []
    frequencies = {}

    for i, kanji in enumerate(filter(None, newspaper_data.split("\n"))):
        kanji_list.append(kanji)

        freq = i + 1
        frequencies[freq] = kanji
        frequencies[kanji] = freq

    return kanji_list, frequencies
