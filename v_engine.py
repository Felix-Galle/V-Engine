#!/usr/bin/env python3

import sys
import logging
import datetime
import os
from lexer import Lexer
from parser import Parser
from game import Game

if __name__ == '__main__':
    log_dir = './logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'vengine-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
    logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    sys.argv = ['vengine.py', 'script.v', '--debug'] # TODO: Remove this line & Uncomment this block (For normal usage)
    """if len(sys.argv) < 2:
        print("Usage: vengine.py <script.v>")
        sys.exit(1)"""

    logging.info("Starting V-Engine with script: %s", sys.argv[1])
    logging.info("Debug mode: %s", '--debug' in sys.argv)
    logging.info("Python version: %s", sys.version)
    logging.info(f"Operating system: {os.name}")
    logging.info("Current working directory: %s", os.getcwd())
    logging.info(f"{os.getlogin()} is running the script")
    try:
        text = open(sys.argv[1]).read()
        win, scenes = Parser(Lexer(text)).parse() # Parses scenes and win
        Game(win, scenes).run(scenes[0].name)
    except Exception as e:
        logging.error("An error occurred: %s", e)
        sys.exit(1)
