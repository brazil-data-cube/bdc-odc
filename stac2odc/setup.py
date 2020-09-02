#
# This file is part of Repository of tools for the Brazil Data Cube Project.
# Copyright (C) 2020 INPE.
#

"""Brazil Data Cube stac2odc tool"""

import os
from setuptools import find_packages, setup

readme = open('README.md').read()
history = open('CHANGES.md').read()

docs_require = []

tests_require = []

extras_require = {
}
extras_require['all'] = [req for exts, reqs in extras_require.items() for req in reqs]

setup_requires = [
    'pytest-runner>=5.2',
]

install_requires = [
    'tqdm==4.48.2',
    'loguru==0.5.1',
    'gdal==2.4.0',
    'requests==2.22.0',
    'jsonschema==3.2.0',
    'pyyaml>=5.3.1',
    'stac @ git+git://github.com/brazil-data-cube/stac.py.git@b-0.9.0#egg=stac',
    'click>=7.1.0'
]

packages = find_packages()

g = {}
with open(os.path.join('stac2odc', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='stac2odc',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    keywords=['STAC', 'OpenDataCube'],
    license='MIT',
    author='INPE',
    author_email='brazildatacube@dpi.inpe.br',
    url='https://github.com/brazil-data-cube/bdc-odc',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'stac2odc = stac2odc.cli:cli'
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Console :: Curses  ',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
