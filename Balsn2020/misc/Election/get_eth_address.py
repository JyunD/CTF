import os
from eth_keys import keys
from eth_utils import decode_hex



target = ['00', '01', '02', '03']
result = []

while True:

    private_key = keys.PrivateKey(os.urandom(32))
    public_key = private_key.public_key
    
    for t in target:
        if public_key.to_checksum_address()[-2:] == t:
            target.remove(t)
            result.append((private_key, public_key.to_checksum_address()))

    if not target:
        break


for r in result:
    print(r)