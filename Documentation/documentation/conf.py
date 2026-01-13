# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Supplier Risk Prediction'
copyright = '2026, GIIA'
author = 'GIIA'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

html_theme = "sphinx_rtd_theme"  # Assurez-vous d'utiliser ce thème
html_static_path = ['_static']  # Assurez-vous d'avoir ce dossier
html_css_files = [
    'custom_css/custom.css',  # Chemin vers votre fichier CSS personnalisé
]
