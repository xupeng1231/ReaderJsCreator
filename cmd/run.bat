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

:LOOP
    call :generate 10
    for %%f in (%INPUT_FOLDER%\*.pdf) do (
        call :test %%f
        echo test %%~nxf ...
        timeout %TIMEOUT% >nul
        taskkill /F /IM windbg.exe
    )
    timeout 1 >nul
    for %%f in (%INPUT_FOLDER%\*.pdf) do (
        del %%f
        echo del %%~nxf ...
    )
    goto :LOOP

:generate
    %PYTHON_EXE% "%GENERATE_PY%" "%SAMPLE_FOLDER%" "%INPUT_FOLDER%" %~1
    exit /B 0

:test :: arg1=testfile_name
    start "" "%WINDBG_EXE%"  -c ".load pykd;!py %WINDBG_SCRIPT% %~nx1 %BASE_FOLDER%\PdfCreator\" -o "%ACRORD32_EXE%" "%INPUT_FOLDER%\%~nx1"
    exit /B 0



:count_file
    set path=%~1
    set local_count=0
    for %%i in (%path%\*) do set /a local_count+=1
    set %~2=%local_count%
    exit /B 0