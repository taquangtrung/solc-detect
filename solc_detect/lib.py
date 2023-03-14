#!/usr/bin/env python3

"""
Module define some utility variables and functions.
"""

from typing import List, Union

import nodesemver
import semantic_version

from . import pragma_parser

# from semantic_version import NpmSpec, Version


def init_all_solidity_versions() -> List[str]:
    """Enumerate all Solidity versions.

    All Solidity releases: https://blog.soliditylang.org/category/releases/"""

    solidity_0_4 = ["0.4.%d" % i for i in range(27)]  # 0.4.0 --> 0.4.26
    solidity_0_5 = ["0.5.%d" % i for i in range(18)]  # 0.5.0 --> 0.5.17
    solidity_0_6 = ["0.6.%d" % i for i in range(13)]  # 0.6.0 --> 0.6.12
    solidity_0_7 = ["0.7.%d" % i for i in range(7)]  # 0.7.0 --> 0.7.6
    solidity_0_8 = ["0.8.%d" % i for i in range(20)]  # 0.8.0 --> 0.8.19

    all_versions = (
        solidity_0_4 + solidity_0_5 + solidity_0_6 + solidity_0_7 + solidity_0_8
    )

    return all_versions


def find_pragma_solc_version(input_file) -> List[str]:
    """Find the Solidity version declared in pragma of a smart contract."""
    pragma_versions = pragma_parser.parse_solidity_version(input_file)
    return pragma_versions


def find_best_solc_version_for_pragma(pragma_versions) -> Union[str, None]:
    """Find the best version of Solc compiler for a pragma version."""
    all_versions = init_all_solidity_versions()
    constraint = " ".join(pragma_versions)
    try:
        # Use `semantic_version` to find the best version first
        all_semvers = [semantic_version.Version(v) for v in all_versions]
        version_spec = semantic_version.NpmSpec(constraint)
        best_version = version_spec.select(all_semvers)
        return str(best_version)
    except ValueError:
        # If errors occur, use `node_semver` to find the best version
        best_version = nodesemver.max_satisfying(all_versions, constraint)
        return str(best_version)


def find_best_solc_version(input_file) -> Union[str, None]:
    """Find the best version of Solc compiler for a smart contract."""
    pragma_versions = find_pragma_solc_version(input_file)
    return find_best_solc_version_for_pragma(pragma_versions)
