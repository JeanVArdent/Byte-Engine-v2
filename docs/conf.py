# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GAME THEMED DOCUMENTATION TITLE'
copyright = '1974-202X, NDSU ACM'
author = 'NDSU ACM Byte-le 202X Dev Team'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_copybutton',
    # 'sphinx_tabs.tabs',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = [
    '_static'
]
html_css_files = [
    'styles/custom.css'
]

CLIENT_PACKAGE_REPO_URL = 'https://github.com/acm-ndsu/Byte-le-2026-Client-Package'
DISCORD_URL = 'https://discord.gg/'
UPDATE_GUIDE_URL = 'useful_commands.html#updating-your-launcher'
SHOW_ANNOUNCEMENT = True
ANNOUNCEMENT = \
    '(12:38 p.m.) UPDATED <a href="tips.html">TIPS & TRICKS</a> AND ADDED <a href="controls.html#pathfinding">SAMPLE A* CODE</a>' \

html_title = '2026 QBB Security Manual'
html_theme = 'shibuya'
html_theme_options = {
    'accent_color': 'indigo', # shibuya
    'github_url': CLIENT_PACKAGE_REPO_URL, # shibuya
    'discord_url': DISCORD_URL, # shibuya
    'announcement': ANNOUNCEMENT if SHOW_ANNOUNCEMENT else '' # shibuya
}
html_logo = '_static/images/bytele-logo.png'
