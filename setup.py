#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

from setuptools import setup, find_packages

version = re.findall(r'__version__ = \'(.*?)\'',
          open('nostrint/redat.py').read())[0]
setup(
    name='strint',
    version=version,
    description='python source code obfuscator. only obscures strings and integers',
    long_description=open('README.txt').read(),
    author='zvtyrdt.id',
    author_email='xnver404@gmail.com',
    url='https://github.com/zevtyardt/no-strint',
    py_modules = ['nostrint'],
    keywords=['obf', 'str', 'int', 'obfuscator', 'source', 'code'],
    packages = find_packages(),
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    entry_points={'console_scripts': ['strint=nostrint.__main__:main']}
)

print ("\nnow you can run by using the 'strint' command. to uninstall 'pip2 uninstall strint'\n")
