@echo off
cls
set RepoName=FastLED
set RepoAddr=https://github.com/FastLED/FastLED.git
Rem Download Repository
Rem Patch Repository
Rem Init sphinx-quickstart
Rem Patch Sphinx

rmdir /S /Q %RepoName% > NUL
rmdir /S /Q %RepoName%_Sphinx  > NUL

Rem Translation
rmdir /S /Q %RepoName%_Italiano & mkdir %RepoName%_Italiano  > NUL

IF NOT EXIST ".\%RepoName%_org\" (
	git clone %RepoAddr%
) ELSE (
    XCOPY ".\%RepoName%_org\" ".\%RepoName%\" /E    > NUL
)


pip install --upgrade myst-parser
REM pip install Linkify
REM pip install linkify-it-py
REM https://myst-parser.readthedocs.io/en/latest/syntax/optional.html

mkdir %RepoName%_Sphinx && cd %RepoName%_Sphinx
sphinx-quickstart --sep -p "%RepoName%" -a "%RepoName% Community" -r "2025" -l "en" --extensions "myst_parser"
rmdir /s /Q build
mklink /D "build"      "..\%RepoName%_Italiano"

copy /Y ..\FastLED_OmegaT\docs\index.rst .\source\index.rst

IF EXIST ".\NotExists\" (
	mklink /D ".\source\FastLED"                     "..\..\FastLED"
	REM All ".\source\FastLED"....: 23291 Segments, 20361 remaining
	REM   Too much, so I'll proceed step by step

	REM ".\source\FastLED\cookbook"...: 2568 Segments, 0 remaining
	REM + examples ...................: 3995 Segments, 1356 remaining
	REM + src ........................:
)

mkdir ".\source\FastLED"
mklink /D ".\source\FastLED\cookbook"                  "..\..\..\FastLED\cookbook"
mklink /D ".\source\FastLED\examples"                  "..\..\..\FastLED\examples"
mklink /D ".\source\.plans"                            "..\..\FastLED\.plans"
REM mklink /D ".\source\src"                       "..\..\FastLED\src"
REM mklink /D ".\source\tests"                     "..\..\FastLED\tests"

REM mklink /D ".\source\cookbook"                  "..\..\%RepoName%\cookbook"
REM mklink /D ".\source\examples"                  "..\..\%RepoName%\examples"
REM mklink /D ".\source\src"                       "..\..\%RepoName%\src"
REM mklink /D ".\source\tests"                     "..\..\%RepoName%\tests"
REM mklink /D ".\source\tests"                     "..\..\%RepoName%\tests"

 
 
 
echo version = '2026'                   >> "source\conf.py"
echo myst_heading_anchors = 5           >> "source\conf.py"

echo.                                   >> "source\conf.py"
echo myst_enable_extensions = [         >> "source\conf.py"
echo     "amsmath",                     >> "source\conf.py"
echo     "attrs_inline",                >> "source\conf.py"
echo     "colon_fence",                 >> "source\conf.py"
echo     "deflist",                     >> "source\conf.py"
echo     "dollarmath",                  >> "source\conf.py"
echo     "fieldlist",                   >> "source\conf.py"
echo     "html_admonition",             >> "source\conf.py"
echo     "html_image",                  >> "source\conf.py"
echo #    "linkify",                    >> "source\conf.py"
echo     "replacements",                >> "source\conf.py"
echo     "smartquotes",                 >> "source\conf.py"
echo     "strikethrough",               >> "source\conf.py"
echo     "substitution",                >> "source\conf.py"
echo     "tasklist",                    >> "source\conf.py"
echo ]                                  >> "source\conf.py"
echo.                                   >> "source\conf.py"


Rem echo suppress_warnings = ('myst.xref_missing','myst.header','misc.highlighting_failure','toc.not_included','toc.not_readable','toc.no_title') >> "source\conf.py"
echo locale_dirs = ['locale/']              >> "source\conf.py"
Rem To translate HTML too
echo gettext_additional_targets = ['raw']   >> "source\conf.py"

echo source_suffix = {               >> "source\conf.py"
echo     '.rst': 'restructuredtext', >> "source\conf.py"
echo     '.md': 'markdown',          >> "source\conf.py"
echo }                               >> "source\conf.py"


rmdir /s /q .\source\locale\
Call make clean
Call make gettext

sphinx-intl update -p build/gettext -l en -l it
ren ".\source\locale\it"        "it_it"
REM rmdir      ..\%RepoName%_OmegaT\source\%RepoName%\it
REM del /S /Q  ..\%RepoName%_OmegaT\source\%RepoName%\it
REM mklink /D "..\%RepoName%_OmegaT\source\%RepoName%\it"             "..\..\..\%RepoName%_Sphinx\source\locale\it_it"

rmdir      ..\FastLED_OmegaT\source\FastLED\it
del /S /Q  ..\FastLED_OmegaT\source\FastLED\it
mklink /D "..\FastLED_OmegaT\source\FastLED\it"             "..\..\..\FastLED_Sphinx\source\locale\it_it"



Rem Translate
rmdir      .\source\locale\it
del /S /Q  .\source\locale\it
mklink /D ".\source\locale\it"                    "..\..\..\FastLED_OmegaT\target\FastLED\it"
REM mklink /D ".\source\locale\it"                "..\..\..\%RepoName%_OmegaT\target\%RepoName%\it"


REM sphinx-build -v -b epub       -D language=it ./source build/epub/it
sphinx-build -v -b html       -D language=it ./source build/html/it

goto :EOF

Rem sphinx-build -v -b latex      -D language=it ./source build/latex/it
Rem Echo.
Rem Echo ****************************************
Rem Echo Create pdf...
Rem PUSHD .\build\latex\it
Rem FOR /R  %%F in (%RepoName%*.tex) do lualatex --interaction=nonstopmode %%~F
Rem FOR /R  %%F in (%RepoName%*.tex) do lualatex --interaction=nonstopmode %%~F
Rem POPD
Rem Echo ****************************************
Rem Echo.

:EOF 