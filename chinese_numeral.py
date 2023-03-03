#!/usr/bin/env python3

"""
Converts between Arabic numerals and Chinese numerals.

Not intended to be exhaustive, just a simple script for basic enumeration.
If you need to actually use this for something, find a proper library.
"""

DIGITS = [
    "零",
    "一",
    "二",
    "三",
    "四",
    "五",
    "六",
    "七",
    "八",
    "九",
]

UNITS = [
    ("十", 10),
    ("百", 100),
    ("千", 1_000),
    ("万", 10_000),
    ("億", 100_000_000),
    ("兆", 1_000_000_000_000),
    ("京", 10_000_000_000_000_000),
]

UNIT_ALIASES = {
    "0": 0,
    "1": 1,
    "壱": 1,
    "壹": 1,
    "弌": 1,
    "2": 2,
    "弐": 2,
    "弍": 2,
    "貳": 2,
    "貮": 2,
    "3": 3,
    "参": 3,
    "弎": 3,
    "4": 4,
    "5": 5,
    "伍": 5,
    "6": 6,
    "陸": 6,
    "7": 7,
    "漆": 7,
    "柒": 7,
    "8": 8,
    "捌": 8,
    "9": 9,
    "玖": 9,
    "廿": 20,
}

def chinese_value(cchar):
    # Error checking
    if len(cchar) != 1:
        raise ValueError(f"Not a character: {cchar!r}")

    for value, kanji in enumerate(DIGITS):
        if kanji == cchar:
            return value

    for kanji, value in UNITS:
        if kanji == cchar:
            return value

    try:
        return UNIT_ALIASES[kanji]
    except KeyError:
        raise ValueError(f"No numeric value found for character {cchar}")


def arabic_to_chinese(num, leading_one=False):
    # Special case for zero
    if num == 0:
        return DIGITS[0]

    # Negative numbers
    if num < 0:
        return "-" + arabic_to_chinese(-num)

    # Optimization for small digits
    if num < 10:
        return DIGITS[num]

    # Each unit
    result = []
    for kanji, value in reversed(UNITS):
        part, num = divmod(num, value)

        if part == 0:
            continue

        if part != 1 or leading_one:
            result.append(arabic_to_chinese(part))

        result.append(kanji)

    # Last digit, finish
    if num > 0:
        result.append(DIGITS[num])

    return "".join(result)


def chinese_to_arabic(cnum):
    # TODO
    raise NotImplementedError
