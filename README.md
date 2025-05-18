# V Engine

## A robust DSL interpreter for V-language game scripts

To view changelog of features and things, [click here](https://github.com/Felix-Galle/V-Engine/blob/main/CHANGES.md).

### Features

- Indentation-based DSL parsing
- Scenes, entities, events (start, update, key_, collision)
- Actions: spawn, destroy, set, change_scene
- Solid-colour or image backgrounds
- Shape-based entities (rectangle, oval)
- 60fps game loop

### Requirements

- Python 3.11+ (the version this project was coded in)

- os module (installed by default)

- re module (installed by default)

- collections module (installed by default)

### Instructions

To run this program you ought to be using windows (I've not tried any other OS)

1. Open Terminal (Powershell or CMD)
2. type: python3 v_engine.py "scriptname"
e.g. script.v

> Currently v_engine.py ignores any given arguements:
>
>~~~python
>    sys.argv = ['vengine.py', 'script.v', '--debug'] # TODO: Remove this line (for normal usage)
>    """if len(sys.argv) < 2: # TODO: Uncomment this block (For normal usage)
>        print("Usage: vengine.py <script.v>")
>        sys.exit(1)"""
>~~~
>
> - To run the file normally, follow the TODO comment(s)
> ie. Uncomment that block & remove the sys.argv = ...
