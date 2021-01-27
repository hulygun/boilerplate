import os
import sys
import sphinx_rtd_theme

project = 'boilerplate'
copyright = '2020, hulygun'
author = 'hulygun'

release = '0.0.1'

sys.path.insert(0, os.path.abspath('../../'))

extensions = ['sphinx.ext.autodoc', 'sphinx_rtd_theme']
templates_path = ['_templates']
language = 'en'
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']