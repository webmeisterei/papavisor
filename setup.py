#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""papavisor package."""

import os
import os.path

from setuptools import find_packages, setup

# The choices for the Trove Development Status line:
# Development Status :: 5 - Production/Stable
# Development Status :: 4 - Beta
# Development Status :: 3 - Alpha


doclines = __doc__.split("\n")


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="papavisor",
    version='0.0.1a4.dev0',
    author="Webmeisterei GmbH",
    maintainer="ReneĂÂ´ Jochum",
    maintainer_email="rene@webmeisterei.com",
    author_email="rene@webmeisterei.com",
    url="https://github.com/webmeisterei/papavisor",
    license="MIT",
    platforms=["any"],
    description=doclines[0],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Topic :: System :: Boot',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
    keywords="papavisor supervisor supervisord",
    long_description=(
        read("README.rst") + "\n\n" +
        read("CHANGES.rst")
    ),

    install_requires=[
        'aiohttp',
        'setuptools',
        'texttable',
        'psutil',
    ],
    extras_require={
    },
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages(
        'src/',
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    package_data={'papavisor': ['config/*.json', 'config/*.sh']},
    scripts=[
        'src/papavisor/scripts/papavisor',
        'src/papavisor/scripts/apapavisor',
    ],
)

