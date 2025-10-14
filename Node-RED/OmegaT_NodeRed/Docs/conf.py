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
locale_dirs = ['../locale/']                                          
myst_enable_extensions = {"colon_fence", "substitution",}          
myst_substitutions = {
    "keyNote":      "```{image} ../img/css-box-icon-note.png\n:alt: Note\n:align: left\n```",
}

suppress_warnings = ['toc.no_title','myst.xref_missing','myst.header','toc.not_readable','epub.unknown_project_files','toc.not_included','docutils']
version = "2025"
gettext_additional_targets = []
#gettext_additional_targets.append('index')          # index terms
#gettext_additional_targets.append('literal-block')  # literal blocks (:: annotation and code-block directive)
#gettext_additional_targets.append('doctest-block')  # doctest block
#gettext_additional_targets.append('raw')            # raw content, To translate HTML too
#gettext_additional_targets.append('image')          # image/figure uri

