# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in done_smb/__init__.py
from done_smb import __version__ as version

setup(
	name='done_smb',
	version=version,
	description='done',
	author='smb',
	author_email='smb',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
