#!/usr/bin/env python3

"""
Get version of Solidity compiler from smart contract source code.

Version of Solidity smart contract follow NPM versioning syntax.
"""

import argparse

import toml

from solc_detect import solc_detect


def configure_cli_arguments():
    """Main function to run solc-detect"""
    arg_parser = argparse.ArgumentParser(
        description="Detect Solidity compiler version for a smart contract",
        add_help=False,
    )

    # Print version
    arg_parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        default=False,
        help="",
    )

    # Print verbose
    arg_parser.add_argument(
        "-v",
        "--verbose",
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
    arg_parser.add_argument(
        "input_file", nargs="?", help="Input smart contracts"
    )

    # Parse CLI arguments
    args = arg_parser.parse_args()

    return (args, arg_parser)


def main():
    """Main function"""
    (args, arg_parser) = configure_cli_arguments()

    if args.version:
        app_version = toml.load("pyproject.toml")["project"]["version"]
        print(f"solc-detect v{app_version}")
        arg_parser.exit()

    input_file = args.input_file
    if input_file is None:
        print("Error: input Solidity file is not provided!\n")
        arg_parser.print_usage()
        arg_parser.exit()

    pragma_version = solc_detect.find_pragma_solc_version(input_file)
    if args.verbose:
        print("Detected pragmas:", pragma_version)

    best_version = solc_detect.find_best_solc_version_for_pragma(pragma_version)
    if args.verbose:
        print("Best version:", best_version)
    else:
        print(best_version)


if __name__ == "__main__":
    main()
