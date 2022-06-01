Aegis 2020 Writeup
===

###### 有點久以前寫的了，有空再補清楚一點

McEliece_MTA
---

* McEliece_encrypt

Public key $G_1$
Private key $S$ , $P$ ($S$ is invertable, $P$ is permutation matrix)

* encrypt m
    * STEP 1
        * generate $G$
        * $G_1 = SGP$
    * STEP 2
        * generate $e$ (random)
        * cipher $c = mG_1 + e$

* decrypt c
    * STEP 1
        * $c_1 = cP^{-1}$
        * 用 $c_1$ 算出 $c_0$ (線性糾錯理論)
        * $m = c_0S^{-1}$

flag = `AEGIS{I!c~r$D}`

Baby Heap
---

大致上要分五大步驟，第二第三步是為了四五做鋪成，為了操控最後 1 byte

當中有利用到 IO_FILE 去 leak libc


Reference
---

[McEliece公鑰密碼體制](https://blog.csdn.net/u010536377/article/details/41924803)

[hackmd](https://hackmd.io/ZRlWS44VSNerBWF9pbmuig)