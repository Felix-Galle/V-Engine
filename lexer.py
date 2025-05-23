import logging

from custom_token import Token
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
        indent_stack = [0]  # Stack to track indentation levels

        # Process each line of the input text
        for line in text.replace('\r', '').split('\n'):
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
            i+= 1
        logging.info("Tokenizing complete !")

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