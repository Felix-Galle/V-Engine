import re

# List of token specifications for a lexer
# Each tuple contains a token name and its corresponding regex pattern
TOKEN_SPECS = [
    ('VAR',      r"var\s+(?P<type>dynamic|static)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<value>[^\n]+)"),  # Matches variable definitions (e.g., var dynamic myVar = "test_value")
    ('LOG',      r'log\s+"[^"\n]*"\s*'),    # Matches log statements (e.g., log "This is a log message")
    ('OUT',      r'out\s+"[^"\n]*"\s*'),    # Matches out statements (e.g., out "This is some out statement")
    ('USING',    r"using"),                 # Matches the 'using' keyword (e.g., using)
    ('COMMENT',  r"(#.*|//.*(?:\n[ \t]*//.*)*)"),    # Matches single-line (#) and multi-line (// ... //) comments
    ('NUMBER',   r"\d+(?:\.\d+)?"),         # Matches integers or floating-point numbers (e.g., 42, 3.14)
    ('STRING',   r'"[^"\n]*"'),             # Matches double-quoted strings (e.g., "hello")
    ('ID',       r"[A-Za-z_][A-Za-z0-9_]*"),# Matches identifiers (e.g., my_var, _temp123)
    ('NEWLINE',  r"\n"),                    # Matches newline characters (e.g., \n)
    ('SKIP',     r"[ \t]+"),                # Matches spaces and tabs (e.g., [space], [tab])
    ('OP',       r"[=+\-*/%(),]"),          # Matches operators and punctuation (e.g., =, +, -, *, /, %, (, ))
    ('COLON',    r":"),                     # Matches a colon character (e.g., :)
    ('LOGIC',    r"(?:&&|\|\||!|\^)"),      # Matches logical operators including XOR (e.g., &&, ||, !, ^)
    ('ARITH',    r"[+\-*/%]"),              # Matches arithmetic operators (e.g., +, -, *, /, %)
    ('COMPARE',  r"(?:==|!=|<=|>=|<|>)"),   # Matches comparison operators (e.g., ==, !=, <=, >=, <, >)
]

# Compile the token specifications into a single regex pattern
# Each token is named using the syntax (?P<name>pattern)
TOK_REGEX = re.compile('|'.join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS))