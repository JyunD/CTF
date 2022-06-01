Aegis 2020 Writeup
===

###### 有點久以前寫的了，有空再補清楚一點

Chatroom
---

很明顯是 Padding Oracle attack 但是用到 utf-8 的規則去判斷


Messy printer
---

crypto + pwn ?

題目會將你的 `title` 變成 `(N - title)` 然後做 RSA 加密，但 e 是 3，因此我們輸入 1 可以推算出 N

$(N-1)^3\space mod\space N = N^3 + 3N^2 - 3N - 1\space mod\space N = -1 mod\space N = N-1$

那麼我們就可以 leak 出 libc address

