AIS3 2021 Pre-exam writeup
===

Rank
---

![](https://i.imgur.com/qqY0n5W.png)


Crypto
---

### Microchip
只是在做 shift 而已，不過順序要換一下，而且 key 只有 4 位，可用 `AIS3` 去推


### ReSident evil villAge
題目要求要偽造 `Ethan Winters` 的 RSA 簽章，題目雖然有限制不能直接拿 `Ethan Winters` 去簽，可是卻沒限制 `\x00Ethan Winters` 這種    


Misc
---

### Microcheese
原先 AIPlayer 都會用最佳解去行動，但若是當前情況是取了會輸，電腦並不能空過一輪，一定要隨機取，而可以發現玩家有空過的方法，因此只要空過一次，就變成玩家必勝的狀態了

### Blind
題目將 stdout 關掉，又可以讓你執行 syscall，那就執行 sys_dup2 讓 stderr 複製到 stdout，讓輸出正常


Pwn
---

### Write Me
source code 可以看出來他只是希望我們將 systemgot 的 address 填回去


### noper
題目說會 random 的將 nop 塞入你輸入的 shellcode 中，可是找來找去卻找不到 srand()，因此發現他的隨機是固定的，因此手動將會填 nop 的位置抓出來，在放自己的 shellcode 避免放在那些位置上以免被改壞。


### AIS3 Shell

可以發現填 command 的 memory 雖然是放在 heap，但是 heap 的 address 有存在全域變數，且存法是 0x100 * 40 , 0x200 * 40 以此類推。
再來發現取的方式很特別，輸入的 size 單純作為 index 用而已，那只要控好 size，就可以選到我們想要的 index，而 size 的檢查只檢查你輸入完 size 之後輸入的字串有沒有超過，換句話說就是輸入的字串長度能超過原先定好的 size，那就能 overflow 到下一塊 chunk。
而 command_check 只在輸入 command 做，輸入 command name 並不會檢查，所以在輸入command name 時將想要執行的 command 放到想要的位置就好。


* 腳本流程
1. 拿到 MEM [0][5]
2. 輸入 command name1
3. 拿到 MEM [0][6]
4. 輸入 command name1 的 command
5. 拿到 MEM [0][3]
6. 在輸入 command name2 的時候蓋到 MEM [0][6] 上的內容
7. 拿到 MEM [0][4]
8. 輸入 command name2 的 command
9. 執行 command name1

Reverse
---

### Piano
因為題目是 .Net，拿 dnSpy 去解就好，可以看到主要是要通過 isValid 這個 function，觀察後找規則，規則是輸入的第 n 個 + 第 n+1 個要等於 list[n]，相減要等於 list2[n]，n 為 0 ~ 13 循環。
```
list1 = [14, 17, 20, 21, 22, 21, 19, 18, 12, 6, 11, 16, 15, 14]
list2 = [0, -3, 0, -1, 0, 1, 1, 0, 6, 0, -5, 0, 1, 0]

answer = [7, 7, 10, 10, 11, 11, 10, 9, 9, 3, 3, 8, 8, 7]
```

### 🐰 Peekora 🥒
先用 pickle.tools 把檔案解析，可以看到 `__getitem__`、`__eq__`、`startswith`、`endswith` 這類的關鍵字，可以推論單純在做字串比較，並在成功後會印出 `Correct!`，比較不同的是在第 13、14 的 index 附近找不到 `STRING`，但是有看到 `GET 3`，因此找一下上一個 `PUT 3`在哪，就知道那是要和哪個字比較了


### COLORS
檢查一下發現有個 encode.js 的 file，看起來邏輯都寫在裡面，beautify 後還是很醜，不過可以看出個大概，發現有個很長的 if else，解讀一下應該是說要先輸入 `上上下下左右左右ba`。
之後會看到一串字，並且輸入的內容會轉成別的字顯示出來，可以發現對應的方式是 5 個字會轉成 4 個字，接下來要解析他是怎麼轉的，我是用 chrome 的 source 對 encode.js 下斷點去觀察每個變數的值，觀察完發現他是將輸入的字傳成 8bits，並分成一次 10bits，再將 10bits 分在 html tag 中，接下來就是將字推論回去。


Web
---

### ⲩⲉⲧ ⲁⲛⲟⲧⲏⲉꞅ 𝓵ⲟ𝓰ⲓⲛ ⲣⲁ𝓰ⲉ
看 sourcecode 可以發現能用 injection 的方式操縱 data，而 python3 在執行 `json.loads` 時，若是有重複的會用後面的蓋掉前面的，因此能讓 `user['showflag'] == True`，接下來要繞過 password 的問題，題目要求拿 flag 的不能是 guest，且 password 要對，但是提取密碼的方式是用 dict 的 get，如果 get 的 key 不存在是會回傳 None 的，因此只要讓 `user['username']` 不是 guest 或 admin，且讓 `user['password']` 是 None 就可以。

註: Json 可以放 null，`json.loads` 後會變為 None

payload: 送 post 到 /login 且 data 為 `username=test&password=", "showflag": true , "password": null, "username": "test`

Welcome
---

### Cat Slayer ᶠᵃᵏᵉ | Nekogoroshi

輸入到正確的數字就會吐 flag

直接 brute-force


[hackmd](https://hackmd.io/ZRlWS44VSNerBWF9pbmuig)