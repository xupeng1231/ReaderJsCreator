@echo off

set TIMEOUT=12

set PYTHON_EXE=c:\Python27\python.exe
set WINDBG_EXE=C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\windbg.exe
set ACRORD32_EXE=C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\Acrord32.exe

set BASE_FOLDER=G:\pycharm-projects\ReaderJsCreator

set CONFIRMS_FOLDER=%BASE_FOLDER%\PdfCreator\confirms
set CONFIRMED_FOLDER=%BASE_FOLDER%\PdfCreator\confirmed

set CONFIRM_SCRIPT=%BASE_FOLDER%\cmd\confirm.py

:LOOP
    for %%f in (%CONFIRMS_FOLDER%\*.pdf) do (
        call :confirm %%f
        echo confirm %%~nxf ...
        timeout %TIMEOUT% >nul
        for %%i in (%CONFIRMED_FOLDER%\*.pdf) do (
			if %%~nxi==%%~nxf (
				exit /B 0
			)
        )
        taskkill /F /IM windbg.exe
    )
    goto :LOOP

:confirm :: arg1=testfile_name
    start "" "%WINDBG_EXE%"  -c ".load pykd;!py %CONFIRM_SCRIPT% %~nx1 %CONFIRMS_FOLDER% %CONFIRMED_FOLDER%" -o "%ACRORD32_EXE%" "%CONFIRMS_FOLDER%\%~nx1"
    exit /B 0
