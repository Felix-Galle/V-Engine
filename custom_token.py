

class Token:
    def __init__(self, typ, val):
        self.type = typ
        self.value = val

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class VariableToken(Token):
    def __init__(self, name, value=None):
        super().__init__('var', name)
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VariableToken({self.name}, {self.value})"