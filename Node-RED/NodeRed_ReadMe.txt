*** In Progress ***

git clone https://github.com/node-red/node-red.github.io.git

REM cd node-red.github.io
REM bundle install
REM bundle exec jekyll serve -w
REM http://127.0.0.1:4000/

mkdir Sphinx_NodeRed && cd Sphinx_NodeRed

sphinx-quickstart --sep -p "Node-Red" -a "Node-Red Community" -r "2025" -l "en" --extensions "myst_parser,sphinx_substitution_extensions"
echo source_suffix = ['.rst', '.md', 'txt']                             >> source\conf.py
echo locale_dirs = ['locale/']                                          >> source\conf.py
echo myst_enable_extensions = {"colon_fence", "substitution",}          >> source\conf.py

rmdir /s /q .\source\locale\      2>nul
Call make clean & Call make gettext
sphinx-intl update -p build/gettext -l en -l it
ren ".\source\locale\it"        "it_it"

rmdir      ..\OmegaT_NodeRed\source\it   2>nul
del /S /Q  ..\OmegaT_NodeRed\source\it   2>nul
mklink /D "..\OmegaT_NodeRed\source\it"          "..\..\Sphinx_NodeRed\source\locale\it_it"

rmdir      .\source\locale\it   2>nul
del /S /Q  .\source\locale\it   2>nul
mklink /D ".\source\locale\it"                    "..\..\..\OmegaT_NodeRed\target\it"

sphinx-build -v -b html       -D language=it ./source build/html/it
sphinx-build -v -b latex      -D language=it ./source build/latex/it
sphinx-build -v -b epub       -D language=it ./source build/epub/it

<img src="./images/			<img src="../../_static/
<img src="../images/		<img src="../../../../_static/

src="./images/		src="../_static/
src="images/		src="../_static/
src="../images/	 	src="../../../../_static