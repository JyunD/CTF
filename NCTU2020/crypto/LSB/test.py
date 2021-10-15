#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Util.number import *


n = top = 168390835017884447783889019525641257115876169369888110368302692204591964660145103764534650980519493334377459609317546048973412083560471082737373465958510733785611607408067712722090901908621110463177300588911930510504781415176601300488137371681203254128599391143929126744835790660517997651256771496295614712781
bottom = 0
e = 65537

k = 2

coff = pow(k, e, n)
c = 85633471908901611531616072122245348345620028069831438873653319121683960461876061592421367975721754731831973709828060351922378865286326779264057172983986194827302129471626051341549212741452241546490777206589962339896006525668365982055337207712253222822101282168851165402280330953975334012723325942018406175402
d = 2055520820518295897387906306674290945461356722094549465105850950816692429133406823803770706385943736629720122792529972979824063763192957660404027843306965016158282184874013009772519918751729751655311457525236595678417299627691336350577967057738370036478242374620212401369596406489916827898434617448178870273

m = 27659554349034193829743341454412116159812688160759045995909785834025774992044906747717319017145105972450041635040736656226046484705195329350519456538679471968470104108974909125763814355221119163002750883796844982425409177388882137596931943261251214183858785051113529934862992645584216989565580406093531005

while True:
    c = (coff * c) % n

    bit = pow(c, d, n)%k

    tmp = top - bottom

    # if 0 < (top - bottom) < 10000:
    #     print(bit)
    #     print((bit == (-n % k)))
    #     print("top : " + str(top))
    #     print("bottom : " + str(bottom))

    if bit == 0:
        top = bottom + tmp // k + 1
    elif bit == (-n % k):
        top = bottom + 2 * tmp // k + 1
        bottom = bottom + tmp // k
    else:
        bottom = bottom + 2 * tmp // k

    # print(str(top - bottom))

    # if 0 < (top - bottom) < 10000:
    #     print("new_top : " + str(top))
    #     print("new_bottom : " + str(bottom))
    #     print("m : " + str(m) + '\n')

    if top - bottom <= 2:
        break




print(m)
print(bottom + 1)

print(long_to_bytes(m))
print(long_to_bytes(bottom + 1))
