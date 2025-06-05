import logging

from custom_token import Token, VariableToken
import param


class Lexer:
    def __init__(self, text):
        logging.debug(f"Contents:\n{text}")
        logging.info("Tokenizing...")
        """
        Initialize the Lexer with the given text and tokenize it.

        Args:
            text (str): The input text to tokenize.
        """
        self.tokens = []  # List to store the generated tokens
        self.vars = {}  # Dictionary to store variable names and their values e.g. {temp: 42}
        indent_stack = [0]  # Stack to track indentation levels

        # Process each line of the input text
        i = 0  # TODO: Remove, used for debugging
        for line in text.replace('\r', '').split('\n'):

            i = i + 1  # TODO: Remove, used for debugging
            logging.debug(f"line{i}: {line}")  # Log the current line being processed

            if not line.strip():  # Skip empty lines
                continue

            # Calculate the current line's indentation level
            indent = len(line) - len(line.lstrip(' '))

            # Handle increased indentation (INDENT token)
            if indent > indent_stack[-1]:
                self.tokens.append(Token('INDENT', ''))
                indent_stack.append(indent)

            # Handle decreased indentation (DEDENT token)
            while indent < indent_stack[-1]:
                self.tokens.append(Token('DEDENT', ''))
                indent_stack.pop()

            # Check for variable definitions
            if line.strip().startswith("var "):
                self._process_variable_definition(line.strip())
                continue

            # Tokenize the line using the regex patterns in `param.TOK_REGEX`
            for m in param.TOK_REGEX.finditer(line):
                typ = m.lastgroup  # Token type
                val = m.group()  # Token value

                if typ == 'SKIP':  # Skip tokens (e.g., whitespace)
                    continue
                if typ == 'STRING':  # Remove quotes from string tokens
                    val = val[1:-1]

                # Append the token to the list
                self.tokens.append(Token(typ, val))

            # Add a NEWLINE token at the end of each line
            self.tokens.append(Token('NEWLINE', ''))

        # Handle any remaining indentation levels at the end of the text
        while len(indent_stack) > 1:
            self.tokens.append(Token('DEDENT', ''))
            indent_stack.pop()

        # Add an EOF (End of File) token to signify the end of the input
        self.tokens.append(Token('EOF', ''))
        self.pos = 0  # Initialize the position pointer for token traversal

        logging.debug("Lexer tokens:")
        i = 0
        for token in self.tokens:
            logging.debug(f"tok{i}: {token.type}, {token.value}")
            i += 1
        logging.info("Tokenizing complete!")

    def _process_variable_definition(self, line):
        """
        Process a variable definition line and generate a VariableToken.

        Args:
            line (str): The line containing the variable definition.
        """
        parts = line.split()
        if len(parts) < 5 or parts[0] != "var" or parts[2][0] != '"' or parts[4][0] != '"':
            raise SyntaxError(f"Invalid variable definition: {line}")

        var_type = parts[1]  # dynamic or static
        var_name = parts[2][1:-1]  # Remove quotes from the variable name
        var_value = parts[4][1:-1]  # Remove quotes from the variable value

        if var_type not in ["dynamic", "static"]:
            raise SyntaxError(f"Invalid variable type: {var_type}")

        # Create a VariableToken and add it to the tokens list
        variable_token = VariableToken(var_name, var_value)
        self.tokens.append(variable_token)

        # Store the variable in the vars dictionary
        self.vars[var_name] = var_value

    def peek(self):
        logging.debug(f"cur tok{self.pos}:{self.tokens[self.pos].type},{self.tokens[self.pos].value}")
        """
        Peek at the current token without advancing the position.

        Returns:
            Token: The current token.
        """
        return self.tokens[self.pos]

    def next(self):
        logging.debug(f"Nxt tok (to tok{self.pos+1}): {self.tokens[self.pos+1].type}, {self.tokens[self.pos+1].value}")
        """
        Get the current token and advance the position.

        Returns:
            Token: The current token.
        """
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, typ, val=None):
        logging.debug(f"Expecting tok typ: {typ}, val: {val}")
        """
        Consume the next token and ensure it matches the expected type and value.

        Args:
            typ (str): The expected token type.
            val (str, optional): The expected token value. Defaults to None.

        Raises:
            SyntaxError: If the next token does not match the expected type or value.

        Returns:
            Token: The consumed token.
        """
        tok = self.next()
        if tok.type != typ or (val is not None and tok.value != val):
            raise SyntaxError(f"Expected {typ} {val}, got {tok}")
        return tok