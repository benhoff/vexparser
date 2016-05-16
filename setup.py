import os
from setuptools import find_packages, setup


# directory = os.path.abspath(os.path.dirname(__file__))
"""
with open(os.path.join(directory, 'README.rst')) as f:
    long_description = f.read()
"""

setup(
    name="vexparser",
    version='0.0.5',
    description='Command parsing for vexbot',
    # long_description=long_description,
    url='https://github.com/benhoff/commandparser',
    license='GPL3',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Operating System :: OS Independent'],
    keywords='command parsing intent classifier',
    author='Ben Hoff',
    author_email='beohoff@gmail.com',
    packages= find_packages(), # exclude=['docs', 'tests']
    entry_points={'vexbot.plugins': ['vexparser=vexparser.__main__'],},
    install_requires=[
        'pluginmanager',
        'pyzmq',
        'numpy',
        'textblob',
        'nltk',
        'pyyaml'
        ],

    extras_require={
        'dev': ['flake8']
        },
)
