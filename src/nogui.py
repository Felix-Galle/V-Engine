import sys
import os
import logging

from lexer import Lexer
from parser import Parser
from game import Game
  

class VEngineNoGUI:
    def __init__(self, script_path):
        self.script_path = script_path

        # Running the script without GUI
        text = open(script_path).read()
        instructions = Parser(Lexer(text)).parse() # Parses scenes and win
        Game(instructions)