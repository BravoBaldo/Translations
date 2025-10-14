

IF NOT EXIST ".\node-red.github.io_org\" (
   git clone https://github.com/node-red/node-red.github.io.git
) ELSE (
    XCOPY ".\node-red.github.io_org\" ".\node-red.github.io\" /E    > NUL
)

if 1==0 (
REM Original build
cd node-red.github.io
bundle install
bundle exec jekyll serve -w
http://127.0.0.1:4000/
)


mkdir Sphinx_NodeRed && cd Sphinx_NodeRed

sphinx-quickstart --sep -p "Node-Red" -a "Node-Red Community" -r "2025" -l "en" --extensions "myst_parser,sphinx_substitution_extensions"
echo source_suffix = ['.rst', '.md', 'txt']                             >> source\conf.py
echo locale_dirs = ['../locale/']                                       >> source\conf.py
echo myst_enable_extensions = {"colon_fence", "substitution",}          >> source\conf.py

copy ..\OmegaT_NodeRed\Docs\conf.py   .\source\ /y
copy ..\OmegaT_NodeRed\Docs\index.rst .\source\ /y

mkdir .\source\docs\user-guide\runtime
mklink    "source\docs\user-guide\index.md"                       "..\..\..\..\node-red.github.io\docs\user-guide\index.md"
mklink    "source\docs\user-guide\writing-functions.md"           "..\..\..\..\node-red.github.io\docs\user-guide\writing-functions.md"
mklink    "source\docs\user-guide\node-red-admin.md"              "..\..\..\..\node-red.github.io\docs\user-guide\node-red-admin.md"
mklink    "source\docs\user-guide\runtime\securing-node-red.md"   "..\..\..\..\node-red.github.io\docs\user-guide\runtime\"
mklink    "source\docs\user-guide\runtime\securing-node-red.md"   "..\..\..\..\..\node-red.github.io\docs\user-guide\runtime\securing-node-red.md"

mklink /D "source\docs\user-guide\images\"                 "..\..\..\..\node-red.github.io\docs\user-guide\images\"
mklink /D "source\docs\developing-flows"    "..\..\..\node-red.github.io\docs\developing-flows"




mklink /D "source\images\"  "..\..\node-red.github.io\images\"

REM When Finish!!!!
REM mklink /D "source\docs\"    "..\..\node-red.github.io\docs\"





rmdir /s /q .\locale\      2>nul
Call make clean & Call make gettext
sphinx-intl update -p build/gettext -l en -l it
ren ".\locale\it"        "it_it"

rmdir      ..\OmegaT_NodeRed\source\it   2>nul
del /S /Q  ..\OmegaT_NodeRed\source\it   2>nul
mklink /D "..\OmegaT_NodeRed\source\it"      "..\..\Sphinx_NodeRed\locale\it_it"

rmdir      .\locale\it   2>nul
del /S /Q  .\locale\it   2>nul
mklink /D ".\locale\it"                      "..\..\OmegaT_NodeRed\target\it"



REM sphinx-build -v -b html       -D language=it ./source build/html/it