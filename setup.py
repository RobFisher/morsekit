"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['MorseKit.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True, 'resources': 'cwtext-0.96,sox-14.3.1'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
