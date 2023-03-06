#!/usr/bin/env python3

"""
Module for parsing version in Solidity smart contracts.

Syntax of Solidity version pragma follows NPM version syntax.
- https://docs.soliditylang.org/en/develop/layout-of-source-files.html#version-pragma
- https://docs.npmjs.com/cli/v6/using-npm/semver
"""

import os
import sys
from dataclasses import dataclass
from typing import List

from lark import Lark, Transformer, ast_utils, v_args

########################################
# Some constants

PARSER_DIR = os.path.dirname(__file__)
THIS_MODULE = sys.modules[__name__]

########################################
# Source code and AST


@dataclass
class AST(ast_utils.Ast):
    """Empty class represent an AST node"""


@dataclass
class SolidityPragma(AST):
    """Class representing a `pragma` version.

    This class corresponds to the rule `solidity_grammar` when
    `ast_utils.create_transformer(this_module, ...)` is called.
    """

    version: str


@dataclass
class SourceUnit(AST):
    """Class representing a source unit.

    This class corresponds to the rule `source_unit` when
    `ast_utils.create_transformer(this_module, ...)`.
    """

    solidity_pragmas: List[SolidityPragma]


########################################
# Other transformer to generate AST


class ASTTransformer(Transformer):
    """Class to define extra rules to transform the parsed tree to AST.

    These rules are the rules that do not correspond to any dataclass defined
    above.
    """

    @v_args(inline=True)
    def source_unit(self, *elements):
        """Parse rule `source_unit`"""
        pragmas = [elem for elem in elements if elem is not None]
        return SourceUnit(pragmas)

    @v_args(inline=True)
    def solidity_pragma(self, version) -> SolidityPragma:
        """Parse rule `solidity_pragma`"""
        return SolidityPragma(version)

    @v_args(inline=True)
    def pragma_version_info(self, version) -> str:
        """Parse rule `pragma_version_info`"""
        version = str(version)
        return version.strip()

    # @v_args(inline=True)
    def non_solidity_pragma(self, non_solidity_pragma):
        """Parse rule `non_solidity_pragma`"""
        # Do not capture `non-solidity-pragma` elements
        return None


########################################
# Parse Solidity `pragma`


def parse_solidity_version(input_file):
    """Parse `pragma` string in a Solidity source code."""
    # Read grammar file
    grammar_file = os.path.join(PARSER_DIR, "pragma_grammar.lark")
    with open(grammar_file, "r", encoding="utf-8") as file:
        grammar = file.read()
        parser = Lark(grammar, start="source_unit")
        # transformer = ast_utils.create_transformer(THIS_MODULE, ToAST())

    # Read file to string
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()
        parsed_tree = parser.parse(content)
        source_unit = ASTTransformer().transform(parsed_tree)
        return [pragma.version for pragma in source_unit.solidity_pragmas]
