#!/usr/bin/python

from setuptools import setup, find_packages
from eds import __VERSION__

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='eds',
    version=__VERSION__,
    description='The Extensible Deployment System (EDS)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Manheim SRE Team',
    author_email='',
    url='https://github.com/manheim/eds',
    keywords='aws deploy plugins jenkins',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'click',
        'setuptools',
        'github3.py>=2.0.0'
    ],
    entry_points={
        'console_scripts': [
            'eds=eds.cli:cli',
        ]
    }
)
