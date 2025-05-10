#!/usr/bin/env python3
"""
V Engine: A robust DSL interpreter for V-language game scripts.
Features:
- Indentation-based DSL parsing
- Scenes, entities, events (start, update, key_<Key>, collision)
- Actions: spawn, destroy, set, change_scene
- Solid-colour or image backgrounds
- Shape-based entities (rectangle, oval)
- 60fps game loop
"""

import sys
import os
import re
import time
import tkinter as tk
from collections import defaultdict
from Lexer import Lexer
from Parser import Parser
from Game import Game


# Canvas defaults for solid-colour backgrounds
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

TOKEN_SPECS = [
    ('NUMBER',   r"\d+(?:\.\d+)?"),
    ('STRING',   r'"[^"\n]*"'),
    ('ID',       r"[A-Za-z_][A-Za-z0-9_]*"),
    ('NEWLINE',  r"\n"),
    ('SKIP',     r"[ \t]+"),
    ('OP',       r"[=+\-*/%(),]"),
    ('COLON',    r":"),
]
TOK_REGEX = re.compile('|'.join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS))



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: vengine.py <script.v>")
        sys.exit(1)
    text = open(sys.argv[1]).read()
    scenes = Parser(Lexer(text)).parse()
    Game(scenes).run(scenes[0].name)
