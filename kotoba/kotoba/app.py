import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.j2')

@app.route('/card/next')
def next_card():
    # TODO

@app.route('/card/answer')
def answer_card():
    # TODO
