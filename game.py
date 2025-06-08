import os
import tkinter as tk
import logging

import param
from entity_def import EntityDef
from entity_inst import EntityInst
from ast_node import Win, Scene, Entity, Statement

class Game:
    def __init__(self, instructions):
        # Initialize the Game object with instructions
        logging.debug("Using Game constructor")
        logging.debug(f"Creating Game with instructions: {instructions}")
        self.instructions = instructions
        self.win = None  # Window configuration
        self.scenes = {}  # Dictionary to store scenes
        self.root = None  # Tkinter root window
        self.canvas = None  # Tkinter canvas
        self.images = {}  # Cache for loaded images
        self.entities = []  # List of entity instances

        # goto run(self) ln 98 (currently)

    def process_instructions(self):
        # Process the list of instructions to set up the game
        for instruction in self.instructions:
            if isinstance(instruction, Win):
                # If the instruction is a window definition, store it
                self.win = instruction
                logging.debug(f"Window defined: {self.win}")
            elif isinstance(instruction, Scene):
                # If the instruction is a scene definition, add it to the scenes dictionary
                self.scenes[instruction.name] = instruction
                logging.debug(f"Scene added: {instruction.name}")

    def setup_scene(self, name):
        # Set up the specified scene
        if not self.win or name not in self.scenes:
            # If the window or scene is not defined, log a warning and skip setup
            logging.warning("Window or scene not defined. Skipping setup.")
            return

        # Create the Tkinter root window
        self.root = tk.Tk()
        self.root.title(self.win.title)
        width, height = self.win.dimensions
        self.root.geometry(f"{width}x{height}")

        # Get the scene object
        scene = self.scenes[name]

        # Process statements to set up the background
        for stmt in scene.statements:
            if isinstance(stmt, Statement) and stmt.cmd == 'background_color':
                # Set background color
                color = stmt.args[0]
                self.canvas = tk.Canvas(self.root, width=width, height=height, bg=color)
                self.canvas.pack()
                break
            elif isinstance(stmt, Statement) and stmt.cmd == 'background':
                # Set background image or color
                path = stmt.args[0]
                if os.path.exists(path):
                    img = tk.PhotoImage(file=path)
                    self.images[path] = img
                    self.canvas = tk.Canvas(self.root, width=img.width(), height=img.height())
                    self.canvas.pack()
                    self.canvas.create_image(0, 0, image=img, anchor='nw')
                else:
                    self.canvas = tk.Canvas(self.root, width=width, height=height, bg=path)
                    self.canvas.pack()
                break

        # Load images specified in the scene statements
        for stmt in scene.statements:
            if isinstance(stmt, Statement) and stmt.cmd == 'image':
                img_file = stmt.args[0]
                if os.path.exists(img_file):
                    img = tk.PhotoImage(file=img_file)
                    self.images[img_file] = img

        # Create entity instances for the scene
        for stmt in scene.statements:
            if isinstance(stmt, Entity):
                ed = EntityDef(stmt)  # Create entity definition
                inst = EntityInst(ed, self.canvas, self.images)  # Create entity instance
                self.entities.append(inst)
                inst.on_event('on_start', self)  # Trigger 'on_start' event for the entity

    def change_scene(self, name):
        # Change the current scene to a new one
        if self.root:
            self.root.destroy()  # Destroy the current Tkinter root window
        if name in self.scenes:
            self.run(name)  # Run the new scene

    def run(self, start):
        # Start the game with the specified scene
        self.process_instructions()  # Process instructions to set up the game
        if start in self.scenes:
            self.setup_scene(start)  # Set up the starting scene
            # Bind key press events to entities
            self.root.bind('<KeyPress>', lambda e: [i.on_event(f'on_key_{e.keysym}', self) for i in self.entities])
            self.root.after(16, self.loop)  # Start the game loop
            self.root.mainloop()  # Run the Tkinter main loop
        else:
            logging.warning(f"Starting scene '{start}' not found.")

    def loop(self):
        # Game loop to update entities
        for inst in list(self.entities):
            inst.on_event('on_update', self)  # Trigger 'on_update' event for each entity
        self.root.after(16, self.loop)  # Schedule the next iteration of the loop
