from Token import Token
import param


class Lexer:
    def __init__(self, text):
        self.tokens = []
        indent_stack = [0]
        for line in text.replace('\r', '').split('\n'):
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip(' '))
            if indent > indent_stack[-1]:
                self.tokens.append(Token('INDENT', ''))
                indent_stack.append(indent)
            while indent < indent_stack[-1]:
                self.tokens.append(Token('DEDENT', ''))
                indent_stack.pop()
            for m in param.TOK_REGEX.finditer(line):
                typ = m.lastgroup
                val = m.group()
                if typ == 'SKIP':
                    continue
                if typ == 'STRING':
                    val = val[1:-1]
                self.tokens.append(Token(typ, val))
            self.tokens.append(Token('NEWLINE', ''))
        while len(indent_stack) > 1:
            self.tokens.append(Token('DEDENT', ''))
            indent_stack.pop()
        self.tokens.append(Token('EOF', ''))
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, typ, val=None):
        tok = self.next()
        if tok.type != typ or (val is not None and tok.value != val):
            raise SyntaxError(f"Expected {typ} {val}, got {tok}")
        return tok