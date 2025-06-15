@echo off
:: For Testing only, remove for normal usage

:: remove old logs
:: del /q logs\*

:: python_command <mainclass> <arguements>
::python3 vengine.py script.v --debug --gui

cd src

python3 vengine.py test.vng --debug

rd __pycache__ /s /q

cd ..