import os
import sys

sys.path.append(os.path.abspath('C:\\Users\\Lenovo\\Documents\\Python-web\\python_web_hw14-Sphinx-Unittest-Pytest\\'))

project = 'REST API Contacts App'
copyright = '2023, Alyona Kirienko'
author = 'Alyona Kirienko'
release = '1.0.0'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']
