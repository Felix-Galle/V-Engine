#!/usr/bin/env python3

import sys
import logging
import datetime
import os
import platform
from lexer import Lexer
from nogui import VEngineNoGUI
from parser import Parser
from game import Game
from gui import VEngineGUI

"""
V-Engine

Created by: Felix-Galle & thatfacelessone
Explanation found in README.md

"""

class VEngine:
    def __init__(self, argv):
        self.argv = argv
        self.script_file = None
        self.gui = True  # Default to GUI mode
        self.setup_logging()
        self.parse_args()

    def setup_logging(self):
        log_dir = './logs'
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'vengine.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='[%(module)s.%(funcName)s/%(levelname)s] %(asctime)s > %(message)s'
            #format='[%(module)s/%(levelname)s] %(asctime)s > %(message)s'
        )
        logging.info("V-Engine logging started")

    def parse_args(self):
        self.gui = False
        logging.info("Checking args...")
        for arg in self.argv:
            logging.info(f"arg: {arg}") # TODO: Remove, just for Testing.
            if arg.endswith('.vng') or arg.endswith('.v'):
                self.script_file = arg
                if arg.endswith('.v'):
                    logging.warning("Using .v file extension, consider using .vng for better compatibility.\n\tThis is due " \
                    "to file extension being mixed up with verilog files.")
            if arg == '--help':
                self.helpme()
                sys.exit(0)
            if arg == '--open':
                if self.script_file:
                    os.system("notepad.exe " + self.script_file)
                else:
                    print("No script file to open.")
            if arg == '--debug' or arg == '--verbose':
                logging.getLogger().setLevel(logging.DEBUG)
                logging.debug("Debug mode enabled")
            if arg == '+gui' or arg == '--gui':
                logging.info("GUI mode enabled")
                self.gui = True

    def run(self):
        '''
        if not self.script_file and not self.gui:
            print("Error: No script file provided.")
            logging.error("No script file provided.")
            self.helpme()
            sys.exit(1)'''

        logging.info("Created by: %s", "thatfacelessone & Felix-Galle")
        logging.info("Python executable: %s", sys.executable)
        logging.info("Python version: %s", getattr(sys, 'winver', platform.python_version()))
        logging.info(f"Operating system: {platform.system()} {platform.release()} {platform.version()}")
        logging.info("Current working directory: %s", os.getcwd())
        try:
            user = os.getlogin()
        except Exception:
            user = "Unknown"
        logging.info(f"{user} is running the script")

        if self.gui:
            app = VEngineGUI()
            app.mainloop()
        else:
            app = VEngineNoGUI(self.script_file)
            app.run()

    def helpme(self):
        print("Usage: vengine.py <script.v>")
        print("Options:")
        print("  --help       Show this help message and exit")
        print("  --open       Open the script file in Notepad (nonoperational, yet -_- )")
        print("  --debug      Enable debug mode")
        print("  --verbose    Enable debug lmode (alias for --debug)")
        print("  +gui         Run the script with GUI")
        print("  --gui        Run the script with GUI (alias for +gui)")

if __name__ == '__main__':
    engine = VEngine(sys.argv)
    engine.run()