@echo off
cls
rmdir /S /Q tdd-ebook > NUL
rmdir /S /Q TddEbook_Sphinx  > NUL
rmdir /S /Q TddEbook_Italiano & mkdir TddEbook_Italiano  > NUL

Rem ****************************************
Rem Sphinx and sphinx-intl are required
Rem ****************************************
Rem pip install sphinx-intl --upgrade

Rem ****************************************
Rem Note: Node.js is required
Rem ****************************************
Rem npm install -g @mermaid-js/mermaid-cli


IF NOT EXIST ".\tdd-ebook_org\" (
   git clone https://github.com/grzesiek-galezowski/tdd-ebook
) ELSE (
    XCOPY ".\tdd-ebook_org\" ".\tdd-ebook\" /E    > NUL
)

"%LOCALAPPDATA%\Apps\grepWin\grepWin.exe" /regex:no /searchfor:"-# "  /searchpath:"%~dp0tdd-ebook\manuscript" /replacewith:"# " /u:yes /filemask:"*.md"  /executereplace /k:no /closedialog


Rem ****************************************
Rem Sphinx
Rem ****************************************
echo.
echo.
echo Sphinx-build Preparation
echo.
echo.

chcp 1252 > nul

mkdir TddEbook_Sphinx && cd TddEbook_Sphinx
sphinx-quickstart --sep -p "TDD" -a "Grzegorz Gałęzowski" -r "2025" -l "en" --extensions "myst_parser,sphinx_substitution_extensions"
rmdir /s /q .\build
mklink /D "build"      "..\TddEbook_Italiano"
mklink /D "source\manuscript"     "..\..\tdd-ebook\manuscript"

echo myst_enable_extensions = {                                                                                       >> ".\source\conf.py"
echo     "colon_fence",                                                                                               >> ".\source\conf.py"
echo     "substitution",                                                                                              >> ".\source\conf.py"
echo }                                                                                                                >> ".\source\conf.py"
echo.                                                                                                                 >> ".\source\conf.py"
echo myst_substitutions = {                                                                                           >> ".\source\conf.py"
echo #    "keyNote":         ">![info](../img/css-box-icon-note.png)",                                                >> ".\source\conf.py"
echo # >![info](./images/info.svg) See                                                                                >> ".\source\conf.py"
echo #Mi piace leggere                                                                                                >> ".\source\conf.py"
echo #Questa introduzione è scritta                                                                                   >> ".\source\conf.py"
echo     "keyNote":         "```{image} ../img/css-box-icon-note.png\n:alt: Note\n:align: left\n```",                 >> ".\source\conf.py"
echo     "keyTip":          "```{image} ../img/css-box-icon-tip.png\n:alt: Tip\n:align: left\n```",                   >> ".\source\conf.py"
echo     "keyExample":      "```{image} ../img/css-box-icon-example.png\n:alt: Example\n:align: left\n```",           >> ".\source\conf.py"
echo     "keyImportant":    "```{image} ../img/alarm-exclamation-regular-48.png\n:alt: Important\n:align: left\n```", >> ".\source\conf.py"
echo     "keyWarning":      "```{image} ../img/css-box-icon-warning.png\n:alt: Warning\n:align: left\n```",           >> ".\source\conf.py"
echo     "keyLock":         "```{image} ../img/key_icon_little.png\n:alt: Lock\n:align: left\n:width: 30px\n```",     >> ".\source\conf.py"
echo     "keyToDo":         "```{image} ../img/ToDo.png\n:alt: ToDo\n:align: left\n:width: 30px\n```",                >> ".\source\conf.py"
echo #   "keyExclamation":  "![info](../img/Exclamation.png)",                                                        >> ".\source\conf.py"
echo    "keyExclamation":  "```{image} ../img/Exclamation.png\n:alt: Exclamation\n:align: left\n:width: 30px\n```",   >> ".\source\conf.py"
echo     "keyInfo":         "```{image} ../img/Info.png\n:alt: Info\n:align: left\n:width: 30px\n```",                >> ".\source\conf.py"
echo }                   >> ".\source\conf.py"


echo locale_dirs = ['locale/']                                >> ".\source\conf.py"
echo suppress_warnings = ["myst.header","myst.xref_missing","ref.footnote","epub.unknown_project_files","misc.highlighting_failure"]  >> ".\source\conf.py"
echo myst_heading_anchors = 7                                 >> ".\source\conf.py"
echo smartquotes = False                                      >> ".\source\conf.py"
echo release = ""                                             >> ".\source\conf.py"
echo release = '2025'                                         >> ".\source\conf.py"
echo version = release                                        >> ".\source\conf.py"
echo latex_documents = [('index', 'tdd_Italiano.tex', 'TDD', 'Grzegorz Gałęzowski \\\\\large(Traduzione: \sphinxhref{https://github.com/BravoBaldo}{Baldassarre Cesarano})', 'manual', 1)]             >> ".\source\conf.py"
echo.                                                                                      >> ".\source\conf.py"
echo _PREAMBLE = r^"^"^"                                                                   >> ".\source\conf.py"
echo \usepackage[]{geometry}                                                               >> ".\source\conf.py"
echo \geometry{bindingoffset=2cm, left=1cm, right=1cm}                                     >> ".\source\conf.py"
echo ^"^"^"                                                                                >> ".\source\conf.py"
echo latex_elements = {                                                                    >> ".\source\conf.py"
echo     'preamble': _PREAMBLE,                                                            >> ".\source\conf.py"
echo     'papersize': 'a4paper', 'pointsize': '10pt', 'release': release + ' (Ita)',}      >> ".\source\conf.py"
#echo suppress_warnings.append('epub.unknown_project_files','misc.highlighting_failure')    >> ".\source\conf.py"

REM ref.footnote
echo # Title                      >> ".\source\manuscript\cover.md"


del /S /Q  .\source\index.rst
copy ..\TddEbook_OmegaT\Docs\index_org.rst .\source\index.rst
xcopy ..\TddEbook_OmegaT\Docs\img\ .\source\img\ /E /I /Y

Rem -------------------------------------------
rmdir /s /q .\source\locale\
Call make clean
Call make gettext
sphinx-intl update -p build/gettext -l en -l it
ren ".\source\locale\it"        "it_it"

rmdir      ..\TddEbook_OmegaT\source\it
del /S /Q  ..\TddEbook_OmegaT\source\it
mklink /D "..\TddEbook_OmegaT\source\it"             "..\..\TddEbook_Sphinx\source\locale\it_it"

# Translate 
rmdir      .\source\locale\it
del /S /Q  .\source\locale\it
mklink /D ".\source\locale\it"                    "..\..\..\TddEbook_OmegaT\target\it"     
Rem -------------------------------------------

goto :EOF


:ErrNoCloning
ECHO "Error Wrong Cloning"
exit /b 1
goto :EOF

:ErrNoIntermediate
ECHO "Error. No Intermediate directory created"
exit /b 1
goto :EOF


:EOF 