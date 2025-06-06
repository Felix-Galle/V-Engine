import logging

from ast_node import *

class Parser:
    def __init__(self, lexer):
        logging.debug(f"Using Lexer: {lexer}") # TODO: Remove, there is no use to knowing the lexer memory address
        logging.info(f"Parsing...")
        self.lex = lexer

    def parse(self):
        logging.debug("parse.Parse.parse()")
        using = []
        win = None
        scenes = []

        while self.lex.peek().type != 'EOF':
            match self.lex.peek().type:
                case 'COMMENT':
                    logging.debug("Urgh... comments >:(")
                    self.skip_comment()
                case 'USING':
                    using.append(self.lex.peek().value)
                    logging.info(f"Using {self.lex.peek().value} !")
                    self.lex.next()  # Consume the 'using' token

            if 'gui' in using:
                logging.info("Found gui declaration !")
                match self.lex.peek().value:
                    case 'win':
                        logging.info("Found win settings declaration !")
                        win = (self.parse_win())
                    case 'scene':
                        logging.info("Found scene declaration !")
                        scenes.append(self.parse_scene())
                    case _:
                        raise SyntaxError(f"Unexpected token {self.lex.peek().value}, expected 'win' or 'scene'")
            self.lex.next()  # Consume the current token
        if not 'gui' in using:
            logging.warning("The whole point of this is the GUI engine. Plz use it :(")
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
        self.lex.expect_next('ID', 'win')
        self.lex.expect_next('COLON')
        self.lex.expect_next('NEWLINE')
        # Only expect INDENT if the next token is INDENT, cuz stoopid ￣へ￣
        if self.lex.peek().type == 'INDENT':
            self.lex.expect_next('INDENT')
        stmts = []
        title = None
        dimensions = None
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            match (tok.type, getattr(tok, 'value', None)):
                case ('COMMENT', _):
                    self.skip_comment()
                case ('ID', 'title'):
                    self.lex.expect_next('ID', 'title')
                    title = self.lex.expect_next('STRING').value
                    logging.debug(f"Parsed ttl: {title}")
                case ('ID', 'dimensions'):
                    self.lex.expect_next('ID', 'dimensions')
                    width = self.lex.expect_next('NUMBER').value
                    height = self.lex.expect_next('NUMBER').value
                    dimensions = (int(width), int(height))
                    logging.debug(f"Parsed dim: {dimensions}")
                case (typ, _) if typ != 'NEWLINE':
                    stmts.append(self.parse_statement())
                case _:
                    self.lex.next()  # Consume the NEWLINE token
        self.lex.expect_next('DEDENT')
        logging.debug(f"Parsed win! \n\ttitle: {title} \n\tdim: {dimensions}")
        return Win(title, dimensions, stmts)


    def parse_scene(self):
        logging.debug("parse.Parse.parse_scene()")
        """
        scene "name01":
            # blah
        """

        self.lex.expect_next('ID', 'scene') # wants ID and it's ID being scene
        # NO NEED TO ADVANCE TEH BLOODY TOKEN, the lexer .expect_next() does it already
        name = self.lex.expect_next('STRING').value # Expects the name of the scene
        self.lex.expect_next('COLON')
        stmts = self.parse_block()
        return Scene(name, stmts)


    def parse_variable(self):
        logging.debug("Parsing variable definition")
        tok = self.lex.peek()
        if not hasattr(tok, 'name') or not hasattr(tok, 'value'):
            raise SyntaxError("Invalid variable token")
        name = tok.name
        value = tok.value
        self.lex.next()  # Consume the variable token
        # You might want to store variables somewhere, or return a Statement/AST node
        return Variable(name, value)

    # In parse_block or wherever you handle statements:
    def parse_block(self):
        logging.debug("parse.Parse.parse_block()")
        logging.debug("Parsing block of statements")

        statements = []
        self.lex.expect_next('NEWLINE')
        self.lex.expect_next('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'COMMENT':
                self.skip_comment()
            elif tok.type == 'ID' and tok.value == 'entity':
                statements.append(self.parse_entity())
            elif tok.type == 'VARIABLE':  # Assuming VariableToken.type == 'VARIABLE'
                statements.append(self.parse_variable())
            else:
                statements.append(self.parse_statement())
        self.lex.expect_next('DEDENT')
        return statements

    def parse_entity(self):
        logging.debug("Parsing entity definition")
        self.lex.expect_next('ID', 'entity') # Expects entity + name of entity
        name = self.lex.expect_next('STRING').value # Expacts entity name
        logging.debug(f"Parsed entity name: {name}")
        self.lex.expect_next('COLON')
        stmts = []
        self.lex.expect_next('NEWLINE')
        self.lex.expect_next('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'COMMENT':
                self.skip_comment()
            elif tok.type == 'ID' and tok.value == 'on':
                stmts.append(self.parse_event())
            else:
                stmts.append(self.parse_statement())
        self.lex.expect_next('DEDENT')
        return Entity(name, stmts)

    def parse_event(self):
        logging.debug("Parsing event definition")

        self.lex.expect_next('ID', 'on')
        event_name = self.lex.expect_next('ID').value
        self.lex.expect_next('COLON')
        stmts = []
        self.lex.expect_next('NEWLINE')
        self.lex.expect_next('INDENT')
        while self.lex.peek().type != 'DEDENT':
            tok = self.lex.peek()
            if tok.type == 'COMMENT':
                self.skip_comment()
            else:
                stmt = self.parse_statement()
                # convert to on_<name> statement
                statements = [stmt.cmd] + stmt.args
                stmts.append(statements)
        self.lex.expect_next('DEDENT')
        # flatten statements into one event
        args = [item for sub in stmts for item in sub]
        return Statement('on_' + event_name, args)

    def parse_statement(self):
        logging.debug("Parsing statement")
        cmd = self.lex.expect_next('ID').value
        args = []
        while self.lex.peek().type not in ('NEWLINE', 'EOF'):
            if self.lex.peek().type == 'COMMENT':
                self.skip_comment()
                break
            args.append(self.lex.next().value)
        if self.lex.peek().type == 'NEWLINE':
            self.lex.next()
        return Statement(cmd, args)
    

    