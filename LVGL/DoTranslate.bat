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
sphinx-build -v -b html       -D language=it ./source build/html/it
sphinx-build -v -b latex      -D language=it ./source build/latex/it
PUSHD .\build\latex\it
FOR /R  %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
FOR /R  %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
POPD

if 1==0 (
ECHO To Run before publish on git
cd ..
rmdir /S /Q lvgl
rmdir /S /Q Sphinx_LVGL
rmdir /S /Q .\LVGL_Italiano\gettext
move .\LVGL_Italiano\latex\it\LVGL_*.pdf LVGL_Italiano\latex\
rmdir /S /Q .\LVGL_Italiano\latex\it
)

goto :eof
