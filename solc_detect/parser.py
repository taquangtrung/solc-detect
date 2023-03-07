#!/usr/bin/env python3

"""
Module for parsing version in Solidity smart contracts.

Syntax of Solidity version pragma follows NPM version syntax.
- https://docs.soliditylang.org/en/develop/layout-of-source-files.html#version-pragma
- https://docs.npmjs.com/cli/v6/using-npm/semver
"""

import sys
from dataclasses import dataclass
from lark import Lark, Transformer, ast_utils, v_args

this_module = sys.modules[__name__]

########################################
# AST capturing pragma version
#


@dataclass
class _AST(ast_utils.Ast):
    # Use `_` in class name to be skipped by create_transformer()
    pass


@dataclass
class PragmaVersion(_AST):
    """Class representing a pragma version"""
    version: str


@dataclass
class SourceUnit(_AST):
    """Class representing a source unit"""
    pragma_version: PragmaVersion
    other_source_unit_elements: str


@dataclass
class _DOT(_AST):
    pass


class ToAST(Transformer):
    """Class to transform the parsed tree to AST tree"""
    @v_args(inline=True)
    def source_unit(self, pragma, _other_source_unit_elements):
        """Parse rule `source_unit`"""
        return pragma

    @v_args(inline=True)
    def pragma_version(self, semver):
        """Parse rule `pragma_version`"""
        return PragmaVersion(semver)

    @v_args(inline=True)
    def semantic_version(self, semver):
        """Parse rule `semantic_version`"""
        version = str(semver)
        return version.strip()

    @v_args(inline=True)
    def other_source_unit_elements(self, other):
        """Parse rule `other_source_unit_elements`"""
        return str(other)


########################################
# Grammar to capture pragma version
#


# NOTE: use the prefix `_` to filter out rules/teminals from the parse tree.
parser = Lark(
    r"""
    source_unit: pragma_version other_source_unit_elements*

    pragma_version: _PRAGMA _SOLIDITY semantic_version _SEMICOLON
    semantic_version: /[^;]+/

    other_source_unit_elements: /(.|\n|\r)+/s

    _PRAGMA: "pragma"
    _SOLIDITY: "solidity"
    _SEMICOLON: ";"

    COMMENT: _COMMENT_LINE | _COMMENT_BLOCK
    %ignore COMMENT

    _COMMENT_LINE: _COMMENT_LINE_START /[^\n]*/ NEWLINE
    _COMMENT_BLOCK: _COMMENT_BLOCK_START  /(((?!\*\/).)|\n|\r)+/ _COMMENT_BLOCK_END
    _COMMENT_LINE_START: "//"
    _COMMENT_BLOCK_START: "/*"
    _COMMENT_BLOCK_END: "*/"

    %import common.NEWLINE
    %import common.WS
    %ignore WS
    """,
    start="source_unit")


# TODO: write unit tests
test1 = """
    // Some comments
    pragma solidity 0.4.15;
    // Some comments
    """

# TODO: write unit tests
test2 = """
    // Some comments
    pragma solidity ^0.4.15;
    """


# TODO: write unit tests
test3 = """
    pragma solidity solidity 1.2 - 2.3.4;
    // Some comments
    """

transformer = ast_utils.create_transformer(this_module, ToAST())

def parse_solidity_version_from_content(content):
    parsed_tree = parser.parse(content)
    source_unit = transformer.transform(parsed_tree)
    return source_unit.pragma_version.version

def parse_solidity_version(input_file):
    # read file to string
    with open(input_file, "r") as f:
        content = f.read()
    return parse_solidity_version_from_content(content)
