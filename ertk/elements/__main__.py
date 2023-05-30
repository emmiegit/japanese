import readline
from pprint import pprint

from .parser import parser

if __name__ == "__main__":
    readline.parse_and_bind("tap: complete")
    readline.parse_and_bind("set editing-mode vi")

    while True:
        try:
            prompt = input("> ")
        except EOFError:
            break

        if prompt in ('q', 'quit', 'exit'):
            break

        tree = parser.parse(prompt)
        if tree is not None:
            pprint(tree)
