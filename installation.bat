@echo off

rem Set the name of the virtual environment
set VENV_NAME=.env

rem Check if the virtual environment already exists
if exist %VENV_NAME% (
    echo Starting...
    goto :run_script
)

rem Set the path to your Python executable (change this if necessary)
set PYTHON_EXECUTABLE=python

rem Create the virtual environment (suppress output)
%PYTHON_EXECUTABLE% -m venv %VENV_NAME% > NUL
%PYTHON_EXECUTABLE% -m pip config set global.disable-pip-version-check true

rem Activate the virtual environment
call %VENV_NAME%\Scripts\activate.ps1

rem Install dependencies from the requirements file (suppress output)
python setup.py install > NUL

:run_script
rem Run your Python script
python .\garrator\run.py
