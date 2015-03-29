#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="pmap",
    author="Henrique Carvalho Alves",
    author_email="hcarvalhoalves@gmail.com",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version="1.0.0",
    install_requires=[],
    dependency_links=[],
    include_package_data=True,
    zip_safe=False,
    test_suite = "pmap.tests")