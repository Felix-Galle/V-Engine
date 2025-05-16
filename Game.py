import os
import tkinter as tk
import param
from entity_def import EntityDef
from entity_inst import EntityInst
from ast_node import Scene, Entity, Statement


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
                self.canvas = tk.Canvas(self.root, width=param.CANVAS_WIDTH, height=param.CANVAS_HEIGHT, bg=color)
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
                    self.canvas = tk.Canvas(self.root, width= param.CANVAS_WIDTH, height=param.CANVAS_HEIGHT, bg=path)
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