#!/usr/bin/env python3

from solc_detect import solc_detect


def find_pragma_solc_version(input_file):
    """Find the Solidity version declared in pragma of a smart contract."""
    return solc_detect.find_pragma_version_string(input_file)


def find_best_solc_version(input_file):
    """Find the best version of Solc compiler for a smart contract."""
    return solc_detect.find_best_solc_version(input_file)


def find_best_solc_version_for_pragma(pragma_version):
    """Find the best version of Solc compiler for pragma."""
    return solc_detect.find_best_solc_version_for_pragma(pragma_version)

def find_all_best_solc_versions_for_pragma(pragma_version):
    """Find all the best versions of Solc compiler for pragma."""
    return solc_detect.find_all_best_solc_versions_for_pragma(pragma_version)
