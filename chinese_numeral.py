#!/usr/bin/env python3

"""
Converts between Arabic numerals and Chinese numerals.

Not intended to be exhaustive, just a simple script for basic enumeration.
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
    ...
