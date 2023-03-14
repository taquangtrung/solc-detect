// SPDX-License-Identifier: UNLICENSED

pragma solidity >=0.4.21 < 0.6.0;

contract Contract2 {
    function sub(uint256 a, uint256 b) internal constant returns (uint256) {
        require(b <= a);
        return a - b;
    }
}
