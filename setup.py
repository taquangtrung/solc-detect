#!/usr/bin/env python

from setuptools import setup

setup(
    name="smartbench-runner",
    package_data={"": ["*.lark"]},
    entry_points={
        "console_scripts": [
            "solc-detect = solc_detect.__main__:main",
        ]
    },
)
