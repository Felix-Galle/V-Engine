from collections import defaultdict

class EntityDef:
    def __init__(self, ast_entity):
        # Initialize the entity definition with its name, properties, and events
        self.name = ast_entity.name  # Name of the entity
        self.props = {}  # Dictionary to store properties of the entity
        self.events = defaultdict(list)  # Dictionary to store events, defaulting to an empty list

        # Process each statement in the AST entity
        for stmt in ast_entity.statements:
            if stmt.cmd.startswith('on'):  # If the command starts with 'on_', treat it as an event
                self.events[stmt.cmd] = stmt.args  # Add the event and its arguments to the events dictionary
            else:  # Otherwise, treat it as a property
                self.props[stmt.cmd] = stmt.args  # Add the property and its arguments to the properties dictionary