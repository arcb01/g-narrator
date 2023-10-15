@echo off

rem Check if the virtual environment directory exists, if not, create it
echo Creating environment. Please wait...
python -m venv .env
call .env\Scripts\activate

rem Install or upgrade dependencies (modify this line as needed)
python setup.py install