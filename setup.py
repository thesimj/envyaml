# -*- coding: utf-8 -*-
from setuptools import setup

from envyaml import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='envyaml',
    packages=['envyaml'],
    version=__version__,
    url='https://github.com/thesimj/envyaml',
    license='MIT',
    author='Mykola Bubelich',
    author_email='thesimj@users.noreply.github.com',
    description='Simple YAML configuration file parser with easy access for structured data',
    install_requires=['PyYAML'],
    python_requires='>=3.6',
    platforms='any',
    test_suite='tests',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
