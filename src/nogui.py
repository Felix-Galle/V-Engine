import sys
import os
import logging

from lexer import Lexer
from parser import Parser
from game import Game
  

class VEngineNoGUI:
    def __init__(self, script_file=None):
        self.script_file = script_file

        # Running the script without GUI
        try:
            text = open(script_file).read()
            win, scenes = Parser(Lexer(text)).parse() # Parses scenes and win
            Game(win, scenes).run(scenes[0].name)
        except Exception as e:
            logging.error("An error occurred: %s", e)
            sys.exit(1)