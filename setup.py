#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'django==1.6.6',
]

# Use part of the sphinx docs index for the long description

setup(
    name="django-form-extensions",
    version='0.0.3',
    packages=find_packages(),
    install_requires=requires,
    description = 'django form extensions',
    long_description=README,
    author="preture",
    author_email="preture@163.com",
    license="BSD",
    url="https://github.com/preture/django-form-extensions",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)