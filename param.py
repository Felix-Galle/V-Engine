import re

debug = False

TOKEN_SPECS = [
    ('NUMBER',   r"\d+(?:\.\d+)?"),
    ('STRING',   r'"[^"\n]*"'),
    ('ID',       r"[A-Za-z_][A-Za-z0-9_]*"),
    ('NEWLINE',  r"\n"),
    ('SKIP',     r"[ \t]+"),
    ('OP',       r"[=+\-*/%(),]"),
    ('COLON',    r":"),
    ('COMMENT',  r"#.*"),
]
TOK_REGEX = re.compile('|'.join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS))