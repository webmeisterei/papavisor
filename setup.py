# -*- coding: utf-8 -*-
"""papavisor package."""

import os
from setuptools import setup

VERSION = "0.0.1.dev0"

# The choices for the Trove Development Status line:
# Development Status :: 5 - Production/Stable
# Development Status :: 4 - Beta
# Development Status :: 3 - Alpha


doclines = __doc__.split("\n")


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="papavisor",
    version=VERSION,
    author="Webmeisterei GmbH",
    maintainer="Rene´ Jochum",
    maintainer_email="rene@webmeisterei.com",
    url="http://github.com/webmeisterei/papavisor",
    license="MIT",
    platforms=["any"],
    description=doclines[0],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent'],
    long_description=(
        read("README.rst") + "\n\n" +
        "Changelog\n" +
        "==============\n\n" +
        read("CHANGES.rst")
    ),

    install_requires=[
        'aiohttp',
        'setuptools',
    ],
    extras_require={
    },
    include_package_data=True,
    zip_safe=False,
    packages=['papavisor'],
    package_dir={'papavisor': 'src/papavisor'},
    scripts=[
        'src/papavisor/scripts/papavisor',
        'src/papavisor/scripts/apapavisor',
    ],
    data_files=[
        ('/etc/papavisor', [
                'config/00_defaults.json',
                'config/apapavisor.sh'
            ],
         ),
    ],
)
