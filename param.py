import re

# List of token specifications for a lexer
# Each tuple contains a token name and its corresponding regex pattern
TOKEN_SPECS = [
    ('VAR',      r"var"),                # Matches the 'var' keyword
    ('NUMBER',   r"\d+(?:\.\d+)?"),      # Matches integers or floating-point numbers
    ('STRING',   r'"[^"\n]*"'),          # Matches double-quoted strings
    ('ID',       r"[A-Za-z_][A-Za-z0-9_]*"),  # Matches identifiers (letters, digits, and underscores, starting with a letter or underscore)
    ('NEWLINE',  r"\n"),                 # Matches newline characters
    ('SKIP',     r"[ \t]+"),             # Matches spaces and tabs (to be skipped)
    ('OP',       r"[=+\-*/%(),]"),       # Matches operators and punctuation
    ('COLON',    r":"),                  # Matches a colon character
    ('COMMENT',  r"//.*"),               # Matches comments starting with //
]

# Compile the token specifications into a single regex pattern
# Each token is named using the syntax (?P<name>pattern)
TOK_REGEX = re.compile('|'.join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS))