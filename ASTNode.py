

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