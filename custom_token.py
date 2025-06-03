class Token:
    # Base class for tokens, representing a generic token with a type and value.
    def __init__(self, typ, val):
        self.type = typ  # The type of the token (e.g., keyword, identifier, etc.).
        self.value = val  # The value of the token (e.g., the actual string or data).

    def __repr__(self):
        # String representation of the Token object for debugging purposes.
        return f"Token({self.type}, {self.value})"
    
# TODO: Find a use for VariableToken, as it is currently not used in the code. Who knows ¯\_(ツ)_/¯

class VariableToken(Token):
    # Subclass of Token, specifically for variable tokens.
    def __init__(self, name, value=None):
        # Initialize with a name and an optional value.
        super().__init__('var', name)  # Call the parent class constructor with type 'var'.
        self.name = name  # The name of the variable.
        self.value = value  # The value assigned to the variable (default is None).

    def __repr__(self):
        # String representation of the VariableToken object for debugging purposes.
        return f"VariableToken({self.name}, {self.value})"