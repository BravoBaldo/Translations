Rem I suppose to be in LVGL of git clone https://github.com/BravoBaldo/Translations.git
Rem LVGL\LVGL_TradIta (OmegaT Folder for translation memories
Rem LVGL\LVGL_Italiano (The resulting files)
Rem @echo off
cls

Rem ****************************************
Rem Sphinx and sphinx-intl are required
Rem ****************************************
pip install sphinx-intl --upgrade

Rem ****************************************
Rem Note: Node.js is required
Rem ****************************************
Rem npm install -g @mermaid-js/mermaid-cli

git clone https://github.com/lvgl/lvgl.git
Rem ToDo: Check cloning!

Rem ****************************************
Rem First build of lvgl's docs
Rem ****************************************
cd .\lvgl\docs
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

Rem **************************************************
Rem First build, and intermediate directory creation
Rem **************************************************
python build.py clean html
Rem ToDo: Check intermediate directory exists!

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

Rem *** Added for Translations **********
echo off
Rem # For Latex
Rem # Append these rows for Italian translation
echo.                                                             >> ".\intermediate\conf.py"
echo.                                                             >> ".\intermediate\conf.py"
echo locale_dirs = ['locale/']                                    >> ".\intermediate\conf.py"
echo import sys                                                   >> ".\intermediate\conf.py"
echo import time                                                  >> ".\intermediate\conf.py"
echo TitleVersion = time.strftime("%Y%m%d")                       >> ".\intermediate\conf.py"
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
echo     version = version + TitleVersion + ' (Ita)'              >> ".\intermediate\conf.py"
echo     latex_elements.update({"papersize": "a4paper"})          >> ".\intermediate\conf.py"
echo     latex_elements.update({"pointsize": "10pt"})             >> ".\intermediate\conf.py"
echo     latex_elements.update({'release': release + " (Ita)"})   >> ".\intermediate\conf.py"
echo     latex_documents = [(master_doc, 'LVGL_'+release+'_Italiano.tex', 'Documentazione di LVGL v' + version, author + '\\\\\large(Traduzione: \sphinxhref{https://github.com/BravoBaldo}{Baldassarre Cesarano})', 'manual', 1),]   >> ".\intermediate\conf.py"
echo on
Rem *********************************************************************************

Rem Continue with other builds for references
Rem Note: The original build of the Latex version crashes 4 times due to "warning" errors.
python build.py latex
python build.py singlehtml
python build.py gettext
Rem ****************************************
Rem ToDo: Check files exists!

cd ..\..


Rem ****************************************
Rem Sphinx
Rem ****************************************

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
sphinx-build -v -b html       -D language=it ./source build/html/it
Rem cls & sphinx-build -v -b singlehtml -D language=it ./source build/singlehtml/it
Rem cls
sphinx-build -v -b latex      -D language=it ./source build/latex/it
PUSHD .\build\latex\it
FOR /R  %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
FOR /R . %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
POPD
Rem cd ..
Rem rmdir /S /Q lvgl
Rem rmdir /S /Q Sphinx_LVGL

