Attack and Defence 2020 Writeup
===

#### 上課作業

helloctf
---

老梗不解釋

helloctf_again
---

老梗不解釋

libccc
---

return to libc
故意給你簡單 leak，再給你 BOF 的位置


Lucky_System
---

簡單的 GOT hijack，leak 出位置後還有個 Out of bound

We_are_family
---

題目會 fork 出 child process，fork 出來的 canary 會一樣，用 child process leak canary，再在 parent process 中疊 ROP

ANALYZER
---

爆懂他的規則後直接填 shellcode 就好

但好像是非預期解....