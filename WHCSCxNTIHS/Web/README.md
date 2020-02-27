# Web

### Type Juggling

要求用 `GET` 方法傳送 `secret` 要求如下
`$secret != '240610708' && md5($secret) == md5('240610708')`

因為 `md5('240610708') = 0e462097431906509019562988736854`
在 `php` 代表 `0` ，雙等於又不比較型態，所以只要讓 `md5($secret)` 是 `0e` 開頭的就可以了

<sup><sub>Author: CSY54</sub></sup>

### Depreciated Page

> 未能解出

<sup><sub>Author: CSY54</sub></sup>

### Ok, Google

> 未能解出

### Weak Credentials

要求要 `admin` 登入後點擊 `Show flag` 才會顯示 `flag` ，並給了一組 `test` 帳號

看 code 會發現 `Show flag` 是檢查 `session` 的值，試著將 test 的 session md5解密回去，發現他是 `md5(2)`，
將 `session` 改成 `md5(1)` 點擊後得到 `flag`

<sup><sub>Author: CSY54</sub></sup> 
