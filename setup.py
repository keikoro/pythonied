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
    version='1.0',
    author='K Kollmann',
    author_email='code∆kerstinkollmann· com',
    license='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='misc., scripts',

    cmdclass = {
        'clean': cleanup
    }, requires=['python-gnupg']
)
