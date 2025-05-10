

class Token:
    def __init__(self, typ, val):
        self.type = typ
        self.value = val

    def __repr__(self):
        return f"Token({self.type}, {self.value})"