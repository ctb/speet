from setuptools import setup, find_packages
from setuptools import Extension
import os

with open('README.md', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

SETUP_METADATA = \
               {
    "name": "speet",
    "description": "tools for comparing text documents with Scaled MinHash",
    "long_description": LONG_DESCRIPTION,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/ctb/speet",
    "author": "C. Titus Brown",
    "author_email": "titus@idyll.org",
    "license": "BSD 3-clause",
    "packages": find_packages(exclude=["tests"]),
    "entry_points": {'console_scripts': [
        'speet = speet.__main__:main'
        ]
    },
    "install_requires": [],
    "setup_requires": ["setuptools>=38.6.0"],
    "extras_require": {
        'test' : ['pytest'],
        },
    }

setup(**SETUP_METADATA)
