#!/usr/bin/env python3

import sys

from heisig import read_kanji_index


def format_result(result):
    if result is None:
        return "(not found)"

    if isinstance(result, list):
        return ", ".join(map(format_result, result))

    if result.alt_kanji is None:
        alternate = ""
    else:
        alternate = f", alt: {result.alt_kanji}"

    return f"{result.kanji} (\"{result.keyword}\", {result.strokes}画{alternate})"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [query...]")
        sys.exit(1)

    index = read_kanji_index()
    exit_code = 0

    for original_query in sys.argv[1:]:
        try:
            if original_query.isdigit():
                query = int(original_query)
            else:
                query = original_query.casefold()

            result = index[query]
        except KeyError:
            result = None
            exit_code = 1

        print(f"{original_query}: {format_result(result)}")

    sys.exit(exit_code)
