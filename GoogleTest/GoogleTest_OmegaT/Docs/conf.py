# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GoogleTest'
copyright = '2024, BravoBaldo'
author = 'BravoBaldo'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
extensions.append('myst_parser') 
locale_dirs = ['locale/']
myst_heading_anchors = 7             

suppress_warnings = ["myst.header","myst.xref_missing"]  

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
'papersize': 'a4paper',

# The font size ('10pt', '11pt' or '12pt').
'pointsize': '12pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',

'release': '2.2.0 (Ita)',
}
latex_documents = [
    # (source start file, target name, title,author, documentclass [howto, manual, or own class]).
    # (startdocname, targetname, title, author, theme, toctree_only)
    ("index", 'GoogleTest_Italiano.tex', 'Documentazione di GoogleTest', 'GoogleTest team \\\\\large(Traduzione: \sphinxhref{https://github.com/BravoBaldo}{Baldassarre Cesarano})', 'manual'),
]


from datetime import datetime

now = datetime.now() # current date and time
version=now.strftime("%Y%m%d_Ita")
#version="20240121_Ita"