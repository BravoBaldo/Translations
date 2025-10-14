*** In Progress ***

git clone https://github.com/node-red/node-red.github.io.git

if 1==0 (
cd node-red.github.io
bundle install
bundle exec jekyll serve -w
http://127.0.0.1:4000/
)
mkdir Sphinx_NodeRed && cd Sphinx_NodeRed

sphinx-quickstart --sep -p "Node-Red" -a "Node-Red Community" -r "2025" -l "en" --extensions "myst_parser,sphinx_substitution_extensions"
echo source_suffix = ['.rst', '.md', 'txt']                             >> source\conf.py
echo locale_dirs = ['../locale/']                                          >> source\conf.py
echo myst_enable_extensions = {"colon_fence", "substitution",}          >> source\conf.py


copy ..\OmegaT_NodeRed\Docs\conf.py   .\source\ /y
copy ..\OmegaT_NodeRed\Docs\index.rst .\source\ /y

mkdir .\source\docs\user-guide
mklink    "source\docs\user-guide\index.md"                "..\..\..\..\node-red.github.io\docs\user-guide\index.md"
mklink    "source\docs\user-guide\writing-functions.md"    "..\..\..\..\node-red.github.io\docs\user-guide\writing-functions.md"
mklink /D "source\docs\user-guide\images\"                 "..\..\..\..\node-red.github.io\docs\user-guide\images\"

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


sphinx-build -v -b html       -D language=it ./source build/html/it
sphinx-build -v -b epub       -D language=it ./source build/epub/it
sphinx-build -v -b latex      -D language=it ./source build/latex/it


PUSHD .\build\latex\it
FOR /R  %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
FOR /R  %%F in (*.tex) do lualatex --interaction=nonstopmode %%~F
POPD
<img src="./images/			<img src="../../_static/
<img src="../images/		<img src="../../../../_static/

src="./images/		src="../_static/
src="images/		src="../_static/
src="../images/	 	src="../../../../_static

<img style="margin-left: 20px;" src="../../_static/function_external_modules.png" width="90%"/>


.doc-callout{
     background-color: #e3eff1;
   font-style: bold;
}

Nota: la creazione di un nuovo oggetto messaggio comporterà la perdita di tutte le proprietà del messaggio ricevuto.
Ciò interromperà alcuni flussi, ad esempio il flusso HTTP In/Response richiede che le proprietà <code>msg.req</code> e <code>msg.res</code> vengano preservate end-to-end.
In generale, i nodi funzione <em>dovrebbero</em> restituire l'oggetto messaggio che è stato loro passato dopo aver apportato modifiche alle sue proprietà.</div>

<div class="doc-callout"><em>Nota</em> : queste variabili predefinite sono una funzionalità del nodo Funzione. Se si sta creando un nodo personalizzato, consultare la <a href="/docs/creating-nodes/context">guida "Creating Nodes"</a> per informazioni su come accedere al contesto.</div>

