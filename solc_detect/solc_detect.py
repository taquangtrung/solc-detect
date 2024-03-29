#!/usr/bin/env python3

"""
Module define some utility variables and functions.
"""

import re
from typing import List, Optional

import nodesemver
import semantic_version

from solc_detect import pragma_parser

# Enumerate all Solidity versions based on information in:
# https://blog.soliditylang.org/category/release
solc_0_4 = ["0.4.%d" % i for i in range(27)]  # 0.4.0 --> 0.4.26
solc_0_5 = ["0.5.%d" % i for i in range(18)]  # 0.5.0 --> 0.5.17
solc_0_6 = ["0.6.%d" % i for i in range(13)]  # 0.6.0 --> 0.6.12
solc_0_7 = ["0.7.%d" % i for i in range(7)]  # 0.7.0 --> 0.7.6
solc_0_8 = ["0.8.%d" % i for i in range(20)]  # 0.8.0 --> 0.8.19


def enumerate_and_group_solc_version_by_minor_version() -> List[List[str]]:
    """Enumerate all Solc versions, group by MINOR version, in each group, sort
    by PATCH version, according to semantic versioning: https://semver.org/."""
    solc_versions = [
        solc_0_4,
        solc_0_5,
        solc_0_6,
        solc_0_7,
        solc_0_8,
    ]
    return solc_versions


def find_pragma_version_string(
    input_file: str, quiet: bool = True
) -> List[str]:
    """Find the pragma Solidity version strings in smart contract."""
    pragma_strs = pragma_parser.parse_solidity_version(input_file)
    if not quiet:
        print("Detected raw pragmas:", pragma_strs)

    pragma_strs = normalize_pragmas(pragma_strs)
    if not quiet:
        print("Normalized pragmas:", pragma_strs)

    return pragma_strs


def normalize_pragmas(pragma_strs: List[str]) -> List[str]:
    """Normalize pragma strings so that `semantic_version` and `nodesemver` can
    process them."""

    new_pragmas = []
    for pragma in pragma_strs:
        # Delete unneeded whitespace
        pragma = re.sub("\\. *", ".", pragma)
        pragma = re.sub(" *\\.", ".", pragma)
        # Simplify .00 => .0
        pragma = re.sub("\\. *00", ".0", pragma)
        new_pragmas.append(pragma)

    return new_pragmas


def find_best_solc_version_for_pragma(pragma_versions) -> Optional[str]:
    """Find the best version of Solc compiler for a pragma version. This version
    is the latest patch of the lowest minor version satisfying the required
    pragmas."""

    version_groups = enumerate_and_group_solc_version_by_minor_version()
    constraint = " ".join(pragma_versions)
    for group in version_groups:
        try:
            # First, use `semantic_version` module to find the best version
            all_semvers = [semantic_version.Version(v) for v in group]
            version_spec = semantic_version.NpmSpec(constraint)
            if best_version := version_spec.select(all_semvers):
                return str(best_version)
        except ValueError:
            # If errors occur, then use `node_semver` module to find it
            if best_version := nodesemver.max_satisfying(group, constraint):
                return str(best_version)

    # Unable to find a suitable version
    return None


def find_all_best_solc_versions_for_pragma(pragma_versions) -> List[str]:
    """Find multiple best versions of Solc compiler for a pragma version. These
    versions are the latest patches of each version satisfying the required
    pragmas.
    """
    version_groups = enumerate_and_group_solc_version_by_minor_version()
    constraint = " ".join(pragma_versions)

    best_versions: List[str] = []
    for group in version_groups:
        try:
            # First, use `semantic_version` module to find the best version
            all_semvers = [semantic_version.Version(v) for v in group]
            version_spec = semantic_version.NpmSpec(constraint)
            if best_version := version_spec.select(all_semvers):
                best_versions.append(str(best_version))
        except ValueError:
            # If errors occur, then use `node_semver` module to find it
            if best_version := nodesemver.max_satisfying(group, constraint):
                best_versions.append(str(best_version))

    # Return all best versions
    return best_versions


def find_best_solc_version(input_file) -> Optional[str]:
    """Find the best version of Solc compiler for a smart contract. This version
    is the latest patch of the lowest minor version satisfying the required
    pragmas."""
    pragma_strs = find_pragma_version_string(input_file)
    return find_best_solc_version_for_pragma(pragma_strs)


def find_all_best_solc_versions(input_file) -> List[str]:
    """Find multiple best versions of Solc compiler for a smart contract. These
    versions are the latest patches of each version satisfying the required
    pragmas.
    """
    pragma_versions = find_pragma_version_string(input_file)
    return find_all_best_solc_versions(pragma_versions)
