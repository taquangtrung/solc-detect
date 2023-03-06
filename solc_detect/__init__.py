#!/usr/bin/env python3

# Third Party
import colored_traceback

from . import lib

# Enable coloring backtrace when printing to terminal
colored_traceback.add_hook()


def find_pragma_solc_version(input_file):
    """Find the Solidity version declared in pragma of a smart contract."""
    return lib.find_pragma_solc_version(input_file)


def find_best_solc_version(input_file):
    """Find the best version of Solc compiler for a smart contract."""
    return lib.find_best_solc_version(input_file)


def find_best_solc_version_for_pragma(pragma_version):
    """Find the best version of Solc compiler for pragma."""
    return lib.find_best_solc_version_for_pragma(pragma_version)
