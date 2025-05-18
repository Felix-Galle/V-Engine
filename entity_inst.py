import logging

class EntityInst:
    def __init__(self, edef, canvas, images):
        # Log the creation of an EntityInst object with its parameters
        logging.info(f"Creating EntityInst with edef: {edef}, canvas: {canvas}, images: {images}")

        # Store the entity definition and canvas
        self.defn = edef
        self.canvas = canvas

        # Extract position from entity properties, defaulting to (0, 0) if not provided
        pos = edef.props.get('position', ['0', '0'])
        self.x = float(pos[0])
        self.y = float(pos[1])

        # Initialize the canvas object ID to None
        self.id = None

        # Check if the entity has a 'shape' property
        if 'shape' in edef.props:
            parts = edef.props['shape']

            # Validate that the shape property has exactly 3 arguments
            if len(parts) != 3:
                raise ValueError(f"Expected 3 arguments for shape, got {len(parts)}: {parts}")

            # Extract shape type, dimensions, and color
            typ, dims, color = parts

            # Parse dimensions (width and height)
            try:
                w, h = map(int, dims.split(','))
            except ValueError:
                raise ValueError(f"Invalid dimensions '{dims}' for shape: must be 'width,height'")

            # Create the appropriate shape on the canvas
            if typ == 'rectangle':
                self.id = canvas.create_rectangle(self.x, self.y, self.x + w, self.y + h, fill=color)
            elif typ == 'oval':
                self.id = canvas.create_oval(self.x, self.y, self.x + w, self.y + h, fill=color)
            elif typ == 'triangle':
                self.id = canvas.create_polygon(self.x, self.y, self.x + w, self.y + h, fill=color)

        # Check if the entity has an 'image' property
        elif 'image' in edef.props:
            imgf = edef.props['image'][0]

            # If the image file exists in the provided images dictionary, create an image on the canvas
            if imgf in images:
                self.id = canvas.create_image(self.x, self.y, image=images[imgf], anchor='nw')

    def on_event(self, ev, game):
        # Handle events associated with the entity
        if ev in self.defn.events:
            args = self.defn.events[ev]
            cmd = args[0]

            # If the command is 'change_scene', invoke the game's scene-changing method
            if cmd == 'change_scene':
                game.change_scene(args[1])