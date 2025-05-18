#!/usr/bin/env python3

import sys
import logging

from lexer import Lexer
from parser import Parser
from game import Game

if __name__ == '__main__':
    sys.argv = ['vengine.py', 'script.v', '--debug']
    """if len(sys.argv) < 2: # TODO: Uncomment this block (For normal usage)
        print("Usage: vengine.py <script.v>")
        sys.exit(1)"""

    text = open(sys.argv[1]).read()
    scenes = Parser(Lexer(text)).parse()
    Game(scenes).run(scenes[0].name)
