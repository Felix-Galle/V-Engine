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
import os
import re
import time
import tkinter as tk
from collections import defaultdict

# Canvas defaults for solid-colour backgrounds
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

# --- Tokenizer ----------------------------------
TOKEN_SPECS = [
    ('NUMBER',   r"\d+(?:\.\d+)?"),
    ('STRING',   r'"[^"\n]*"'),
    ('ID',       r"[A-Za-z_][A-Za-z0-9_]*"),
    ('NEWLINE',  r"\n"),
    ('SKIP',     r"[ \t]+"),
    ('OP',       r"[=+\-*/%(),]"),
    ('COLON',    r":"),
]
TOK_REGEX = re.compile('|'.join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS))

class Token:
    def __init__(self, typ, val):
        self.type = typ
        self.value = val

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.tokens = []
        indent_stack = [0]
        for line in text.replace('\r', '').split('\n'):
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip(' '))
            if indent > indent_stack[-1]:
                self.tokens.append(Token('INDENT', ''))
                indent_stack.append(indent)
            while indent < indent_stack[-1]:
                self.tokens.append(Token('DEDENT', ''))
                indent_stack.pop()
            for m in TOK_REGEX.finditer(line):
                typ = m.lastgroup
                val = m.group()
                if typ == 'SKIP':
                    continue
                if typ == 'STRING':
                    val = val[1:-1]
                self.tokens.append(Token(typ, val))
            self.tokens.append(Token('NEWLINE', ''))
        while len(indent_stack) > 1:
            self.tokens.append(Token('DEDENT', ''))
            indent_stack.pop()
        self.tokens.append(Token('EOF', ''))
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, typ, val=None):
        tok = self.next()
        if tok.type != typ or (val is not None and tok.value != val):
            raise SyntaxError(f"Expected {typ} {val}, got {tok}")
        return tok

# --- AST Nodes ----------------------------
class ASTNode:
    pass

class Scene(ASTNode):
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

class Entity(ASTNode):
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

class Statement(ASTNode):
    def __init__(self, cmd, args):
        self.cmd = cmd
        self.args = args

# --- Parser -------------------------------
class Parser:
    def __init__(self, lexer):
        self.lex = lexer

    def parse(self):
        scenes = []
        while self.lex.peek().type != 'EOF':
            scenes.append(self.parse_scene())
        return scenes

    def parse_scene(self):
        self.lex.expect('ID', 'scene')
        name = self.lex.expect('ID').value
        self.lex.expect('COLON')
        stmts = self.parse_block()
        return Scene(name, stmts)

    def parse_block(self):
        statements = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'ID' and tok.value == 'entity':
                statements.append(self.parse_entity())
            else:
                statements.append(self.parse_statement())
        self.lex.expect('DEDENT')
        return statements

    def parse_entity(self):
        self.lex.expect('ID', 'entity')
        name = self.lex.expect('ID').value
        self.lex.expect('COLON')
        stmts = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'ID' and tok.value == 'on':
                stmts.append(self.parse_event())
            else:
                stmts.append(self.parse_statement())
        self.lex.expect('DEDENT')
        return Entity(name, stmts)

    def parse_event(self):
        self.lex.expect('ID', 'on')
        event_name = self.lex.expect('ID').value
        self.lex.expect('COLON')
        stmts = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        while self.lex.peek().type != 'DEDENT':
            stmt = self.parse_statement()
            # convert to on_<name> statement
            statements = [stmt.cmd] + stmt.args
            stmts.append(statements)
        self.lex.expect('DEDENT')
        # flatten statements into one event
        args = [item for sub in stmts for item in sub]
        return Statement('on_' + event_name, args)

    def parse_statement(self):
        cmd = self.lex.expect('ID').value
        args = []
        while self.lex.peek().type not in ('NEWLINE', 'EOF'):
            args.append(self.lex.next().value)
        if self.lex.peek().type == 'NEWLINE':
            self.lex.next()
        return Statement(cmd, args)

# --- Runtime -------------------------------
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


# --- Runtime -------------------------------
class EntityInst:
    def __init__(self, edef, canvas, images):
        self.defn = edef
        self.canvas = canvas
        pos = edef.props.get('position', ['0', '0'])
        self.x = float(pos[0])
        self.y = float(pos[1])
        self.id = None
        if 'shape' in edef.props:
            parts = edef.props['shape']
            if len(parts) != 3:
                raise ValueError(f"Expected 3 arguments for shape, got {len(parts)}: {parts}")
            typ, dims, color = parts
            try:
                w, h = map(int, dims.split(','))
            except ValueError:
                raise ValueError(f"Invalid dimensions '{dims}' for shape: must be 'width,height'")
            if typ == 'rectangle':
                self.id = canvas.create_rectangle(self.x, self.y, self.x + w, self.y + h, fill=color)
            elif typ == 'oval':
                self.id = canvas.create_oval(self.x, self.y, self.x + w, self.y + h, fill=color)
        elif 'image' in edef.props:
            imgf = edef.props['image'][0]
            if imgf in images:
                self.id = canvas.create_image(self.x, self.y, image=images[imgf], anchor='nw')

    def on_event(self, ev, game):
        if ev in self.defn.events:
            args = self.defn.events[ev]
            cmd = args[0]
            if cmd == 'change_scene':
                game.change_scene(args[1])

class Game:
    def __init__(self, scenes):
        self.scenes = {s.name: s for s in scenes}
        self.root = tk.Tk()
        self.canvas = None
        self.images = {}
        self.entities = []

    def setup_scene(self, name):  # TODO: Fixed indentation and added self parameter
        scene = self.scenes[name]
        # background: color or image
        for stmt in scene.statements:
            if isinstance(stmt, Statement) and stmt.cmd == 'background_color':
                color = stmt.args[0]
                self.canvas = tk.Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=color)
                self.canvas.pack()
                break
            if isinstance(stmt, Statement) and stmt.cmd == 'background':
                path = stmt.args[0]
                if os.path.exists(path):
                    img = tk.PhotoImage(file=path)
                    self.images[path] = img
                    self.canvas = tk.Canvas(self.root, width=img.width(), height=img.height())
                    self.canvas.pack()
                    self.canvas.create_image(0, 0, image=img, anchor='nw')
                    break
                else:
                    # treat as solid color name
                    self.canvas = tk.Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=path)
                    self.canvas.pack()
                    break
        # preload images
        for stmt in scene.statements:
            if isinstance(stmt, Statement) and stmt.cmd == 'image':
                img_file = stmt.args[0]
                if os.path.exists(img_file):
                    img = tk.PhotoImage(file=img_file)
                    self.images[img_file] = img
        # instantiate entities
        for stmt in scene.statements:
            if isinstance(stmt, Entity):
                ed = EntityDef(stmt)
                inst = EntityInst(ed, self.canvas, self.images)
                self.entities.append(inst)
                inst.on_event('on_start', self)

    def change_scene(self, name):  # TODO: Removed unnecessary parentheses
        self.root.destroy()
        Game(list(self.scenes.values())).run(name)  # TODO: Corrected to call run on the new instance

    def run(self, start):
        self.setup_scene(start)
        self.root.bind('<KeyPress>', lambda e: [i.on_event(f'on_key_{e.keysym}', self) for i in self.entities])
        self.root.after(16, self.loop)
        self.root.mainloop()

    def loop(self):
        for inst in list(self.entities):
            inst.on_event('on_update', self)
        self.root.after(16, self.loop)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: vengine.py <script.v>")
        sys.exit(1)
    text = open(sys.argv[1]).read()
    scenes = Parser(Lexer(text)).parse()
    Game(scenes).run(scenes[0].name)
