@ECHO OFF
CLS
Rem I suppose to be in Sphinx_LVGL directory!
REM set BATCH_PATH=%~dp0
REM set BATCH_PATH=%BATCH_PATH:~-12,-1%
REM if "%BATCH_PATH%" NEQ "Sphinx_LVGL" (
REM     echo This file is not in the correct dir.
REM 	goto :eof
REM )

Rem cls
echo.
echo.
echo Building Translations
echo.
echo.

ECHO OFF
REM Requires additional manual intervention
REM sphinx-build -v -b epub       -D language=it ./source build/epub/it
sphinx-build -v -b html       -D language=it ./source build/html/it
sphinx-build -v -b latex      -D language=it ./source build/latex/it

Echo.
Echo ****************************************
Echo Create pdf...
PUSHD .\build\latex\it
FOR /R  %%F in (LVGL*.tex) do lualatex --interaction=nonstopmode %%~F
FOR /R  %%F in (LVGL*.tex) do lualatex --interaction=nonstopmode %%~F
POPD
Echo ****************************************
Echo.

goto :eof
