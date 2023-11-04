@echo off

rem Check if the virtual environment directory exists, if not, create it
echo Creating environment. Please wait...
python -m venv .env
call .env\Scripts\activate

rem Install or upgrade dependencies (modify this line as needed)
python setup.py install
python -m pip uninstall PyQt5 -y
python -m pip uninstall PyQt5-Qt5 -y
python -m pip install PyQt5 --upgrade

rem Check the exit code of the installation process
if %errorlevel% equ 0 (
    echo -----------------------------------------
    echo Installation was successful.
    echo You can now close this window.
    echo -----------------------------------------
) else (
    echo -----------------------------------------
    echo Installation failed. Please check for errors and try again.
    echo -----------------------------------------
)

rem Pause to keep the window open until the user presses a key
pause
