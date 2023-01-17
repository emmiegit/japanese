## 言葉

Kotoba is a flash card-lite program I wrote to supplement my vocabulary study. Previously I had a deck in [Anki](https://ankiweb.net/about) where I added new words I had seen (but hadn't learned in Tango) or the kanji form of a word usually in hiragana. However Anki aims to ensure perfect memorization, drilling until it's known. For this deck, I've found I have a reasonable enough recollection of words after only seeing them a few times, even if I don't get it "right" before moving on.

This program seeks to remedy this. It is similar to Anki but is more forgiving with when cards are "done". The goal is simply to expose myself to the items occasionally and ensure loose retention that way.

### Execution

The program is a locally-run web app. Start the web server, study, then take it down.

Setup:

```
$ pip3 install --user requirements.txt
```

Run:

```
$ flask run
```

Default settings:
* Location: http://localhost:12754/
* Port: `12754`
* Database: `kotoba.sqlite`
