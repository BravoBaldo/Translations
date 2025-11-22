Rem  Official display: https://google.github.io/googletest/

@echo off
cls
rmdir /S /Q googletest > NUL
rmdir /S /Q GoogleTest_Sphinx  > NUL
rmdir /S /Q GoogleTest_Italiano & mkdir GoogleTest_Italiano  > NUL

Rem ****************************************
Rem Sphinx and sphinx-intl are required
Rem ****************************************
pip install sphinx-intl      --upgrade
pip install sphinx-rtd-theme --upgrade
Rem ****************************************


IF NOT EXIST ".\googletest_org\" (
   git clone https://github.com/google/googletest.git
) ELSE (
    XCOPY ".\googletest_org\" ".\googletest\" /E    > NUL
)


IF NOT EXIST ".\googletest\" GOTO ErrNoCloning 


mkdir GoogleTest_Sphinx && cd GoogleTest_Sphinx
sphinx-quickstart --sep -p "GoogleTest" -a "GoogleTest Community" -r "2025" -l "en" --extensions "myst_parser"
REM ren source source_org
REM ren build build_org
REM del /S /Q source_org
REM del /S /Q build_org

cls

echo latex_elements = {}                                                             >> source\conf.py
echo latex_documents = []                                                            >> source\conf.py
echo locale_dirs = ['locale/']                                                       >> source\conf.py
echo myst_heading_anchors = 7                                                        >> "source\conf.py"
echo suppress_warnings = ['myst.header','myst.xref_missing','toc.not_readable','epub.duplicated_toc_entry','epub.unknown_project_files']      >> "source\conf.py"
echo.                                                             >> ".\source\conf.py"

REM echo gettext_additional_targets = ['raw']                         >> ".\source\conf.py"
echo release = '1.16.0'                                           >> ".\source\conf.py"
echo version = release                                            >> ".\source\conf.py"

echo import sys                                                   >> ".\source\conf.py"
echo import time                                                  >> ".\source\conf.py"
echo TimePrint = time.strftime("%%Y%%m%%d")                       >> ".\source\conf.py"
echo Showversion = version + ' ' + TimePrint + ' (Ita)'           >> ".\source\conf.py"
echo print("")                                                    >> ".\source\conf.py"
echo print("--------------------------------------")              >> ".\source\conf.py"
echo print("Added for Translations!")                             >> ".\source\conf.py"
echo print("Release.......: " + release)                          >> ".\source\conf.py"
echo print("Version.......: " + version)                          >> ".\source\conf.py"
echo print("Time Print....: " + TimePrint)                        >> ".\source\conf.py"
echo print("Show Version..: " + Showversion)                      >> ".\source\conf.py"
echo print(sys.argv)                                              >> ".\source\conf.py"
echo print("--------------------------------------")              >> ".\source\conf.py"
echo print("")                                                    >> ".\source\conf.py"
echo if "language=it" in sys.argv:                                >> ".\source\conf.py"
echo     language = 'it'                                          >> ".\source\conf.py"
echo     print("Traduzione Italiana")                             >> ".\source\conf.py"
echo     latex_elements.update({"papersize": "a4paper"})          >> ".\source\conf.py"
echo     latex_elements.update({"pointsize": "10pt"})             >> ".\source\conf.py"
echo     latex_elements.update({'release': release + " (Ita)"})   >> ".\source\conf.py"
echo.                                                             >> ".\source\conf.py"
echo     pdfAuthor = '\\\\\\large(Traduzione: \\sphinxhref{https://github.com/BravoBaldo/Translations}{Baldassarre Cesarano})'   >> ".\source\conf.py"
echo     latex_documents = [('index',                                                      >> ".\source\conf.py"
echo     					'GoogleTest_'+release+'_Italiano'+'_'+TimePrint+'.tex',        >> ".\source\conf.py"
echo     					'Documentazione di GoogleTest v' + Showversion,                >> ".\source\conf.py"
echo     					author + pdfAuthor,                                            >> ".\source\conf.py"
echo     					'manual', 1),                                                  >> ".\source\conf.py"
echo     				]                                                                  >> ".\source\conf.py"
echo.                                                                                      >> ".\source\conf.py"
echo.                                                                                      >> ".\source\conf.py"

echo if "epub" in sys.argv:                                                                           >> ".\source\conf.py"
echo     # *** EPUB Parameters EXPERIMENTAL ***                                                       >> ".\source\conf.py"
echo     # https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-epub-output      >> ".\source\conf.py"
echo     # https://sphinx-rtd-trial.readthedocs.io/en/1.1.3/config.html#options-for-epub-output       >> ".\source\conf.py"
echo     print("")                                                                                    >> ".\source\conf.py"
echo     print("--------------------------------------")                                              >> ".\source\conf.py"
echo     print("Compilazione EPUB")                                                                   >> ".\source\conf.py"
echo     print("--------------------------------------")                                              >> ".\source\conf.py"
echo     print("")                                                                                    >> ".\source\conf.py"
echo     language = 'it'                                                                              >> ".\source\conf.py"

echo     epub_basename = 'GoogleTest_'+release+'_Italiano'+'_'+TimePrint                                    >> ".\source\conf.py"
echo     epub_show_urls = 'no' # 'inline' # "footnote"                                                >> ".\source\conf.py"                                           >> ".\source\conf.py"
echo     epub_title = 'Documentazione di GoogleTest v' + Showversion                                        >> ".\source\conf.py"
echo     epub_contributor = "BravoBaldo"                                                              >> ".\source\conf.py"
echo     epub_language = "it"                                                                         >> ".\source\conf.py"
echo     # epub_cover                                                                                 >> ".\source\conf.py"
REM echo     suppress_warnings = ['epub.unknown_project_files','epub.duplicated_toc_entry']               >> ".\source\conf.py"
echo     #master_doc = 'index_it'                                                                     >> ".\source\conf.py"
echo     epub_tocdepth = 2                                                                            >> ".\source\conf.py"




REM xcopy /E /H /C /I /Y ..\GoogleTest_OmegaT\Docs\conf.py   .\source\
xcopy /E /H /C /I /Y ..\GoogleTest_OmegaT\Docs\index.rst .\source\
rmdir /s /q .\build

REM ren source source_org
REM ren build build_org
REM del /S /Q source_org
REM del /S /Q build_org
mklink /D "build"             "..\GoogleTest_Italiano"


REM mklink /D ".\source\docs"     "..\googletest\docs\intermediate"
mkdir .\source\docs

mklink ".\source\CONTRIBUTING.md"                          "..\..\googletest\CONTRIBUTING.md"
mklink ".\source\README.md"                                "..\..\googletest\README.md"

mklink ".\source\docs\advanced.md"                          "..\..\..\googletest\docs\advanced.md"
mklink ".\source\docs\community_created_documentation.md"   "..\..\..\googletest\docs\community_created_documentation.md"
mklink ".\source\docs\faq.md"                               "..\..\..\googletest\docs\faq.md"
mklink ".\source\docs\gmock_cheat_sheet.md"                 "..\..\..\googletest\docs\gmock_cheat_sheet.md"
mklink ".\source\docs\gmock_cook_book.md"                   "..\..\..\googletest\docs\gmock_cook_book.md"
mklink ".\source\docs\gmock_faq.md"                         "..\..\..\googletest\docs\gmock_faq.md"
mklink ".\source\docs\gmock_for_dummies.md"                 "..\..\..\googletest\docs\gmock_for_dummies.md"
mklink ".\source\docs\index.md"                             "..\..\..\googletest\docs\index.md"
mklink ".\source\docs\pkgconfig.md"                         "..\..\..\googletest\docs\pkgconfig.md"
mklink ".\source\docs\platforms.md"                         "..\..\..\googletest\docs\platforms.md"
mklink ".\source\docs\primer.md"                            "..\..\..\googletest\docs\primer.md"
mklink ".\source\docs\quickstart-bazel.md"                  "..\..\..\googletest\docs\quickstart-bazel.md"
mklink ".\source\docs\quickstart-cmake.md"                  "..\..\..\googletest\docs\quickstart-cmake.md"
mklink ".\source\docs\samples.md"                           "..\..\..\googletest\docs\samples.md"


REM mklink ".\source\docs\actions.md"                           "..\..\..\googletest\docs\reference\actions.md"
REM mklink ".\source\docs\assertions.md"                        "..\..\..\googletest\docs\reference\assertions.md"
REM mklink ".\source\docs\matchers.md"                          "..\..\..\googletest\docs\reference\matchers.md"
REM mklink ".\source\docs\mocking.md"                           "..\..\..\googletest\docs\reference\mocking.md"
REM mklink ".\source\docs\testing.md"                           "..\..\..\googletest\docs\reference\testing.md"

rmdir /s /q .\source\locale\
Call make clean
Call make gettext

sphinx-intl update -p build/gettext -l en -l it
ren ".\source\locale\it"        "it_it"

rmdir      ..\GoogleTest_OmegaT\source\it
del /S /Q  ..\GoogleTest_OmegaT\source\it
mklink /D "..\GoogleTest_OmegaT\source\it"             "..\..\GoogleTest_Sphinx\source\locale\it_it"



rmdir      .\source\locale\it
del /S /Q  .\source\locale\it
mklink /D ".\source\locale\it"                    "..\..\..\GoogleTest_OmegaT\target\it"     


Rem -------------------------------------------
REM del       "..\GoogleTest_OmegaT\source\README.md"
REM mklink    "..\GoogleTest_OmegaT\source\README.md"          "..\..\GoogleTest\docs\README.md"
REM del       "..\GoogleTest_OmegaT\source\CONTRIBUTING.md"
REM mklink    "..\GoogleTest_OmegaT\source\CONTRIBUTING.md"    "..\..\GoogleTest\docs\CONTRIBUTING.md"
Rem -------------------------------------------



sphinx-build -b singlehtml -D language=it ./source build/singlehtml/it
sphinx-build -b epub       -D language=it ./source build/epub/it
sphinx-build -b latex      -D language=it ./source build/latex/it

Echo.
Echo ****************************************
Echo Create pdf...
PUSHD .\build\latex\it
FOR /R  %%F in (GoogleTest*.tex) do lualatex --interaction=nonstopmode %%~F
FOR /R  %%F in (GoogleTest*.tex) do lualatex --interaction=nonstopmode %%~F
POPD
Echo ****************************************
Echo.
goto :EOF


:ErrNoCloning
ECHO "Error Wrong Cloning"
exit /b 1
goto :EOF

:EOF 