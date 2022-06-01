## Hero CTF

無聊打個題目玩玩

Crypto
--- 

### Oracles_apprentice
題目會幫你解密文，但不能是特定的密文，很明顯是經典的 Chosen cipher attack，只是這題要自己拿公鑰

$(-1)^d \space mod\space N = (-1) \space mod\space N = (N-1 \space mod\space N $

送 `-1` 可以拿到 `N-1`

e 很小，直接爆破就好

先傳 2 得到 $2^d \space mod\space N = c_2$

只要找到 e 使得 $(c_2)^e\space mod\space N = 2$ 就好

最後傳送 $2^e*cipher = (2M)^e\space mod\space N$

把得到的數字除二就可以拿到 flag

flag = `Hero{m4ybe_le4ving_the_1nt3rn_run_th3_plac3_wasnt_a_g00d_id3a}`


Web3
---
### Challenge0

先 call `accept_rules()` 再 call `get_flag_part_one()`

flag = `Hero{W3lC0me_2_H3r0Ch41n_W@gM1}`

### Challenge1

題目要提光合約中所有存款

withdraw 中計算 balance 部分放在 msg.sender.call 之後，又msg.sender 如果是合約地址的話，msg.sender.call 會執行合約的 receive function，這是典型的 Reentrancy attack，因此只要再 receive function 再繼續 call withdraw 就好

flag = `Hero{@M_A_m3l_sT34l3r_Am_v3rY_AngR}`

### Challenge2

題目要猜 random，但 random 的部分是由block.timestamp、block.number、block.gaslimit、gasleft()組成，block.timestamp、block.number 只要是同一個 block 的交易就會一樣，block.gaslimit 是定值，gasleft()是剩餘的 gas，是可以操縱的，那麼就可以破解 random 了

flag = `Hero{keccack256(Nath_The_Menace_2_Society}`

### Challenge3

那時候沒看懂題目要幹嘛，call 10 次 `deposit()` 再 call `claimAuction()` 就可以拿到 flag 了
結果我看大家解法都是用 `selfdestruct()`，讓合約中的 balance 全部送到指定 address

flag = `Hero{1n_F4cT_H3_d1dNT_g0t_It}`

### Challenge4

目標是讓 `3viL.com` 綁到 `0xffffffffffffffffffffffffffffffffffffffff` 上

Uninitialized Storage Pointer

貌似是舊版本 solidity 的 bug，簡單的說就是未初始化的 storage 變數會指到其他變數空間

那就
`register(0x0x0000000000000000000000000000000000000000000000000000000000000000, own_address)`

此時 `locked = false`
`register(0x3376694c2e636f6d000000000000000000000000000000000000000000000000, 0xffffffffffffffffffffffffffffffffffffffff)`

flag = `Hero{DontForgetMelIsTheBoss!}`