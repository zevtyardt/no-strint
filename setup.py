#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = re.findall(r'no strint> (.*?) \(', open('no_strint.py').read())[0]

setup(
    name='strint',
    version=version,
    description='simple str & int obfuscator',
    author='zvtyrdt.id',
    author_email='xnver404@gmail.com',
    url='https://github.com/zevtyardt/no-strint',
    py_modules = ['no_strint'],
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    entry_points='''
        [console_scripts]
        strint=no_strint:main
    ''',
)

print ("\n\nnow you can run by using the 'strint' command. to uninstall 'pip2 uninstall strint'\n")
