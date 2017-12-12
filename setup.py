#!/usr/bin/env python3

import os

from pip.req import parse_requirements
from setuptools import find_packages, setup


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

dependency_links = [
    (
        'https://github.com/m157q/robobrowser/'
        'tarball/babf6dd#egg=robobrowser-0.5.3'
    ),
]

install_requirements = parse_requirements(
    os.path.join(ROOT_DIR, 'requirements.txt'), session=False
)
install_requires = [str(ir.req) for ir in install_requirements]

setup(
    packages=find_packages(exclude=['gettitle.bin']),
    scripts=['gettitle/bin/gettitle'],
    dependency_links=dependency_links,
    install_requires=install_requires,
    name='gettitle',
    version='0.1.3',
    author='Shun-Yi Jheng',
    author_email='M157q.tw@gmail.com',
    url="https://github.com/M157q/gettitle",
    keywords="cli, webpage, title",
    description="Get webpage title by url from terminal.",
    platforms=['Linux'],
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
)
