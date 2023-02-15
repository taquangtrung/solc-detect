#!/usr/bin/env python3

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='solc_detect',
                 packages=['solc_detect'],
                 install_requires=install_requires)
