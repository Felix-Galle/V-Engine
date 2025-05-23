# Syntax Dictionary for `script.v`

---

## Command Line Arguments

The `vengine.py` script can be executed from the command line with the following options:

- `<script.v>`: The main script file that defines the structure, scenes, entities, and events for the V-Engine. This file must follow the syntax rules outlined in this document.

- `--help`: Displays a help message explaining the usage of the script and its available options.

- `--open`: Opens the specified `<script.v>` file in Notepad for editing.

- `--debug`: Enables debug mode, showing a lot more detail inthe logs:

---

### Notes

>Variable names of your choosing are shown as `<name>`, however if a stringtype is mandated they are shown as `"<name>"`.
Integers/floats aren't effected e.g. `<number>`.

---

## Script Syntax

## Window Structure

- `win:`: Defines the window properties.
**Must** have a colon `:` before the nextline
Items **must** be indented!

- `title "<title>"` - Sets the title of the window.
Title **must** be surrounded by quotes `""`
Example: `title "script.v"`

- `dimensions <width> <height>` - Sets the width and height of the window.
Dimensions **must** be full numbers (cuz obvious; u cannot have half a pixel of size)
Example: `dimensions 400 300`

```python
win:
    title "<title>"
    dimensions 400 300
```

## Scene Structure

- `scene "<name>"`: Defines a scene in the script.

- `background_color`: Sets the background color of the scene.
Example: `background_color blue`

```python
scene "<name>":
    background_color <color>
```

## Entity

- `entity`: Defines an entity within a scene.
- `position` - Sets the x, y position of the entity.
Example: `position 0 0`

- `shape` - Defines the shape, dimensions, and color of the entity.
Example: `shape rectangle "50,100" green`

## Event Handlers

- `on key_"key"`: Defines an action when a specific key is pressed.
Example: `on key_space:`

- `change_scene` - Changes the current scene.
Example: `change_scene end`

- `on start`: Defines an action that occurs when the scene or entity starts.
Example: `on start:`

## Comments

- `#`: Denotes a comment.
Example: `# This is a comment`

---

## Potential Future Features

- **Animations**:

- `animate`: Adds animations to entities.
Example: `animate "move" duration 2s`

- **Sound Effects**:

- `play_sound`: Plays a sound file.
Example: `play_sound "click.wav"`

- **Collision Detection**:

- `on collision`: Defines behavior when two entities collide.
Example: `on collision entity1 entity2:`

- **Loops**:

- `loop`: Repeats a block of code.
Example: `loop 5 times:`

- **Timers**:

- `set_timer`: Executes code after a delay.
Example: `set_timer 3s:`

- **Dynamic Text**:

- `set_text`: Updates text dynamically.
Example: `set_text "Score: 100"`
