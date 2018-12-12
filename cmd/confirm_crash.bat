@echo off

set TIMEOUT=12

set PYTHON_EXE=c:\Python27\python.exe
set WINDBG_EXE=C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\windbg.exe
set ACRORD32_EXE=C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\Acrord32.exe

set BASE_FOLDER=G:\pycharm-projects\ReaderJsCreator

set CONFIRM_FOLDER=%BASE_FOLDER%\PdfCreator\confirms
set CRASH_FOLDER=%BASE_FOLDER%\PdfCreator\crashes

set CONFIRM_SCRIPT=%BASE_FOLDER%\cmd\confirm.py

:LOOP
    for %%f in (%CRASH_FOLDER%\*.pdf) do (
        call :confirm %%f
        echo confirm %%~nxf ...
        timeout %TIMEOUT% >nul
        for %%i in (%CONFIRM_FOLDER%\*.pdf) do (
            exit /B 0
        )
        taskkill /F /IM windbg.exe
    )
    goto :LOOP

:confirm :: arg1=testfile_name
    start "" "%WINDBG_EXE%"  -c ".load pykd;!py %CONFIRM_SCRIPT% %~nx1 %BASE_FOLDER%\PdfCreator\" -o "%ACRORD32_EXE%" "%INPUT_FOLDER%\%~nx1"
    exit /B 0



:count_file
    set path=%~1
    set local_count=0
    for %%i in (%path%\*) do set /a local_count+=1
    set %~2=%local_count%
    exit /B 0