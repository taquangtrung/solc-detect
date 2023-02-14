#!/usr/bin/env python3

"""
Get version of Solidity compiler from smart contract source code.
"""

import argparse
from . import parser


def configure_cli_arguments():
    """Main function to run solc-detect"""
    parser = argparse.ArgumentParser(
        description="Detect Solidity compiler version for a smart contract",
        add_help=False
    )

    # Help
    parser.add_argument(
        "-h", "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit")

    # Input
    parser.add_argument(
        "input_file",
        help="Input smart contracts")

    # Parse CLI arguments
    args = parser.parse_args()

    return args


def main():
    """Main function"""
    args = configure_cli_arguments()

    print("Running Solc-detect")
    print("Input file: ", args.input_file)

    parser.parse_solidity_version(args.input_file)


if __name__ == "__main__":
    main()
