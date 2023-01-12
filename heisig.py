"""
Python library for loading the Heisig kanji index.
"""

import json
import gzip
import sys
import os
from collections import namedtuple

Kanji = namedtuple("Kanji", ("number", "kanji", "keyword", "strokes", "lesson"))

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

def read_newspaper_kanji():
    current_directory = os.path.dirname(sys.argv[0])
    newspaper_path = os.path.join(current_directory, "data", "kanji-frequency-in-newspapers.txt")

    kanji_list = []
    frequencies = {}
    with open(newspaper_path, "r") as file:
        contents = file.read()

    for i, kanji in enumerate(filter(None, contents.split("\n"))):
        kanji_list.append(kanji)

        freq = i + 1
        frequencies[freq] = kanji
        frequencies[kanji] = freq

    return kanji_list, frequencies
