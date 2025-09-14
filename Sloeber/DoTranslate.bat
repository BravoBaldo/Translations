@ECHO OFF
CLS

Rem cls
echo.
echo.
echo Building Translations
echo.
echo.

ECHO OFF
sphinx-build -v -b html       -D language=it ./source build/html/it
sphinx-build -v -b latex      -D language=it ./source build/latex/it
sphinx-build -v -b epub       -D language=it ./source build/epub/it

Echo.
Echo ****************************************
Echo Create pdf...
PUSHD .\build\latex\it
FOR /R  %%F in (Sloeber*.tex) do lualatex --interaction=nonstopmode %%~F
FOR /R  %%F in (Sloeber*.tex) do lualatex --interaction=nonstopmode %%~F
POPD
Echo ****************************************
Echo.

if 1==0 (
ECHO To Run before publish on git
deactivate
cd ..
rmdir /S /Q arduino-eclipse-plugin
rmdir /S /Q Sphinx_Sloeber
rmdir /S /Q .\Sloeber_Italiano\gettext
move .\Sloeber_Italiano\latex\it\Sloeber_*.pdf .\Sloeber_Italiano\latex\
rmdir /S /Q .\Sloeber_Italiano\latex\it

move .\Sloeber_Italiano\epub\it\Sloeber_*.epub .\Sloeber_Italiano\epub\
rmdir /S /Q .\Sloeber_Italiano\epub\it

del /S /Q   .\Sloeber_TradIta\omegat\*.bak                 2>nul
del /S /Q   .\Sloeber_TradIta\*.bak                        2>nul
del /S /Q   .\Sloeber_TradIta\target\it\LC_MESSAGES\*.mo   2>nul
)

goto :eof
