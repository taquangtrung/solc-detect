Solc-detect
================

Tool to detect compatible version of the `Solc` compiler in Solidity smart
contracts.

# Installation

- Install prerequisite libraries:

  ``` sh
  pip install -r requirements.txt
  ```

# Usage


  ```sh
  python -m solc_detect <input-contract>

  ```

  Example:

  ```sh
  $ python -m solc_detect examples/test1.sol
  Detected pragmas: ['^0.4.15']
  Best version: 0.4.26

  $ python -m solc_detect examples/test2.sol
  Detected pragmas: ['0.4.0 - 0.4.19']
  Best version: 0.4.19

  $ python -m solc_detect examples/test3.sol
  Detected pragmas: ['>0.6.0 <0.8.0']
  Best version: 0.7.6

  $ python -m solc_detect examples/rubixi.sol
  Detected pragmas: ['^0.4.15']
  Best version: 0.4.26

  $ python -m solc_detect examples/multiple_pragmas.sol
  Detected pragmas: ['>0.6.0 <0.8.0', '^0.7.0', '^0.7.2']
  Best version: 0.7.6
  ```
