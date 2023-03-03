#!/usr/bin/env python3

import csv
import sys

import jinja2

DOCUMENT_TEMPLATE = jinja2.Template("""\
## ひらがな

[Origin Chart](https://commons.wikimedia.org/wiki/File:Hiragana_origin.svg)

{{ tables[0] }}

## カタカナ

[Origin Chart](https://commons.wikimedia.org/wiki/File:Katakana_origine.svg)

{{ tables[1] }}
""")

MARKDOWN_TABLE_HEAD = """\
| Kana | Kanji | Example Word | Definition |
|:----:|:-----:|:------------:|:----------:|\
"""

MARKDOWN_TABLE_ROW = jinja2.Template("| {{ kana }} | {{ kanji }} | {% if ruby_word %}<ruby>{% for ch, furigana in ruby_word %}{{ ch }}<rp>(</rp><rt>{{ furigana }}</rt><rp>)</rp>{% endfor %}</ruby>{% endif %} | {{ definition }} |")

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
