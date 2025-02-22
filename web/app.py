import os
import markdown
import markdown_mermaidjs

from flask import Flask
from settings import MACHINE_ROOT

SIMPLE_CSS = '<link rel="stylesheet" ' \
    'href="https://unpkg.com/simpledotcss/simple.min.css">' \
    '<style>' \
    'h1,h2,h3,h4,h5,h6 { margin: 0.5rem; }' \
    'p { margin: 0.5rem; }' \
    '.mermaid { height: 60vw; }' \
    '</style>'

app = Flask(__name__)

@app.route('/')
def readme():
    with open(os.path.join(MACHINE_ROOT, 'README.md')) as f:
        html = markdown.markdown(
            f.read(), extensions=["markdown_mermaidjs"]
        )
        return SIMPLE_CSS + html

if __name__ == '__main__':
    app.run()
