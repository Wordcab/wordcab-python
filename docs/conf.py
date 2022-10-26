"""Sphinx configuration."""
project = "Wordcab Python SDK"
author = "Thomas Chaigneau"
copyright = "2022, Thomas Chaigneau"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
