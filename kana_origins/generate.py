#!/usr/bin/env python3

import csv
import sys

import jinja2

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.csv>")
        sys.exit(1)

    kanji_cache = {}
    table_rows = [MARKDOWN_TABLE_HEAD]
    tables = []

    # Process the file
    with open(sys.argv[1]) as file:
        reader = csv.reader(file)

        # Skip the first row (has the column names)
        row = next(reader)
        assert row[0] == "kana"

        # Process each row
        for row in reader:
            kana, kanji, word, furigana, definition = row

            # Control word, start a new table
            if kana == "%NEW%":
                tables.append("\n".join(table_rows))
                table_rows = [MARKDOWN_TABLE_HEAD]
                continue

            # Check if it's a kanji we've already seen, then just copy
            # Duplicate rows are marked with '-'
            if kanji in kanji_cache:
                assert word == "-", f"Identical kanji {kanji}, but specified twice for {kana}"
                ruby_word, definition = kanji_cache[kanji]
            else:
                assert word != "-", f"Unique kanji {kanji} marked as duplicate for {kana}"
                ruby_word = tuple(zip(word, furigana.split(".")))
                kanji_cache[kanji] = ruby_word, definition

            table_rows.append(MARKDOWN_TABLE_ROW.render(
                kana=kana,
                kanji=kanji,
                definition=definition,
                ruby_word=ruby_word,
            ))

    if table_rows:
        tables.append("\n".join(table_rows))

    # Print final output
    print(DOCUMENT_TEMPLATE.render(tables=tables))
