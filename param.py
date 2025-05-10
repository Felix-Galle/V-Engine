import re

# Canvas defaults for solid-colour backgrounds
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

TOKEN_SPECS = [
    ('NUMBER',   r"\d+(?:\.\d+)?"),
    ('STRING',   r'"[^"\n]*"'),
    ('ID',       r"[A-Za-z_][A-Za-z0-9_]*"),
    ('NEWLINE',  r"\n"),
    ('SKIP',     r"[ \t]+"),
    ('OP',       r"[=+\-*/%(),]"),
    ('COLON',    r":"),
]
TOK_REGEX = re.compile('|'.join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS))