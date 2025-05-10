import sys
import os
import re
import time
import tkinter as tk
from collections import defaultdict

class EntityDef:
    def __init__(self, ast_entity):
        self.name = ast_entity.name
        self.props = {}
        self.events = defaultdict(list)
        for stmt in ast_entity.statements:
            if stmt.cmd.startswith('on_'):
                self.events[stmt.cmd] = stmt.args
            else:
                self.props[stmt.cmd] = stmt.args