#!/usr/bin/env python3

"""
Module for parsing version in Solidity smart contracts.
"""

from lark import Lark

parser = Lark(r"""
    start: pragma_version anything

    pragma_version: PRAGMA version SEMICOLON
    version: CARET? INT DOT INT DOT INT

    COMMENT: COMMENT_LINE | COMMENT_BLOCK
    COMMENT_LINE: COMMENT_LINE_START /[^\n]*/ NEWLINE
    COMMENT_BLOCK: COMMENT_BLOCK_START  /(.|\n)*?/ COMMENT_BLOCK_END
    %ignore COMMENT

    anything: /(.|\n)*?/

    PRAGMA: "pragma"
    SOLIDITY: "solidity"

    CARET: "^"
    DOT: "."
    SEMICOLON: ";"
    COMMENT_LINE_START: "//"
    COMMENT_BLOCK_START: "/*"
    COMMENT_BLOCK_END: "*/"

    %import common.NEWLINE
    %import common.INT
    %import common.WS
    %ignore WS
    """)

data1 = """
    // Some comment
    pragma soldity ^0.4.15;
    // Some comment

    Contract A{}
    """


def parse_solidity_version(input_file):
    tree1 = parser.parse(data1)
    print("Tree 1: " + str(tree1))
