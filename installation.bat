@echo off

rem Check if the virtual environment directory exists, if not, create it
echo Creating environment. Please wait...
python -m venv .env
call .env\Scripts\activate

setlocal enabledelayedexpansion

set "pythonScript=.\gnarrator\utils\pytorch_install_command.py"
python "%pythonScript%"

set "commandFile=.pytorch_cuda_install_command.txt"

if not exist "%commandFile%" (
    echo Error: Command file "%commandFile%" not found.
    exit /b 1
)

set /p command=<"%commandFile%"

if errorlevel 1 (
    echo Error: Command execution failed.
    exit /b 1
)



rem Install or upgrade dependencies (modify this line as needed)
python setup.py install
python -m pip uninstall PyQt5 -y
python -m pip uninstall PyQt5-Qt5 -y
python -m pip install PyQt5 --upgrade
!command! || (
    echo Warning: PyTorch CUDA installation failed. Running CPU installation instead
)

del "%commandFile%"

endlocal

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
