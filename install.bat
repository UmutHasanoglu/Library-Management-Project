@echo off
echo Creating virtual environment with uv...
uv venv

echo.
echo Activating the virtual environment...
call .\.venv\Scripts\activate.bat

echo.
echo Installing required packages from requirements.txt...
uv pip install -r requirements.txt

echo.
echo Installation complete!
pause
