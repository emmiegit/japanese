#!/usr/bin/env python3

import sys

from heisig import read_kanji_index

if __name__ == "__main__":
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
            result = "(not found)"
            exit_code = 1

        print(f"{original_query}: {result}")

    sys.exit(exit_code)
