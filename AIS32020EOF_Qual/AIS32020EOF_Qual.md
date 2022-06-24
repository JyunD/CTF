Aegis 2020 Writeup
===

###### 有點久以前寫的了，有空再補清楚一點

Chatroom
---

從`server.py`中可以看到 flag 會經由 Blowfish 的 CBC 加密後印出，而 server 會根據你的輸入回傳不同的訊息
1. utf-8 decode 失敗
    * 印出"系統訊息" + 一段加密過的訊息
2. utf-8 decode 成功且裡面含有"男"這個字
    * 印出"系統訊息: 對方離開了，請按離開按鈕回到首頁"
3. utf-8 decode 成功且裡面含有"男"這個字
    * 印出"陌生人: 哈哈哈哈"

而根據`decrypt`這個 function 我們可以了解，印出的加密訊息前面 8 bytes 是他的 iv，既然是 CBC mode，那麼我們就有了每個 block 的 input了，接下來就是爆搜的過程了，不過要切記的是，如果改了密文的其中一段，會使的後面的密文解密解果改變，這會導致 decode 失敗，會無法得到我們想要的結果，因此一次應該只提取一個 block 來暴，題目`server.py`也提供了一個訊息，flag 是可以由 ascii decode的，代表說 flag 中的每個字都將會只是由 1 bytes 組成的，所以才能逐個 block 做爆破。
只是若是盲目的爆搜效率實在太低了，因此利用了 utf-8 的特性，"男"的這個字是由 3 個 bytes 組成的，根據規則，第一個 byte 換成 bits 應是`1110xxxx`而第二第三個 bytes 應該是`10xxxxxx`，又因為若是經由 utf-8 decode 認定是 1 byte 的字應該是`0xxxxxxx`，所以我將要爆的 3 個 bytes 開頭都 xor 1，而第二三 bytes 的後面 6 bits 都 xor 0，剩下的 bits 用爆搜的方式，在此時間複雜度是 $2^9$，這些步驟是為了找出 xor 完能夠符合 utf-8 decode 的 bits。之後固定這些 bits，剩下的再拿去爆，直到得到"對方離開了"這個訊息為止，第一到三個字分別要爆 4、6、6 bits，共是$2^{16}$到此步驟可以推出 3 個 bytes，一個 block 有 8 bytes，一個 block 爆 3 次，然後分 3 個 block 爆就可以推出 flag。

![](https://i.imgur.com/rURwATj.png)


Messy printer
---

很明顯的有 printf 漏洞在，但是結果都是用 RSA 加密送回來的，而且也沒告訴我們 N 是多少。不過可以注意到他說如果 plaintext 太小(<N/2) 的話會把 plaintext 變成 $N-\mathrm{plaintext}$，所以當 plaintext 是 1 的時候有 $(N-1)^3\equiv(-1)^3\equiv -1\equiv N-1\pmod{N}$，所以傳回來的 ciphertext 其實是 N-1，就能得到 N 了。用一樣的方法，假設明文是 $m<N^{1/3}$，有 $(N-m)^3\equiv (-m)^3\equiv -m^3\equiv N-m^3\pmod{N}$，所以 $N-\mathrm{ciphertext}$ 是完全平方數，算回來就能得到 plaintext 了。

之後 pwn 的部份就 leak 一下 libc 的位置，查 libc 版本，算出 system 的位置，然後在 magic 的地方把 system 的位置傳過去就能得到 shell 了。

