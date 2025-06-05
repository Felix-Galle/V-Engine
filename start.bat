@echo off
:: For Testing only, remove for normal usage

:: remove old logs
:: del /q logs\*

:: python_command <mainclass> <arguements>
::python3 v_engine.py script.v --debug --gui
python3 v_engine.py test.vng --debug

rd __pycache__ /s /q