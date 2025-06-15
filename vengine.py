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
        self.script_path = None
        self.gui = False  # Default to no GUI
        self.setup_logging()
        self.env_info()
        self.parse_args()
        self.script_path = self.find_script_file()

    def find_script_file(self):
        logging.info("Fetching script's path...")
        script_path = None
        """
        Search for the script file in the project directory and its subfolders.
        Warn if found in an inappropriate folder.
        Returns the absolute path if found, else None.
        """
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        inappropriate_folders = ['.github', 'logs', 'src','.git','__pycache__'] 
        # the list could be endless, cuz user stoopid ¯\_(ツ)_/¯

        for root, dirs, files in os.walk(project_root):
            if self.script_file in files:
                script_path = os.path.join(root, self.script_file)
                # Check if in an inappropriate folder
                rel_path = os.path.relpath(root, project_root)
                parts = rel_path.split(os.sep)
                if any(part in inappropriate_folders for part in parts):
                    logging.warning(f"Script file '{self.script_file}' found in inappropriate folder: {root}")
                break

        if not script_path:
            logging.error(f"Script file '{self.script_file}' not found in project directory.")

        logging.info(f"Script Path: {script_path}")
        return script_path

    def setup_logging(self):
        log_dir = '../logs'
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'vengine.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='[%(module)s.%(funcName)s/%(levelname)s] %(asctime)s > %(message)s'
            #format='[%(module)s/%(levelname)s] %(asctime)s > %(message)s' # Less detail
        )
        logging.info("V-Engine logging started")

    def parse_args(self):
        logging.info("Checking args...")
        for arg in self.argv:
            logging.info(f"arg: {arg}") # TODO: Remove, just for Testing.
            if arg.endswith('.vng') or arg.endswith('.v'):
                self.script_file = arg
                if arg.endswith('.v'):
                    logging.warning("Script using .v file extension, consider using .vng for better compatibility.\n\tThis is due " \
                    "to file extension maybe being mixed up with verilog files. ")
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
        if not self.gui and not self.script_file:
            logging.critical(f"Script ({self.script_file}) not found!")
            logging.info("exiting...")
            sys.exit()

    def env_info(self):
        '''
        Print environment information for debugging purposes.
        '''
        logging.info("Created by: %s", "thatfacelessone & Felix-Galle")
        try:
            user = os.getlogin()
        except Exception:
            user = "Unknown"
        logging.info(f"{user} is running the script")
        logging.info("Python executable: %s", sys.executable)
        logging.info("Python version: %s", getattr(sys, 'winver', platform.python_version()))
        logging.info(f'Operating system: "{platform.system()} {platform.release()}" Build: {platform.version()}')
        logging.info("Current working directory: %s", os.getcwd())
        

    def run(self):
        if self.gui:
            app = VEngineGUI()
            app.mainloop()
        if self.script_path is None:
            logging.critical(f"Script ({self.script_file}) not found!")
            logging.info("exiting...")
            sys.exit()

        else:
            try:
                app = VEngineNoGUI(self.script_path)
                app.run()
            except Exception as e:
                logging.error(f"An error occurred: {e}")

    def helpme(self):
        print("Usage: vengine.py <script.v>")
        print("Options:")
        print("  --help       Show this help message and exit")
        print("  --open       Open the script file in Notepad (nonoperational, yet -_- )")
        print("  --debug      Enable debug mode")
        print("  --verbose    Enable debug mode (alias for --debug)")
        print("  +gui         Run the script with GUI")
        print("  --gui        Run the script with GUI (alias for +gui)")

if __name__ == '__main__':
    engine = VEngine(sys.argv)
    engine.run()