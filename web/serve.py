#!/usr/bin/env python
import subprocess
from livereload import Server


def rebuild():
    subprocess.run(['mkdocs', 'build', '--quiet'], check=False)


rebuild()

server = Server()
server.watch('docs/', rebuild, delay=0.5)
server.watch('mkdocs.yml', rebuild, delay=0.5)
server.serve(root='site', host='localhost', port=8000)
