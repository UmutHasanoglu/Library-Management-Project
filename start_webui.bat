@echo off
echo Activating the virtual environment...
call .\.venv\Scripts\activate.bat

echo.
echo Opening the Web UI in your default browser...
start index.html

echo.
echo Starting the FastAPI server...
echo (You can close this window to stop the server)
uvicorn api:app --reload
