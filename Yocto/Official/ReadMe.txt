In progress:

========== Linux Environment just once ============================================================

sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv make tar git sphinx-common -y
sudo apt install librsvg2-bin -y
sudo apt install sphinx-intl
pip install sphinx_rtd_theme
pip3  install sphinx sphinx_rtd_theme 
------------------------------------------------
cd ~/data/yocto
git clone https://git.yoctoproject.org/yocto-docs
vi yocto-docs/documentation/conf.py 
### Add Italian info
cd yocto-docs
python3 -m venv venv
source venv/bin/activate
python3 -m pip install sphinx sphinx_rtd_theme pyyaml sphinx-copybutton 'sphinxcontrib-svg2pdfconverter>=2.0.0'
cd documentation

rm -r ./locale/
make clean
make gettext
clear
sphinx-intl update -p _build/gettext -l en -l it
mv ./locale/it        ./locale/it_it
--------------
---Add To Conf.py ----
locale_dirs = ['locale/']
smartquotes = False
gettext_additional_targets = ['raw']
import sys                                                   
import time                                                  
TimePrint = time.strftime("%Y%m%d")
Showversion = current_version + ' ' + TimePrint + ' (Ita)'           
print("")                                                    
print("--------------------------------------")              
print("Added for Translations!")                             
print("Release.......: " + release)                          
print("Version.......: " + version)                          
print("Time Print....: " + TimePrint)                        
print("Show Version..: " + Showversion)                      
print(sys.argv)                                              
print("--------------------------------------")              
print("")                                                    
if "language=it" in sys.argv:
    language = 'it'
    print("Traduzione Italiana")
    latex_elements.update({"papersize": "a4paper"})
    latex_elements.update({"pointsize": "10pt"})
    latex_elements.update({'release': release + " (Ita)"})
    pdfAuthor = '\\\\\\large(Traduzione: \\sphinxhref{https://github.com/BravoBaldo/Translations/tree/main/Yocto/}{Baldassarre Cesarano})'
    latex_documents = [(master_doc,
    					'YoctoProject_'+release+'_Italiano'+'_'+TimePrint+'.tex',
    					'Documentazione di Yocto Project ' + Showversion,
    					author + pdfAuthor,
    					'manual', 1),
    				]

if "epub" in sys.argv:                                                                           
    # *** EPUB Parameters EXPERIMENTAL ***                                                       
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-epub-output      
    # https://sphinx-rtd-trial.readthedocs.io/en/1.1.3/config.html#options-for-epub-output       
    print("")                                                                                    
    print("--------------------------------------")                                              
    print("Compilazione EPUB")                                                                   
    print("--------------------------------------")                                              
    print("")                                                                                    
    language = 'it'                                                                              
    epub_basename = 'YoctoProject_'+release+'_Italiano'+'_'+TimePrint                                    
    epub_show_urls = 'no' # 'inline' # "footnote"                                                
    epub_title = 'Documentazione di Yocto Project ' + Showversion                                        
    epub_contributor = "BravoBaldo"                                                              
    epub_language = "it"                                                                         
    # epub_cover                                                                                 
    #master_doc = 'index_it'           
    suppress_warnings = ['epub.unknown_project_files','epub.duplicated_toc_entry']    
    epub_tocdepth = 2                                                                            
----------------------
========================================================================================

======= Win Environment just once =============
cd .....\Translations\Yocto\Official\Yocto_OmegaT
mkdir .\source\Yocto\
rmdir .\source\Yocto\it
mklink /D ".\source\Yocto\it"             "\\wsl.localhost\Ubuntu\home\balda\data\yocto\yocto-docs\documentation\locale\it_it"

------------------------
%%% (Administrator) choco install make
%%% set RepoName=Yocto
%%% mkdir %RepoName%_Sphinx && cd %RepoName%_Sphinx
%%% sphinx-quickstart --sep -p 'The Yocto Project \xae' -a 'The Linux Foundation' -r "2026" -l "en" --extensions "'sphinx.ext.autosectionlabel','sphinx.ext.extlinks','sphinx.ext.intersphinx','sphinx_copybutton','sphinxcontrib.rsvgconverter','yocto-vars'"
-------------------------------

------------------


=============Restart========

---Ubuntu---
cd ~/data/yocto/yocto-docs/documentation
unlink ./locale/it
%%% ln -s /mnt/c/Dati/BravoBaldo/Yocto/Yocto_OmegaT/target//Yocto/it ./locale/it
ln -s /mnt/c/Dati/BravoBaldo/Translations/Yocto/Official/Yocto_OmegaT/target/Yocto/it ./locale/it
sphinx-build -v -b html       -D language=it . _build/html/it
--------------

===UBUNTU==============================================
cd ~/data/yocto/yocto-docs
source venv/bin/activate
cd ./documentation
rm -r _build/html/it
sphinx-build -v -b html       -D language=it . _build/html/it
rm -r _build/epub/it
sphinx-build -v -b epub       -D language=it . _build/epub/it
rm -r _build/latex/it
sphinx-build -v -b latex      -D language=it . _build/latex/it
pushd _build/latex/it
make
cd -
=================================================




