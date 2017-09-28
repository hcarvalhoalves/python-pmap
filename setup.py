#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="python-pmap",
    description="Clojure's pmap implementation for Python.",
    long_description=open("README.md").read(),
    author="Henrique Carvalho Alves",
    author_email="hcarvalhoalves@gmail.com",
    url="https://github.com/hcarvalhoalves/python-pmap",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version="1.3.0",
    install_requires=[
        "future",
        "pytest",
        "pytest-xdist",
        "six",
        "toolz"
    ],
    dependency_links=[],
    include_package_data=True,
    zip_safe=False)
