
from ASTNode import Scene, Entity, Statement

class Parser:
    def __init__(self, lexer):
        self.lex = lexer

    def parse(self):
        scenes = []
        while self.lex.peek().type != 'EOF':
            scenes.append(self.parse_scene())
        return scenes

    def parse_scene(self):
        self.lex.expect('ID', 'scene')
        name = self.lex.expect('ID').value
        self.lex.expect('COLON')
        stmts = self.parse_block()
        return Scene(name, stmts)

    def parse_block(self):
        statements = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'ID' and tok.value == 'entity':
                statements.append(self.parse_entity())
            else:
                statements.append(self.parse_statement())
        self.lex.expect('DEDENT')
        return statements

    def parse_entity(self):
        self.lex.expect('ID', 'entity')
        name = self.lex.expect('ID').value
        self.lex.expect('COLON')
        stmts = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'ID' and tok.value == 'on':
                stmts.append(self.parse_event())
            else:
                stmts.append(self.parse_statement())
        self.lex.expect('DEDENT')
        return Entity(name, stmts)

    def parse_event(self):
        self.lex.expect('ID', 'on')
        event_name = self.lex.expect('ID').value
        self.lex.expect('COLON')
        stmts = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        while self.lex.peek().type != 'DEDENT':
            stmt = self.parse_statement()
            # convert to on_<name> statement
            statements = [stmt.cmd] + stmt.args
            stmts.append(statements)
        self.lex.expect('DEDENT')
        # flatten statements into one event
        args = [item for sub in stmts for item in sub]
        return Statement('on_' + event_name, args)

    def parse_statement(self):
        cmd = self.lex.expect('ID').value
        args = []
        while self.lex.peek().type not in ('NEWLINE', 'EOF'):
            args.append(self.lex.next().value)
        if self.lex.peek().type == 'NEWLINE':
            self.lex.next()
        return Statement(cmd, args)