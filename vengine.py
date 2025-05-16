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
from lexer import Lexer
from parser import Parser
from game import Game

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: vengine.py <script.v>")
        sys.exit(1)
    text = open(sys.argv[1]).read()
    scenes = Parser(Lexer(text)).parse()
    Game(scenes).run(scenes[0].name)
