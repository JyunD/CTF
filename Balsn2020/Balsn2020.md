## Balsn 2020 writeup
===



###### 雖然不是我寫的，但弄懂後還是紀錄一下


Crypto
---

### HappyFarm

* 3 道小題目
1. AES CBC-mode
    * 算出 my_seed 加密 9000 次的結果
    * 只能輸入兩次，IV(start_date)、data(seed)自訂
    * seed 不能包含在 my_seed 裡面，加密次數只能從 0 ~ 8999
    1. 用 xor 繞過 `my_seed in seed` 的限制 (繞過 line 31)，level 設 1 即可
        ```python3=
        new_iv = bytearray.fromhex(start_date)
        new_iv[0] ^= 1
        new_iv.hex()

        new_seed = bytearray.fromhex(seed)
        new_seed[0] ^= 1
        new_seed.hex()
        ```
    2. 控制 `IV` 使得先加密 1 次再加密 8999 次會和加密 9000 的結果相等 (繞過 line 34)
        ```python3=
        aes = AES.new(mode=AES.MODE_CBC, key=key, iv=first_seed[-32:])
        aes.encrypt(first_seed)
        ```
        * review CBC
        ![review](https://upload.wikimedia.org/wikipedia/commons/d/d3/Cbc_encryption.png)
        
2. RSA
    * 算出 my_seed 加密 9000 次的結果
    * 第一次必須用他的 seed，第二次才能使用自己的 seed
    * 加密方式為 $seed^{(d^{layer} mod \space \phi)} \space mod \space n$
    1. 用原始 seed 和第一次加密算出 n
    
        原始
        seed $pow(2^{1023}, 3, n)$
        $= pow(2, 1023 \cdot 3, n)$
        $kn = 2^{1023 \cdot 3} - seed = n_1$
        
        第一次 (layer: 8999)
        $pow(pow(2^{1023}, 3, n), pow(d, 8999, \phi), n)$
        $= pow(2^{1023 \cdot 3}, d^{8999}, n)$
        $= pow(2^{1023}, e * d^{8999}, n)$
        $= pow(2^{1023}, d^{8998}, n)$
        
        $first = pow(2^{1023}, d^{8998}, n)$
        
        $pow(first, e^{8998}, n) = 2^{1023}$
        $kn = pow(first, 3^{8998}, n) - 2^{1023} = n_2$
        
        $n = GCD(n1, n2)$
    2. 輸入上次加密的結果，並將 layer 設 1，就可以得到加密 9000 的結果
        $first = pow(seed, d^{8999}, n)$
        $= pow(first, pow(d, 1, n), n)$
        $= pow(first, d, n)$
        $= pow(seed, d^{9000}, n)$
        $= pow(seed, d^{9000}, n_1)$
    3. 但是輸出有少 bytes，需用 Coppersmith method 解 (e 很小)
        略
3. RC4
    * 算出用加密 $9000^3$ 後的結果
    * new_left = right
    * new_right = left xor [RC4](https://zh.wikipedia.org/zh-tw/RC4).encrypt(right)
    1. swap 並沒有功能
        ```python3=
        def swap(self, a, b):
            a, b = b, a
        ```
    2. 以 192 為一個循環 
        輸入 $9000^{3} mod \space 192$
        [no_swap_rc4](https://link.springer.com/content/pdf/10.1007/3-540-49649-1_26.pdf) $Chapter 3.1$


Misc
---

### Election

* 共有 3 個 stage (用 `_setStage()` 控制)
    * propose 
        * 提出候選人
    * vote 
        * 投票
    * reveal
        * 結果
* 目標
    * 成為 winner
    * call `giveMeFlag()`
        
        
### 思路
可以發現在第 56 行處的 `abi.encodeWithSignature()` 內容是可控的，那麼就可以繞過 `modifier`，而在第 145 行有個 integer overflow 可以控制票數，到此就可以完成我們所需的目的。

```solidity=
function _transfer(address from, address to, uint value, bytes memory data, string memory customFallback) internal returns (bool) {
    require(from != address(0), "ERC223: transfer from the zero address");
    require(to != address(0), "ERC223: transfer to the zero address");
    require(_balances[from] >= value, "ERC223: transfer amount exceeds balance");
    _balances[from] -= value;
    _balances[to] += value;

    if (_isContract(to)) {
        (bool success,) = to.call{value: 0}(
            abi.encodeWithSignature(customFallback, msg.sender, value, data)
        ); // customFallback 可控`
        assert(success);
    }
    emit Transfer(msg.sender, to, value, data);
    return true;
}
```

```solidity=
function reveal(uint voteHashID, Ballot[] memory ballots) public {
    require(stage == 2, "Election: stage incorrect");
    require(!revealed[msg.sender], "Election: already revealed");
    require(voteHashes[voteHashID] == keccak256(abi.encode(ballots)), "Election: hash incorrect");
    revealed[msg.sender] = true;

    uint totalVotes = 0;
    for (uint i = 0; i < ballots.length; i++) {
        address candidate = ballots[i].candidate;
        uint votes = ballots[i].votes;
        totalVotes += votes; // integer overflow
        voteCount[candidate] += votes;
    }
    require(totalVotes <= balanceOf(msg.sender), "Election: insufficient tokens"); // 用 overflow 繞過
    emit Reveal(voteHashID, ballots);
}
```

### 如何利用 `abi.encodeWithSignature()` 呼叫所需的函數

``` solidity
extcodesize()
// 若長度為 0 就表示是外部地址發出的，否則就是合約
encodeWithSignature()
// 用 Signature call function
```
[參考資料](https://hitcxy.com/2021/argument-encoding/)

![](https://i.imgur.com/lfwMNXT.png)

* propose
    * candidate (msg.sender)
    * offset to proposal (value) (0x40)
    * offset to name (offset to data) (0x60)
    * offset to policies (length of data) (0xa0)

* _setStage
    * stage (msg.sender)

### 詳細步驟

1. 準備 3 個帳戶，地址分別是 00 02 03 結尾的 [how](https://stackoverflow.com/questions/51945714/how-do-i-generate-an-ethereum-public-key-from-a-known-private-key-using-python)
2. 用 `giveMeMoney` 拿到 0x40 個 token
3. 製作 voteHashes，讓 attacker 是 $2^{256}-1$，Alice 是 $1$
4. 用帳戶 00 切回 stage 0
5. Propose attacker
6. 用帳戶 02 切回 stage 2
7. 對兩個人投票，一個 1 票，一個是 $2^{256} -1$ (攻擊者)
8. 用帳戶 03 切回 stage 3
9. call `giveMeFlag`