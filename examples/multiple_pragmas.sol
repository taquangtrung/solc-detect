/*
 * @source: https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-101#bectokensol
 * @author: -
 * @vulnerable_at_lines: 264
 */

pragma solidity >0.6.0 <0.8.0;

contract Contract1 {
    function add(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a + b;
        require(c >= a);
        return c;
    }
}

pragma solidity ^0.7.0;

pragma solidity ^0.7.2;

contract Contract2 {
    function sub(uint256 a, uint256 b) internal constant returns (uint256) {
        require(b <= a);
        return a - b;
    }
}
