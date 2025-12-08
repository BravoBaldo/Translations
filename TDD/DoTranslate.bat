@ECHO OFF
CLS
echo.
echo.
echo Building Translations
echo.
echo.

ECHO OFF
REM Requires additional manual intervention
sphinx-build -v -b epub       -D language=it ./source build/epub/it
sphinx-build -v -b html       -D language=it ./source build/html/it
sphinx-build -v -b latex      -D language=it ./source build/latex/it

Echo.
Echo ****************************************
Echo Create pdf...
PUSHD .\build\latex\it
FOR /R  %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
FOR /R  %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
POPD
Echo ****************************************
Echo.

goto :eof
