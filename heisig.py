"""
Python library for loading the Heisig kanji index.
"""

import json
import gzip
import sys
import os
from collections import namedtuple
from functools import cache

Kanji = namedtuple("Kanji", ("kanji", "number_v4", "number_v6", "strokes", "elements", "keyword", "on_yomi", "kun_yomi", "hochanh_url"))

class UniqueDict(dict):
    """
    Wrapper around the regular dict object, except it errors if a key would be overwritten.
    """

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(key)

        super().__setitem__(key, value)

@cache
def read_kanji(*, limit=None, version=6):
    limit = limit or 100000
    current_directory = os.path.dirname(sys.argv[0])
    heisig_path = os.path.join(current_directory, "data", "heisig.json.gz")

    if version == 4:
        heisig_number_key = "v4"
    elif version == 6:
        heisig_number_key = "v6"
    else:
        raise ValueError(f"No stored Heisig number for version {version:r}")

    with gzip.open(heisig_path, "rt") as file:
        heisig_data = json.load(file)

    kanji = []
    for entry in heisig_data:
        if entry["heisig"][heisig_number_key] < limit:
            kanji.append(
                Kanji(
                    kanji=entry["kanji"],
                    number_v4=entry["heisig"]["v4"],
                    number_v6=entry["heisig"]["v6"],
                    strokes=entry["strokes"],
                    elements=entry["elements"],
                    keyword=entry["elements"].split(",")[0].strip(),
                    on_yomi=entry["on-yomi"],
                    kun_yomi=entry["kun-yomi"],
                    hochanh_url=entry["hochanh-url"],
                )
            )

    return kanji

@cache
def read_kanji_index(*, limit=None, version=6):
    kanji = read_kanji(limit=limit, version=version)
    index = UniqueDict()

    if version == 4:
        heisig_number_key = "number_v4"
    elif version == 6:
        heisig_number_key = "number_v6"
    else:
        raise ValueError(f"No stored Heisig number for version {version:r}")

    for entry in kanji:
        number = getattr(entry, heisig_number_key)
        index[number] = entry
        index[entry.keyword.casefold()] = entry
        index[entry.kanji] = entry

    return index

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
