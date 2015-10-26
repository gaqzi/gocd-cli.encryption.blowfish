#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


def version():
    from gocd_cli.encryption import blowfish
    return blowfish.__version__


setup(
    name='gocd-cli.encryption.blowfish',
    author='Björn Andersson',
    author_email='ba@sanitarium.se',
    license='MIT License',
    description='Encryption/decryption module using Blowfish',
    long_description=README,
    version=version(),
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'gocd-cli>=0.9,<1.0',
        'pycrypto>=2.0.1'
    ],
)
