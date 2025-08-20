@echo off
echo Activating the virtual environment...
call .\.venv\Scripts\activate.bat

echo.
echo Starting the Command-Line Interface (CLI)...
python main.py

echo.
echo CLI has been closed.
pause
