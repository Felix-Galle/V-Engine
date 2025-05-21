#!/usr/bin/env python3

import sys
import logging
import datetime
import os
import platform
from lexer import Lexer
from parser import Parser
from game import Game

"""
V-Engine

Created by: Felix-Galle & thatfacelessone
Explanation found in README.md

"""

if __name__ == '__main__':

    # Requires v_engine.py + script.v
    if len(sys.argv) < 2:
        print("Usage: vengine.py <script.v>")
        sys.exit(1)

    # Finds all args
    script_file = None
    for arg in sys.argv:
        if arg.endswith('.v'):
            script_file = arg

    if not script_file:
        print("Error: No script file provided.")
        sys.exit(1)

    log_dir = './logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'vengine-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
    logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(name)s/%(levelname)s] %(asctime)s > %(message)s')
    logging.info("Starting V-Engine with script: %s", script_file)
    logging.info("Created by: %s", "Felix-Galle & thatfacelessone")
    logging.info("Python version: %s", sys.winver)
    logging.info(f"Operating system:{platform.system()}")
    logging.info("Current working directory: %s", os.getcwd())
    logging.info(f"{os.getlogin()} is running the script")

    #try:
    text = open(script_file).read()
    win, scenes = Parser(Lexer(text)).parse() # Parses scenes and win
    Game(win, scenes).run(scenes[0].name)
    # except Exception as e:
    #    logging.error("An error occurred: %s", e)
    #    sys.exit(1)