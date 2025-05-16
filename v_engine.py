#!/usr/bin/env python3

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
