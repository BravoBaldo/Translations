Rem https://github.com/chidiwilliams/buzz/tree/main/docs/docs
Rem C:\Dati\BravoBaldo\Buzz\BUZZ_Sphinx

@echo off
cls
rmdir /S /Q buzz > NUL
rmdir /S /Q Buzz_Sphinx  > NUL
Rem del /S /Q Buzz_Italiano  > NUL
rmdir /S /Q Buzz_Italiano & mkdir Buzz_Italiano  > NUL

IF NOT EXIST ".\buzz_org\" (
   git clone https://github.com/chidiwilliams/buzz.git
) ELSE (
    XCOPY ".\buzz_org\" ".\buzz\" /E    > NUL
)

mkdir Buzz_Sphinx && cd Buzz_Sphinx
sphinx-quickstart --sep -p "Buzz" -a "Buzz Community" -r "2026" -l "en" --extensions "myst_parser"


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
echo     					'Buzz_'+release+'_Italiano'+'_'+TimePrint+'.tex',        >> ".\source\conf.py"
echo     					'Documentazione di Buzz v' + Showversion,                >> ".\source\conf.py"
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

echo     epub_basename = 'Buzz_'+release+'_Italiano'+'_'+TimePrint                                    >> ".\source\conf.py"
echo     epub_show_urls = 'no' # 'inline' # "footnote"                                                >> ".\source\conf.py"                                           >> ".\source\conf.py"
echo     epub_title = 'Documentazione di Buzz v' + Showversion                                        >> ".\source\conf.py"
echo     epub_contributor = "BravoBaldo"                                                              >> ".\source\conf.py"
echo     epub_language = "it"                                                                         >> ".\source\conf.py"
echo     # epub_cover                                                                                 >> ".\source\conf.py"
REM echo     suppress_warnings = ['epub.unknown_project_files','epub.duplicated_toc_entry']               >> ".\source\conf.py"
echo     #master_doc = 'index_it'                                                                     >> ".\source\conf.py"
echo     epub_tocdepth = 2                                                                            >> ".\source\conf.py"



copy /Y ..\Buzz_OmegaT\Docs\index.rst .\source\

rmdir /s /q .\build
mklink /D "build"             "..\Buzz_Italiano"

mkdir .\source\docs

mklink /D ".\source\Images\"          "..\..\Buzz_OmegaT\Docs\Img"
mklink    "source\docs\README.md"     "..\..\..\buzz\docs\README.md"
mklink /D "source\docs\docs"          "..\..\..\buzz\docs\docs"

REM Prepend as first 2 rows: ":orphan:" + CrLf in 
REM		1_file_import.md
REM		2_live_recording.md
REM		3_translations.md
REM		4_edit_and_resize.md
REM		5_speaker_identification.md


rmdir /s /q .\source\locale\
Call make clean
Call make gettext
sphinx-intl update -p build/gettext -l en -l it
ren ".\source\locale\it"        "it_it"

rmdir      ..\Buzz_OmegaT\source\it
del /S /Q  ..\Buzz_OmegaT\source\it
mklink /D "..\Buzz_OmegaT\source\it"             "..\..\Buzz_Sphinx\source\locale\it_it"


rmdir      .\source\locale\it
del /S /Q  .\source\locale\it
mklink /D ".\source\locale\it"                    "..\..\..\Buzz_OmegaT\target\it"

sphinx-build -v -b epub       -D language=it ./source build/epub/it
sphinx-build -v -b html       -D language=it ./source build/html/it
sphinx-build -v -b latex      -D language=it ./source build/latex/it

Echo.
Echo ****************************************
Echo Create pdf...
PUSHD .\build\latex\it
FOR /R  %%F in (*.tex) do pdflatex --interaction=nonstopmode %%~F
FOR /R  %%F in (*.tex) do pdflatex --interaction=nonstopmode %%~F
POPD
Echo ****************************************
Echo.


REM In the English segmentation  add "[0-9]\."

