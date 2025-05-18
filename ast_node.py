

class ASTNode:
    pass

class Win(ASTNode):
    def __init__(self, title, dimensions, statements):
        self.title = title
        self.dimensions = dimensions
        self.statements = statements

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