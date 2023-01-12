#!/usr/bin/env python3

"""
Reverse kanji review, for a random selection of characters.

Only tests those with Heisig numbers smaller than the specified value.
"""

import random
import sys

from heisig import read_kanji

if __name__ == "__main__":
    if len(sys.argv) < 2:
        limit = None
        print("No Heisig number limit passed, testing all")
    else:
        limit = int(sys.argv[1])
        print(f"Only reviewing Kanji up to {limit}")

    kanji = read_kanji(limit)
    random.shuffle(kanji)

    for k in kanji:
        input(f"{k.kanji} ? ")
        print(f"{k.keyword} [{k.strokes}] (#{k.number}, lesson {k.lesson})\n")
