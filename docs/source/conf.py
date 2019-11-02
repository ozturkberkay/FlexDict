import alabaster
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join('..', '..'))
)
import flexdict

# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosectionlabel',
    'alabaster',
    'recommonmark'
]
templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
project = 'FlexDict'
copyright = '2019, Berkay Öztürk'
author = 'Berkay Öztürk'
version = flexdict.__version__
release = flexdict.__version__
language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True

# -- Options for HTML output ----------------------------------------------
html_theme_path = [alabaster.get_path()]
html_theme = 'alabaster'
html_static_path = ['_static']
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}
html_theme_options = {
    'logo': 'logo.png',
    'github_user': 'ozturkberkay',
    'github_repo': 'FlexDict',
    'github_banner': 'true',
}

# -- Options for HTMLHelp output ------------------------------------------
htmlhelp_basename = 'FlexDictdoc'

# -- Options for LaTeX output ---------------------------------------------
latex_elements = {}
latex_documents = [(
    master_doc,
    'FlexDict.tex',
    'FlexDict Documentation',
    'Berkay Öztürk',
    'manual'
),]

# -- Options for manual page output ---------------------------------------
man_pages = [(
    master_doc,
    'flexdict',
    'FlexDict Documentation',
    [author],
    1
)]

# -- Options for Texinfo output -------------------------------------------
texinfo_documents = [(
    master_doc,
    'FlexDict',
    'FlexDict Documentation',
    author,
    'FlexDict',
    'Python dict with automatic and arbitrary levels of nesting along with additional utility methods.',
    'Miscellaneous'
),]
