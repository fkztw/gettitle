#!/usr/bin/env python3

from setuptools import find_packages, setup

requires = [
    'beautifulsoup4',
    'dryscrape',
    'requests',
    'robobrowser',
]

setup(
    packages=find_packages(exclude=['gettitle.bin']),
    scripts=['gettitle/bin/gettitle'],
    install_requires=requires,
    name='gettitle',
    version='0.0.1',
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
