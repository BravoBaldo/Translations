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
Rem # For Latex
Rem # Append these rows to conf.py (example of batch file/command line)
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
python build.py latex

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


echo.                                                             >> ".\intermediate\conf.py"
echo.                                                             >> ".\intermediate\conf.py"
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
echo.                                                             >> ".\intermediate\conf.py"
echo.                                                             >> ".\intermediate\conf.py"




Rem *** Added for Translations **********
echo off
Rem # For Latex
Rem # Append these rows for Italian translation
echo.                                                             >> ".\intermediate\conf.py"
echo.                                                             >> ".\intermediate\conf.py"
echo locale_dirs = ['locale/']                                    >> ".\intermediate\conf.py"

Rem To translate HTML too
echo gettext_additional_targets = {'raw'}                         >> ".\intermediate\conf.py"

echo import sys                                                   >> ".\intermediate\conf.py"
echo import time                                                  >> ".\intermediate\conf.py"
echo TitleVersion = time.strftime("%%Y%%m%%d")                    >> ".\intermediate\conf.py"
echo print("")                                                    >> ".\intermediate\conf.py"
echo print("Added for Translations!")                             >> ".\intermediate\conf.py"
echo print("Version. " + version)                                 >> ".\intermediate\conf.py"
echo print("Title Version. " + TitleVersion)                      >> ".\intermediate\conf.py"
echo print(sys.argv)                                              >> ".\intermediate\conf.py"
echo print("")                                                    >> ".\intermediate\conf.py"
echo if "language=it" in sys.argv:                                >> ".\intermediate\conf.py"
echo     language = 'it'                                          >> ".\intermediate\conf.py"
echo     print("Traduzione Italiana")                             >> ".\intermediate\conf.py"
echo     #release = release                                       >> ".\intermediate\conf.py"
echo     version = version + ' ' + TitleVersion + ' (Ita)'        >> ".\intermediate\conf.py"
echo     latex_elements.update({"papersize": "a4paper"})          >> ".\intermediate\conf.py"
echo     latex_elements.update({"pointsize": "10pt"})             >> ".\intermediate\conf.py"
echo     latex_elements.update({'release': release + " (Ita)"})   >> ".\intermediate\conf.py"
echo     latex_documents = [(master_doc, 'LVGL_'+release+'_Italiano.tex', 'Documentazione di LVGL v' + version, author + '\\\\\\large(Traduzione: \\sphinxhref{https://github.com/BravoBaldo/Translations/tree/main/LVGL/}{Baldassarre Cesarano})', 'manual', 1),]   >> ".\intermediate\conf.py"

echo     latex_elements.update({'preamble': r'''   >> ".\intermediate\conf.py"
echo \usepackage{fontspec}                         >> ".\intermediate\conf.py"
echo \setmonofont[Scale=.8]{DejaVu Sans Mono}       >> ".\intermediate\conf.py"
echo \usepackage{silence}                           >> ".\intermediate\conf.py"
echo \WarningsOff*                                  >> ".\intermediate\conf.py"
echo ''',                                           >> ".\intermediate\conf.py"
echo })                                             >> ".\intermediate\conf.py"


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
rmdir /s /q .\source\locale\
Call make clean
Call make gettext
sphinx-intl update -p build/gettext -l en -l it
ren ".\source\locale\it"        "it_it"

rmdir      ..\LVGL_TradIta\source\it
mklink /D "..\LVGL_TradIta\source\it"             "..\..\Sphinx_LVGL\source\locale\it_it"
rmdir      .\source\locale\it
mklink /D ".\source\locale\it"                    "..\..\..\..\LVGL_TradIta\target\it"     

Rem cls
echo.
echo.
echo Building Translations
echo.
echo.


sphinx-build -v -b html       -D language=it ./source build/html/it
sphinx-build -v -b latex      -D language=it ./source build/latex/it
PUSHD .\build\latex\it
FOR /R  %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
FOR /R . %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
POPD

if 1==0 (
ECHO To Run before publish on git
cd ..
rmdir /S /Q lvgl
rmdir /S /Q Sphinx_LVGL
)

goto :eof

:ErrNoCloning
ECHO "Error Wrong Cloning"
goto :eof

:ErrNoIntermediate
ECHO "Error. No Intermediate directory created"
goto :eof

goto :eof
goto :eof
