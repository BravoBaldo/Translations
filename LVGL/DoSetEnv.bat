Rem I suppose to be in LVGL of git clone https://github.com/BravoBaldo/Translations.git
Rem LVGL\LVGL_TradIta (OmegaT Folder for translation memories
Rem LVGL\LVGL_Italiano (The resulting files)
@echo off
cls
rmdir /S /Q lvgl > NUL
rmdir /S /Q Sphinx_LVGL  > NUL
Rem del /S /Q LVGL_Italiano  > NUL
rmdir /S /Q LVGL_Italiano & mkdir LVGL_Italiano  > NUL

Rem ****************************************
Rem Sphinx and sphinx-intl are required
Rem ****************************************
pip install sphinx-intl --upgrade

Rem ****************************************
Rem Note: Node.js is required
Rem ****************************************
Rem npm install -g @mermaid-js/mermaid-cli


IF NOT EXIST ".\lvgl_org\" (
   git clone https://github.com/lvgl/lvgl.git
) ELSE (
    XCOPY ".\lvgl_org\" ".\lvgl\" /E    > NUL
)


IF NOT EXIST ".\lvgl\" GOTO ErrNoCloning 

Rem ****************************************
Rem First build of lvgl's docs
Rem ****************************************
cd .\lvgl\docs
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

Rem **************************************************
Rem First build, and intermediate directory creation
Rem **************************************************
ECHO OFF

echo.
echo.
echo **************************************************
echo Start Original Docs Buildings
echo **************************************************
echo.
echo.

echo.
echo **************************************************
echo Building HTML
echo **************************************************
echo.
python build.py clean html
Rem Continue with other builds for references
Rem Note: The original build of the Latex version crashes 4 times due to "warning" errors.


echo.
echo.
echo **************************************************
echo Add patch for mermaid
echo **************************************************
echo.
echo.
Rem *** To avoid "mmdc" command not found in Latex *************************************
echo off
echo #                                                        >> ".\intermediate\conf.py"
echo # To avoid "mmdc" command not found in Latex             >> ".\intermediate\conf.py"
echo mermaid_cmd_shell = str(True)                            >> ".\intermediate\conf.py"
echo mermaid_cmd = os.getenv('APPDATA') + "\\npm\\mmdc"       >> ".\intermediate\conf.py"
echo #                                                        >> ".\intermediate\conf.py"
echo on
Rem *********************************************************************************




echo.
echo **************************************************
echo Building LATEX
echo **************************************************
echo.
Rem python build.py latex

REM echo.
REM echo **************************************************
REM echo Building GETTEXT
REM echo **************************************************
REM echo.
REM python build.py gettext

IF NOT EXIST ".\intermediate\" GOTO ErrNoIntermediate 





echo.
echo.
echo **************************************************
echo Conf.py Customization
echo **************************************************
echo.
echo.


echo.                                                                    >> ".\intermediate\conf.py"
echo.                                                                    >> ".\intermediate\conf.py"
Echo # ####### Trick to reduce the font size of the code   ##########    >> ".\intermediate\conf.py"
Echo from sphinx.highlighting import PygmentsBridge                      >> ".\intermediate\conf.py"
Echo from pygments.formatters.latex import LatexFormatter                >> ".\intermediate\conf.py"
Echo.                                                                    >> ".\intermediate\conf.py"
Echo class CustomLatexFormatter(LatexFormatter):                         >> ".\intermediate\conf.py"
Echo     def __init__(self, **options):                                  >> ".\intermediate\conf.py"
Echo         super(CustomLatexFormatter, self).__init__(**options)       >> ".\intermediate\conf.py"
Echo         self.verboptions = r"formatcom=\tiny"                       >> ".\intermediate\conf.py"
Echo.                                                                    >> ".\intermediate\conf.py"
Echo PygmentsBridge.latex_formatter = CustomLatexFormatter               >> ".\intermediate\conf.py"
Echo ################################################################    >> ".\intermediate\conf.py"
echo.                                                                    >> ".\intermediate\conf.py"
echo.                                                                    >> ".\intermediate\conf.py"


Rem *** Added for Translations **********
echo off
echo.                                                             >> ".\intermediate\conf.py"
echo.                                                             >> ".\intermediate\conf.py"
echo locale_dirs = ['locale/']                                    >> ".\intermediate\conf.py"
Rem To translate HTML too
echo gettext_additional_targets = ['raw']                         >> ".\intermediate\conf.py"
echo import sys                                                   >> ".\intermediate\conf.py"
echo import time                                                  >> ".\intermediate\conf.py"
echo TimePrint = time.strftime("%%Y%%m%%d")                       >> ".\intermediate\conf.py"
echo Showversion = version + ' ' + TimePrint + ' (Ita)'           >> ".\intermediate\conf.py"
echo print("")                                                    >> ".\intermediate\conf.py"
echo print("--------------------------------------")              >> ".\intermediate\conf.py"
echo print("Added for Translations!")                             >> ".\intermediate\conf.py"
echo print("Release.......: " + release)                          >> ".\intermediate\conf.py"
echo print("Version.......: " + version)                          >> ".\intermediate\conf.py"
echo print("Time Print....: " + TimePrint)                        >> ".\intermediate\conf.py"
echo print("Show Version..: " + Showversion)                      >> ".\intermediate\conf.py"
echo print(sys.argv)                                              >> ".\intermediate\conf.py"
echo print("--------------------------------------")              >> ".\intermediate\conf.py"
echo print("")                                                    >> ".\intermediate\conf.py"
echo if "language=it" in sys.argv:                                >> ".\intermediate\conf.py"
echo     language = 'it'                                          >> ".\intermediate\conf.py"
echo     print("Traduzione Italiana")                             >> ".\intermediate\conf.py"
echo     latex_elements.update({"papersize": "a4paper"})          >> ".\intermediate\conf.py"
echo     latex_elements.update({"pointsize": "10pt"})             >> ".\intermediate\conf.py"
echo     latex_elements.update({'release': release + " (Ita)"})   >> ".\intermediate\conf.py"

echo     pdfAuthor = '\\\\\\large(Traduzione: \\sphinxhref{https://github.com/BravoBaldo/Translations/tree/main/LVGL/}{Baldassarre Cesarano})'   >> ".\intermediate\conf.py"
echo     latex_documents = [(master_doc,                                       >> ".\intermediate\conf.py"
echo     					'LVGL_'+release+'_Italiano'+'_'+TimePrint+'.tex',  >> ".\intermediate\conf.py"
echo     					'Documentazione di LVGL v' + Showversion,          >> ".\intermediate\conf.py"
echo     					author + pdfAuthor,                                >> ".\intermediate\conf.py"
echo     					'manual', 1),                                      >> ".\intermediate\conf.py"
echo     				]                                                      >> ".\intermediate\conf.py"

echo     latex_elements.update({'preamble': r'''    >> ".\intermediate\conf.py"
echo \usepackage{fontspec}                          >> ".\intermediate\conf.py"
echo \setmonofont[Scale=.8]{DejaVu Sans Mono}       >> ".\intermediate\conf.py"
REM echo \setmonofont[Scale=.8]{MS Gothic}              >> ".\intermediate\conf.py"
echo \usepackage{silence}                           >> ".\intermediate\conf.py"
REM Rem ***EXPERIMENTAL 1 ***
REM echo \usepackage{polyglossia}                       >> ".\intermediate\conf.py"
REM echo \setotherlanguage{hebrew}                      >> ".\intermediate\conf.py"
REM echo \setotherlanguage{chinese}                     >> ".\intermediate\conf.py"
REM Rem ***EXPERIMENTAL 2 ***
REM echo \usepackage{enumitem}\setlistdepth{99}         >> ".\intermediate\conf.py"

echo \WarningsOff*                                  >> ".\intermediate\conf.py"
echo ''',                                           >> ".\intermediate\conf.py"
echo })                                             >> ".\intermediate\conf.py"

echo.                                                                                             >> ".\intermediate\conf.py"
echo.                                                                                             >> ".\intermediate\conf.py"

echo if "epub" in sys.argv:                                                                           >> ".\intermediate\conf.py"
echo     # *** EPUB Parameters EXPERIMENTAL ***                                                       >> ".\intermediate\conf.py"
echo     # https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-epub-output      >> ".\intermediate\conf.py"
echo     # https://sphinx-rtd-trial.readthedocs.io/en/1.1.3/config.html#options-for-epub-output       >> ".\intermediate\conf.py"
echo     print("")                                                                                    >> ".\intermediate\conf.py"
echo     print("--------------------------------------")                                              >> ".\intermediate\conf.py"
echo     print("Compilazione EPUB")                                                                   >> ".\intermediate\conf.py"
echo     print("--------------------------------------")                                              >> ".\intermediate\conf.py"
echo     print("")                                                                                    >> ".\intermediate\conf.py"
echo     language = 'it'                                                                              >> ".\intermediate\conf.py"

echo     epub_basename = 'LVGL_'+release+'_Italiano'+'_'+TimePrint                                    >> ".\intermediate\conf.py"
echo     epub_show_urls = 'no' # 'inline' # "footnote"                                                >> ".\intermediate\conf.py"                                           >> ".\intermediate\conf.py"
echo     epub_title = 'Documentazione di LVGL v' + Showversion                                        >> ".\intermediate\conf.py"
echo     epub_contributor = "BravoBaldo"                                                              >> ".\intermediate\conf.py"
echo     epub_language = "it"                                                                         >> ".\intermediate\conf.py"
echo     # epub_cover                                                                                 >> ".\intermediate\conf.py"
echo     suppress_warnings = ['epub.unknown_project_files','epub.duplicated_toc_entry']               >> ".\intermediate\conf.py"
echo     #master_doc = 'index_it'                                                                     >> ".\intermediate\conf.py"
echo     epub_tocdepth = 2                                                                            >> ".\intermediate\conf.py"
#epub_exclude_files
#epub_tocdup = False


echo on
Rem *********************************************************************************

Rem ****************************************
Rem ToDo: Check files exists! IF [NOT] EXIST filename command

cd ..\..


Rem ****************************************
Rem Sphinx
Rem ****************************************
echo.
echo.
echo Sphinx-build Preparation
echo.
echo.

mkdir Sphinx_LVGL && cd Sphinx_LVGL
sphinx-quickstart --sep -p "LVGL" -a "LVGL Community" -r "2025" -l "en" --extensions "sphinx.ext.autodoc,sphinx.ext.extlinks,sphinx.ext.intersphinx,sphinx.ext.todo,sphinx.ext.viewcode,sphinx_copybutton,breathe,sphinx_sitemap,lv_example,sphinx_design,sphinxcontrib.mermaid'"
ren source source_org
ren build build_org
del /S /Q source_org
del /S /Q build_org

mklink /D "source"     "..\lvgl\docs\intermediate"
mklink /D "build"      "..\LVGL_Italiano"
Rem -------------------------------------------
rmdir /s /q .\source\locale\
Call make clean
Call make gettext
sphinx-intl update -p build/gettext -l en -l it
ren ".\source\locale\it"        "it_it"

rmdir      ..\LVGL_TradIta\source\it
del /S /Q  ..\LVGL_TradIta\source\it
mklink /D "..\LVGL_TradIta\source\it"             "..\..\Sphinx_LVGL\source\locale\it_it"

del       "..\LVGL_TradIta\source\README.md"
mklink    "..\LVGL_TradIta\source\README.md"             "..\..\lvgl\docs\README.md"
del       "..\LVGL_TradIta\source\CODE_OF_CONDUCT.md"
mklink    "..\LVGL_TradIta\source\CODE_OF_CONDUCT.md"    "..\..\lvgl\docs\CODE_OF_CONDUCT.md"

rmdir      .\source\locale\it
del /S /Q  .\source\locale\it
mklink /D ".\source\locale\it"                    "..\..\..\..\LVGL_TradIta\target\it"     
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