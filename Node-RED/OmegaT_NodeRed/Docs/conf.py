# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Node-Red'
copyright = '2025, Node-Red Community'
author = 'Node-Red Community'
release = '2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_substitution_extensions',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
source_suffix = ['.rst', '.md', 'txt']                             
locale_dirs = ['locale/']                                          
myst_enable_extensions = {"colon_fence", "substitution",}          

suppress_warnings = ['toc.no_title','myst.xref_missing','myst.header','toc.not_readable','epub.unknown_project_files']