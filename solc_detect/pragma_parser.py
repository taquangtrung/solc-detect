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

from lark import Lark, Transformer, ast_utils, v_args

########################################
# Constants

PARSER_DIR = os.path.dirname(__file__)
THIS_MODULE = sys.modules[__name__]

########################################
# AST capturing pragma version


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


def parse_solidity_version(input_file):
    """Parse pragma string in a Solidity source code."""
    # Read grammar file
    grammar_file = os.path.join(PARSER_DIR, "pragma_grammar.lark")
    with open(grammar_file, "r", encoding="utf-8") as file:
        grammar = file.read()
        parser = Lark(grammar, start="source_unit")
        transformer = ast_utils.create_transformer(THIS_MODULE, ToAST())

    # Read file to string
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()
        parsed_tree = parser.parse(content)
        source_unit = transformer.transform(parsed_tree)
        return source_unit.pragma_version.version
