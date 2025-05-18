@echo off
:: For Testing only, remove for normal usage

:: remove previous build
rd __pycache__ /s /q

:: python_command <mainclass> <arguements>
python3 v_engine.py script.v