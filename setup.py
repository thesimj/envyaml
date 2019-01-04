# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='envyaml',
    packages=['envyaml'],
    version='0.1901',
    url='https://github.com/thesimj/envyaml',
    license='MIT',
    author='Mykola Bubelich',
    author_email='',
    description='Simple YAML configuration file parser',
    install_requires=['PyYAML'],
    python_requires='>=3.6',
    platforms='any',
    test_suite='tests',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
