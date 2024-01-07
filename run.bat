@echo off

rem Check if the virtual environment directory exists, if not, create it
if not exist .env (
	echo Creating environment. Please wait...
    python -m venv .env
    call .env\Scripts\activate

    rem Install or upgrade dependencies (modify this line as needed)
    python setup.py install
) else (
    rem Activate the virtual environment
    call .env\Scripts\activate
)

echo Starting. Please wait...
rem Run the Python script
python -m gnarrator
