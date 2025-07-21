# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the package to get version info
try:
    import ai_agent_scaffold
    version = ai_agent_scaffold.__version__
    author = ai_agent_scaffold.__author__
except ImportError:
    version = "0.1.0"
    author = "AI Agent Scaffold Team"

project = 'AI Agent Scaffold'
copyright = '2024, AI Agent Scaffold Team'
author = author
release = version
version = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
    'myst_parser',  # For Markdown support
]

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pydantic': ('https://docs.pydantic.dev/latest/', None),
    'httpx': ('https://www.python-httpx.org/', None),
}

# Source file suffixes
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Language settings
language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

# Custom sidebar
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}

# HTML context
html_context = {
    'display_github': True,
    'github_user': 'ai-agent-scaffold',
    'github_repo': 'ai-agent-scaffold',
    'github_version': 'main',
    'conf_py_path': '/docs/',
}

# Logo and favicon
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

# Additional HTML options
html_title = f'{project} v{version}'
html_short_title = project
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',
    
    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',
    
    # Additional stuff for the LaTeX preamble.
    'preamble': r'''
\usepackage{xeCJK}
\setCJKmainfont{SimSun}
''',
    
    # Latex figure (float) alignment
    'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('index', 'ai-agent-scaffold.tex', 'AI Agent Scaffold Documentation',
     author, 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'ai-agent-scaffold', 'AI Agent Scaffold Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'ai-agent-scaffold', 'AI Agent Scaffold Documentation',
     author, 'ai-agent-scaffold', 'A unified SDK for AI Agent development.',
     'Miscellaneous'),
]

# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for coverage extension ------------------------------------------

coverage_ignore_modules = [
    'ai_agent_scaffold.cli',
]

coverage_ignore_functions = [
    'main',
]

# -- Custom configuration ----------------------------------------------------

# Mock imports for modules that might not be available during doc build
autodoc_mock_imports = [
    'zhipuai',
    'openai', 
    'dashscope',
    'volcengine',
    'langchain',
    'langchain_core',
    'langchain_community',
    'langgraph',
    'crewai',
    'llama_index',
    'autogen',
    'metagpt',
]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
if not os.path.exists('_static'):
    os.makedirs('_static')

# Create a simple custom CSS file if it doesn't exist
custom_css_path = Path('_static/custom.css')
if not custom_css_path.exists():
    custom_css_path.write_text("""
/* Custom CSS for AI Agent Scaffold documentation */

.wy-nav-content {
    max-width: 1200px;
}

.rst-content .section > img {
    max-width: 100%;
    height: auto;
}

/* Code block styling */
.highlight {
    background: #f8f8f8;
    border: 1px solid #e1e4e5;
    border-radius: 3px;
    padding: 6px;
}

/* API documentation styling */
.py.class, .py.method, .py.function {
    border-left: 3px solid #2980b9;
    padding-left: 10px;
    margin-bottom: 20px;
}

/* Note and warning boxes */
.admonition {
    margin: 20px 0;
    padding: 15px;
    border-radius: 5px;
}

.admonition.note {
    background-color: #e7f2fa;
    border-left: 5px solid #2980b9;
}

.admonition.warning {
    background-color: #fff3cd;
    border-left: 5px solid #f39c12;
}
""")