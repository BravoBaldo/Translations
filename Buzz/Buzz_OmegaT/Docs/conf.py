# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Buzz'
copyright = '2026, Buzz Community'
author = 'Buzz Community'
release = '2026'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
latex_elements = {}                                                             
latex_documents = []                                                            
locale_dirs = ['locale/']                                                       
myst_heading_anchors = 7                                                        
suppress_warnings = ['myst.header','myst.xref_missing','toc.not_readable','epub.duplicated_toc_entry','epub.unknown_project_files']      
                                                             
release = '1.16.0'                                           
version = release                                            
import sys                                                   
import time                                                  
TimePrint = time.strftime("%Y%m%d")                       
Showversion = version + ' ' + TimePrint + ' (Ita)'           
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
                                                             
    pdfAuthor = '\\\\\\large(Traduzione: \\sphinxhref{https://github.com/BravoBaldo/Translations}{Baldassarre Cesarano})'   
    latex_documents = [('index',                                                      
    					'Buzz_'+release+'_Italiano'+'_'+TimePrint+'.tex',        
    					'Documentazione di Buzz v' + Showversion,                
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
    epub_basename = 'Buzz_'+release+'_Italiano'+'_'+TimePrint                                    
    epub_show_urls = 'no' # 'inline' # "footnote"                                                
    epub_title = 'Documentazione di Buzz v' + Showversion                                        
    epub_contributor = "BravoBaldo"                                                              
    epub_language = "it"                                                                         
    # epub_cover                                                                                 
    #master_doc = 'index_it'                                                                     
    epub_tocdepth = 2                                                                            
