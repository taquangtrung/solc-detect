#!/usr/bin/env python3

"""
Get version of Solidity compiler from smart contract source code.

Version of Solidity smart contract follow NPM versioning syntax.
"""

import argparse
from semantic_version import NpmSpec, Version
from . import parser

# All Solidity releases: https://blog.soliditylang.org/category/releases/
solidity_0_4 = ['0.4.%d' % i for i in range(27)]      # 0.4.0 --> 0.4.26
solidity_0_5 = ['0.5.%d' % i for i in range(18)]      # 0.5.0 --> 0.5.17
solidity_0_6 = ['0.6.%d' % i for i in range(13)]      # 0.6.0 --> 0.6.12
solidity_0_7 = ['0.7.%d' % i for i in range(7)]       # 0.7.0 --> 0.7.6
solidity_0_8 = ['0.8.%d' % i for i in range(19)]      # 0.8.0 --> 0.8.19
all_solidity_versions = (solidity_0_4 +
                         solidity_0_5 +
                         solidity_0_6 +
                         solidity_0_7 +
                         solidity_0_8)


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


def find_best_solidity_version(version):
    """Find the best Solidity version satisfying a version specification.

    The input string `version` follows NPM version specification format.

    This function returns the latest suitable Solidity version"""

    version_spec = NpmSpec(version)
    all_versions = (Version(v) for v in all_solidity_versions)
    best_version = version_spec.select(all_versions)
    print("Best version: " + str(best_version))


def main():
    """Main function"""
    args = configure_cli_arguments()

    version = parser.parse_solidity_version(args.input_file)
    print("Input pragma version: " + version)

    find_best_solidity_version(version)


if __name__ == "__main__":
    main()
