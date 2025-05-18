# Base class for all Abstract Syntax Tree (AST) nodes
class ASTNode:
    pass

# Represents a window in the AST
class Win(ASTNode):
    def __init__(self, title, dimensions, statements):
        # Title of the window
        self.title = title
        # Dimensions of the window (e.g., width and height)
        self.dimensions = dimensions
        # List of statements associated with the window
        self.statements = statements

# Represents a scene in the AST
class Scene(ASTNode):
    def __init__(self, name, statements):
        # Name of the scene
        self.name = name
        # List of statements associated with the scene
        self.statements = statements

# Represents an entity in the AST
class Entity(ASTNode):
    def __init__(self, name, pos_x, pos_y, statements):
        # Name of the entity
        self.name = name
        # Position of the entity (x, y)
        self.pos = (pos_x, pos_y)
        # List of statements associated with the entity
        self.statements = statements

# Represents a generic statement in the AST
class Statement(ASTNode):
    def __init__(self, cmd, args):
        # Command or operation of the statement
        self.cmd = cmd
        # Arguments for the command
        self.args = args