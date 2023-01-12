#!/usr/bin/env python3

"""
Determines statistics related to Heisig review and kanji in newspapers.

Given the current Heisig number, it sees which kanji have and haven't been
seen compared to their frequency in the kanji newspaper list.
"""

import sys

from heisig import read_kanji, read_newspaper_kanji


def print_newspaper_frequency(frequency_learned, count):
    learned = sum(1 for learned in frequency_learned[:count] if learned)
    percent = learned / count * 100
    print(f"Learned {learned} of the top {count} kanji ({percent:.3}%)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <heisig-number>")
        sys.exit(1)

    heisig_number = int(sys.argv[1])
    heisig = read_kanji(heisig_number)
    heisig_map = {kanji.kanji: kanji for kanji in heisig}
    frequency_list, frequency_map = read_newspaper_kanji()

    frequency_learned = []
    for i, kanji in enumerate(frequency_list):
        frequency_learned.append(kanji in heisig_map)

    print_newspaper_frequency(frequency_learned, 50)
    print_newspaper_frequency(frequency_learned, 100)
    print_newspaper_frequency(frequency_learned, 500)
    print_newspaper_frequency(frequency_learned, 1000)
    print_newspaper_frequency(frequency_learned, len(frequency_list))
