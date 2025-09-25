@echo off
echo PDF to Markdown Converter
echo ========================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

REM Run the conversion script
echo.
echo Starting PDF to Markdown conversion...
python pdf_to_markdown_converter.py

echo.
echo Conversion completed! Check the markdown_output folder for results.
pause
