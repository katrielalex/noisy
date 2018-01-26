#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='noisy',
    version='0.1.0a',
    description='noisy runs linters on noise protocol specifications',
    long_description=readme,
    author='Katriel Cohn-Gordon',
    author_email='noisy@katriel.co.uk',
    url='https://github.com/katrielalex/noisy',
    packages=find_packages(include=['noisy']),
    entry_points={
        'console_scripts': [
            'noisy=noisy.cli:main',
        ],
    },
    include_package_data=True,
    install_requires=[
        'antlr4-python3-runtime==4.7.1',
        'Click>=6.0',
        # TODO: put package requirements here
    ],
    license='GNU General Public License v3',
    zip_safe=False,
    keywords='marmoscet',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],

    # test_suite='tests',
    # tests_require=[
    #     'pytest',
    #     # TODO: put package test requirements here
    # ],

    # setup_requires=[
    #     'pytest-runner',
    #     # TODO(katrielalex): put setup requirements (distutils extensions, etc.) here
    # ],
)
