@echo off

set TIMEOUT=12

set PYTHON_EXE=c:\Python27\python.exe
set WINDBG_EXE=C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\windbg.exe
set ACRORD32_EXE=C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\Acrord32.exe

set BASE_FOLDER=G:\pycharm-projects\ReaderJsCreator

set INPUT_FOLDER=%BASE_FOLDER%\PdfCreator\inputs
set SAMPLE_FOLDER=%BASE_FOLDER%\PdfCreator\samples

set WINDBG_SCRIPT=%BASE_FOLDER%\cmd\windbg.py
set GENERATE_PY=%BASE_FOLDER%\PdfCreator\generate_pdf.py

start "" "%WINDBG_EXE%"  -c ".load pykd;g;g;" -o "%ACRORD32_EXE%"
exit /B 0