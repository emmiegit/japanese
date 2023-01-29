#!/usr/bin/env python3

# Temporary ad hoc script to generate an HTML file with elements notation in it.
# Usage: ./render_elements.py 'olden times' 'walking stick + day'

import jinja2
import sys

import elements

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <keyword> <syntax> [output-path]")
        sys.exit(1)

    keyword = sys.argv[1]
    expression = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    element = elements.parser.parse(expression)

    with open("static/style.css") as file:
        style = file.read()

    loader = jinja2.FileSystemLoader(searchpath="templates")
    env = jinja2.Environment(loader=loader)
    env.globals.update(isinstance=isinstance, types=elements.types)
    template = env.get_template("elements-full.j2")

    html = template.render({
        "keyword": keyword,
        "style": style,
        "element": element,
    })

    if output_path is None:
        print(html)
    else:
        with open(output_path, "w") as file:
            file.write(html)
