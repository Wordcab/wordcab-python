"""Sphinx configuration."""
project = "Wordcab Python"
author = "Wordcab"
copyright = "2022, The Wordcab Team"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
