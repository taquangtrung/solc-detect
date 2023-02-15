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
  $ python -m solc_detect examples/unchecked_return_value.sol
  Input pragma version: 0.4.25
  Best version: 0.4.25

  $ python -m solc_detect examples/BECToken.sol
  Input pragma version: ^0.4.16
  Best version: 0.4.26

  $ python -m solc_detect examples/test2.sol
  Input pragma version: 0.4.0 - 0.4.19
  Best version: 0.4.19

  $ python -m solc_detect examples/test3.sol
  Input pragma version: >0.6.0 <0.8.0
  Best version: 0.7.6
  ```
