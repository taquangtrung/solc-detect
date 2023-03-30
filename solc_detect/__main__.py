#!/usr/bin/env python3

"""
Get version of Solidity compiler from smart contract source code.

Version of Solidity smart contract follow NPM versioning syntax.
"""

import argparse

from . import lib


def configure_cli_arguments():
    """Main function to run solc-detect"""
    arg_parser = argparse.ArgumentParser(
        description="Detect Solidity compiler version for a smart contract",
        add_help=False,
    )

    # Help
    arg_parser.add_argument(
        "--verbal",
        action="store_true",
        default=False,
        help="",
    )

    # Help
    arg_parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit",
    )

    # Input
    arg_parser.add_argument("input_file", help="Input smart contracts")

    # Parse CLI arguments
    args = arg_parser.parse_args()

    return args


def main():
    """Main function"""
    args = configure_cli_arguments()
    input_file = args.input_file

    pragma_version = lib.find_pragma_solc_version(input_file)
    if args.verbal:
        print("Detected pragmas:", pragma_version)

    best_version = lib.find_best_solc_version_for_pragma(pragma_version)
    if args.verbal:
        print("Best version:", best_version)
    else:
        print(best_version)


if __name__ == "__main__":
    main()
