import os
import tkinter as tk
import logging

import param
from entity_def import EntityDef
from entity_inst import EntityInst
from ast_node import Win, Scene, Entity, Statement

# Game class: Manages scenes, entities, and the game loop
class Game:
    def __init__(self, win, scenes):
        logging.debug("Using Game constructor")
        logging.debug(f"Creating Game with window: {win}")
        logging.debug(f"Creating Game with scenes: {scenes}")
        # Initialize the game with a dictionary of scenes
        self.win = win  # Window definition (title and dimensions)
        self.scenes = {s.name: s for s in scenes}
        self.root = tk.Tk()  # Create the main Tkinter window
        self.canvas = None  # Canvas for rendering the game
        self.images = {}  # Dictionary to store preloaded images
        self.entities = []  # List of entity instances in the current scene

    def setup_scene(self, name):
        # Set up the game window with the specified title and dimensions
        self.root.title(self.win.title)
        width, height = self.win.dimensions
        self.root.geometry(f"{width}x{height}") # TODO: Remove, I can't find a use.
        # Set up the specified scene by name
        scene = self.scenes[name]

        # Handle background setup (color or image)
        for stmt in scene.statements:
            if isinstance(stmt, Statement) and stmt.cmd == 'background_color':
                # Set background color
                color = stmt.args[0]
                self.canvas = tk.Canvas(self.root, width=width, height=height, bg=color)
                self.canvas.pack()
                break
            if isinstance(stmt, Statement) and stmt.cmd == 'background':
                # Set background image or fallback to color
                path = stmt.args[0]
                if os.path.exists(path):
                    # Load and display background image
                    img = tk.PhotoImage(file=path)
                    self.images[path] = img
                    self.canvas = tk.Canvas(self.root, width=img.width(), height=img.height())
                    self.canvas.pack()
                    self.canvas.create_image(0, 0, image=img, anchor='nw')
                    break
                else:
                    # Treat as a solid color name
                    self.canvas = tk.Canvas(self.root, width=scene.width, height=scene.height, bg=path)
                    self.canvas.pack()
                    break

        # Preload images specified in the scene
        for stmt in scene.statements:
            if isinstance(stmt, Statement) and stmt.cmd == 'image':
                img_file = stmt.args[0]
                if os.path.exists(img_file):
                    # Load and store the image
                    img = tk.PhotoImage(file=img_file)
                    self.images[img_file] = img

        # Instantiate entities defined in the scene
        for stmt in scene.statements:
            if isinstance(stmt, Entity):
                # Create an entity definition and instance
                ed = EntityDef(stmt)
                inst = EntityInst(ed, self.canvas, self.images)
                self.entities.append(inst)
                # Trigger the 'on_start' event for the entity
                inst.on_event('on_start', self)

    def change_scene(self, name):
        # Change to a different scene by destroying the current window
        self.root.destroy()
        # Create a new Game instance and run the specified scene
        Game(list(self.scenes.values())).run(name)

    def run(self, start):
        # Start the game loop with the specified starting scene
        self.setup_scene(start)
        # Bind key press events to entities
        self.root.bind('<KeyPress>', lambda e: [i.on_event(f'on_key_{e.keysym}', self) for i in self.entities])
        # Schedule the game loop to run every 16ms (approximately 60 FPS)
        self.root.after(16, self.loop)
        # Start the Tkinter main loop
        self.root.mainloop()

    def loop(self):
        # Main game loop: Trigger 'on_update' event for all entities
        for inst in list(self.entities):
            inst.on_event('on_update', self)
        # Schedule the next iteration of the loop
        self.root.after(16, self.loop)