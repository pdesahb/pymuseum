#!/usr/bin/env python

from setuptools import setup, find_packages

# notez qu'on import la lib
# donc assurez-vous que l'importe n'a pas d'effet de bord
import pymuseum

setup(
    name='pymuseum',
    version=pymuseum.__version__,
    packages=find_packages(),
    author="Pierre de Sahb",
    author_email="pierre@sahb.me",
    description="Scrap and transforms pictures to make beautiful wallpapers",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='http://github.com/pdesahb/pymuseum',
    classifiers=[],
    entry_points = {
        'console_scripts': [
            'pymuseum = pymuseum.cli:cli',
        ],
    },
    license="WTFPL",
)
