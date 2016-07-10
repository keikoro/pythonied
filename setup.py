#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup, Command


class cleanup(Command):
    """Get rid of unneeded files after running setup.py."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("rm -rfv ./build ./dist ./*.pyc ./*.tgz ./*.egg-info")


setup(
    name='pythonied',
    description='Miscellaneous Python scripts (some short and simple)',
    version='1.0',
    author='K Kollmann',
    author_email='code∆k.kollmann·moe',
    url='https://github.com/keikoro/pythonied',
    license='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=[
        'misc',
        'scripts'
    ],
    install_requires=[
        'python-gnupg'
    ],
    cmdclass={
        'clean': cleanup
    }
)
