# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='envyaml',
    packages=['envyaml'],
    version='0.1901',
    url='https://github.com/thesimj/envyaml',
    license='MIT',
    author='Mykola Bubelich',
    author_email='',
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
