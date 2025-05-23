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

- Python 3.11 & 3.12 (the version(s) this project was coded in)

- os module (installed by default)

- re module (installed by default)

- collections module (installed by default)

### Instructions

To run this program you ought to be using windows (I've not tried any other OS)

1. Open Terminal (Powershell or CMD)
2. type: `python3 v_engine.py "<scriptname>"`

#### File arguments

>A copy of these file arguments can be found [here](https://github.com/Felix-Galle/V-Engine/blob/main/SYNTAX.md)

The `vengine.py` script can be executed from the command line with the following options:

- `<script.v>`: The main script file that defines the structure, scenes, entities, and events for the V-Engine. This file must follow the syntax rules outlined in this document.

- `--help`: Displays a help message explaining the usage of the script and its available options.

- `--open`: Opens the specified `<script.v>` file in Notepad for editing.

- `--debug`: Enables debug mode, showing a lot more detail in the logs.
