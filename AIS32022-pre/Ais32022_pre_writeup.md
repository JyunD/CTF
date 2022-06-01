## AIS3 2022 Pre-exam writeup
===

Rank
---

![](https://i.imgur.com/8jcy7Xu.png)


###### 花一個小時隨便寫一下


Crypto
---

### SC

`cipher.py.enc`的排版很明顯跟`cipher.py`一模一樣，那麼我直接建個表紀錄它的對應就好，然後又有一個檔名叫`flag.txt.enc`，那麼我只要根據我所記錄的表就能推回去了。

### Fast Cipher
加密方式是將`flag`的每個 byte 跟 key 的最低 byte 做 XOR，那麼我只要知道 key 並且 XOR cipher 就可以了。我們知道`flag`的開頭是 AIS3 那我們可以知道前幾個 key 的最低 byte 是多少，接下來嘗試了一下`f()&0xFF`，發現它其實會收斂到某個數，那代表我們可以藉由第一個 key 的最低 byte 推回去就好。


### Really Strange orAcle
題目可以將我們所輸入的值做 RSA 加密，那麼根據以下式子我們可以推算出 N
$C_2 = 2^e mod\space N$
$C_4 = 4^e mod\space N = 2^{2e} mod\space N = 2^e mod\space N * 2^e mod\space N = C_2 * C_2 mod\space N$
$C_8 = 8^e mod\space N = 2^{3e} mod\space N = C_2 * C_2 * C_2 mod\space N$

$C_4 - C_2^2 = k_1*N$
$C_8 - C_2^3 = k_2*N$
$N = gcd(k_1N, k_2N)$

又 $N = p^2$，根據二項式定理可以化簡以下式子

$C_{1+p} = (1+p)^e mod\space N = (1+p)^e mod\space p^2 = 1 + ep + \begin{pmatrix} e \\ 2 \end{pmatrix}p^2 \space mod\space p^2 =  1 + ep \space mod\space p^2$
又 $e < p$
$\frac{C_{1+p} - 1}{p} = e$

根據 RSA $ed = 1 mod\space \phi(N)$

Pwn
---

### SAAS Crash
題目看起來是只要觸發 double free 就可以了，但其實我按到一半它就自己 crash 了


### BOF2WIN
gets 的輸入不限長度，buf 大小只有0x10，有 get_the_flag() 可以拿 flag，因此只要 main function return 時能夠跳到那邊就好


### Give Me SC
單純的執行你所輸入的 shellcode，只是架構是aarch64，網路上找一下或pwntools就可以弄shellcode了


[hackmd](https://hackmd.io/dy7TUJ4ASaSrt5czhd-goA)