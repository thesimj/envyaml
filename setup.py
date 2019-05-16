# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from envyaml import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="envyaml",
    packages=find_packages(),
    version=__version__,
    url="https://github.com/thesimj/envyaml",
    license="MIT",
    author="Mykola Bubelich",
    author_email="projects@bubelich.com",
    description="Simple YAML configuration file parser with easy access for structured data",
    install_requires=["PyYAML"],
    python_requires=">=2.7",
    include_package_data=True,
    platforms="any",
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
