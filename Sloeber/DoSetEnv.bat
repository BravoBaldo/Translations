Rem I suppose to be in LVGL of git clone https://github.com/BravoBaldo/Translations.git
Rem Sloeber\Sloeber_TradIta (OmegaT Folder for translation memories
Rem Sloeber\Sloeber_Italiano (The resulting files)

@echo off
cls
rmdir /S /Q arduino-eclipse-plugin 2>nul
rmdir /S /Q Sphinx_Sloeber         2>nul
rmdir /S /Q Sloeber_Italiano & mkdir Sloeber_Italiano  > NUL


Echo.
Echo ****************************************
Echo Sphinx and sphinx-intl are required...
pip install sphinx-intl --upgrade  > NUL
Echo ****************************************
Echo.

Rem ****************************************
Rem Note: Node.js is required
Rem ****************************************
Rem npm install -g @mermaid-js/mermaid-cli

IF NOT EXIST ".\arduino-eclipse-plugin_org\" (
   git clone https://github.com/Sloeber/arduino-eclipse-plugin.git
) ELSE (
    XCOPY ".\arduino-eclipse-plugin_org\" ".\arduino-eclipse-plugin\" /E    > NUL
)

IF NOT EXIST ".\arduino-eclipse-plugin\" GOTO ErrNoCloning 
Rem -----------------------------------------------------------------------------------------------


Rem ****************************************
Rem Sphinx
Rem ****************************************
Echo.
Echo ****************************************
echo Sphinx-build Preparation
Echo ****************************************
Echo.

mkdir Sphinx_Sloeber && cd Sphinx_Sloeber

Echo.
Echo ****************************************
Echo Create and Activate Virtual Env...
Call ..\activate
Echo ****************************************
Echo.


Echo.
Echo ***********************
Echo Start Install Requirements
Echo ***********************
Echo.

echo sphinx                          >> requirements.txt
echo myst-parser                     >> requirements.txt
echo sphinx-book-theme               >> requirements.txt
echo sphinx-togglebutton             >> requirements.txt
echo sphinx-copybutton               >> requirements.txt
echo sphinx-design                   >> requirements.txt
echo Sphinx-Substitution-Extensions  >> requirements.txt
echo Sphinx-build                    >> requirements.txt

python.exe -m pip install --upgrade pip
pip install -r requirements.txt    > NUL
Echo.
Echo *************************
Echo End Install Requirements
Echo *************************
Echo.
Rem -------------------------------------------------------

sphinx-quickstart --sep -p "Sloeber" -a "Sloeber Community" -r "2025" -l "en" --extensions "myst_parser,sphinx_substitution_extensions"
echo source_suffix = ['.rst', '.md', 'txt']                             >> source\conf.py
echo locale_dirs = ['locale/']                                          >> source\conf.py
echo myst_enable_extensions = {"colon_fence", "substitution",}          >> source\conf.py

Rem *** Added for Translations **********
echo off
echo.                                                             >> "source\conf.py"
echo.                                                             >> "source\conf.py"

echo if 'version' not in globals():                               >> "source\conf.py"
echo     version = "2.0"                                          >> "source\conf.py"
echo if 'suppress_warnings' not in globals():                     >> "source\conf.py"
echo     suppress_warnings = []                                   >> "source\conf.py"
echo if 'latex_documents' not in globals():                       >> "source\conf.py"
echo     latex_documents = []                                     >> "source\conf.py"
echo if 'latex_elements' not in globals():                        >> "source\conf.py"
echo     latex_elements = {}                                      >> "source\conf.py"
echo if 'master_doc' not in globals():                            >> "source\conf.py"
echo     master_doc = 'index'                                     >> "source\conf.py"


echo suppress_warnings.append('toc.not_included')                 >> "source\conf.py"
echo suppress_warnings.append('myst.xref_missing')                >> "source\conf.py"


Rem To translate HTML too
echo exclude_patterns.append("source/fragments/install_advice/mac_make.md")   >> source\conf.py

echo import sys                                                   >> "source\conf.py"
echo import time                                                  >> "source\conf.py"
echo TimePrint = time.strftime("%%Y%%m%%d")                       >> "source\conf.py"
echo Showversion = version + ' ' + TimePrint + ' (Ita)'           >> "source\conf.py"
echo print("")                                                    >> "source\conf.py"
echo print("--------------------------------------")              >> "source\conf.py"
echo print("Added for Translations!")                             >> "source\conf.py"
echo print("Release.......: " + release)                          >> "source\conf.py"
echo print("Version.......: " + version)                          >> "source\conf.py"
echo print("Time Print....: " + TimePrint)                        >> "source\conf.py"
echo print("Show Version..: " + Showversion)                      >> "source\conf.py"
echo print(sys.argv)                                              >> "source\conf.py"
echo print("--------------------------------------")              >> "source\conf.py"
echo print("")                                                    >> "source\conf.py"
echo if "language=it" in sys.argv:                                >> "source\conf.py"
echo     language = 'it'                                          >> "source\conf.py"
echo     print("Traduzione Italiana")                             >> "source\conf.py"
echo     latex_elements.update({"papersize": "a4paper"})          >> "source\conf.py"
echo     latex_elements.update({"pointsize": "10pt"})             >> "source\conf.py"
echo     latex_elements.update({'release': release + " (Ita)"})   >> "source\conf.py"

echo     pdfAuthor = '\\\\\\large(Traduzione: \\sphinxhref{https://github.com/BravoBaldo/Translations/tree/main/Sloeber/}{Baldassarre Cesarano})'   >> "source\conf.py"
echo     latex_documents = [(master_doc,                                          >> "source\conf.py"
echo     					'Sloeber_'+release+'_Italiano'+'_'+TimePrint+'.tex',  >> "source\conf.py"
echo     					'Documentazione di Sloeber v' + Showversion,          >> "source\conf.py"
echo     					author + pdfAuthor,                                   >> "source\conf.py"
echo     					'manual', 1),                                         >> "source\conf.py"
echo     				]                                                         >> "source\conf.py"

echo     latex_elements.update({'preamble': r'''    >> "source\conf.py"
echo \usepackage{fontspec}                          >> "source\conf.py"
echo \setmonofont[Scale=.8]{DejaVu Sans Mono}       >> "source\conf.py"
echo \usepackage{silence}                           >> "source\conf.py"

echo \WarningsOff*                                  >> "source\conf.py"
echo ''',                                           >> "source\conf.py"
echo })                                             >> "source\conf.py"

echo.                                                                                             >> "source\conf.py"
echo.                                                                                             >> "source\conf.py"

echo if "epub" in sys.argv:                                                                           >> "source\conf.py"
echo     # *** EPUB Parameters EXPERIMENTAL ***                                                       >> "source\conf.py"
echo     # https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-epub-output      >> "source\conf.py"
echo     # https://sphinx-rtd-trial.readthedocs.io/en/1.1.3/config.html#options-for-epub-output       >> "source\conf.py"
echo     print("")                                                                                    >> "source\conf.py"
echo     print("--------------------------------------")                                              >> "source\conf.py"
echo     print("Compilazione EPUB")                                                                   >> "source\conf.py"
echo     print("--------------------------------------")                                              >> "source\conf.py"
echo     print("")                                                                                    >> "source\conf.py"
echo     language = 'it'                                                                              >> "source\conf.py"

echo     epub_basename = 'Sloeber_'+release+'_Italiano'+'_'+TimePrint                                 >> "source\conf.py"
echo     epub_show_urls = 'no' # 'inline' # "footnote"                                                >> "source\conf.py"                                           >> "source\conf.py"
echo     epub_title = 'Documentazione di Sloeber v' + Showversion                                     >> "source\conf.py"
echo     epub_contributor = "BravoBaldo"                                                              >> "source\conf.py"
echo     epub_language = "it"                                                                         >> "source\conf.py"
echo     # epub_cover                                                                                 >> "source\conf.py"
echo     suppress_warnings.append('epub.unknown_project_files')                                       >> "source\conf.py"
echo     suppress_warnings.append('epub.duplicated_toc_entry')                                        >> "source\conf.py"
echo     #master_doc = 'index_it'                                                                     >> "source\conf.py"
echo     epub_tocdepth = 2                                                                            >> "source\conf.py"

Echo.
Echo ****************************************
Echo Fine Preparazione
Echo ****************************************

Echo.
Echo ****************************************
Echo Creazione Link per Build...
rmdir /s /q .\build & mklink /D "build"  "..\Sloeber_Italiano"
mklink /D "source\fragments"     "..\..\arduino-eclipse-plugin\website\WebContent\fragments"
Echo ****************************************
Echo.

copy /y ..\Sloeber_TradIta\Docs\index.rst source\index.rst

Call make clean
Call make gettext

rmdir /s /q .\source\locale\      > NUL
Call make clean
Call make gettext
sphinx-intl update -p build/gettext -l en -l it
ren ".\source\locale\it"        "it_it"

rmdir      ..\Sloeber_TradIta\source\it   > NUL
del /S /Q  ..\Sloeber_TradIta\source\it   > NUL
mklink /D "..\Sloeber_TradIta\source\it"          "..\..\Sphinx_Sloeber\source\locale\it_it"

rmdir      .\source\locale\it   > NUL
del /S /Q  .\source\locale\it   > NUL
mklink /D ".\source\locale\it"                    "..\..\..\Sloeber_TradIta\target\it"


Rem CALL deactivate 
Rem cd ..
ECHO Finish



goto :EOF


:ErrNoCloning
ECHO "Error Wrong Cloning"
exit /b 1
goto :EOF

:ErrGeneric
ECHO "Someting was wrong"
goto :eof

:EOF 