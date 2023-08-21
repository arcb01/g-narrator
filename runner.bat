@echo off

rem Set the name of the virtual environment
set VENV_NAME=.env

rem Set the path to your Python executable (change this if necessary)
set PYTHON_EXECUTABLE=python

rem Create the virtual environment
%PYTHON_EXECUTABLE% -m venv %VENV_NAME%
%PYTHON_EXECUTABLE% -m pip config set global.disable-pip-version-check true

rem Activate the virtual environment
call %VENV_NAME%\Scripts\activate

rem Install dependencies from the requirements file
pip install -r requirements.txt | find /V "already satisfied"

rem Run your Python script
python .\modules\run.py