import sys
import os
import re
import time
import tkinter as tk
from collections import defaultdict

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