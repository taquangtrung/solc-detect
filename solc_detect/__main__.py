#!/usr/bin/env python3

"""
Get version of Solidity compiler from smart contract source code.

Version of Solidity smart contract follow NPM versioning syntax.
"""

import argparse
from semantic_version import NpmSpec, Version
from . import parser, lib


def configure_cli_arguments():
    """Main function to run solc-detect"""
    arg_parser = argparse.ArgumentParser(
        description="Detect Solidity compiler version for a smart contract",
        add_help=False
    )

    # Help
    arg_parser.add_argument(
        "-h", "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit")

    # Input
    arg_parser.add_argument(
        "input_file",
        help="Input smart contracts")

    # Parse CLI arguments
    args = arg_parser.parse_args()

    return args


# def find_best_solc_version(version):
#     """Find the best Solidity version satisfying a version specification.

#     The input string `version` follows NPM version specification format.

#     This function returns the latest suitable Solidity version"""

#     version_spec = NpmSpec(version)
#     all_versions = lib.init_all_solidity_versions()
#     best_version = version_spec.select(all_versions)
#     print("Best version: " + str(best_version))


def main():
    """Main function"""
    args = configure_cli_arguments()
    input_file = args.input_file

    pragma_version = lib.find_pragma_solc_version(input_file)
    print("Input pragma version:", pragma_version)

    best_version = lib.find_best_solc_version_for_pragma(pragma_version)
    print("Best  version:", best_version)

    return best_version


if __name__ == "__main__":
    main()
