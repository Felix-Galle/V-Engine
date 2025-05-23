import logging

from ast_node import Win, Scene, Entity, Statement

class Parser:
    def __init__(self, lexer):
        logging.debug(f"Using Lexer: {lexer}")
        logging.info(f"Parsing...")
        self.lex = lexer

    def parse(self):
        logging.debug("parse.Parse.parse()")
        win = None
        scenes = []
        
        while self.lex.peek().type != 'EOF':
            if self.lex.peek().type == 'COMMENT':
                logging.debug("Urgh... comments >:(")
                self.skip_comment()
            else:
                if self.lex.peek().value == 'win':
                    logging.info("Found win settings declaration !")
                    win = (self.parse_win())
                elif self.lex.peek().value == 'scene':
                    logging.info("Found scne declaration !")
                    scenes.append(self.parse_scene())
                else:
                    raise SyntaxError(f"Unexpected token {self.lex.peek().value}, expected 'win' or 'scene'")
        return win, scenes

    def skip_comment(self):
        logging.debug("parse.Parse.skip_comment()")
        while self.lex.peek().type != 'NEWLINE' and self.lex.peek().type != 'EOF':
            self.lex.next()
        if self.lex.peek().type == 'NEWLINE':
            self.lex.next()

    def parse_win(self):
        logging.debug("parse.Parse.parse_win()")
        """
        win:
            title "My Game"
            dimensions 800 600
        """
        self.lex.expect('ID', 'win')
        self.lex.expect('COLON')
        stmts = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        title = None
        dimensions = None
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'COMMENT': # Skip comments
                self.skip_comment()
            elif tok.type == 'ID' and tok.value == 'title':
                self.lex.expect('ID', 'title')
                title = self.lex.expect('STRING').value
                logging.debug(f"Parsed ttl: {title}")
            elif tok.type == 'ID' and tok.value == 'dimensions':
                self.lex.expect('ID', 'dimensions')
                width = self.lex.expect('NUMBER').value
                height = self.lex.expect('NUMBER').value
                dimensions = (int(width), int(height))
                logging.debug(f"Parsed dim: {dimensions}")
            elif tok.type != 'NEWLINE':
                stmts.append(self.parse_statement())
            else:
                self.lex.next()  # Consume the NEWLINE token
        self.lex.expect('DEDENT')
        logging.debug(f"Parsed win! \n\tttl: {title} \n\tdim: {dimensions}")
        return Win(title, dimensions, stmts)


    def parse_scene(self):
        logging.debug("parse.Parse.parse_scene()")
        """
        scene "name01":
            # blah
        """

        self.lex.expect('ID', 'scene') # wants ID and it's ID being scene
        # NO NEED TO ADVANCE TEH BLOODY TOKEN, the lexer .expect() does it already
        name = self.lex.expect('STRING').value # Expects the name of the scene
        self.lex.expect('COLON')
        stmts = self.parse_block()
        return Scene(name, stmts)

    def parse_block(self):
        logging.debug("parse.Parse.parse_block()")
        logging.debug("Parsing blk of statements")

        statements = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'COMMENT':
                self.skip_comment()
            elif tok.type == 'ID' and tok.value == 'entity':
                statements.append(self.parse_entity())
            else:
                statements.append(self.parse_statement())
        self.lex.expect('DEDENT')
        return statements

    def parse_entity(self):
        logging.debug("Parsing entity definition")
        self.lex.expect('ID', 'entity') # Expects entity + name of entity
        name = self.lex.expect('STRING').value # Expacts entity name
        logging.debug(f"Parsed entity name: {name}")
        self.lex.expect('COLON')
        stmts = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'COMMENT':
                self.skip_comment()
            elif tok.type == 'ID' and tok.value == 'on':
                stmts.append(self.parse_event())
            else:
                stmts.append(self.parse_statement())
        self.lex.expect('DEDENT')
        return Entity(name, stmts)

    def parse_event(self):
        logging.debug("Parsing event definition")

        self.lex.expect('ID', 'on')
        event_name = self.lex.expect('ID').value
        self.lex.expect('COLON')
        stmts = []
        self.lex.expect('NEWLINE')
        self.lex.expect('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'COMMENT':
                self.skip_comment()
            else:
                stmt = self.parse_statement()
                # convert to on_<name> statement
                statements = [stmt.cmd] + stmt.args
                stmts.append(statements)
        self.lex.expect('DEDENT')
        # flatten statements into one event
        args = [item for sub in stmts for item in sub]
        return Statement('on_' + event_name, args)

    def parse_statement(self):
        logging.debug("Parsing statement")
        cmd = self.lex.expect('ID').value
        args = []
        while self.lex.peek().type not in ('NEWLINE', 'EOF'):
            if self.lex.peek().type == 'COMMENT':
                self.skip_comment()
                break
            args.append(self.lex.next().value)
        if self.lex.peek().type == 'NEWLINE':
            self.lex.next()
        return Statement(cmd, args)