#!/usr/bin/python3

"""
Generation script for an Anki "Kana" deck.
"""

import gzip
import json
import os

import genanki

OUTPUT_PATH = "kana.apkg"
KANA_DATA_PATH = "data/kana.json.gz"

def _load_kana(path=KANA_DATA_PATH):
    with gzip.open(path) as file:
        return json.load(file)

KANA_DATA = _load_kana()

CARD_CSS = """\
.card {
    font-family: arial;
    font-size: 3.5em;
    text-align: center;
    color: black;
    background-color: white;
}

.info {
    font-family: arial;
    font-size: 0.4em;
}
"""

MODEL_ID = 103818381
DECK_ID = 103818390

DECK_TIMESTAMP = 1670821200

NOT_VOICED = 0
VOICED = 1
HALF_VOICED = 2

HIRAGANA = KANA_DATA['words']['hiragana']
KATAKANA = KANA_DATA['words']['katakana']
KANJI = KANA_DATA['words']['kanji']
ROMAJI = KANA_DATA['words']['romaji']

MAIN_DECK = "Kana"
HIRAGANA_DECK = "Kana::Hiragana"
HIRAGANA_VOICED_DECK = "Kana::Hiragana::1. Voiced"
HIRAGANA_YOON_DECK = "Kana::Hiragana::2. Yōon"
HIRAGANA_FOREIGN_DECK = "Kana::Hiragana::3. Foreign"
HIRAGANA_OBSOLETE_DECK = "Kana::Hiragana::4. Obsolete"
KATAKANA_DECK = "Kana::Katakana"
KATAKANA_VOICED_DECK = "Kana::Katakana::1. Voiced"
KATAKANA_YOON_DECK = "Kana::Katakana::2. Yōon"
KATAKANA_FOREIGN_DECK = "Kana::Katakana::3. Foreign"
KATAKANA_OBSOLETE_DECK = "Kana::Katakana::4. Obsolete"


class NoDuplicateSet(set):
    def add(self, item):
        if item in self:
            raise KeyError(f"Item already in set: {item!r}")

        print(f"Adding new item: {item!r}")
        super().add(item)


def make_info(kana_type, *, voiced=NOT_VOICED, digraph=False, foreign=False, obsolete=False):
    parts = []
    tags = []

    if kana_type == HIRAGANA:
        tags.append("Hiragana")
    elif kana_type == KATAKANA:
        tags.append("Katakana")

    if voiced == VOICED:
        parts.append("Voiced")
        tags.append("Kana-Voiced")
    elif voiced == HALF_VOICED:
        parts.append("Half-voiced")
        tags.append("Kana-Voiced")
        tags.append("Kana-Halfvoiced")

    if digraph:
        parts.append("Yōon")
        tags.append("Kana-Yoon")

    if foreign:
        parts.append("Foreign sound")
        tags.append("Kana-Foreign")

    if obsolete:
        parts.append("Obsolete")
        tags.append("Kana-Obsolete")

    if parts:
        return (f"[{kana_type}] {', '.join(parts)}", tags)
    else:
        return (f"[{kana_type}]", tags)


def get_kana(romaji):
    for kana in KANA_DATA['kana']:
        if kana['romaji'] == romaji:
            return kana

    return ValueError(f"No kana found for '{romaji}'")


if __name__ == "__main__":
    # To catch duplicates
    all_kana = NoDuplicateSet()

    # Create kana model
    model = genanki.Model(
        MODEL_ID,
        'Kana',
        fields=[
            {'name': 'Kana'},
            {'name': 'Romaji'},
            {'name': 'Info'},
        ],
        templates=[
            {
                'name': 'Kana Card',
                'qfmt': '{{Kana}}<div class="info">{{Info}}</div>',
                'afmt': '{{Kana}}<div class="info">{{Info}}</div><hr id="answer"><em>{{Romaji}}</em></hr>',
            },
            {
                'name': 'Romaji Card',
                'qfmt': '<em>{{Romaji}}</em><div class="info">{{Info}}</div>',
                'afmt': '<em>{{Romaji}}</em><div class="info">{{Info}}</div><hr id="answer">{{Kana}}</hr>',
            },
        ],
        css=CARD_CSS, # BUG: this doesn't affect the card model?
    )

    # Create decks
    main_deck = genanki.Deck(DECK_ID, MAIN_DECK)
    hiragana_deck = genanki.Deck(DECK_ID + 1, HIRAGANA_DECK)
    katakana_deck = genanki.Deck(DECK_ID + 2, KATAKANA_DECK)
    hiragana_voiced_deck = genanki.Deck(DECK_ID + 3, HIRAGANA_VOICED_DECK)
    hiragana_yoon_deck = genanki.Deck(DECK_ID + 4, HIRAGANA_YOON_DECK)
    hiragana_foreign_deck = genanki.Deck(DECK_ID + 5, HIRAGANA_FOREIGN_DECK)
    hiragana_obsolete_deck = genanki.Deck(DECK_ID + 6, HIRAGANA_OBSOLETE_DECK)
    katakana_voiced_deck = genanki.Deck(DECK_ID + 7, KATAKANA_VOICED_DECK)
    katakana_yoon_deck = genanki.Deck(DECK_ID + 8, KATAKANA_YOON_DECK)
    katakana_foreign_deck = genanki.Deck(DECK_ID + 9, KATAKANA_FOREIGN_DECK)
    katakana_obsolete_deck = genanki.Deck(DECK_ID + 10, KATAKANA_OBSOLETE_DECK)

    # Generate notes
    for kana in KANA_DATA['kana']:
        # Extract fields
        voiced = kana.get('voiced', NOT_VOICED)
        legacy = kana.get('legacy', False)

        # Add non-voiced non-legacy notes
        if voiced == NOT_VOICED and not legacy:
            info, tags = make_info(HIRAGANA)
            hiragana_deck.add_note(genanki.Note(
                model=model,
                fields=[
                    kana['hiragana'],
                    kana['romaji'],
                    info,
                ],
                tags=tags,
            ))
            all_kana.add(kana['hiragana'])

            info, tags = make_info(KATAKANA)
            katakana_deck.add_note(genanki.Note(
                model=model,
                fields=[
                    kana['katakana'],
                    kana['romaji'],
                    info,
                ],
                tags=tags,
            ))
            all_kana.add(kana['katakana'])

        # Add voiced non-legacy notes
        elif voiced != NOT_VOICED:
            info, tags = make_info(HIRAGANA, voiced=voiced)
            hiragana_voiced_deck.add_note(genanki.Note(
                model=model,
                fields=[
                    kana['hiragana'],
                    kana['romaji'],
                    info,
                ],
                tags=tags,
            ))
            all_kana.add(kana['hiragana'])

            info, tags = make_info(KATAKANA, voiced=voiced)
            katakana_voiced_deck.add_note(genanki.Note(
                model=model,
                fields=[
                    kana['katakana'],
                    kana['romaji'],
                    info,
                ],
                tags=tags,
            ))
            all_kana.add(kana['katakana'])

        # Add legacy notes
        else:
            assert legacy, "Not a legacy kana"

            info, tags = make_info(HIRAGANA, obsolete=True)
            hiragana_obsolete_deck.add_note(genanki.Note(
                model=model,
                fields=[
                    kana['hiragana'],
                    kana['romaji'],
                    info,
                ],
                tags=tags,
            ))
            all_kana.add(kana['hiragana'])

            info, tags = make_info(KATAKANA, obsolete=True)
            katakana_obsolete_deck.add_note(genanki.Note(
                model=model,
                fields=[
                    kana['katakana'],
                    kana['romaji'],
                    info,
                ],
                tags=tags,
            ))
            all_kana.add(kana['katakana'])

    # Add new foreign kana
    for kana in KANA_DATA['kana-foreign']:
        voiced = kana.get('voiced', 0)

        info, tags = make_info(HIRAGANA, foreign=True, voiced=voiced)
        hiragana_foreign_deck.add_note(genanki.Note(
            model=model,
            fields=[
                kana['hiragana'],
                kana['romaji'],
                info,
            ],
            tags=tags,
        ))
        all_kana.add(kana['hiragana'])

        info, tags = make_info(KATAKANA, foreign=True, voiced=voiced)
        katakana_foreign_deck.add_note(genanki.Note(
            model=model,
            fields=[
                kana['katakana'],
                kana['romaji'],
                info,
            ],
            tags=tags,
        ))
        all_kana.add(kana['katakana'])

    # Add yo-on
    for digraph_base_romaji in KANA_DATA['kana-digraph']:
        for digraph_small in KANA_DATA['kana-digraph-small']:
            digraph_base = get_kana(digraph_base_romaji)
            digraph_romaji = digraph_base_romaji[:-1] + digraph_small['romaji']
            digraph_hiragana = digraph_base['hiragana'] + digraph_small['hiragana']
            digraph_katakana = digraph_base['katakana'] + digraph_small['katakana']
            digraph_voiced = digraph_base.get('voiced', NOT_VOICED)

            info, tags = make_info(HIRAGANA, digraph=True, voiced=digraph_voiced)
            hiragana_yoon_deck.add_note(genanki.Note(
                model=model,
                fields=[
                    digraph_hiragana,
                    digraph_romaji,
                    info,
                ],
                tags=tags,
            ))
            all_kana.add(digraph_hiragana)

            info, tags = make_info(KATAKANA, digraph=True, voiced=digraph_voiced)
            katakana_yoon_deck.add_note(genanki.Note(
                model=model,
                fields=[
                    digraph_katakana,
                    digraph_romaji,
                    info,
                ],
                tags=tags,
            ))
            all_kana.add(digraph_katakana)

    # Create package
    genanki.Package([
        main_deck,
        hiragana_deck,
        katakana_deck,
        hiragana_voiced_deck,
        hiragana_yoon_deck,
        hiragana_foreign_deck,
        hiragana_obsolete_deck,
        katakana_voiced_deck,
        katakana_yoon_deck,
        katakana_foreign_deck,
        katakana_obsolete_deck,
    ]).write_to_file(OUTPUT_PATH, DECK_TIMESTAMP)
