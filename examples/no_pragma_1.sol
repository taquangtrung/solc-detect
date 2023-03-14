// pragma solidity >0.6.0 <0.8.0;

contract Contract {
    function add(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a + b;
        require(c >= a);
        return c;
    }
}
