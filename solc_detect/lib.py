#!/usr/bin/env python3

"""
Module define some utility variables and functions.
"""

from semantic_version import NpmSpec, Version

from . import pragma_parser


def init_all_solidity_versions():
    """Enumerate all Solidity versions.

    All Solidity releases: https://blog.soliditylang.org/category/releases/"""

    solidity_0_4 = ['0.4.%d' % i for i in range(27)]      # 0.4.0 --> 0.4.26
    solidity_0_5 = ['0.5.%d' % i for i in range(18)]      # 0.5.0 --> 0.5.17
    solidity_0_6 = ['0.6.%d' % i for i in range(13)]      # 0.6.0 --> 0.6.12
    solidity_0_7 = ['0.7.%d' % i for i in range(7)]       # 0.7.0 --> 0.7.6
    solidity_0_8 = ['0.8.%d' % i for i in range(19)]      # 0.8.0 --> 0.8.19

    all_versions = (solidity_0_4 +
                    solidity_0_5 +
                    solidity_0_6 +
                    solidity_0_7 +
                    solidity_0_8)

    return (Version(v) for v in all_versions)


def find_pragma_solc_version(input_file):
    """Find the Solidity version declared in pragma of a smart contract."""
    pragma_version = pragma_parser.parse_solidity_version(input_file)
    return pragma_version


def find_best_solc_version_for_pragma(pragma_version):
    """Find the best version of Solc compiler for a pragma version."""
    version_spec = NpmSpec(pragma_version)
    all_versions = init_all_solidity_versions()
    best_version = version_spec.select(all_versions)
    return best_version


def find_best_solc_version(input_file):
    """Find the best version of Solc compiler for a smart contract."""
    pragma_version = find_pragma_solc_version(input_file)
    version_spec = NpmSpec(pragma_version)
    all_versions = init_all_solidity_versions()
    best_version = version_spec.select(all_versions)
    return best_version
